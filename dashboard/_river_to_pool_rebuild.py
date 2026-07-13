#!/usr/bin/env python3
"""Rebuild dashboard pools G1–G5 from locked READY_FOR_TEAM river.

Owners: dashboard/docs/RIVER_OWNERS.md
GERD: gated hierarchical river (gerd_pct_gdp_hierarchical.csv) — WB base;
  OECD fills true holes only if country overlap ≤0.05 pp; UIS≡WB (no extra years);
  then **display LOCF ffill** (last observation carried forward) within each
  country so G1/G2 show the last known GERD when later years are missing
  (user override 2026-07-12 — see docs/G2_CARRY_AND_GERD_FFILL.md).
Does NOT invent H/GDP. Does NOT use stub sjr / master H columns.
G3 live default = Lane C L3 college cross-domain (same OpenAlex level;
same field NOT required). See dashboard/docs/G3_SAME_LEVEL_COMPETITION_PLAN.md.
G4 rebuilds ALL years into VIZ4_BY_YEAR (no single-year regression).
"""
from __future__ import annotations

import csv
import json
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASH = ROOT / "dashboard"
RIVER = ROOT / "CS661_Dataset" / "raw_vault" / "READY_FOR_TEAM"
TOPICS_FULL = ROOT / "CS661_Dataset" / "raw_vault" / "04_openalex" / "topics_full"
PROOF: dict = {"built_at": datetime.now(timezone.utc).isoformat()}

# Lane C L3 college cross-domain (default live race). Order = plan table.
# Keep UI (g3.js) in the same order. ML / Data science / Renewable stay in
# river CSV for other lanes but are NOT emitted to viz3_data.js.
REQUIRED_G3_TOPICS = [
    "Infectious disease",   # C524204448 — COVID peer
    "Robotics",             # C34413123
    "Quantum computer",     # C58053490 — sole Quantum
    "CRISPR",               # C98108389
    "Energy storage",       # C73916439
    "Photovoltaics",        # C542589376
    "Supervised learning",  # C136389625 — L3 AI/ML (replaces QI)
]
# Canonical live display name → OpenAlex concept id (strict allowlist).
G3_TOPIC_CONCEPT_IDS: dict[str, str] = {
    "Infectious disease": "C524204448",
    "Robotics": "C34413123",
    "Quantum computer": "C58053490",
    "CRISPR": "C98108389",
    "Energy storage": "C73916439",
    "Photovoltaics": "C542589376",
    "Supervised learning": "C136389625",
}
# River may still use older dashboard_topic labels for the four pre-existing IDs.
G3_RIVER_TOPIC_ALIASES: dict[str, str] = {
    "Infectious Diseases": "Infectious disease",
    "Robotics & Automation": "Robotics",
    "Quantum Computing": "Quantum computer",
    "CRISPR & Genomics": "CRISPR",
    "Energy storage": "Energy storage",
    "Photovoltaics": "Photovoltaics",
    "Supervised learning": "Supervised learning",
}
G3_FORBIDDEN_PRIMARY_IDS = frozenset({"C154945302"})  # mega-AI — never default primary
G3_ALLOWED_CONCEPT_IDS = frozenset(G3_TOPIC_CONCEPT_IDS.values())
G3_CONCEPT_TO_TOPIC = {oid: name for name, oid in G3_TOPIC_CONCEPT_IDS.items()}
YEAR_MAX = 2024
YEAR_FLOOR = 1950

# Shared scrubber start 1974 for all Lane C peers (no fake milestone floors).
G3_TOPIC_START_YEARS: dict[str, int] = {t: 1974 for t in REQUIRED_G3_TOPICS}

SIMPLE_REGION = {
    "AU": "Oceania",
    "BR": "Latin America",
    "CA": "North America",
    "CH": "Europe",
    "CN": "Asia",
    "DE": "Europe",
    "ES": "Europe",
    "FR": "Europe",
    "GB": "Europe",
    "IN": "Asia",
    "IR": "Middle East",
    "IT": "Europe",
    "JP": "Asia",
    "KR": "Asia",
    "NL": "Europe",
    "PL": "Europe",
    "RU": "Europe",
    "SE": "Europe",
    "TR": "Middle East",
    "US": "North America",
}


