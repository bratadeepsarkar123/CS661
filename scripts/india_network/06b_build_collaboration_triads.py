#!/usr/bin/env python3
"""Precompute collaboration triads (3+ institution papers) for focus-mode map."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402
from triad_builder import build_triads_from_works, load_domestic_works, oa_map_from_master  # noqa: E402

DOMESTIC_PATH = PROCESSED_DIR / "domestic_works.parquet"
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
OUT_PATH = PROCESSED_DIR / "collaboration_triads.parquet"


def main() -> None:
    if not DOMESTIC_PATH.exists():
        raise FileNotFoundError(DOMESTIC_PATH)
    master = pd.read_csv(MASTER_PATH)
    oa_map = oa_map_from_master(master)
    domestic = load_domestic_works(DOMESTIC_PATH)

    rows: list[dict] = []
    years = sorted(domestic["year"].dropna().unique())
    for year in years:
        triads = build_triads_from_works(domestic, oa_map, year=int(year))
        for focus, pairs in triads.items():
            for a, b, weight in pairs:
                rows.append(
                    {
                        "year": int(year),
                        "focus_id": focus,
                        "partner_a": a,
                        "partner_b": b,
                        "weight": weight,
                    }
                )

    # all-years rollup
    triads_all = build_triads_from_works(domestic, oa_map, year=None)
    for focus, pairs in triads_all.items():
        for a, b, weight in pairs:
            rows.append(
                {
                    "year": -1,
                    "focus_id": focus,
                    "partner_a": a,
                    "partner_b": b,
                    "weight": weight,
                }
            )

    df = pd.DataFrame(rows)
    df.to_parquet(OUT_PATH, index=False)
    print(f"Wrote {OUT_PATH} ({len(df)} triad rows, years {len(years)} + rollup)")


if __name__ == "__main__":
    main()
