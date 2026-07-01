#!/usr/bin/env python3
"""Phase 0 gate: estimate domestic edge density on top-30 premier institutions."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
EDGES_PATH = PROCESSED_DIR / "collaboration_edges_full.csv"
REPORT_PATH = PROCESSED_DIR / "feasibility_report.md"
GATE_MIN_EDGES = 500


def main() -> None:
    lines = ["# Feasibility Report — Domestic Edges\n"]

    if not MASTER_PATH.exists():
        lines.append("**Status:** BLOCKED — run 03_build_institution_master.py first.\n")
        REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
        print(REPORT_PATH.read_text())
        return

    master = pd.read_csv(MASTER_PATH)
    premier = master[master["tier"] == "premier"].nlargest(30, "total_works")
    lines.append(f"- Premier institutions in sample: **{len(premier)}**\n")

    if EDGES_PATH.exists() and EDGES_PATH.stat().st_size > 0:
        edges = pd.read_csv(EDGES_PATH)
        top_ids = set(premier["institution_id"])
        sub = edges[edges["inst_a"].isin(top_ids) & edges["inst_b"].isin(top_ids)]
        total_weight = int(sub["weight"].sum()) if len(sub) else 0
        lines.append(f"- Edges among top-30 (all years, summed weight): **{total_weight}**\n")
        lines.append(f"- Unique edge rows: **{len(sub)}**\n")
        passed = total_weight >= GATE_MIN_EDGES
        lines.append(f"- Gate (>={GATE_MIN_EDGES}): **{'PASS' if passed else 'FAIL'}**\n")
        if not passed:
            lines.append("- Action: widen year range or run 05_fetch_openalex_works for full master list.\n")
    else:
        lines.append("- Edges file not built yet. Run `05_fetch_openalex_works.py` then `06_build_domestic_edges.py`.\n")
        lines.append(f"- Gate threshold when built: >={GATE_MIN_EDGES} summed weight among top-30 premier.\n")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(REPORT_PATH.read_text())


if __name__ == "__main__":
    main()
