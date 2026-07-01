#!/usr/bin/env python3
"""Verify OPENALEX_API_KEY in .env without printing the key."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from openalex_http import openalex_get  # noqa: E402


def main() -> None:
    resp = openalex_get(
        "works",
        {"filter": "institutions.country_code:IN", "per_page": 1},
        timeout=60,
        max_retries=2,
    )
    resp.raise_for_status()
    count = resp.json().get("meta", {}).get("count", "?")
    print("OpenAlex API key OK.")
    print(f"Sample query succeeded (India works count meta: {count}).")
    print("Safe to run: python scripts/india_network/05_fetch_openalex_works.py --pilot-top 30")


if __name__ == "__main__":
    main()
