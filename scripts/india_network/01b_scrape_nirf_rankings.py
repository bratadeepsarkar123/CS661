#!/usr/bin/env python3
"""Scrape NIRF ranking tables from nirfindia.org into data/raw/nirf_rankings.csv."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from config import OPENALEX_USER_AGENT, RAW_DIR  # noqa: E402

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": OPENALEX_USER_AGENT})

CATEGORIES = [
    "Overall",
    "University",
    "College",
    "Research",
    "Engineering",
    "Management",
    "Pharmacy",
    "Medical",
    "Dental",
    "Law",
    "Architecture",
    "Agriculture",
    "Innovation",
]

INST_ID_RE = re.compile(r"^IR-[A-Z]-[A-Z]-\d+$")


def clean_name(raw: str) -> str:
    name = raw.split("More Details")[0].strip()
    name = re.sub(r"\s+", " ", name)
    return name


def parse_ranking_page(html: str, category: str, year: int) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_=lambda cls: cls and "table-condensed" in cls)
    if table is None:
        return []

    rows: list[dict] = []
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 10:
            continue
        vals = [td.get_text(" ", strip=True) for td in tds]
        institute_id = vals[0]
        if not INST_ID_RE.match(institute_id):
            continue
        try:
            score = float(vals[9])
            rank = int(float(vals[10]))
        except (ValueError, IndexError):
            continue
        rows.append(
            {
                "institute_id": institute_id,
                "institute_name": clean_name(vals[1]),
                "city": vals[7],
                "state": vals[8],
                "score": score,
                "rank": rank,
                "ranking_category": category,
                "nirf_year": year,
            }
        )
    return rows


def fetch_category(year: int, category: str) -> list[dict]:
    url = f"https://www.nirfindia.org/Rankings/{year}/{category}Ranking.html"
    print(f"  Fetching {category} ...")
    resp = SESSION.get(url, timeout=60)
    resp.raise_for_status()
    rows = parse_ranking_page(resp.text, category, year)
    print(f"    -> {len(rows)} institutes")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape NIRF rankings to CSV")
    parser.add_argument("--year", type=int, default=2024, help="NIRF release year (default: 2024)")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: data/raw/nirf_rankings_{year}.csv + nirf_rankings.csv)",
    )
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    year_path = RAW_DIR / f"nirf_rankings_{args.year}.csv"
    canonical_path = RAW_DIR / "nirf_rankings.csv"
    output_path = args.output or year_path
    all_rows: list[dict] = []
    for category in CATEGORIES:
        try:
            all_rows.extend(fetch_category(args.year, category))
        except requests.RequestException as exc:
            print(f"  FAILED {category}: {exc}")

    if not all_rows:
        print("No rows scraped. Check network or NIRF site layout.")
        sys.exit(1)

    df = pd.DataFrame(all_rows).drop_duplicates(
        subset=["institute_id", "ranking_category", "nirf_year"]
    )
    df = df.sort_values(["ranking_category", "rank", "institute_name"]).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    update_canonical = True
    if canonical_path.exists() and output_path.resolve() != canonical_path.resolve():
        try:
            existing_year = int(pd.read_csv(canonical_path, usecols=["nirf_year"])["nirf_year"].iloc[0])
            if args.year < existing_year:
                update_canonical = False
        except (ValueError, KeyError, IndexError):
            pass
    if update_canonical or output_path.resolve() == canonical_path.resolve():
        df.to_csv(canonical_path, index=False)
        print(f"Canonical copy -> {canonical_path} (year {args.year})")
    else:
        print(f"Left canonical copy at {existing_year} (newer than scraped {args.year})")

    print(f"\nWrote {len(df):,} rows -> {output_path}")
    print(f"Categories: {df['ranking_category'].nunique()}")
    print(f"Unique institutes: {df['institute_id'].nunique()}")
    print(f"NIRF year in file: {args.year}")
    print("Note: Innovation category often has 0 rows (different page layout) — not blocking.")


if __name__ == "__main__":
    main()
