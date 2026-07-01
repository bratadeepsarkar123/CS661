#!/usr/bin/env python3
"""Normalize scraped NIRF patent CSV into per-institute summary for join."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR, RAW_DIR  # noqa: E402

OUT_PATH = PROCESSED_DIR / "nirf_patents_by_institute.csv"
INPUTS = [
    RAW_DIR / "nirf_patents_scraped.csv",
    RAW_DIR / "nirf_patents.csv",
]


def _norm(s: str) -> str:
    s = str(s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _load() -> pd.DataFrame:
    for path in INPUTS:
        if path.exists():
            df = pd.read_csv(path)
            print(f"  Loaded {path.name}: {len(df):,} rows")
            return df
    raise FileNotFoundError(
        "No patent raw file. Run: python scripts/india_network/01f_scrape_nirf_patents_from_pdfs.py"
    )


def main() -> None:
    raw = _load()
    required = {"institute_id", "institute_name", "sub_category", "value"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Patent CSV missing columns. Need {required}, got {list(raw.columns)}")

    raw["institute_id"] = raw["institute_id"].astype(str).str.strip()
    raw["institute_name"] = raw["institute_name"].astype(str).str.strip()
    raw["sub_category_norm"] = raw["sub_category"].astype(str).str.lower()
    raw["value"] = pd.to_numeric(raw["value"], errors="coerce")
    raw["calendar_year"] = raw.get("calendar_year", pd.NA)
    raw["name_norm"] = raw["institute_name"].map(_norm)

    rows = []
    for (iid, name_norm), grp in raw.groupby(["institute_id", "name_norm"]):
        inst_name = grp["institute_name"].iloc[0]
        latest_year = grp["calendar_year"].max()
        sub = grp[grp["calendar_year"] == latest_year] if pd.notna(latest_year) else grp

        pub = sub[sub["sub_category_norm"].str.contains("published", na=False)]["value"]
        grant = sub[sub["sub_category_norm"].str.contains("granted", na=False)]["value"]

        rows.append(
            {
                "name_norm": name_norm,
                "institute_name_nirf": inst_name,
                "nirf_institute_id": iid,
                "patent_calendar_year": latest_year,
                "patents_published": int(pub.iloc[-1]) if len(pub) else pd.NA,
                "patents_granted": int(grant.iloc[-1]) if len(grant) else pd.NA,
                "patents_published_3yr": int(
                    grp[grp["sub_category_norm"].str.contains("published", na=False)]["value"].sum()
                ),
                "patents_granted_3yr": int(
                    grp[grp["sub_category_norm"].str.contains("granted", na=False)]["value"].sum()
                ),
            }
        )

    out = pd.DataFrame(rows)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_PATH, index=False)
    has = out["patents_published"].notna().sum()
    print(f"Wrote {len(out):,} institutes -> {OUT_PATH}")
    print(f"  With patent counts: {has}")
    print("Next: python scripts/india_network/08b_join_nirf_patents.py")


if __name__ == "__main__":
    main()
