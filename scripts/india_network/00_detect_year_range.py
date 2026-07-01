#!/usr/bin/env python3
"""Detect YEAR_MAX from OpenAlex IN works counts (Phase 0)."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import (  # noqa: E402
    PROCESSED_DIR,
    YEAR_MIN,
    YEAR_RANGE_JSON,
)
from openalex_http import openalex_get  # noqa: E402

STABILITY_RATIO = 0.90


def count_in_works(year: int) -> int | None:
    params = {
        "filter": f"institutions.country_code:IN,publication_year:{year}",
        "per_page": 1,
    }
    try:
        resp = openalex_get("works", params, timeout=60, max_retries=3)
        resp.raise_for_status()
        return int(resp.json()["meta"]["count"])
    except SystemExit:
        return None


def detect_year_max(current_calendar_year: int | None = None) -> dict:
    import datetime

    end_probe = current_calendar_year or datetime.date.today().year
    counts: dict[int, int] = {}

    for year in range(YEAR_MIN, end_probe + 1):
        print(f"Probing {year}...", flush=True)
        c = count_in_works(year)
        if c is None:
            print(f"  skipped (API error)")
            continue
        counts[year] = c
        print(f"  {c:,} works")
        time.sleep(0.2)

    if len(counts) < 2:
        fallback = 2024
        return {
            "year_min": YEAR_MIN,
            "year_max": fallback,
            "counts": counts,
            "method": "fallback_api_blocked_or_insufficient_data",
        }

    years_sorted = sorted(counts)
    chosen = years_sorted[-1]
    for i in range(len(years_sorted) - 1, 0, -1):
        y = years_sorted[i]
        prev = years_sorted[i - 1]
        if prev == y - 1 and counts[y] >= STABILITY_RATIO * counts[prev]:
            chosen = y
            break
        if counts[y] < STABILITY_RATIO * counts[prev]:
            chosen = years_sorted[i - 1]
            break

    return {
        "year_min": YEAR_MIN,
        "year_max": chosen,
        "counts": counts,
        "method": "stability_ratio",
        "stability_ratio": STABILITY_RATIO,
    }


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    result = detect_year_max()
    YEAR_RANGE_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nWrote {YEAR_RANGE_JSON}")
    print(f"Recommended YEAR_MAX = {result['year_max']}")


if __name__ == "__main__":
    main()
