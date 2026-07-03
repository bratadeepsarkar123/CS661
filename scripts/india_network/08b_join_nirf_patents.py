#!/usr/bin/env python3
"""Join NIRF patent counts to institution_master."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402
from nirf_utils import FUNDING_NAME_ALIASES, load_nirf_id_overrides, name_similarity, norm_name  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
PATENTS_PATH = PROCESSED_DIR / "nirf_patents_by_institute.csv"
OUT_PATH = PROCESSED_DIR / "institution_patents.csv"

# Institutions not in NIRF 2024 — no official Innovation PDF exists.
UNRANKED_NIRF_NAMES = {
    "Guru Nanak Dev University",
    "Dr. Hari Singh Gour University",
    "Indian Association for the Cultivation of Science",
    "G.S. Science, Arts And Commerce College",
}


def _pick_row(inst: pd.Series, patents: pd.DataFrame, idx: pd.DataFrame, id_lookup: dict) -> tuple[pd.Series | None, float, str | None]:
    name = inst["canonical_name"]
    nn = norm_name(FUNDING_NAME_ALIASES.get(name, name))

    nirf_id = inst.get("nirf_institute_id")
    if pd.isna(nirf_id):
        nirf_id = load_nirf_id_overrides().get(name)
    if pd.notna(nirf_id) and str(nirf_id) in id_lookup:
        row = id_lookup[str(nirf_id)]
        return row, 1.0, str(row.get("nirf_institute_id") or nirf_id)
    if nn in idx.index:
        row = idx.loc[nn]
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        return row, 1.0, str(row.get("nirf_institute_id") or nn)

    best = None
    best_score = 0.0
    for _, p in patents.iterrows():
        score = name_similarity(name, p["institute_name_nirf"])
        if inst.get("city") and str(inst["city"]).lower() in str(p.get("institute_name_nirf", "")).lower():
            score += 0.05
        if score > best_score:
            best_score = score
            best = p
    if best is not None and best_score >= 0.78:
        patent_id = str(best.get("nirf_institute_id") or "")
        inst_id = inst.get("nirf_institute_id")
        if pd.notna(inst_id) and patent_id and str(inst_id) != patent_id:
            return None, 0.0, None
        return best, best_score, str(best.get("nirf_institute_id") or best.get("name_norm"))
    return None, 0.0, None


def _name_match_rank(canonical_name: str, patent_institute_name: str) -> float:
    return name_similarity(canonical_name, patent_institute_name)


def _dedupe_patent_collisions(out: pd.DataFrame, patents: pd.DataFrame) -> pd.DataFrame:
    """Only one institution may claim the same NIRF source row (by nirf_institute_id)."""
    out = out.copy()
    if "nirf_patent_source_id" not in out.columns:
        return out
    has = out["nirf_patent_source_id"].notna()
    if not has.any():
        return out

    patent_names = {
        str(row["nirf_institute_id"]): str(row.get("institute_name_nirf") or "")
        for _, row in patents.iterrows()
        if pd.notna(row.get("nirf_institute_id"))
    }

    null_cols = [
        "patents_published",
        "patents_granted",
        "patents_published_3yr",
        "patents_granted_3yr",
        "patent_calendar_year",
        "nirf_patent_source_id",
    ]
    for source_id, group in out[has].groupby("nirf_patent_source_id", dropna=False):
        if len(group) <= 1:
            continue
        patent_name = patent_names.get(str(source_id), "")
        ranked = group.copy()
        ranked["_name_match"] = ranked["canonical_name"].map(
            lambda n: _name_match_rank(n, patent_name) if patent_name else 0.0
        )
        keep_idx = ranked.sort_values(
            ["_name_match", "match_score", "canonical_name"],
            ascending=[False, False, True],
        ).index[0]
        for idx in group.index:
            if idx == keep_idx:
                continue
            out.loc[idx, null_cols] = pd.NA
            out.loc[idx, "patent_status"] = "duplicate_resolved"
    return out


def main() -> None:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Missing {MASTER_PATH}")
    if not PATENTS_PATH.exists():
        raise FileNotFoundError(f"Run 01g_prepare_nirf_patents.py first: {PATENTS_PATH}")

    master = pd.read_csv(MASTER_PATH)
    patents = pd.read_csv(PATENTS_PATH)
    idx = patents.set_index("name_norm")
    id_lookup = {str(r["nirf_institute_id"]): r for _, r in patents.iterrows()}

    rows = []
    for _, inst in master.iterrows():
        name = inst["canonical_name"]
        if name in UNRANKED_NIRF_NAMES:
            rows.append(
                {
                    "institution_id": inst["institution_id"],
                    "canonical_name": name,
                    "patents_published": pd.NA,
                    "patents_granted": pd.NA,
                    "patents_published_3yr": pd.NA,
                    "patents_granted_3yr": pd.NA,
                    "patent_calendar_year": pd.NA,
                    "match_score": pd.NA,
                    "nirf_patent_source_id": pd.NA,
                    "patent_status": "unranked",
                }
            )
            continue

        row, score, source_id = _pick_row(inst, patents, idx, id_lookup)
        if row is not None and pd.notna(row.get("patents_published")):
            status = "reported"
        elif pd.notna(inst.get("nirf_rank")) or pd.notna(inst.get("nirf_institute_id")):
            status = "unavailable"
        else:
            status = "unavailable"
        rows.append(
            {
                "institution_id": inst["institution_id"],
                "canonical_name": name,
                "patents_published": row["patents_published"] if row is not None else pd.NA,
                "patents_granted": row["patents_granted"] if row is not None else pd.NA,
                "patents_published_3yr": row.get("patents_published_3yr", pd.NA) if row is not None else pd.NA,
                "patents_granted_3yr": row.get("patents_granted_3yr", pd.NA) if row is not None else pd.NA,
                "patent_calendar_year": row.get("patent_calendar_year", pd.NA) if row is not None else pd.NA,
                "match_score": score if row is not None else pd.NA,
                "nirf_patent_source_id": source_id if source_id else pd.NA,
                "patent_status": status if row is not None else status,
            }
        )

    out = pd.DataFrame(rows)
    out = _dedupe_patent_collisions(out, patents)
    # Losers in a collision have nulled source ids; treat as unavailable in the UI.
    stale_dup = out["patent_status"].eq("duplicate_resolved") & out["nirf_patent_source_id"].isna()
    out.loc[stale_dup, "patent_status"] = "unavailable"
    out.to_csv(OUT_PATH, index=False)
    has = out["patents_published"].notna().sum()
    dup = (out["patent_status"] == "duplicate_resolved").sum()
    print(f"Wrote {OUT_PATH}")
    print(f"  Master rows with NIRF patents: {has} / {len(out)}")
    if dup:
        print(f"  Duplicate-resolved (nulled): {dup}")


if __name__ == "__main__":
    main()