def csv_cell(value: object) -> str:
    s = str(value)
    if any(ch in s for ch in (",", '"', "\n", "\r")):
        return '"' + s.replace('"', '""') + '"'
    return s


def load_js_array(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
    i, j = text.find("["), text.rfind("]")
    return json.loads(text[i : j + 1])


def load_js_object_after(path: Path, marker: str) -> dict:
    text = path.read_text(encoding="utf-8")
    i = text.find(marker)
    if i < 0:
        raise SystemExit(f"marker not found in {path.name}: {marker}")
    i = text.find("{", i)
    depth = 0
    for k, ch in enumerate(text[i:]):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[i : i + k + 1])
    raise SystemExit(f"unbalanced object after {marker} in {path.name}")


def assert_no_stub_h_sources() -> None:
    stub = ROOT / "CS661_Dataset" / "sjr_country_metrics.csv"
    if stub.exists():
        raise SystemExit(
            "REFUSING rebuild: sjr_country_metrics.csv still at dataset root — "
            "move to _QUARANTINE first (stub H)."
        )
    master = ROOT / "CS661_Dataset" / "master_dataset.csv"
    if master.exists():
        header = master.read_text(encoding="utf-8", errors="replace").splitlines()[0]
        if ",H_Index," in f",{header}," or header.startswith("H_Index,") or header.endswith(",H_Index"):
            # allow only renamed stub column
            if "H_Index_STUB" not in header and "H_Index," in header + ",":
                # Exact column named H_Index is forbidden
                cols = header.split(",")
                if "H_Index" in cols:
                    raise SystemExit(
                        "REFUSING rebuild: master_dataset.csv still has H_Index column — "
                        "rename stub columns first (see _QUARANTINE/README.md)."
                    )
    PROOF["stub_guard"] = "ok — no drinkable stub H at root"


