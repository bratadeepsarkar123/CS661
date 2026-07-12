#!/usr/bin/env python3
"""Build institution_master.csv from overrides + OpenAlex + NIRF (Phase 0 stub)."""
from __future__ import annotations

import re
import sys
import uuid
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import (  # noqa: E402
    DATA_DIR,
    MANUAL_OVERRIDES_CSV,
    PREMIER_CAP,
    PREMIER_WORKS_MIN,
    PROCESSED_DIR,
    STATE_CAP,
    STATE_WORKS_MIN,
)
from ini_tier import apply_ini_premier_identity  # noqa: E402

OUT_PATH = PROCESSED_DIR / "institution_master.csv"
OPENALEX_PATH = PROCESSED_DIR / "openalex_institutions.parquet"


def load_openalex() -> pd.DataFrame:
    if not OPENALEX_PATH.exists():
        raise FileNotFoundError(f"Run 02_fetch_openalex_institutions.py first: {OPENALEX_PATH}")
    return pd.read_parquet(OPENALEX_PATH)


def _name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _fuzzy_match_openalex(oa: pd.DataFrame, canonical_name: str, city: str | None) -> pd.DataFrame:
    pool = oa.copy()
    if city and pd.notna(city):
        city_norm = str(city).strip().lower()
        pool = pool[pool["city"].fillna("").str.lower() == city_norm]
    if pool.empty:
        pool = oa

    tokens = {
        t
        for t in re.split(r"[^a-z0-9]+", canonical_name.lower())
        if len(t) > 2 and t not in {"indian", "institute", "technology", "the", "and", "of"}
    }
    if tokens:
        mask = pool["display_name"].fillna("").str.lower().apply(lambda name: all(t in name for t in tokens))
        pool = pool[mask]
    if pool.empty:
        return pd.DataFrame()

    pool = pool.assign(_sim=pool["display_name"].apply(lambda n: _name_similarity(canonical_name, str(n))))
    best = pool.loc[pool["_sim"].idxmax()]
    if best["_sim"] < 0.72:
        return pd.DataFrame()
    return pd.DataFrame([best.drop("_sim")])


def _override_stub_row(ov: pd.Series) -> dict | None:
    oid = str(ov.get("openalex_id") or "").strip()
    ror = str(ov.get("ror_id") or "").strip()
    if not oid:
        return None
    return {
        "institution_id": str(uuid.uuid4()),
        "canonical_name": ov["canonical_name"],
        "tier": ov.get("tier", "premier"),
        "inst_type": ov.get("inst_type", ""),
        "city": ov.get("city"),
        "state": ov.get("state"),
        "openalex_id": oid,
        "ror_id": ror or None,
        "latitude": pd.NA,
        "longitude": pd.NA,
        "total_works": int(ov.get("total_works") or 0),
        "match_confidence": "manual",
        "is_hub": False,
    }


def match_overrides(oa: pd.DataFrame, overrides: pd.DataFrame) -> pd.DataFrame:
    oa = oa.copy()
    oa["ror_id_norm"] = oa["ror_id"].fillna("").str.lower()
    rows = []

    for _, ov in overrides.iterrows():
        ror = str(ov.get("ror_id") or "").strip().lower()
        match = oa[oa["ror_id_norm"] == ror] if ror else pd.DataFrame()
        if match.empty and pd.notna(ov.get("openalex_id")):
            oid = str(ov["openalex_id"]).strip()
            match = oa[oa["openalex_id"] == oid]
        if match.empty:
            match = _fuzzy_match_openalex(oa, str(ov["canonical_name"]), ov.get("city"))
        if match.empty:
            stub = _override_stub_row(ov)
            if stub:
                rows.append(stub)
                print(f"NOTE: using override IDs for {ov['canonical_name']} (not in openalex_institutions.parquet)")
            else:
                print(f"WARN: no OpenAlex match for {ov['canonical_name']}")
            continue
        m = match.iloc[0]
        rows.append(
            {
                "institution_id": str(uuid.uuid4()),
                "canonical_name": ov["canonical_name"],
                "tier": ov.get("tier", "premier"),
                "inst_type": ov.get("inst_type", ""),
                "city": ov.get("city") or m["city"],
                "state": ov.get("state") or m.get("region"),
                "openalex_id": m["openalex_id"],
                "ror_id": m["ror_id"],
                "latitude": m["latitude"],
                "longitude": m["longitude"],
                "total_works": int(m["works_count"]),
                "match_confidence": "manual",
                "is_hub": False,
            }
        )
    return pd.DataFrame(rows)


