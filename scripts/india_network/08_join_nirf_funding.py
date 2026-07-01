#!/usr/bin/env python3
"""Join NIRF funding totals to institution_master.csv."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402
from nirf_utils import FUNDING_NAME_ALIASES, best_nirf_match, load_nirf_id_overrides, name_similarity, norm_name  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
FUNDING_PATH = PROCESSED_DIR / "nirf_funding_by_institute.csv"
OUT_PATH = PROCESSED_DIR / "institution_funding.csv"


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

    if pd.notna(nirf_id) and str(nirf_id) in id_lookup:
        return id_lookup[str(nirf_id)], 1.0

    if nn in funding_idx.index:
        row = funding_idx.loc[nn]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        return row, 1.0

    best = None
    best_score = 0.0
    for _, f in funding.iterrows():
        score = name_similarity(name, f["institute_name_nirf"])
        if alias:
            score = max(score, name_similarity(alias, f["institute_name_nirf"]))
        if inst.get("city") and pd.notna(f.get("institute_name_nirf")):
            if str(inst["city"]).lower() in str(f["institute_name_nirf"]).lower():
                score += 0.05
        if score > best_score:
            best_score = score
            best = f
    if best is not None and best_score >= 0.78:
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
