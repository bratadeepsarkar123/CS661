#!/usr/bin/env python3
"""Join NIRF funding totals to institution_master.csv."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402
from nirf_utils import (  # noqa: E402
    FUNDING_NAME_ALIASES,
    extract_distinguishing_tokens,
    funding_campus_compatible,
    load_nirf_id_overrides,
    name_similarity,
    norm_name,
)

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
FUNDING_PATH = PROCESSED_DIR / "nirf_funding_by_institute.csv"
OUT_PATH = PROCESSED_DIR / "institution_funding.csv"
FUZZY_MIN = 0.88



def _funding_name_score(inst: pd.Series, funding_row: pd.Series, alias: str | None = None) -> float:
    name = inst["canonical_name"]
    target = str(funding_row.get("institute_name_nirf", ""))
    if not funding_campus_compatible(name, target, city=inst.get("city")):
        return 0.0

    score = name_similarity(name, target)
    if alias:
        score = max(score, name_similarity(alias, target))

    canon_tokens = extract_distinguishing_tokens(name)
    if canon_tokens:
        target_tokens = extract_distinguishing_tokens(target)
        if not (canon_tokens & target_tokens):
            return 0.0

    if inst.get("city") and target:
        city = str(inst["city"]).lower()
        if city and city in target.lower():
            score += 0.05
    return score


def _pick_funding_row(
    inst: pd.Series,
    funding: pd.DataFrame,
    funding_idx: pd.DataFrame,
    id_lookup: dict[str, pd.Series],
) -> tuple[pd.Series | None, float]:
    name = inst["canonical_name"]
    nn = norm_name(name)
    alias = FUNDING_NAME_ALIASES.get(name)
    if alias:
        nn = norm_name(alias)

    nirf_id = inst.get("nirf_institute_id")
    if pd.isna(nirf_id):
        overrides = load_nirf_id_overrides()
        nirf_id = overrides.get(name)

    # ID match first — same display name can map to multiple NIRF category rows.
    if pd.notna(nirf_id) and str(nirf_id) in id_lookup:
        row = id_lookup[str(nirf_id)]
        target = str(row.get("institute_name_nirf", ""))
        if funding_campus_compatible(name, target, city=inst.get("city")):
            score = _funding_name_score(inst, row, alias=alias)
            return row, max(score, 0.95)

    # Name match when unambiguous (single row per normalized name).
    if nn in funding_idx.index:
        row = funding_idx.loc[nn]
        if isinstance(row, pd.DataFrame):
            if pd.notna(nirf_id):
                matched = row[row["nirf_institute_ids"].astype(str).str.contains(str(nirf_id), regex=False)]
                if not matched.empty:
                    row = matched.iloc[0]
                else:
                    row = row.iloc[0]
            else:
                row = row.iloc[0]
        target = str(row.get("institute_name_nirf", ""))
        if funding_campus_compatible(name, target, city=inst.get("city")):
            return row, 1.0

    best = None
    best_score = 0.0
    for _, f in funding.iterrows():
        score = _funding_name_score(inst, f, alias=alias)
        if score > best_score:
            best_score = score
            best = f

    if best is not None and best_score >= FUZZY_MIN:
        return best, best_score
    return None, 0.0


def main() -> None:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Run 03_build_institution_master.py first: {MASTER_PATH}")
    if not FUNDING_PATH.exists():
        raise FileNotFoundError(
            f"Run 01d_prepare_nirf_funding.py first (needs nirf_research_projects.csv): {FUNDING_PATH}"
        )

    master = pd.read_csv(MASTER_PATH)
    funding = pd.read_csv(FUNDING_PATH)
    funding_idx = funding.set_index("name_norm")

    id_lookup: dict[str, pd.Series] = {}
    for _, f in funding.iterrows():
        ids = str(f.get("nirf_institute_ids", "")).split("|")
        for iid in ids:
            iid = iid.strip()
            if iid:
                id_lookup[iid] = f

    rows = []
    for _, inst in master.iterrows():
        name = inst["canonical_name"]
        row, match_score = _pick_funding_row(inst, funding, funding_idx, id_lookup)
        rows.append(
            {
                "institution_id": inst["institution_id"],
                "canonical_name": name,
                "research_funding_cr": row["research_funding_cr"] if row is not None else pd.NA,
                "sponsored_projects": row["sponsored_projects"] if row is not None else pd.NA,
                "total_expenditure_cr": row.get("total_expenditure_cr", pd.NA) if row is not None else pd.NA,
                "funding_academic_year": row["academic_year"] if row is not None else pd.NA,
                "match_score": match_score if row is not None else pd.NA,
            }
        )

    out = pd.DataFrame(rows)
    out.to_csv(OUT_PATH, index=False)
    has_funding = out["research_funding_cr"].notna().sum()
    print(f"Wrote {OUT_PATH}")
    print(f"  Master rows with NIRF funding: {has_funding} / {len(out)}")


if __name__ == "__main__":
    main()
