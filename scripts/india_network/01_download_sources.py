#!/usr/bin/env python3
"""Download Tier-0 raw sources into data/raw/."""
from __future__ import annotations

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import RAW_DIR, SOURCE_URLS, OPENALEX_USER_AGENT  # noqa: E402

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": OPENALEX_USER_AGENT})


def download_url(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  exists: {dest.name}")
        return True
    try:
        resp = SESSION.get(url, timeout=120, allow_redirects=True)
        resp.raise_for_status()
        dest.write_bytes(resp.content)
        print(f"  saved: {dest.name} ({len(resp.content):,} bytes)")
        return True
    except requests.RequestException as exc:
        print(f"  FAILED {dest.name}: {exc}")
        return False


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print("=== India HE geo (GitHub — clone or manual CSV) ===")
    print(f"  Repo: {SOURCE_URLS['india_he_geo']}")
    geo_dest = RAW_DIR / "india_higher_education.csv"
    if geo_dest.exists():
        print(f"  OK: {geo_dest.name}")
    else:
        print(f"  MISSING: clone repo and copy CSV to {geo_dest}")

    print("\n=== Manual downloads required if not present ===")
    manual = [
        ("nirf_rankings", "nirf_rankings.csv", SOURCE_URLS["nirf_rankings"], False),
        ("nirf_research_funding", "nirf_research_projects.csv", "https://dataful.in/datasets/19311/", False),
        ("nirf_expenditure", "nirf_expenditure.csv", "https://dataful.in/datasets/19317/", True),
        ("nirf_patents", "nirf_patents.csv", SOURCE_URLS["nirf_patents"], True),
        ("scimago_india", "scimago_india.csv", SOURCE_URLS["scimago_india"], False),
        ("aishe_universities", "aishe_universities.xlsx", SOURCE_URLS["aishe_universities"], True),
    ]
    for key, filename, page_url, optional in manual:
        dest = RAW_DIR / filename
        if dest.exists():
            print(f"  OK: {filename}")
        elif optional:
            print(f"  SKIP (optional): {filename}")
            if key == "nirf_patents":
                print("    Patent counts optional for v1.")
            elif key == "nirf_expenditure":
                print("    Free CSV at URL — improves Funding tab expenditure row.")
            elif key == "aishe_universities":
                print("    AISHE directory optional — run validate_aishe.py if present.")
        else:
            print(f"  MISSING: {filename}")
            print(f"    Download from: {page_url}")
            print(f"    Save to: {dest}")


if __name__ == "__main__":
    main()
