#!/usr/bin/env python3
"""In-place INI premier reclassification for existing institution_master.csv.

Does NOT regenerate institution_id values (edges stay valid). Use after the
volume-based master is already built; then re-run 09_export + regenerate JS.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PREMIER_CAP, PROCESSED_DIR  # noqa: E402
from ini_tier import apply_ini_premier_identity, is_ini_premier_name  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
BACKUP_PATH = PROCESSED_DIR / "institution_master_pre_ini_tier.csv"
MIRROR_PATHS = [
    Path(__file__).resolve().parents[2] / "CS661 Project" / "data" / "processed" / "institution_master.csv",
]


def main() -> None:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(MASTER_PATH)

    before = pd.read_csv(MASTER_PATH)
    shutil.copy2(MASTER_PATH, BACKUP_PATH)

    after = apply_ini_premier_identity(before, premier_cap=PREMIER_CAP)

    changed = before[["openalex_id", "canonical_name", "tier"]].merge(
        after[["openalex_id", "tier", "inst_type", "match_confidence"]],
        on="openalex_id",
        suffixes=("_before", "_after"),
    )
    flips = changed[changed["tier_before"] != changed["tier_after"]].copy()
    flips = flips.sort_values(["tier_after", "canonical_name"])

    after.to_csv(MASTER_PATH, index=False)
    for mirror in MIRROR_PATHS:
        if mirror.parent.exists():
            after.to_csv(mirror, index=False)
            print(f"Mirrored -> {mirror}")

    print(f"Backup -> {BACKUP_PATH}")
    print(f"Updated -> {MASTER_PATH}")
    print(f"  premier: {(after['tier'] == 'premier').sum()} (was {(before['tier'] == 'premier').sum()})")
    print(f"  state_affiliated: {(after['tier'] == 'state_affiliated').sum()}")
    print(f"  tier flips: {len(flips)}")
    if not flips.empty:
        print(flips[["canonical_name", "tier_before", "tier_after", "inst_type", "match_confidence"]].to_string(index=False))

    aiims = after[after["canonical_name"].map(is_ini_premier_name) & after["canonical_name"].str.contains("All India|AIIMS", case=False, na=False)]
    print("\nAIIMS in master after fix:")
    print(aiims[["canonical_name", "tier", "inst_type", "total_works", "match_confidence", "city"]].to_string(index=False))


if __name__ == "__main__":
    main()
