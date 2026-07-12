"""INI / national-institute identity helpers for Graph 5 tier assignment.

Premier is primarily research-volume based (top 60 by OpenAlex works, plus
manual IIT/IISc overrides). That alone mislabels newer AIIMS / NITs / JIPMER
as state_affiliated because they publish less than older high-volume schools.

This module applies an honest name-identity override: recognized Institutes of
National Importance (and explicit AIIMS campus names) that already appear in
the master are forced to tier=premier, with reciprocal demotions of lowest
works non-INI auto rows to keep the 60/60 cap.
"""
from __future__ import annotations

import re

import pandas as pd

# Honest identity patterns only — do not invent campuses; only reclassify rows
# already present in institution_master / the OpenAlex candidate pool.
INI_PREMIER_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"all india institute of medical sciences", re.I),
    re.compile(r"\baiims\b", re.I),
    re.compile(
        r"jawaharlal institute of post[\s\-]?graduate medical education and research",
        re.I,
    ),
    re.compile(r"\bjipmer\b", re.I),
    re.compile(
        r"post graduate institute of medical education and research",
        re.I,
    ),
    re.compile(r"\bpgimer\b", re.I),
    # NITs (incl. named variants: Malaviya / Sardar Vallabhbhai / …)
    re.compile(r"national institute of technology\b", re.I),
    # Other central research INIs that volume-fill already ranked premier;
    # protect them from being demoted when AIIMS/NITs are promoted.
    re.compile(r"^indian statistical institute\b", re.I),
    re.compile(r"^homi bhabha national institute\b", re.I),
)

INI_INST_TYPE_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"all india institute of medical sciences|\baiims\b", re.I), "AIIMS"),
    (
        re.compile(
            r"jawaharlal institute of post[\s\-]?graduate medical|\bjipmer\b",
            re.I,
        ),
        "JIPMER",
    ),
    (
        re.compile(
            r"post graduate institute of medical education|\bpgimer\b",
            re.I,
        ),
        "PGIMER",
    ),
    (re.compile(r"national institute of technology\b", re.I), "NIT"),
    (re.compile(r"^indian statistical institute\b", re.I), "ISI"),
    (re.compile(r"^homi bhabha national institute\b", re.I), "HBNI"),
)


def is_ini_premier_name(name: str | None) -> bool:
    text = str(name or "").strip()
    if not text:
        return False
    return any(p.search(text) for p in INI_PREMIER_PATTERNS)


def ini_inst_type(name: str | None, fallback: str = "Central_Univ") -> str:
    text = str(name or "")
    for pattern, label in INI_INST_TYPE_RULES:
        if pattern.search(text):
            return label
    return fallback


def _protected_premier_mask(df: pd.DataFrame) -> pd.Series:
    """Rows that must stay premier when rebalancing the 60-cap."""
    manual = df["match_confidence"].astype(str).eq("manual")
    ini = df["canonical_name"].map(is_ini_premier_name)
    ini_marked = df["match_confidence"].astype(str).isin({"ini_identity", "manual"})
    return manual | ini | ini_marked


def apply_ini_premier_identity(master: pd.DataFrame, premier_cap: int = 60) -> pd.DataFrame:
    """Force INI-identity rows to premier; demote lowest non-protected auto premiers.

    Preserves institution_id and does not add/remove institutes — only swaps
    tier (+ inst_type) so existing collaboration edges stay valid.
    """
    out = master.copy()
    name = out["canonical_name"].astype(str)

    ini_mask = name.map(is_ini_premier_name)
    promote_mask = ini_mask & out["tier"].astype(str).eq("state_affiliated")
    promote_idx = list(out.index[promote_mask])

    for idx in promote_idx:
        out.at[idx, "tier"] = "premier"
        out.at[idx, "inst_type"] = ini_inst_type(out.at[idx, "canonical_name"])
        # Keep manual if already manual; otherwise mark identity override.
        if str(out.at[idx, "match_confidence"]) != "manual":
            out.at[idx, "match_confidence"] = "ini_identity"

    # Align inst_type for INI rows already premier (e.g. AIIMS Delhi).
    already = ini_mask & out["tier"].astype(str).eq("premier")
    for idx in out.index[already]:
        out.at[idx, "inst_type"] = ini_inst_type(
            out.at[idx, "canonical_name"],
            fallback=str(out.at[idx, "inst_type"] or "Central_Univ"),
        )
        if str(out.at[idx, "match_confidence"]) == "openalex_auto":
            out.at[idx, "match_confidence"] = "ini_identity"

    n_premier = int(out["tier"].astype(str).eq("premier").sum())
    overflow = n_premier - premier_cap
    if overflow > 0:
        protected = _protected_premier_mask(out)
        demote_pool = out[
            out["tier"].astype(str).eq("premier") & ~protected
        ].copy()
        demote_pool["_works"] = pd.to_numeric(demote_pool["total_works"], errors="coerce").fillna(0)
        demote_pool = demote_pool.sort_values(["_works", "canonical_name"], ascending=[True, True])
        demote_idx = list(demote_pool.head(overflow).index)
        for idx in demote_idx:
            out.at[idx, "tier"] = "state_affiliated"
            out.at[idx, "inst_type"] = "State_Univ"
            if str(out.at[idx, "match_confidence"]) == "ini_identity":
                out.at[idx, "match_confidence"] = "openalex_auto"

    return out
