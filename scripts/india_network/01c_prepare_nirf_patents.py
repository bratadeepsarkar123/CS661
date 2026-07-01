#!/usr/bin/env python3
"""
Normalize manually downloaded NIRF patent data into data/raw/nirf_patents.csv.

Dataful (free browser download):
  https://dataful.in/datasets/20551/
  Save the downloaded CSV/XLSX as one of:
    - data/raw/nirf_patents_dataful.csv
    - data/raw/nirf_patents_dataful.xlsx

Output schema (long format, ETL-friendly):
  institute_id, institute_name, state, city, calendar_year,
  category, sub_category, value, unit, ranking_year
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import RAW_DIR  # noqa: E402

OUT_PATH = RAW_DIR / "nirf_patents.csv"
INPUT_CANDIDATES = [
    RAW_DIR / "nirf_patents_dataful.csv",
    RAW_DIR / "nirf_patents_dataful.xlsx",
    RAW_DIR / "nirf_patents_download.csv",
]

RENAME = {
    "Institute ID": "institute_id",
    "Institute Id": "institute_id",
    "institute id": "institute_id",
    "Institute Name": "institute_name",
    "Calendar Year": "calendar_year",
    "Sub Category": "sub_category",
    "Sub category": "sub_category",
    "Ranking Year": "ranking_year",
}


def load_raw() -> pd.DataFrame:
    for path in INPUT_CANDIDATES:
        if not path.exists():
            continue
        if path.suffix.lower() == ".xlsx":
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        print(f"Loaded {path.name}: {len(df)} rows")
        return df
    raise FileNotFoundError(
        "No manual download found. Steps:\n"
        "  1) Open https://dataful.in/datasets/20551/\n"
        "  2) Click CSV and download (free account may be required)\n"
        "  3) Save as data/raw/nirf_patents_dataful.csv\n"
        "  4) Re-run this script"
    )


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    lower_map = {c.lower().replace("_", " "): c for c in df.columns}
    for src, dst in RENAME.items():
        key = src.lower()
        if key in lower_map:
            df = df.rename(columns={lower_map[key]: dst})

    required = ["institute_id", "sub_category", "value"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Unexpected columns. Missing {missing}. Got: {list(df.columns)}")

    df["institute_id"] = df["institute_id"].astype(str).str.strip()
    df["sub_category"] = df["sub_category"].astype(str).str.strip()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["institute_id", "value"])

    keep = [
        "ranking_year",
        "institute_id",
        "institute_name",
        "state",
        "city",
        "calendar_year",
        "category",
        "sub_category",
        "value",
        "unit",
    ]
    for col in keep:
        if col not in df.columns:
            df[col] = pd.NA
    out = df[keep].sort_values(["institute_id", "calendar_year", "sub_category"]).reset_index(drop=True)
    return out


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = normalize(load_raw())
    df.to_csv(OUT_PATH, index=False)
    inst = df["institute_id"].nunique()
    published = df[df["sub_category"].str.contains("Published", case=False, na=False)]["value"].sum()
    granted = df[df["sub_category"].str.contains("Granted", case=False, na=False)]["value"].sum()
    print(f"\nWrote {len(df):,} rows -> {OUT_PATH}")
    print(f"Unique institutes: {inst}")
    print(f"Sum published (all years/rows): {published:.0f}")
    print(f"Sum granted (all years/rows): {granted:.0f}")
    print("\nNote: Dataful patent data covers only institutes that filed detailed NIRF submissions (~10-50 HEIs).")


if __name__ == "__main__":
    main()
