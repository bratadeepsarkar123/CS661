#!/usr/bin/env python3
"""Propagate institution_master tier/inst_type into Graph 5 JSON + dashboard JS.

Surgical update: does not recompute edges/funding — only node tier, color, and
tier_summary/tier_panels aggregates. Preserves VIZ5 UI files untouched.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402
from regenerate_india_network_data_js import main as regen_js  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
JSON_DIRS = [
    ROOT / "dashboard" / "data" / "india_network",
    ROOT / "public" / "india_network",
]

TIER_COLOR = {"premier": "#3b82f6", "state_affiliated": "#a855f7"}


def tier_summary(nodes: list[dict]) -> list[dict]:
    out = []
    for tier in ["premier", "state_affiliated"]:
        tier_nodes = [n for n in nodes if n.get("tier") == tier]
        if not tier_nodes:
            continue
        works = [n.get("total_works") or 0 for n in tier_nodes]
        pcts = [n["scimago_pct"] for n in tier_nodes if n.get("scimago_pct") is not None]
        fundings = [
            n["research_funding_cr"]
            for n in tier_nodes
            if n.get("research_funding_cr") is not None
        ]
        out.append(
            {
                "tier": tier,
                "institution_count": len(tier_nodes),
                "mean_total_works": round(sum(works) / len(works), 1) if works else 0,
                "mean_scimago_pct": round(sum(pcts) / len(pcts), 2) if pcts else None,
                "mean_research_funding_cr": round(sum(fundings) / len(fundings), 1) if fundings else None,
            }
        )
    return out


def patch_payload(data: dict, by_oa: dict[str, dict]) -> int:
    flips = 0
    nodes = data.get("nodes") or []
    for n in nodes:
        oid = str(n.get("openalex_id") or "")
        meta = by_oa.get(oid)
        if not meta:
            continue
        new_tier = meta["tier"]
        if n.get("tier") != new_tier:
            flips += 1
        n["tier"] = new_tier
        n["color"] = TIER_COLOR.get(new_tier, n.get("color"))
    summaries = tier_summary(nodes)
    data["tier_summary"] = summaries
    data["tier_panels"] = {
        "premier": next((t for t in summaries if t["tier"] == "premier"), {}),
        "state_affiliated": next((t for t in summaries if t["tier"] == "state_affiliated"), {}),
    }
    return flips


def main() -> None:
    master = pd.read_csv(MASTER_PATH)
    by_oa = {
        str(r.openalex_id): {"tier": r.tier, "inst_type": r.inst_type}
        for r in master.itertuples(index=False)
    }

    total_files = 0
    total_flips = 0
    for folder in JSON_DIRS:
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.json")):
            if path.name in {"manifest.json", "india_outline.geojson"}:
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if "nodes" not in data:
                continue
            flips = patch_payload(data, by_oa)
            path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            total_files += 1
            total_flips += flips
            print(f"  {path.relative_to(ROOT)}: node tier flips={flips}")

    print(f"Patched {total_files} JSON payloads ({total_flips} node tier field updates)")
    regen_js()

    # Spot-check AIIMS in 2024_full
    sample = ROOT / "dashboard" / "data" / "india_network" / "2024_full.json"
    if sample.exists():
        data = json.loads(sample.read_text(encoding="utf-8"))
        aiims = [
            n
            for n in data["nodes"]
            if "All India Institute of Medical" in str(n.get("name", ""))
        ]
        print("\n2024_full AIIMS tiers:")
        for n in sorted(aiims, key=lambda x: x["name"]):
            print(f"  {n['name']}: {n['tier']} color={n.get('color')}")


if __name__ == "__main__":
    main()
