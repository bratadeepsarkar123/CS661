#!/usr/bin/env python3
"""Export per-year JSON payloads (2015-2024) for Module 5 year slider."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import importlib

_export = importlib.import_module("09_export_payloads")
from config import PROCESSED_DIR, PUBLIC_DIR, YEAR_MIN  # noqa: E402


def main() -> None:
    import argparse
    import json
    import shutil

    parser = argparse.ArgumentParser()
    parser.add_argument("--year-max", type=int, default=2024)
    args = parser.parse_args()

    for path in [
        PROCESSED_DIR / "institution_master.csv",
        PROCESSED_DIR / "collaboration_edges_full.csv",
    ]:
        if not path.exists():
            raise SystemExit(f"Missing {path} — run 06_build_domestic_edges.py first")

    import pandas as pd

    master = pd.read_csv(PROCESSED_DIR / "institution_master.csv")
    edges = pd.read_csv(PROCESSED_DIR / "collaboration_edges_full.csv")
    hubs = (
        pd.read_csv(PROCESSED_DIR / "hub_flags.csv")
        if (PROCESSED_DIR / "hub_flags.csv").exists()
        else pd.DataFrame()
    )
    quality = _export.load_quality()

    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    available: list[int] = []

    print(f"Exporting year slices {YEAR_MIN}-{args.year_max} -> {PUBLIC_DIR}")
    for year in range(YEAR_MIN, args.year_max + 1):
        year_edges = edges[edges["year"] == year]
        if year_edges.empty:
            print(f"  skip {year}: no edges")
            continue
        _export.export_year(year, master, edges, hubs, quality)
        available.append(year)

    # Rollup; 2024 slice already exported in loop above (true calendar-year edges).
    _export.export_year(None, master, edges, hubs, quality)

    import importlib

    _nirf = importlib.import_module("nirf_utils")
    rank_years = _nirf.discover_nirf_ranking_years()
    fund_years = list(_nirf.FUNDING_ACADEMIC_YEARS)
    patent_years = list(_nirf.PATENT_CALENDAR_YEARS)

    manifest = {
        "year_min": YEAR_MIN,
        "year_max": args.year_max,
        "available_years": available,
        "default_year": 2024 if 2024 in available else (available[-1] if available else "all"),
        "quality_year": 2019,
        "funding_academic_years": fund_years,
        "patent_calendar_years": patent_years,
        "nirf_ranking_seasons": rank_years,
    }
    (PUBLIC_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest.json ({len(available)} years with edges)")

    dash_dir = Path(__file__).resolve().parents[2] / "dashboard" / "data" / "india_network"
    dash_dir.mkdir(parents=True, exist_ok=True)
    for path in PUBLIC_DIR.glob("*.json"):
        shutil.copy(path, dash_dir / path.name)
    print(f"Synced {len(list(PUBLIC_DIR.glob('*.json')))} JSON files -> {dash_dir}")


if __name__ == "__main__":
    main()