def rebuild_g2() -> None:
    src = DASH / "ridgeline_data.js"
    bak = DASH / "ridgeline_data_BEFORE_POOLFIX.js"
    if not bak.exists():
        shutil.copy2(src, bak)
    river_q = list(csv.DictReader((RIVER / "q1_q4_country_year.csv").open(encoding="utf-8")))
    by_year: dict[str, list] = defaultdict(list)
    for r in river_q:
        year = str(int(r["year"]))
        by_year[year].append(
            {
                "country": r["country"],
                "region": r["region"],
                "q1": int(float(r["q1"])),
                "q4": int(float(r["q4"])),
                "total": int(float(r["total"])),
                "ratio": float(r["ratio"]),
            }
        )
    out = {y: sorted(by_year[y], key=lambda x: x["country"]) for y in sorted(by_year, key=int)}
    src.write_text(
        "// River→pool G2 — READY_FOR_TEAM/q1_q4_country_year.csv (publisher country, uncapped ratio)\n"
        "const REAL_RIDGELINE_DATA = "
        + json.dumps(out, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    river_2022 = {r["country"]: r for r in river_q if r["year"] == "2022"}
    pool = load_js_object_after(src, "const REAL_RIDGELINE_DATA")
    checks = []
    for c in ("United States", "India", "China", "United Kingdom"):
        p = next(x for x in pool["2022"] if x["country"] == c)
        rv = river_2022[c]
        ok = (
            int(p["q1"]) == int(float(rv["q1"]))
            and int(p["q4"]) == int(float(rv["q4"]))
            and abs(float(p["ratio"]) - float(rv["ratio"])) < 1e-9
        )
        checks.append({"country": c, "pool_ratio": p["ratio"], "river_ratio": float(rv["ratio"]), "exact": ok})
    assert all(x["exact"] for x in checks), checks
    PROOF["G2"] = {"bytes": src.stat().st_size, "anchors_2022": checks}
    print("G2 OK", checks)


def rebuild_g4() -> None:
    src = DASH / "viz4_data.js"
    bak = DASH / "viz4_data_BEFORE_POOLFIX.js"
    if not bak.exists():
        shutil.copy2(src, bak)

    # Prefer existing region map from current multi-year pool if present
    region_by_name: dict[str, str] = {}
    try:
        by = load_js_object_after(src, "const VIZ4_BY_YEAR")
        for rows in by.values():
            for r in rows:
                region_by_name[r["name"]] = r["region"]
    except SystemExit:
        old = load_js_array(bak)
        region_by_name = {r["name"]: r["region"] for r in old}

    prem = list(csv.DictReader((RIVER / "collaboration_premium.csv").open(encoding="utf-8")))
    years = sorted({int(r["Year"]) for r in prem})
    by_year: dict[str, list] = {}
    for y in years:
        rows_y = [r for r in prem if int(r["Year"]) == y]
        out_rows = []
        for r in sorted(rows_y, key=lambda x: x["Country_Name"]):
            name = r["Country_Name"]
            if name == "Russian Federation":
                name = "Russia"
            region = region_by_name.get(name) or SIMPLE_REGION.get(r["Country_Code"], "Unknown")
            domestic = round(float(r["Domestic_Avg_Citations"]), 3)
            international = round(float(r["International_Avg_Citations"]), 3)
            gain = round(float(r["Citation_Gain"]), 3)
            out_rows.append(
                {
                    "name": name,
                    "region": region,
                    "domestic": domestic,
                    "international": international,
                    "gain": gain,
                    "year": y,
                    "domestic_papers": int(float(r["Domestic_Papers"])),
                    "international_papers": int(float(r["International_Papers"])),
                }
            )
        by_year[str(y)] = out_rows

    meta = {
        "years": years,
        "year_min": min(years),
        "year_max": max(years),
        "n_countries": 20,
        "source": "CS661_Dataset/raw_vault/READY_FOR_TEAM/collaboration_premium.csv",
        "semantics": "Mean citations/paper: domestic-only vs international coauthorship; gain = intl - domestic",
    }
    # Also expose latest year as VIZ4_DATA for older fallbacks
    latest = by_year[str(max(years))]
    body = (
        "// Generated Data for Viz 4 — collaboration premium (river→pool)\n"
        f"// Source: READY_FOR_TEAM/collaboration_premium.csv — ALL years\n"
        f"const VIZ4_META = {json.dumps(meta, indent=2)};\n"
        f"const VIZ4_BY_YEAR = {json.dumps(by_year, indent=2)};\n"
        f"const VIZ4_DATA = {json.dumps(latest, indent=2)};\n"
    )
    src.write_text(body, encoding="utf-8")

    usa = next(x for x in by_year["2022"] if x["name"] == "United States")
    ind = next(x for x in by_year["2022"] if x["name"] == "India")
    PROOF["G4"] = {
        "years": years,
        "USA_2022": usa,
        "India_2022": ind,
        "bytes": src.stat().st_size,
    }
    print("G4 OK USA", usa["gain"], "India", ind["gain"])


def load_g3_empty_year_pairs() -> set[tuple[str, int]]:
    """(openalex_id, year) fetched with 0 country groups — still a complete year (count=0)."""
    path = TOPICS_FULL / "fetched_empty.json"
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    out: set[tuple[str, int]] = set()
    for item in data.get("pairs") or []:
        try:
            oid = str(item["openalex_id"])
            year = int(item["year"])
        except (KeyError, TypeError, ValueError):
            continue
        if oid in G3_ALLOWED_CONCEPT_IDS:
            out.add((oid, year))
    return out


def load_g3_primaries() -> dict[str, str]:
    """Return Lane C display_topic → concept id (map may list extras; live = allowlist)."""
    map_path = RIVER / "topic_id_map.json"
    if not map_path.exists():
        map_path = TOPICS_FULL / "topic_id_map.json"
    data = json.loads(map_path.read_text(encoding="utf-8"))
    # Start from locked Lane C ids; overlay map only when ids match.
    out = dict(G3_TOPIC_CONCEPT_IDS)
    for t in data.get("topics") or []:
        dash = t.get("dashboard_topic")
        oid = (t.get("primary") or {}).get("openalex_id")
        if not dash or not oid:
            continue
        canon = G3_RIVER_TOPIC_ALIASES.get(dash, dash)
        if canon in out and oid == out[canon]:
            continue
        if oid in G3_ALLOWED_CONCEPT_IDS:
            # Map may use older dashboard labels; keep locked Lane C names.
            continue
    return out


def largest_shared_window(by_topic_years: dict[str, set[int]]) -> tuple[int, int]:
    """Legacy helper: earliest year where every required topic has continuous coverage."""
    for y_min in range(YEAR_FLOOR, YEAR_MAX + 1):
        need = set(range(y_min, YEAR_MAX + 1))
        if all(need <= by_topic_years.get(t, set()) for t in REQUIRED_G3_TOPICS):
            return y_min, YEAR_MAX
    raise SystemExit("REFUSING G3 rebuild — no shared complete primary window")


def rebuild_g3() -> None:
    src = DASH / "viz3_data.js"
    bak = DASH / "viz3_data_BEFORE_HONEST_TRIM.js"
    if not bak.exists() and src.exists():
        shutil.copy2(src, bak)

    if set(G3_TOPIC_START_YEARS) != set(REQUIRED_G3_TOPICS):
        raise SystemExit(
            "REFUSING G3 rebuild: G3_TOPIC_START_YEARS keys must equal REQUIRED_G3_TOPICS"
        )
    for topic in REQUIRED_G3_TOPICS:
        if topic not in G3_TOPIC_START_YEARS:
            raise SystemExit(f"REFUSING G3 rebuild: missing honesty floor for {topic!r}")

    river_csv = RIVER / "openalex_topic_country_year.csv"
    if not river_csv.exists():
        river_csv = TOPICS_FULL / "openalex_topic_country_year.csv"
    pool_primaries = load_g3_primaries()
    missing_map = [t for t in REQUIRED_G3_TOPICS if t not in pool_primaries]
    if missing_map:
        raise SystemExit(f"REFUSING G3 rebuild: missing primaries for {missing_map}")
    for topic, oid in pool_primaries.items():
        if topic not in REQUIRED_G3_TOPICS:
            continue
        if oid in G3_FORBIDDEN_PRIMARY_IDS:
            raise SystemExit(
                f"REFUSING G3 rebuild: topic {topic!r} primary is forbidden mega-AI {oid}."
            )
        if oid not in G3_ALLOWED_CONCEPT_IDS:
            raise SystemExit(
                f"REFUSING G3 rebuild: topic {topic!r} primary {oid} is not in "
                f"G3_ALLOWED_CONCEPT_IDS ({sorted(G3_ALLOWED_CONCEPT_IDS)})."
            )
        expected = G3_TOPIC_CONCEPT_IDS[topic]
        if oid != expected:
            raise SystemExit(
                f"REFUSING G3 rebuild: topic {topic!r} primary {oid} != locked {expected}"
            )
    if set(pool_primaries[t] for t in REQUIRED_G3_TOPICS) != G3_ALLOWED_CONCEPT_IDS:
        raise SystemExit(
            "REFUSING G3 rebuild: pool primaries must be exactly the 7 Lane C concept IDs. "
            f"got={sorted(set(pool_primaries[t] for t in REQUIRED_G3_TOPICS))} "
            f"want={sorted(G3_ALLOWED_CONCEPT_IDS)}"
        )

    rows = list(csv.DictReader(river_csv.open(encoding="utf-8", newline="")))
    # Match by allowlisted concept id (river may still carry old dashboard_topic labels
    # for Infectious/Robotics/Quantum/CRISPR). Never pass mega-AI / L1/L2 into the pool.
    kept = []
    for r in rows:
        oid = r.get("openalex_id") or ""
        if oid not in G3_ALLOWED_CONCEPT_IDS or oid in G3_FORBIDDEN_PRIMARY_IDS:
            continue
        topic = G3_CONCEPT_TO_TOPIC[oid]
        year = int(r["year"])
        start = G3_TOPIC_START_YEARS[topic]
        if year < start or year > YEAR_MAX or year < YEAR_FLOOR:
            continue
        kept.append(
            {
                **r,
                "dashboard_topic": topic,
                "openalex_id": oid,
            }
        )

    if not kept:
        raise SystemExit("REFUSING G3 rebuild — no rows after honesty floors / allowlist")

    leaked_ids = sorted({r["openalex_id"] for r in kept} - G3_ALLOWED_CONCEPT_IDS)
    if leaked_ids:
        raise SystemExit(
            f"REFUSING G3 rebuild: non-allowlisted concept IDs would enter pool: {leaked_ids}"
        )
    if {r["openalex_id"] for r in kept} != G3_ALLOWED_CONCEPT_IDS:
        have = sorted({r["openalex_id"] for r in kept})
        missing = sorted(G3_ALLOWED_CONCEPT_IDS - set(have))
        raise SystemExit(
            "REFUSING G3 rebuild: pool must emit exactly the 7 Lane C concept IDs "
            f"(got {have}; missing {missing})"
        )

    # Each topic must have continuous coverage from its floor through YEAR_MAX.
    # Years recorded in fetched_empty.json (0 country groups) count as present (=0 works).
    empty_pairs = load_g3_empty_year_pairs()
    by_topic_years: dict[str, set[int]] = defaultdict(set)
    for r in kept:
        by_topic_years[r["dashboard_topic"]].add(int(r["year"]))
    for oid, year in empty_pairs:
        topic = G3_CONCEPT_TO_TOPIC.get(oid)
        if topic:
            by_topic_years[topic].add(year)
    for topic in REQUIRED_G3_TOPICS:
        start = G3_TOPIC_START_YEARS[topic]
        need = set(range(start, YEAR_MAX + 1))
        have = by_topic_years.get(topic, set())
        missing = sorted(need - have)
        if missing:
            raise SystemExit(
                f"REFUSING G3 rebuild — {topic!r} missing years after floor {start}: "
                f"{missing[:12]}{'...' if len(missing) > 12 else ''}"
            )

    topic_rank = {t: i for i, t in enumerate(REQUIRED_G3_TOPICS)}
    year_min = min(int(r["year"]) for r in kept)
    year_max = YEAR_MAX
    kept_sorted = sorted(
        kept,
        key=lambda r: (int(r["year"]), topic_rank[r["dashboard_topic"]], r["country_iso2"]),
    )
    lines = ["year,topic_name,subfield_id,country_name,country_code,publications_count"]
    for r in kept_sorted:
        lines.append(
            ",".join(
                [
                    csv_cell(str(int(r["year"]))),
                    csv_cell(r["dashboard_topic"]),
                    csv_cell(r["openalex_id"]),
                    csv_cell(r["country_key_display_name"]),
                    csv_cell(r["country_iso2"]),
                    csv_cell(str(int(r["works_count"]))),
                ]
            )
        )
    csv_body = "\n".join(lines) + "\n"
    assert "Quantum computer,C58053490," in csv_body
    assert "Infectious disease,C524204448," in csv_body
    assert "Energy storage,C73916439," in csv_body
    assert "Photovoltaics,C542589376," in csv_body
    assert "Supervised learning,C136389625," in csv_body
    assert "Quantum information,C169699857," not in csv_body
    assert "C154945302" not in csv_body
    assert ",2500," not in csv_body
    # Dropped from live pool (may still exist in river CSV)
    assert "AI & Machine Learning,C119857082," not in csv_body
    assert "Data Science & Big Data,C2522767166," not in csv_body
    assert "Renewable Energy,C188573790," not in csv_body
    for oid in G3_FORBIDDEN_PRIMARY_IDS:
        assert oid not in csv_body
    assert "1974,CRISPR,C98108389," in csv_body
    assert "1974,Quantum computer,C58053490," in csv_body
    assert "1974,Robotics,C34413123," in csv_body
    assert "1974,Infectious disease,C524204448," in csv_body
    assert "Supervised learning,C136389625," in csv_body

    starts_json = json.dumps(
        {t: G3_TOPIC_START_YEARS[t] for t in REQUIRED_G3_TOPICS},
        indent=2,
    )
    meta = {
        "year_min": year_min,
        "year_max": year_max,
        "unit": "OpenAlex concept-tagged works (retrospective taxonomy)",
        "note": (
            "Counts are works OpenAlex tags with locked concept IDs — not the year "
            "a buzzword was coined. Live race = seven OpenAlex level-3 peers "
            "(same college abstraction; cross-domain by design). Shared scrubber "
            "start 1974; no fake milestone floors. Lane: L3_college_cross_domain."
        ),
        "lane_id": "L3_college_cross_domain",
        "openalex_level": 3,
        "same_field_required": False,
        "Quantum_primary": "C58053490",
        "display_order": list(REQUIRED_G3_TOPICS),
        "display_order_rule": "Lane C L3 college cross-domain (plan order; floors = 1974)",
        "allowed_concept_ids": sorted(G3_ALLOWED_CONCEPT_IDS),
        "topic_start_years": {t: G3_TOPIC_START_YEARS[t] for t in REQUIRED_G3_TOPICS},
        "topic_concept_ids": {t: pool_primaries[t] for t in REQUIRED_G3_TOPICS},
        "dropped_from_live_pool": [
            "C119857082",  # Machine learning (L1)
            "C2522767166",  # Data science (L1)
            "C188573790",  # Renewable energy (L2)
            "C169699857",  # Quantum information (second Quantum — replaced by Supervised learning)
        ],
        "empty_fetched_years": sorted(
            f"{oid}:{year}"
            for oid, year in empty_pairs
            if year >= G3_TOPIC_START_YEARS[G3_CONCEPT_TO_TOPIC[oid]]
        ),
    }
    meta_json = json.dumps(meta, indent=2)
    src.write_text(
        "window.CSV_DATA = `"
        + csv_body
        + "`;\n"
        + "window.VIZ3_TOPIC_START_YEARS = "
        + starts_json
        + ";\n"
        + "window.VIZ3_META = "
        + meta_json
        + ";\n",
        encoding="utf-8",
    )

    def count(cc: str, topic: str, year: int = 2022) -> int | None:
        for r in kept:
            if (
                r["country_iso2"] == cc
                and r["dashboard_topic"] == topic
                and int(r["year"]) == year
            ):
                return int(r["works_count"])
        return None

    def global_count(topic: str, year: int) -> int:
        return sum(
            int(r["works_count"])
            for r in kept
            if r["dashboard_topic"] == topic and int(r["year"]) == year
        )

    PROOF["G3"] = {
        "year_min": year_min,
        "year_max": year_max,
        "rows": len(kept),
        "lane_id": "L3_college_cross_domain",
        "display_order": list(REQUIRED_G3_TOPICS),
        "allowed_concept_ids": sorted(G3_ALLOWED_CONCEPT_IDS),
        "topic_start_years": {t: G3_TOPIC_START_YEARS[t] for t in REQUIRED_G3_TOPICS},
        "topic_concept_ids": {t: pool_primaries[t] for t in REQUIRED_G3_TOPICS},
        "Quantum_primary": "C58053490",
        "USA_2022_Infectious": count("US", "Infectious disease"),
        "India_2022_Infectious": count("IN", "Infectious disease"),
        "honesty_1974": {t: global_count(t, 1974) for t in REQUIRED_G3_TOPICS},
        "bytes": src.stat().st_size,
    }
    for t, v in PROOF["G3"]["honesty_1974"].items():
        # Empty-fetched years (0 country groups) may legitimately total 0.
        oid = pool_primaries[t]
        if (oid, 1974) in empty_pairs:
            assert v == 0, f"{t} empty-fetched 1974 should total 0 (got {v})"
        else:
            assert v > 0, f"{t} must be present at 1974 (got {v})"
    pool_text = src.read_text(encoding="utf-8")
    assert "C154945302" not in pool_text
    # QI may appear only in dropped_from_live_pool meta — never as a data row.
    csv_blob = pool_text.split("window.VIZ3_TOPIC_START_YEARS", 1)[0]
    assert "C169699857" not in csv_blob
    assert "C136389625" in csv_blob
    assert '"Supervised learning"' in pool_text
    print("G3 OK", PROOF["G3"])


def ensure_gerd_hierarchy() -> Path:
    """GERD river must be gated hierarchical CSV (OECD hole-fill only if overlap-ok)."""
    gerd_path = RIVER / "gerd_pct_gdp_hierarchical.csv"
    build = DASH / "_build_gerd_hierarchy.py"
    if not gerd_path.exists():
        if not build.exists():
            raise SystemExit("Missing gerd_pct_gdp_hierarchical.csv and builder script")
        import subprocess
        import sys

        subprocess.check_call([sys.executable, str(build)], cwd=str(ROOT))
    if not gerd_path.exists():
        raise SystemExit("GERD hierarchy CSV still missing after build")
    PROOF["gerd_hierarchy"] = str(gerd_path.relative_to(ROOT)).replace("\\", "/")
    return gerd_path


def apply_gerd_locf(v1: list[dict]) -> dict:
    """Forward-fill GERD within each country (LOCF) for display continuity.

    River hierarchy stays exact-year only; this LOCF is a documented pool/display
    policy (user override). Tagged GERD_Source like LOCF:WB:y2020.
    """
    by_code: dict[str, list[dict]] = defaultdict(list)
    for row in v1:
        by_code[str(row["Country_Code"])].append(row)

    ffilled = 0
    countries = 0
    examples: list[dict] = []
    for code, rows in by_code.items():
        rows.sort(key=lambda r: int(r["Year"]))
        last_g = None
        last_src = None
        last_y = None
        country_hit = False
        for row in rows:
            g = row.get("GERD_Percent_GDP")
            if g not in (None, ""):
                last_g = float(g)
                raw_src = row.get("GERD_Source") or "UNKNOWN"
                # Keep original source year for non-LOCF cells
                if isinstance(raw_src, str) and raw_src.startswith("LOCF:"):
                    last_src = raw_src.split(":")[1] if raw_src.count(":") >= 1 else "UNKNOWN"
                else:
                    last_src = raw_src
                last_y = int(row["Year"])
            elif last_g is not None:
                row["GERD_Percent_GDP"] = last_g
                row["GERD_Source"] = f"LOCF:{last_src}:y{last_y}"
                ffilled += 1
                country_hit = True
                if len(examples) < 25:
                    examples.append(
                        {
                            "Country_Code": code,
                            "Year": int(row["Year"]),
                            "GERD_Percent_GDP": last_g,
                            "GERD_Source": row["GERD_Source"],
                            "carried_from_year": last_y,
                        }
                    )
        if country_hit:
            countries += 1

    return {
        "gerd_locf_country_years": ffilled,
        "gerd_locf_countries": countries,
        "gerd_locf_examples": examples,
    }


def verify_g1() -> None:
    """G1 pool: SCImago H + WB GDP + gated hierarchical GERD + display LOCF ffill."""
    ensure_gerd_hierarchy()
    src = DASH / "viz1_data.js"
    bak = DASH / "viz1_data_BEFORE_POOLFIX.js"
    if not bak.exists():
        shutil.copy2(src, bak)

    panel = list(csv.DictReader((RIVER / "g1_features_panel.csv").open(encoding="utf-8")))
    by_cy = {(r["Country_Code"], int(r["Year"])): r for r in panel}
    gerd_rows = list(csv.DictReader((RIVER / "gerd_pct_gdp_hierarchical.csv").open(encoding="utf-8")))
    gerd_by = {(r["Country_Code"], int(r["Year"])): r for r in gerd_rows}
    v1 = load_js_array(src)

    updated = 0
    gerd_cleared = 0
    for row in v1:
        key = (row["Country_Code"], int(row["Year"]))
        riv = by_cy.get(key)
        if not riv:
            continue
        for col, cast in (
            ("H_Index", float),
            ("GDP_Per_Capita_PPP", float),
            ("Total_Docs", float),
        ):
            raw = riv.get(col, "")
            if raw in ("", None):
                continue
            new_v = cast(raw)
            old_v = row.get(col)
            if old_v is None or abs(float(old_v) - new_v) > 1e-6:
                updated += 1
            row[col] = new_v
        # GERD from hierarchical river (prefer explicit hierarchy; fall back to panel cell)
        g_riv = gerd_by.get(key) or riv
        g_raw = g_riv.get("GERD_Percent_GDP", "") if g_riv else ""
        if g_raw not in ("", None):
            new_g = float(g_raw)
            old_g = row.get("GERD_Percent_GDP")
            if old_g is None or old_g == "" or abs(float(old_g) - new_g) > 1e-6:
                updated += 1
            row["GERD_Percent_GDP"] = new_g
            src_lab = g_riv.get("GERD_Source") or riv.get("GERD_Source") or ""
            if src_lab:
                row["GERD_Source"] = src_lab
        else:
            # Exact-year missing in hierarchy — clear before LOCF pass
            if row.get("GERD_Percent_GDP") not in (None, ""):
                gerd_cleared += 1
            row["GERD_Percent_GDP"] = None
            row["GERD_Source"] = None

    locf_stats = apply_gerd_locf(v1)

    src.write_text("const VIZ1_DATA = " + json.dumps(v1, separators=(",", ":")) + ";\n", encoding="utf-8")

    def sample(code: str, year: int = 2022) -> dict:
        r = next(x for x in v1 if x["Country_Code"] == code and int(x["Year"]) == year)
        return {
            "H_Index": r["H_Index"],
            "GDP_Per_Capita_PPP": r["GDP_Per_Capita_PPP"],
            "GERD_Percent_GDP": r["GERD_Percent_GDP"],
            "GERD_Source": r.get("GERD_Source"),
            "Total_Docs": r["Total_Docs"],
        }

    usa, ind = sample("USA"), sample("IND")
    riv_usa = by_cy[("USA", 2022)]
    assert abs(float(usa["H_Index"]) - float(riv_usa["H_Index"])) < 1e-6
    assert abs(float(usa["H_Index"]) - 3388) < 1e-6
    assert abs(float(ind["H_Index"]) - 1001) < 1e-6
    # India 2022 GERD: user-requested LOCF from WB 2020 (~0.64558)
    assert ind["GERD_Percent_GDP"] is not None and ind["GERD_Percent_GDP"] != ""
    assert abs(float(ind["GERD_Percent_GDP"]) - 0.64558) < 1e-5, ind
    assert str(ind.get("GERD_Source", "")).startswith("LOCF:"), ind
    usa24 = sample("USA", 2024)
    # USA 2024 may be OECD hole-fill if eligible (exact source, not LOCF)
    ind_series = []
    for y in range(2015, 2025):
        try:
            ind_series.append({"year": y, **sample("IND", y)})
        except StopIteration:
            ind_series.append({"year": y, "missing_row": True})
    PROOF["G1"] = {
        "rows": len(v1),
        "field_updates": updated,
        "gerd_cleared_before_locf": gerd_cleared,
        **locf_stats,
        "USA_2022": usa,
        "USA_2024": usa24,
        "India_2022": ind,
        "India_GERD_2015_2024": [
            {
                "year": s.get("year"),
                "GERD_Percent_GDP": s.get("GERD_Percent_GDP"),
                "GERD_Source": s.get("GERD_Source"),
            }
            for s in ind_series
        ],
        "bytes": src.stat().st_size,
    }
    print("G1 OK USA H", usa["H_Index"], "India H", ind["H_Index"], "India2022 GERD", ind["GERD_Percent_GDP"], ind.get("GERD_Source"))
    print("G1 USA2024 GERD", usa24["GERD_Percent_GDP"], usa24.get("GERD_Source"))
    print("G1 GERD LOCF country-years", locf_stats["gerd_locf_country_years"], "countries", locf_stats["gerd_locf_countries"])


def verify_g5() -> None:
    india_dir = DASH / "data" / "india_network"
    manifest = india_dir / "manifest.json"
    n_json = len(list(india_dir.glob("*.json")))
    PROOF["G5"] = {
        "manifest_exists": manifest.exists(),
        "json_files": n_json,
        "action": "KEEP processed JSON — no demo DATA.getIndiaNetwork",
    }
    assert manifest.exists() and n_json >= 10, PROOF["G5"]
    print("G5 OK", PROOF["G5"])


def main() -> None:
    assert_no_stub_h_sources()
    verify_g1()
    rebuild_g2()
    rebuild_g3()
    rebuild_g4()
    verify_g5()
    notes = RIVER / "_notes"
    notes.mkdir(exist_ok=True)
    out = notes / "_river_to_pool_rebuild_proof.json"
    out.write_text(json.dumps(PROOF, indent=2), encoding="utf-8")
    dash_docs = DASH / "docs"
    (dash_docs / "_river_to_pool_rebuild_proof.json").write_text(
        json.dumps(PROOF, indent=2), encoding="utf-8"
    )
    print("PROOF written to", out)


if __name__ == "__main__":
    main()
