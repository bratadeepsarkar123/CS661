#!/usr/bin/env python3
"""Join Scimago India university rankings to institution_master (static quality layer)."""
from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR, RAW_DIR  # noqa: E402

SCIMAGO_PATH = RAW_DIR / "scimago_india.csv"
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
OUT_PATH = PROCESSED_DIR / "institution_quality_static.csv"
SCIMAGO_YEAR = 2019
MATCH_THRESHOLD = 0.72


def _clean_scimago_name(name: str) -> str:
    s = str(name).strip()
    s = re.sub(r"\s*\*$", "", s)
    s = re.sub(r",\s*india$", "", s, flags=re.IGNORECASE)
    return s


def _name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _fuzzy_match_scimago(
    universities: pd.DataFrame,
    canonical_name: str,
    city: str | None,
) -> pd.Series | None:
    pool = universities.assign(
        _sim=universities["Institution"].apply(
            lambda n: _name_similarity(canonical_name, _clean_scimago_name(str(n)))
        )
    )
    best_overall = pool.loc[pool["_sim"].idxmax()]
    if best_overall["_sim"] < MATCH_THRESHOLD:
        return None

    if city and pd.notna(city):
        city_norm = str(city).strip().lower()
        city_pool = pool[pool["Institution"].fillna("").str.lower().str.contains(re.escape(city_norm), regex=True)]
        if not city_pool.empty:
            best_city = city_pool.loc[city_pool["_sim"].idxmax()]
            # Prefer city only when it remains competitive with the global best match.
            if best_city["_sim"] >= MATCH_THRESHOLD and best_city["_sim"] >= best_overall["_sim"] - 0.02:
                return best_city

    return best_overall


def main() -> None:
    if not SCIMAGO_PATH.exists():
        raise FileNotFoundError(f"Missing Scimago source: {SCIMAGO_PATH}")
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Run 03_build_institution_master.py first: {MASTER_PATH}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    scimago = pd.read_csv(SCIMAGO_PATH, sep=";")
    universities = scimago[scimago["Sector"].fillna("").str.contains("Universit", case=False, na=False)].copy()
    master = pd.read_csv(MASTER_PATH)

    rows: list[dict] = []
    for _, inst in master.iterrows():
        match = _fuzzy_match_scimago(universities, str(inst["canonical_name"]), inst.get("city"))
        if match is None:
            continue
        rows.append(
            {
                "institution_id": inst["institution_id"],
                "openalex_id": inst["openalex_id"],
                "canonical_name": inst["canonical_name"],
                "scimago_idp": int(match["Idp"]),
                "scimago_rank": int(match["Rank"]),
                "scimago_global_rank": int(match["Global Rank"]),
                "scimago_pct": float(match["Percentage"]),
                "scimago_percentile": float(match["Percentile"]),
                # Scimago export has no Q1 field; Percentage is used as a proxy for Q1 share.
                "scimago_q1_pct": float(match["Percentage"]),
                "scimago_year": SCIMAGO_YEAR,
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(OUT_PATH, index=False)

    matched = len(out)
    total = len(master)
    print(f"Scimago matches: {matched} / {total} master rows")
    print(f"Wrote {matched} rows -> {OUT_PATH}")


if __name__ == "__main__":
    main()