def add_tier_candidates(
    oa: pd.DataFrame,
    existing_ids: set[str],
    premier_slots: int,
    state_slots: int,
) -> pd.DataFrame:
    pool = oa[~oa["openalex_id"].isin(existing_ids)].copy()
    pool = pool[pool["latitude"].notna() & pool["longitude"].notna()]

    premier = (
        pool[pool["works_count"] >= PREMIER_WORKS_MIN].nlargest(max(premier_slots, 0), "works_count")
        if premier_slots > 0
        else pd.DataFrame()
    )
    premier_ids = set(premier["openalex_id"]) if not premier.empty else set()
    state_pool = pool[~pool["openalex_id"].isin(premier_ids)]
    state = (
        state_pool[state_pool["works_count"] >= STATE_WORKS_MIN].nlargest(max(state_slots, 0), "works_count")
        if state_slots > 0
        else pd.DataFrame()
    )

    def to_rows(df: pd.DataFrame, tier: str) -> list[dict]:
        out = []
        for _, m in df.iterrows():
            out.append(
                {
                    "institution_id": str(uuid.uuid4()),
                    "canonical_name": m["display_name"],
                    "tier": tier,
                    "inst_type": "State_Univ" if tier == "state_affiliated" else "Central_Univ",
                    "city": m["city"],
                    "state": m.get("region"),
                    "openalex_id": m["openalex_id"],
                    "ror_id": m["ror_id"],
                    "latitude": m["latitude"],
                    "longitude": m["longitude"],
                    "total_works": int(m["works_count"]),
                    "match_confidence": "openalex_auto",
                    "is_hub": False,
                }
            )
        return out

    return pd.DataFrame(to_rows(premier, "premier") + to_rows(state, "state_affiliated"))


def enforce_tier_caps(master: pd.DataFrame) -> pd.DataFrame:
    """Keep manual + INI-identity overrides; trim auto rows to 60 premier + 60 state."""

    def trim(tier: str, cap: int) -> pd.DataFrame:
        tier_df = master[master["tier"] == tier].copy()
        rest = master[master["tier"] != tier]
        conf = tier_df["match_confidence"].astype(str)
        # Priority: manual (2) > ini_identity (1) > openalex_auto (0)
        tier_df["_prio"] = 0
        tier_df.loc[conf.eq("ini_identity"), "_prio"] = 1
        tier_df.loc[conf.eq("manual"), "_prio"] = 2
        tier_df = (
            tier_df.sort_values(["_prio", "total_works"], ascending=[False, False])
            .head(cap)
            .drop(columns="_prio")
        )
        return pd.concat([rest, tier_df], ignore_index=True)

    out = master
    out = trim("premier", PREMIER_CAP)
    out = trim("state_affiliated", STATE_CAP)
    return out.drop_duplicates(subset=["openalex_id"])


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    overrides_path = MANUAL_OVERRIDES_CSV if MANUAL_OVERRIDES_CSV.exists() else DATA_DIR / "manual_institution_overrides.csv"
    overrides = pd.read_csv(overrides_path)
    oa = load_openalex()

    manual_df = match_overrides(oa, overrides)
    manual_premier = int((manual_df["tier"] == "premier").sum()) if not manual_df.empty else 0
    manual_state = int((manual_df["tier"] == "state_affiliated").sum()) if not manual_df.empty else 0
    premier_slots = max(PREMIER_CAP - manual_premier, 0)
    state_slots = max(STATE_CAP - manual_state, 0)

    extra_df = add_tier_candidates(
        oa,
        set(manual_df["openalex_id"]) if not manual_df.empty else set(),
        premier_slots,
        state_slots,
    )
    master = pd.concat([manual_df, extra_df], ignore_index=True)
    master = master.drop_duplicates(subset=["openalex_id"])
    # Volume fill first, then promote recognized INIs (AIIMS/NIT/JIPMER/…) and
    # rebalance the 60/60 caps without dropping protected rows.
    master = apply_ini_premier_identity(master, premier_cap=PREMIER_CAP)
    master = enforce_tier_caps(master)
    # Second pass keeps INI labels if enforce_tier_caps reshuffled auto rows.
    master = apply_ini_premier_identity(master, premier_cap=PREMIER_CAP)

    master.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(master)} rows -> {OUT_PATH}")
    print(f"  premier: {(master['tier'] == 'premier').sum()}")
    print(f"  state_affiliated: {(master['tier'] == 'state_affiliated').sum()}")
    ini_n = int(master["match_confidence"].astype(str).eq("ini_identity").sum())
    print(f"  ini_identity: {ini_n}")


if __name__ == "__main__":
    main()
