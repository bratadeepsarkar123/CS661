#!/usr/bin/env python3
"""Normalize free NIRF funding CSVs from Dataful (no payment — one-click download).

Research projects (sponsored funding amounts):
  https://dataful.in/datasets/19311/
  Save as: data/raw/nirf_research_projects.csv  (or .xlsx)

Expenditure (capital + operational):
  https://dataful.in/datasets/19317/
  Save as: data/raw/nirf_expenditure.csv

Optional consultancy:
  https://dataful.in/datasets/19310/  (search "Consultation Projects" on dataful.in)
  Save as: data/raw/nirf_consultancy.csv

Output: data/processed/nirf_funding_by_institute.csv (long + wide ready for join)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR, RAW_DIR  # noqa: E402

OUT_PATH = PROCESSED_DIR / "nirf_funding_by_institute.csv"

RESEARCH_INPUTS = [
    RAW_DIR / "nirf_research_projects.csv",
    RAW_DIR / "nirf_research_projects.xlsx",
    RAW_DIR / "nirf_research_projects_dataful.csv",
]
EXPENDITURE_INPUTS = [
    RAW_DIR / "nirf_expenditure.csv",
    RAW_DIR / "nirf_expenditure.xlsx",
    RAW_DIR / "nirf_expenditure_dataful.csv",
]

RENAME = {
    "Institute ID": "institute_id",
    "Institute Id": "institute_id",
    "Institute Name": "institute_name",
    "Calendar Year": "academic_year",
    "Academic Year": "academic_year",
    "Ranking Year": "ranking_year",
    "Ranking Category": "ranking_category",
    "Sub Category": "sub_category",
    "Category": "category",
}


def _load_first(paths: list[Path]) -> pd.DataFrame | None:
    for path in paths:
        if not path.exists():
            continue
        if path.suffix.lower() == ".xlsx":
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        print(f"  Loaded {path.name}: {len(df):,} rows")
        return df
    return None


def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    for src, dst in RENAME.items():
        if src in df.columns and dst not in df.columns:
            df = df.rename(columns={src: dst})
    if "category" not in df.columns and "sub_category" in df.columns:
        df["category"] = df["sub_category"]
    return df


def _norm_name(name: str) -> str:
    s = str(name or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _to_crores(value: float, unit: str) -> float:
    u = str(unit or "").lower()
    if "crore" in u:
        return float(value)
    if "lakh" in u:
        return float(value) / 100.0
    # Dataful research amounts are often absolute rupees
    if "rupee" in u or value > 1_000_000:
        return float(value) / 1e7
    return float(value)


def _parse_research(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_cols(df)
    required = {"institute_id", "institute_name", "category", "value"}
    if not required.issubset(df.columns):
        raise ValueError(f"Research CSV missing columns. Need {required}, got {list(df.columns)}")

    df["institute_id"] = df["institute_id"].astype(str).str.strip()
    df["institute_name"] = df["institute_name"].astype(str).str.strip()
    df["category_norm"] = df["category"].astype(str).str.strip().str.lower()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["unit"] = df.get("unit", pd.Series([""] * len(df))).astype(str)

    if "academic_year" not in df.columns:
        df["academic_year"] = pd.NA
    if "ranking_year" not in df.columns:
        df["ranking_year"] = pd.NA

    # Latest academic year per institute name (IDs differ by NIRF category)
    df["name_norm"] = df["institute_name"].map(_norm_name)
    df = df.sort_values(["name_norm", "academic_year"], na_position="first")
    latest = df.groupby("name_norm", as_index=False).tail(1)[["name_norm", "academic_year", "ranking_year"]]
    latest_map = latest.set_index("name_norm")

    rows: list[dict] = []
    for name_norm, grp in df.groupby("name_norm"):
        # Prefer rows from latest academic year when present
        ac_year = latest_map.loc[name_norm, "academic_year"] if name_norm in latest_map.index else grp["academic_year"].max()
        sub = grp[grp["academic_year"] == ac_year] if pd.notna(ac_year) else grp
        if sub.empty:
            sub = grp

        inst_name = sub["institute_name"].iloc[0]
        inst_ids = "|".join(sorted(sub["institute_id"].unique()))

        amount_mask = sub["category_norm"].str.contains("amount", na=False) & sub["category_norm"].str.contains(
            "received|sponsor", na=False
        )
        if not amount_mask.any():
            amount_mask = sub["category_norm"].str.contains("total amount", na=False)
        project_mask = sub["category_norm"].str.contains("sponsored project", na=False) & ~sub[
            "category_norm"
        ].str.contains("amount", na=False)

        amount_inr = 0.0
        if amount_mask.any():
            amount_rows = sub[amount_mask]
            vals = []
            for _, row in amount_rows.iterrows():
                v = _to_crores(row["value"], row["unit"])
                if v and v > 0:
                    vals.append(v)
            if vals:
                amount_inr = max(vals)

        project_count = None
        if project_mask.any():
            project_count = int(sub[project_mask].iloc[-1]["value"])

        rows.append(
            {
                "name_norm": name_norm,
                "institute_name_nirf": inst_name,
                "nirf_institute_ids": inst_ids,
                "academic_year": ac_year,
                "ranking_year": sub["ranking_year"].max(),
                "research_funding_cr": round(amount_inr, 2) if amount_inr else None,
                "sponsored_projects": project_count,
            }
        )
    return pd.DataFrame(rows)


def _parse_expenditure(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_cols(df)
    if "institute_name" not in df.columns or "value" not in df.columns:
        return pd.DataFrame()

    cat_col = "category" if "category" in df.columns else "sub_category"
    df["institute_name"] = df["institute_name"].astype(str).str.strip()
    df["category_norm"] = df[cat_col].astype(str).str.lower()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["unit"] = df.get("unit", pd.Series([""] * len(df))).astype(str)
    df["name_norm"] = df["institute_name"].map(_norm_name)

    if "academic_year" in df.columns:
        df = df.sort_values(["name_norm", "academic_year"])
        latest_year = df.groupby("name_norm")["academic_year"].max()
    else:
        latest_year = None

    out_rows = []
    for name_norm, grp in df.groupby("name_norm"):
        if latest_year is not None and name_norm in latest_year.index:
            grp = grp[grp["academic_year"] == latest_year[name_norm]]
        cap = grp[grp["category_norm"].str.contains("capital", na=False)]["value"].sum()
        op = grp[grp["category_norm"].str.contains("operational", na=False)]["value"].sum()
        total = cap + op
        if total <= 0:
            total = grp["value"].sum()
        unit = grp["unit"].iloc[0] if len(grp) else ""
        out_rows.append(
            {
                "name_norm": name_norm,
                "total_expenditure_cr": round(_to_crores(total, unit), 2) if total else None,
            }
        )
    return pd.DataFrame(out_rows)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    research_raw = _load_first(RESEARCH_INPUTS)
    if research_raw is None:
        print(
            "MISSING: nirf_research_projects.csv\n\n"
            "Free download (no payment):\n"
            "  1. Open https://dataful.in/datasets/19311/\n"
            "  2. Click CSV (free Factly account if prompted)\n"
            "  3. Save as data/raw/nirf_research_projects.csv\n"
            "  4. Re-run this script\n\n"
            "Optional expenditure: https://dataful.in/datasets/19317/ -> nirf_expenditure.csv"
        )
        sys.exit(1)

    out = _parse_research(research_raw)
    exp_raw = _load_first(EXPENDITURE_INPUTS)
    if exp_raw is not None:
        exp = _parse_expenditure(exp_raw)
        out = out.merge(exp, on="name_norm", how="left")
    else:
        out["total_expenditure_cr"] = pd.NA
        print("  (No expenditure file — optional: dataful.in/datasets/19317/)")

    out.to_csv(OUT_PATH, index=False)
    matched = out["research_funding_cr"].notna().sum()
    print(f"\nWrote {len(out):,} institutes -> {OUT_PATH}")
    print(f"  With research funding amount: {matched}")
    print("Next: python scripts/india_network/08_join_nirf_funding.py")


if __name__ == "__main__":
    main()
