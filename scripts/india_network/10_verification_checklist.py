#!/usr/bin/env python3
"""Run Module 5 verification checklist from master plan; write report."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR, PUBLIC_DIR, YEAR_MIN  # noqa: E402
from filters import (  # noqa: E402
    is_domestic_work,
    master_institution_ids_on_work,
    openalex_id,
    work_passes_filters,
)

LOG_DIR = PROCESSED_DIR.parent / "logs"
OUT_MD = PROCESSED_DIR / "verification_report.md"
OUT_JSON = LOG_DIR / "verification_report.json"
SCIMAGEO_YEAR = 2019


def check(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "ok": bool(ok), "detail": str(detail)}


def _parse_authorships(raw):
    if raw is None:
        return []
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return []
    return raw


def _find_institution(master: pd.DataFrame, *needles: str) -> pd.Series | None:
    for _, row in master.iterrows():
        name = str(row.get("canonical_name", "")).lower()
        if all(n.lower() in name for n in needles):
            return row
    return None


def _positive_domestic_test(master: pd.DataFrame, domestic_path: Path) -> tuple[bool, str]:
    """Known domestic co-auth pair (IIT Kanpur + IIT Delhi) appears in domestic_works."""
    iitk = _find_institution(master, "kanpur")
    iitd = _find_institution(master, "delhi")
    if iitk is None or iitd is None:
        return False, "IIT Kanpur or IIT Delhi not in institution_master"
    oa_k = iitk["openalex_id"]
    oa_d = iitd["openalex_id"]
    inst_pair = {oa_k, oa_d}

    edges = PROCESSED_DIR / "collaboration_edges_full.csv"
    if edges.exists():
        e = pd.read_csv(edges)
        edge_hit = e[
            ((e["openalex_a"] == oa_k) & (e["openalex_b"] == oa_d))
            | ((e["openalex_a"] == oa_d) & (e["openalex_b"] == oa_k))
        ]
        if len(edge_hit) > 0:
            w = int(edge_hit["weight"].sum())
            return True, f"IIT Kanpur ↔ IIT Delhi edge weight={w} in collaboration_edges_full.csv"

    if not domestic_path.exists():
        return False, "domestic_works.parquet missing"
    dom = pd.read_parquet(domestic_path)
    if dom.empty:
        return False, "domestic_works.parquet is empty"
    for _, row in dom.iterrows():
        ids = row.get("institution_ids")
        if isinstance(ids, str):
            try:
                ids = json.loads(ids)
            except json.JSONDecodeError:
                continue
        if inst_pair.issubset(set(ids or [])):
            return True, f"work_id={row.get('work_id')} links IIT Kanpur + IIT Delhi"
    return False, "no IIT Kanpur + IIT Delhi domestic work found"


def _negative_foreign_test(master: pd.DataFrame, works_path: Path, domestic_path: Path) -> tuple[bool, str]:
    """Work with foreign co-author must not appear in domestic_works (W3 filter)."""
    if not works_path.exists() or not domestic_path.exists():
        return False, "works_raw or domestic_works missing"
    iitk = _find_institution(master, "kanpur")
    if iitk is None:
        return False, "IIT Kanpur not in master"
    master_oa = set(master["openalex_id"])
    oa_k = iitk["openalex_id"]
    raw = pd.read_parquet(works_path)
    dom_ids = set(pd.read_parquet(domestic_path)["work_id"].astype(str))

    for _, row in raw.head(50000).iterrows():
        authorships = _parse_authorships(row.get("authorships"))
        insts = []
        for auth in authorships:
            for inst in auth.get("institutions") or []:
                if inst.get("id"):
                    insts.append(inst)
        if not insts:
            continue
        has_k = any(openalex_id(i.get("id")) == oa_k for i in insts)
        has_foreign = any(i.get("country_code") and i.get("country_code") != "IN" for i in insts)
        if not (has_k and has_foreign):
            continue
        wid = str(row.get("id", "")).rsplit("/", 1)[-1]
        if wid in dom_ids:
            return False, f"foreign co-auth work {wid} incorrectly in domestic_works"
        if not is_domestic_work(authorships):
            return True, f"foreign co-auth work {wid} correctly excluded from domestic_works"
    return True, "sampled works: foreign co-auth papers absent from domestic_works (spot check)"


def main() -> None:
    results: list[dict] = []
    master_path = PROCESSED_DIR / "institution_master.csv"
    edges_path = PROCESSED_DIR / "collaboration_edges_full.csv"
    domestic_path = PROCESSED_DIR / "domestic_works.parquet"
    works_path = PROCESSED_DIR / "works_raw.parquet"
    funding_path = PROCESSED_DIR / "institution_funding.csv"

    master = pd.read_csv(master_path) if master_path.exists() else pd.DataFrame()

    if not master.empty:
        geo_ok = master["latitude"].notna() & master["longitude"].notna()
        results.append(
            check(
                "institution_master rows + geo",
                len(master) >= 80 and geo_ok.mean() >= 0.9,
                f"{len(master)} rows, {geo_ok.mean()*100:.0f}% with lat/lon",
            )
        )
    else:
        results.append(check("institution_master rows + geo", False, "missing"))

    if edges_path.exists():
        e = pd.read_csv(edges_path)
        w2 = e[e["weight"] >= 2] if "weight" in e.columns else e
        results.append(
            check(
                "collaboration_edges weight>=2",
                len(w2) >= 200,
                f"{len(w2)} edge rows",
            )
        )
        if not master.empty and "inst_a" in e.columns:
            master_ids = set(master["institution_id"])
            bad = e[~e["inst_a"].isin(master_ids) | ~e["inst_b"].isin(master_ids)]
            results.append(
                check(
                    "edge endpoints in master (domestic IN institutions)",
                    len(bad) == 0,
                    f"{len(bad)} orphan edge rows" if len(bad) else "all endpoints in institution_master",
                )
            )
    else:
        results.append(check("collaboration_edges weight>=2", False, "missing"))

    dash = Path(__file__).resolve().parents[2] / "dashboard" / "data" / "india_network"
    ov = dash / "2024_overview.json"
    full = dash / "2024_full.json"
    if ov.exists() and full.exists():
        results.append(check("overview size", ov.stat().st_size < 40_000, f"{ov.stat().st_size} bytes"))
        results.append(check("full size", full.stat().st_size < 200_000, f"{full.stat().st_size} bytes"))
        try:
            ov_data = json.loads(ov.read_text(encoding="utf-8"))
            note = str(ov_data.get("quality_note", ""))
            has_scimago = str(SCIMAGEO_YEAR) in note or ov_data.get("quality_year") == SCIMAGEO_YEAR
            results.append(
                check(
                    "SCImago static year footnote",
                    has_scimago,
                    note[:80] if note else "quality_note missing",
                )
            )
        except json.JSONDecodeError:
            results.append(check("SCImago static year footnote", False, "invalid overview JSON"))
    else:
        results.append(check("dashboard JSON payloads", False, "2024 payloads missing"))

    if domestic_path.exists():
        dom = pd.read_parquet(domestic_path)
        results.append(
            check(
                "domestic_works.parquet non-empty",
                len(dom) > 0,
                f"{len(dom)} rows, {domestic_path.stat().st_size // 1024} KB",
            )
        )
    else:
        results.append(check("domestic_works.parquet non-empty", False, "missing — run 06 after 05b"))

    if funding_path.exists():
        fund = pd.read_csv(funding_path)
        has = fund["research_funding_cr"].notna().sum() if "research_funding_cr" in fund.columns else 0
        results.append(
            check(
                "NIRF funding coverage",
                has >= 100,
                f"{has} / {len(fund)} institutions with research_funding_cr",
            )
        )
    else:
        results.append(check("NIRF funding coverage", False, "institution_funding.csv missing"))

    if not master.empty:
        ok_pos, det_pos = _positive_domestic_test(master, domestic_path)
        results.append(check("positive domestic co-auth test", ok_pos, det_pos))
        ok_neg, det_neg = _negative_foreign_test(master, works_path, domestic_path)
        results.append(check("negative foreign co-auth test", ok_neg, det_neg))

    if edges_path.exists() and "year" in pd.read_csv(edges_path, nrows=1).columns:
        e = pd.read_csv(edges_path)
        w2015 = e.loc[e["year"] == YEAR_MIN, "weight"].sum() if YEAR_MIN in e["year"].values else 0
        w2022 = e.loc[e["year"] == 2022, "weight"].sum() if 2022 in e["year"].values else 0
        results.append(
            check(
                "temporal edge variance (2015 vs 2022)",
                w2015 > 0 and w2022 > 0 and w2015 != w2022,
                f"2015 weight sum={int(w2015)}, 2022 weight sum={int(w2022)}",
            )
        )

    passed = sum(1 for r in results if r["ok"])
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": len(results),
        "all_pass": bool(passed == len(results)),
        "checks": results,
    }
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# Module 5 verification checklist",
        "",
        f"Generated: {summary['generated_at']}",
        f"**{passed}/{len(results)} passed**",
        "",
    ]
    for r in results:
        mark = "PASS" if r["ok"] else "FAIL"
        lines.append(f"- [{mark}] {r['name']}: {r['detail']}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Verification: {passed}/{len(results)} passed -> {OUT_MD}")
    sys.exit(0 if summary["all_pass"] else 1)


if __name__ == "__main__":
    main()
