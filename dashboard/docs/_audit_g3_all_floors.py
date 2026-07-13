#!/usr/bin/env python3
"""Audit all G3 honesty floors: raw river global counts vs pool around each floor."""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RIVER = ROOT / "CS661_Dataset" / "raw_vault" / "READY_FOR_TEAM" / "openalex_topic_country_year.csv"
VIZ3 = ROOT / "dashboard" / "viz3_data.js"
OUT = Path(__file__).resolve().parent / "_audit_g3_all_floors.json"

# topic_name, concept_id, CURRENT floor after soft-1974 policy, window
TOPICS = [
    ("Infectious Diseases", "C524204448", 1974, (1970, 1980)),
    ("Renewable Energy", "C188573790", 1974, (1970, 1980)),
    ("AI & Machine Learning", "C119857082", 1974, (1970, 1985)),
    ("Robotics & Automation", "C34413123", 1974, (1974, 1985)),
    ("Quantum Computing", "C58053490", 1974, (1985, 2000)),
    ("Data Science & Big Data", "C2522767166", 1974, (1995, 2005)),
    ("CRISPR & Genomics", "C98108389", 1974, (2005, 2015)),
]
# Historical floors (before soft-1974 policy) — for cliff reporting only
OLD_FLOORS = {
    "Infectious Diseases": 1974,
    "Renewable Energy": 1974,
    "AI & Machine Learning": 1980,  # softened earlier same day → 1974
    "Robotics & Automation": 1980,
    "Quantum Computing": 1994,
    "Data Science & Big Data": 2001,
    "CRISPR & Genomics": 2012,
}
IDS = {cid for _, cid, _, _ in TOPICS}
SHARED_START = 1974


def load_river() -> dict[str, dict[int, int]]:
    """openalex_id -> year -> global works_count sum."""
    raw: dict[str, dict[int, int]] = {cid: defaultdict(int) for cid in IDS}
    names: dict[str, str] = {}
    with RIVER.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row["openalex_id"]
            if cid not in IDS:
                continue
            y = int(row["year"])
            raw[cid][y] += int(row["works_count"])
            names[cid] = row["topic_display_name"]
    return {"raw": raw, "names": names}


def load_pool() -> dict[str, dict[int, int]]:
    """concept_id -> year -> global publications from viz3_data.js lines."""
    pool: dict[str, dict[int, int]] = {cid: defaultdict(int) for cid in IDS}
    text = VIZ3.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line or line.startswith("window.") or line.startswith("`") or line.startswith("const"):
            continue
        # year,topic,CID,country,iso,count
        parts = line.split(",")
        if len(parts) < 6:
            continue
        try:
            y = int(parts[0])
        except ValueError:
            continue
        cid = parts[2]
        if cid not in IDS:
            continue
        try:
            pool[cid][y] += int(parts[-1])
        except ValueError:
            continue
    return pool


def decide(topic: str, cid: str, floor: int, raw: dict[int, int]) -> dict:
    """Recommend floor based on continuous substantial volume before floor."""
    before = floor - 1
    at = floor
    raw_before = raw.get(before, 0)
    raw_at = raw.get(at, 0)

    # Look at 5 years before floor for continuity
    pre_years = list(range(max(SHARED_START, floor - 5), floor))
    pre_vals = [raw.get(y, 0) for y in pre_years]
    pre_nonzero = sum(1 for v in pre_vals if v > 0)
    pre_mean = (sum(pre_vals) / len(pre_vals)) if pre_vals else 0
    pre_min = min(pre_vals) if pre_vals else 0

    # Substantial = at least ~100 global works in year before floor,
    # continuous = most of last 5 pre-floor years nonzero, and not a birth cliff
    # (raw growth floor-1 → floor is gentle, not inventing the field)
    substantial = raw_before >= 100
    continuous = pre_nonzero >= max(3, len(pre_years) - 1) and pre_min >= 50
    # Also: if mean of pre-window is already high relative to floor year
    high_pre = pre_mean >= 200 and raw_before >= 200

    soften = (substantial and continuous) or high_pre

    # Special: if floor already == SHARED_START, keep
    if floor <= SHARED_START:
        action = "keep"
        new_floor = floor
        reason = f"already at shared scrubber start {SHARED_START}"
    elif soften:
        action = "soften_to_1974"
        new_floor = SHARED_START
        reason = (
            f"raw continuous/substantial before floor: "
            f"{before}={raw_before}, {at}={raw_at}, "
            f"pre5 mean={pre_mean:.0f} nonzero={pre_nonzero}/{len(pre_years)}"
        )
    else:
        action = "keep"
        new_floor = floor
        reason = (
            f"raw before floor weak or discontinuous: "
            f"{before}={raw_before}, {at}={raw_at}, "
            f"pre5 mean={pre_mean:.0f} nonzero={pre_nonzero}/{len(pre_years)}"
        )

    return {
        "topic": topic,
        "concept_id": cid,
        "old_floor": floor,
        "raw_year_before_floor": raw_before,
        "raw_year_at_floor": raw_at,
        "year_before": before,
        "year_at": at,
        "pre5_years": pre_years,
        "pre5_vals": pre_vals,
        "pre5_mean": round(pre_mean, 1),
        "action": action,
        "new_floor": new_floor,
        "reason": reason,
    }


def main() -> None:
    river = load_river()
    pool = load_pool()
    decisions = []
    series = {}

    print(f"River: {RIVER.exists()} {RIVER}")
    print(f"Names: {river['names']}")
    print()

    for topic, cid, floor, (y0, y1) in TOPICS:
        raw = river["raw"][cid]
        p = pool.get(cid, {})
        years = list(range(y0, y1 + 1))
        rows = []
        for y in years:
            rg = raw.get(y, 0)
            pg = p.get(y, 0)
            rows.append(
                {
                    "year": y,
                    "raw_global": rg,
                    "pool_global": pg,
                    "floor_zeroed": rg > 0 and pg == 0 and y < floor,
                }
            )
        d = decide(topic, cid, floor, raw)
        decisions.append(d)
        series[cid] = rows

        print("=" * 72)
        print(f"{topic} ({cid}) floor={floor} -> action={d['action']} new={d['new_floor']}")
        print(f"  before {d['year_before']}={d['raw_year_before_floor']}  at {d['year_at']}={d['raw_year_at_floor']}")
        print(f"  pre5: {list(zip(d['pre5_years'], d['pre5_vals']))}")
        print(f"  reason: {d['reason']}")
        print(f"  {'year':>4} {'RAW':>8} {'POOL':>8} {'zeroed?':>8}")
        for r in rows:
            print(
                f"  {r['year']:4d} {r['raw_global']:8d} {r['pool_global']:8d} "
                f"{'YES' if r['floor_zeroed'] else '':>8}"
            )

    payload = {
        "decisions": decisions,
        "series": series,
        "names": river["names"],
        "proposed_floors": {d["topic"]: d["new_floor"] for d in decisions},
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print()
    print("PROPOSED FLOORS:", payload["proposed_floors"])
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
