#!/usr/bin/env python3
"""Cell-level audit: G3 AI (C119857082) raw river vs honesty-floored pool, 1970-1990."""
from __future__ import annotations

import csv
import io
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RIVER = ROOT / "CS661_Dataset" / "raw_vault" / "READY_FOR_TEAM" / "openalex_topic_country_year.csv"
VIZ3 = ROOT / "dashboard" / "viz3_data.js"
OUT_JSON = Path(__file__).resolve().parent / "_audit_g3_ai_1980_jump.json"

ML = "C119857082"
MEGA = "C154945302"
BIG4 = ("US", "CN", "IN", "GB")
YEARS = list(range(1970, 1991))


def sum_river() -> dict:
    raw: dict[str, dict[int, dict[str, int]]] = {
        ML: defaultdict(lambda: defaultdict(int)),
        MEGA: defaultdict(lambda: defaultdict(int)),
    }
    names: dict[str, str] = {}
    n_rows = 0
    with RIVER.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n_rows += 1
            cid = row["openalex_id"]
            if cid not in (ML, MEGA):
                continue
            y = int(row["year"])
            iso = row["country_iso2"]
            wc = int(row["works_count"])
            raw[cid][y][iso] += wc
            names[cid] = row["topic_display_name"]
    return {"raw": raw, "names": names, "n_rows": n_rows}


def spot_rows(years: tuple[int, ...]) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {y: [] for y in years}
    with RIVER.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["openalex_id"] != ML:
                continue
            y = int(row["year"])
            if y in out:
                out[y].append(
                    {
                        "iso": row["country_iso2"],
                        "name": row["country_key_display_name"],
                        "works": int(row["works_count"]),
                    }
                )
    for y in out:
        out[y].sort(key=lambda r: -r["works"])
    return out


def parse_pool() -> dict[int, dict[str, int]]:
    text = VIZ3.read_text(encoding="utf-8")
    meta_m = re.search(r"const VIZ3_META\s*=\s*(\{.*?\});", text, re.S)
    meta = json.loads(meta_m.group(1)) if meta_m else {}
    csv_m = re.search(r"const VIZ3_CSV\s*=\s*`([\s\S]*?)`;", text)
    if not csv_m:
        csv_m = re.search(r"const VIZ3_RAW_CSV\s*=\s*`([\s\S]*?)`;", text)
    pool: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    if csv_m:
        reader = csv.DictReader(io.StringIO(csv_m.group(1)))
        for row in reader:
            topic = row.get("topic_name") or ""
            sid = row.get("subfield_id") or ""
            if "AI" not in topic and sid != ML:
                continue
            if sid and sid != ML:
                continue
            y = int(row["year"])
            iso = row.get("country_code") or row.get("country_iso2") or "?"
            pool[y][iso] += int(row["publications_count"])
    else:
        # Fallback: count embedded CSV lines without const name
        for line in text.splitlines():
            if ",AI & Machine Learning,C119857082," not in line:
                continue
            parts = next(csv.reader([line]))
            if len(parts) < 6:
                continue
            y = int(parts[0])
            iso = parts[4]
            pool[y][iso] += int(parts[5])
    return {"meta": meta, "pool": pool}


def year_table(raw_ml, pool) -> list[dict]:
    rows = []
    for y in YEARS:
        by_c = raw_ml.get(y, {})
        g = sum(by_c.values()) if by_c else 0
        p_by = pool.get(y, {})
        pg = sum(p_by.values()) if p_by else 0
        rows.append(
            {
                "year": y,
                "raw_global": g,
                "raw_US": by_c.get("US", 0),
                "raw_CN": by_c.get("CN", 0),
                "raw_IN": by_c.get("IN", 0),
                "raw_GB": by_c.get("GB", 0),
                "raw_n_countries": len(by_c),
                "pool_global": pg,
                "pool_present": bool(p_by),
                "floor_zeroed": g > 0 and not p_by,
            }
        )
    return rows


def main() -> None:
    river = sum_river()
    raw_ml = river["raw"][ML]
    raw_mega = river["raw"][MEGA]
    spot = spot_rows((1978, 1979, 1980))
    parsed = parse_pool()
    table = year_table(raw_ml, parsed["pool"])

    print("River path:", RIVER)
    print("River exists:", RIVER.exists(), "rows:", river["n_rows"])
    print("ML display_name:", river["names"].get(ML))
    print("MEGA display_name:", river["names"].get(MEGA))
    print("ML years in river:", sorted(raw_ml.keys())[:3], "...", sorted(raw_ml.keys())[-3:])
    print("MEGA in river years sample:", sorted(raw_mega.keys())[:5], "n=", len(raw_mega))
    print()
    print(
        f"{'year':>4} {'RAW_G':>8} {'US':>6} {'CN':>6} {'IN':>6} {'GB':>6} "
        f"{'POOL_G':>8} {'present':>8} {'floor?':>7}"
    )
    for r in table:
        print(
            f"{r['year']:4d} {r['raw_global']:8d} {r['raw_US']:6d} {r['raw_CN']:6d} "
            f"{r['raw_IN']:6d} {r['raw_GB']:6d} {r['pool_global']:8d} "
            f"{'YES' if r['pool_present'] else 'NO':>8} "
            f"{'YES' if r['floor_zeroed'] else '':>7}"
        )

    print()
    print("=== SPOT-CHECK top countries ML C119857082 ===")
    for y in (1978, 1979, 1980):
        rows = spot[y]
        g = sum(r["works"] for r in rows)
        print(f"--- {y}: {len(rows)} countries, global={g} ---")
        for r in rows[:10]:
            print(f"  {r['iso']:3s} {r['name'][:42]:42s} {r['works']:6d}")

    print()
    print("=== MEGA-AI C154945302 global (for context; forbidden as primary) ===")
    for y in YEARS:
        by_c = raw_mega.get(y, {})
        print(f"{y}: global={sum(by_c.values()) if by_c else 0}")

    # Cliff diagnostics
    r79 = next(r for r in table if r["year"] == 1979)
    r80 = next(r for r in table if r["year"] == 1980)
    verdict_bits = []
    if r79["raw_global"] > 100 and not r79["pool_present"] and r80["pool_present"]:
        verdict_bits.append(
            "VILLAIN=HONESTY_FLOOR: raw 1979 already has substantial ML counts; "
            "pool hides them until 1980, creating a fake n/a→thousands cliff."
        )
    elif r79["raw_global"] < 50 and r80["raw_global"] > 1000:
        verdict_bits.append(
            "VILLAIN=RAW_RIVER: OpenAlex itself jumps 1979→1980; floor amplifies display."
        )
    else:
        verdict_bits.append(
            f"MIXED: raw79={r79['raw_global']} raw80={r80['raw_global']} "
            f"pool79={r79['pool_global']} pool80={r80['pool_global']}"
        )

    payload = {
        "river": str(RIVER),
        "ml_id": ML,
        "mega_id": MEGA,
        "names": river["names"],
        "viz3_meta": parsed["meta"],
        "year_table": table,
        "spot_1978_1980": {str(k): v[:15] for k, v in spot.items()},
        "mega_global_1970_1990": {
            str(y): sum(raw_mega.get(y, {}).values()) for y in YEARS
        },
        "verdict": " ".join(verdict_bits),
        "r79": r79,
        "r80": r80,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print()
    print("VERDICT:", payload["verdict"])
    print("Wrote", OUT_JSON)


if __name__ == "__main__":
    main()
