#!/usr/bin/env python3
"""Print OpenAlex cache progress vs institution_master (safe, read-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import importlib

_fetch = importlib.import_module("05_fetch_openalex_works")
from config import CACHE_DIR, PROCESSED_DIR, YEAR_RANGE_JSON, YEAR_MIN  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"


def load_year_max() -> int:
    if YEAR_RANGE_JSON.exists():
        return int(json.loads(YEAR_RANGE_JSON.read_text(encoding="utf-8"))["year_max"])
    return 2024


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-top", type=int, default=30)
    parser.add_argument("--full-master", action="store_true", help="All 120 institutions in master")
    args = parser.parse_args()

    master = pd.read_csv(MASTER_PATH)
    if args.full_master:
        scope = master
        label = len(master)
    else:
        scope = master[master["tier"] == "premier"].nlargest(args.pilot_top, "total_works")
        label = args.pilot_top
    year_max = load_year_max()

    cache_files = list(CACHE_DIR.glob("works_*.json"))
    cache_bytes = sum(f.stat().st_size for f in cache_files)

    print(f"Cache: {len(cache_files):,} files, {cache_bytes / 1e9:.2f} GB")
    print(f"Year span: {YEAR_MIN}-{year_max} | scope: {len(scope)} institutions\n")
    print(f"{'Status':<10} {'Files':>6}  Institution")
    print("-" * 60)

    complete = 0
    for _, row in scope.iterrows():
        inst_id = str(row["openalex_id"])
        name = row["canonical_name"]
        nfiles = _fetch.count_cache_files(inst_id)
        if _fetch.institution_is_cached(inst_id, year_max):
            status = "DONE"
            complete += 1
        elif nfiles > 0:
            status = "PARTIAL"
        else:
            status = "pending"
        print(f"{status:<10} {nfiles:>6}  {name}")

    print("-" * 60)
    print(f"Complete: {complete}/{len(scope)} institutions")


if __name__ == "__main__":
    main()
