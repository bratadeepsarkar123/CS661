#!/usr/bin/env python3
"""Enrich institution_master: fix missing geo, join NIRF ids/ranks."""
from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_DIR, PROCESSED_DIR, RAW_DIR  # noqa: E402
from nirf_utils import assign_nirf_matches, load_nirf_all, update_master_in_scrape_gaps  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
LOSERS_PATH = PROCESSED_DIR / "nirf_match_losers.csv"
GEO_PATH = RAW_DIR / "india_higher_education.csv"
NIRF_PATH = RAW_DIR / "nirf_rankings.csv"
OPENALEX_PATH = PROCESSED_DIR / "openalex_institutions.parquet"


def _norm(s: str) -> str:
    s = str(s or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def load_geo_lookup() -> pd.DataFrame:
    if not GEO_PATH.exists():
        return pd.DataFrame()
    geo = pd.read_csv(GEO_PATH, encoding="latin-1")
    geo["name_norm"] = geo["proper_university"].fillna(geo.get("university", "")).map(_norm)
    return geo


def load_nirf_best() -> pd.DataFrame:
    if not NIRF_PATH.exists():
        return pd.DataFrame()
    nirf = pd.read_csv(NIRF_PATH)
    # Prefer Overall category; keep best (lowest) rank per institute_id
    overall = nirf[nirf["ranking_category"] == "Overall"].copy()
    if overall.empty:
        overall = nirf.copy()
    overall = overall.sort_values(["institute_id", "rank"]).drop_duplicates("institute_id", keep="first")
    overall["name_norm"] = overall["institute_name"].map(_norm)
    return overall


def fill_geo_from_sources(master: pd.DataFrame, geo: pd.DataFrame, oa: pd.DataFrame) -> pd.DataFrame:
    master = master.copy()
    oa_idx = oa.set_index("openalex_id") if not oa.empty else pd.DataFrame()

    for idx, row in master.iterrows():
        if pd.notna(row.get("latitude")) and pd.notna(row.get("longitude")):
            continue
        oid = row.get("openalex_id")
        if not oa.empty and oid in oa_idx.index:
            o = oa_idx.loc[oid]
            if pd.notna(o.get("latitude")) and pd.notna(o.get("longitude")):
                master.at[idx, "latitude"] = o["latitude"]
                master.at[idx, "longitude"] = o["longitude"]
                continue
        if not geo.empty:
            best = None
            best_score = 0.0
            for _, g in geo.iterrows():
                score = _sim(row["canonical_name"], g["name_norm"])
                if row.get("city") and pd.notna(g.get("lat")):
                    city_norm = _norm(row["city"])
                    if city_norm and city_norm in g["name_norm"]:
                        score += 0.05
                if score > best_score:
                    best_score = score
                    best = g
            if best is not None and best_score >= 0.65:
                master.at[idx, "latitude"] = best["lat"]
                master.at[idx, "longitude"] = best["long"]

    return master


def join_nirf(master: pd.DataFrame, nirf_all: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    if nirf_all.empty:
        return master, pd.DataFrame()
    return assign_nirf_matches(master, nirf_all)


def main() -> None:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Run 03_build_institution_master.py first: {MASTER_PATH}")

    master = pd.read_csv(MASTER_PATH)
    geo = load_geo_lookup()
    nirf_all = load_nirf_all()
    oa = pd.read_parquet(OPENALEX_PATH) if OPENALEX_PATH.exists() else pd.DataFrame()

    before_missing = master["latitude"].isna().sum()
    master = fill_geo_from_sources(master, geo, oa)
    master, losers = join_nirf(master, nirf_all)

    master.to_csv(MASTER_PATH, index=False)
    if not losers.empty:
        losers.to_csv(LOSERS_PATH, index=False)
        print(f"  NIRF match losers: {len(losers)} -> {LOSERS_PATH}")
    elif LOSERS_PATH.exists():
        LOSERS_PATH.unlink()

    gaps_path = update_master_in_scrape_gaps(master)
    print(f"  NIRF scrape gaps (master) -> {gaps_path}")

    after_missing = master["latitude"].isna().sum()
    nirf_matched = master["nirf_institute_id"].notna().sum()
    print(f"Updated -> {MASTER_PATH}")
    print(f"  Geo fixed: {before_missing - after_missing} rows (missing lat/lon now: {after_missing})")
    print(f"  NIRF matched: {nirf_matched} / {len(master)}")


if __name__ == "__main__":
    main()
