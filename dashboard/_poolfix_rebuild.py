"""POOL fix: backup + regenerate pool data files from river sources."""
from __future__ import annotations

import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\brata\Downloads\CS661")
DASH = ROOT / "dashboard"
RIVER = ROOT / "CS661_Dataset" / "raw_vault" / "READY_FOR_TEAM"
PROOF: dict = {}

# ---------------------------------------------------------------------------
# G2 — ridgeline from river CSV (uncapped ratio). REBUILT.js had capped ratios.
# ---------------------------------------------------------------------------
src_g2 = DASH / "ridgeline_data.js"
bak_g2 = DASH / "ridgeline_data_BEFORE_POOLFIX.js"
if not bak_g2.exists():
    shutil.copy2(src_g2, bak_g2)
    PROOF["G2_backup"] = f"created {bak_g2.name} ({bak_g2.stat().st_size} bytes)"
else:
    PROOF["G2_backup"] = f"already existed {bak_g2.name}"

river_q = list(csv.DictReader(open(RIVER / "q1_q4_country_year.csv", encoding="utf-8")))
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
            "ratio": float(r["ratio"]),  # uncapped
        }
    )
out_g2_obj = {y: sorted(by_year[y], key=lambda x: x["country"]) for y in sorted(by_year.keys(), key=int)}
src_g2.write_text(
    "const REAL_RIDGELINE_DATA = " + json.dumps(out_g2_obj, separators=(",", ":")) + ";\n",
    encoding="utf-8",
)
PROOF["G2_replaced"] = f"{src_g2.name} <- q1_q4_country_year.csv uncapped ({src_g2.stat().st_size} bytes)"


def load_ridgeline(path: Path):
    text = path.read_text(encoding="utf-8")
    i, j = text.find("{"), text.rfind("}")
    return json.loads(text[i : j + 1])


river_2022 = {r["country"]: r for r in river_q if r["year"] == "2022"}
pool_g2 = load_ridgeline(src_g2)
pool_2022 = {r["country"]: r for r in pool_g2["2022"]}
anchors = ["United States", "China", "India", "United Kingdom"]
g2_checks = []
for c in anchors:
    p, rv = pool_2022[c], river_2022[c]
    ok = (
        int(p["q1"]) == int(float(rv["q1"]))
        and int(p["q4"]) == int(float(rv["q4"]))
        and int(p["total"]) == int(float(rv["total"]))
        and abs(float(p["ratio"]) - float(rv["ratio"])) < 1e-9
    )
    g2_checks.append(
        {
            "country": c,
            "pool_q1": p["q1"],
            "river_q1": int(float(rv["q1"])),
            "pool_q4": p["q4"],
            "river_q4": int(float(rv["q4"])),
            "pool_total": p["total"],
            "river_total": int(float(rv["total"])),
            "pool_ratio": p["ratio"],
            "river_ratio": float(rv["ratio"]),
            "exact": ok,
        }
    )
PROOF["G2_2022_anchors"] = g2_checks
assert all(x["exact"] for x in g2_checks), g2_checks
print("G2 OK:", [(x["country"], x["pool_ratio"], x["exact"]) for x in g2_checks])

# ---------------------------------------------------------------------------
# G4 — viz4 from collaboration_premium latest year
# ---------------------------------------------------------------------------
src_g4 = DASH / "viz4_data.js"
bak_g4 = DASH / "viz4_data_BEFORE_POOLFIX.js"
if not bak_g4.exists():
    shutil.copy2(src_g4, bak_g4)
    PROOF["G4_backup"] = f"created {bak_g4.name} ({bak_g4.stat().st_size} bytes)"
else:
    PROOF["G4_backup"] = f"already existed {bak_g4.name}"

old_v4_text = bak_g4.read_text(encoding="utf-8")
i, j = old_v4_text.find("["), old_v4_text.rfind("]")
old_v4 = json.loads(old_v4_text[i : j + 1])
region_by_name = {r["name"]: r["region"] for r in old_v4}
old_names = set(region_by_name)

ISO_REGION = {
    "AU": "Pacific Region",
    "BR": "Latin America",
    "CA": "North America",
    "CH": "Western Europe",
    "CN": "Asiatic Region",
    "DE": "Western Europe",
    "ES": "Western Europe",
    "FR": "Western Europe",
    "GB": "Western Europe",
    "IN": "Asiatic Region",
    "IR": "Middle East",
    "IT": "Western Europe",
    "JP": "Asiatic Region",
    "KR": "Asiatic Region",
    "NL": "Western Europe",
    "PL": "Eastern Europe",
    "RU": "Eastern Europe",
    "SE": "Western Europe",
    "TR": "Middle East",
    "US": "Northern America",
}

# Normalize ISO fallback regions to old viz4 vocabulary when possible
# Inspect what old viz4 actually used for our 20
print("Old viz4 sample regions:", sorted({r["region"] for r in old_v4})[:20])

prem = list(csv.DictReader(open(RIVER / "collaboration_premium.csv", encoding="utf-8")))
years = sorted({int(r["Year"]) for r in prem})
target_year = max(years)  # 2024
PROOF["G4_year"] = target_year
rows_y = [r for r in prem if int(r["Year"]) == target_year]
assert len(rows_y) == 20, len(rows_y)

new_v4 = []
for r in sorted(rows_y, key=lambda x: x["Country_Name"]):
    river_name = r["Country_Name"]
    display = river_name
    if river_name == "Russian Federation" and "Russia" in old_names:
        display = "Russia"
    elif river_name not in old_names:
        # try common variants
        for cand in (river_name, river_name.replace("Russian Federation", "Russia")):
            if cand in old_names:
                display = cand
                break

    region = region_by_name.get(display) or region_by_name.get(river_name)
    if not region:
        # map ISO to old-style by looking at similar countries, else ISO_REGION
        region = ISO_REGION.get(r["Country_Code"], "Unknown")
        # if ISO used SCImago-ish labels but old used simpler, prefer old style for known
        # Prefer simpler continental labels matching old viz4 for these codes:
        SIMPLE = {
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
        # Prefer old vocabulary if we can infer from any old country in same SIMPLE bucket
        region = SIMPLE.get(r["Country_Code"], region)

    domestic = round(float(r["Domestic_Avg_Citations"]), 1)
    international = round(float(r["International_Avg_Citations"]), 1)
    gain = round(float(r["Citation_Gain"]), 1)
    new_v4.append(
        {
            "name": display,
            "region": region,
            "domestic": domestic,
            "international": international,
            "gain": gain,
        }
    )

out_g4 = (
    f"// Generated Data for Viz 4 — rebuilt from collaboration_premium.csv year={target_year} (POOLFIX)\n"
    f"const VIZ4_DATA = {json.dumps(new_v4, indent=2)};\n"
)
src_g4.write_text(out_g4, encoding="utf-8")
PROOF["G4_replaced"] = {
    "countries": len(new_v4),
    "year": target_year,
    "names": [x["name"] for x in new_v4],
    "bytes": src_g4.stat().st_size,
    "before_countries": len(old_v4),
}
print("G4 OK:", len(new_v4), "countries year", target_year)
for x in new_v4:
    print(" ", x)

# ---------------------------------------------------------------------------
# G3 — viz3 from openalex
# ---------------------------------------------------------------------------
src_g3 = DASH / "viz3_data.js"
bak_g3 = DASH / "viz3_data_BEFORE_POOLFIX.js"
if not bak_g3.exists():
    shutil.copy2(src_g3, bak_g3)
    PROOF["G3_backup"] = f"created {bak_g3.name} ({bak_g3.stat().st_size} bytes)"
else:
    PROOF["G3_backup"] = f"already existed {bak_g3.name}"

# Keep dashboard_topic as topic_name so TAP filters still match labels;
# store OpenAlex concept id in subfield_id (NOT ASJC 2500 for Quantum).
oa = list(csv.DictReader(open(RIVER / "openalex_topic_country_year.csv", encoding="utf-8")))
# Honesty policy (2026-07-12): only ship complete 7-topic window to tap.
# Pre-2000 AI mega-concept / partial Infectious backfill omitted — see docs/GRAPH3_DATA_ROOT_CAUSE.md
G3_YEAR_MIN, G3_YEAR_MAX = 2000, 2024
oa = [r for r in oa if G3_YEAR_MIN <= int(r["year"]) <= G3_YEAR_MAX]
oa_sorted = sorted(
    oa,
    key=lambda r: (int(r["year"]), r["dashboard_topic"], r["country_iso2"]),
)
def csv_cell(value: str) -> str:
    """Quote CSV cells that need it (commas, quotes, newlines)."""
    s = str(value)
    if any(ch in s for ch in (",", '"', "\n", "\r")):
        return '"' + s.replace('"', '""') + '"'
    return s


lines = ["year,topic_name,subfield_id,country_name,country_code,publications_count"]
for r in oa_sorted:
    name = r["country_key_display_name"]
    lines.append(
        ",".join(
            [
                csv_cell(str(int(r["year"]))),
                csv_cell(r["dashboard_topic"]),
                csv_cell(r["openalex_id"]),
                csv_cell(name),
                csv_cell(r["country_iso2"]),
                csv_cell(str(int(r["works_count"]))),
            ]
        )
    )
csv_body = "\n".join(lines) + "\n"
assert "Quantum Computing,C58053490," in csv_body
quantum_bad = any("Quantum Computing,2500," in l for l in lines)
assert not quantum_bad
# No leading newline after backtick — Papa/DictReader need header on first line
out_g3 = "window.CSV_DATA = `" + csv_body + "`;\n"
src_g3.write_text(out_g3, encoding="utf-8")
years_by_topic: dict[str, set[int]] = defaultdict(set)
for r in oa:
    years_by_topic[r["dashboard_topic"]].add(int(r["year"]))
PROOF["G3_replaced"] = {
    "rows": len(oa),
    "bytes": src_g3.stat().st_size,
    "year_coverage": {
        t: {"min": min(ys), "max": max(ys), "n_years": len(ys)}
        for t, ys in sorted(years_by_topic.items())
    },
    "quantum_id": "C58053490",
    "forbidden_2500_in_quantum": quantum_bad,
    "before_bytes": bak_g3.stat().st_size,
}
print("G3 OK:", len(oa), "rows")

# ---------------------------------------------------------------------------
# G1 — H_Index join only (leave x,y unchanged)
# ---------------------------------------------------------------------------
src_g1 = DASH / "viz1_data.js"
bak_g1 = DASH / "viz1_data_BEFORE_POOLFIX.js"
if not bak_g1.exists():
    shutil.copy2(src_g1, bak_g1)
    PROOF["G1_backup"] = f"created {bak_g1.name} ({bak_g1.stat().st_size} bytes)"
else:
    PROOF["G1_backup"] = f"already existed {bak_g1.name}"

panel = list(csv.DictReader(open(RIVER / "g1_features_panel.csv", encoding="utf-8")))
h_by_cy: dict[tuple[str, int], float] = {}
h_by_c: dict[str, tuple[int, float]] = {}
for r in panel:
    if r["H_Index"] in ("", None):
        continue
    h = float(r["H_Index"])
    code = r["Country_Code"]
    year = int(r["Year"])
    h_by_cy[(code, year)] = h
    prev = h_by_c.get(code)
    if prev is None or year >= prev[0]:
        h_by_c[code] = (year, h)

v1_text = bak_g1.read_text(encoding="utf-8")
i, j = v1_text.find("["), v1_text.rfind("]")
v1 = json.loads(v1_text[i : j + 1])

# Capture xy fingerprint before
xy_before = [(r["Country_Code"], r["Year"], r["x"], r["y"]) for r in v1[:50]]

updated = 0
missing = 0
before_usa = None
after_usa = None
for row in v1:
    if row["Country_Code"] == "USA" and int(row["Year"]) == 2022:
        before_usa = row["H_Index"]
    key = (row["Country_Code"], int(row["Year"]))
    if key in h_by_cy:
        new_h = h_by_cy[key]
        if float(row["H_Index"]) != new_h:
            updated += 1
        row["H_Index"] = new_h
    elif row["Country_Code"] in h_by_c:
        new_h = h_by_c[row["Country_Code"]][1]
        if float(row["H_Index"]) != new_h:
            updated += 1
        row["H_Index"] = new_h
    else:
        missing += 1
    if row["Country_Code"] == "USA" and int(row["Year"]) == 2022:
        after_usa = row["H_Index"]

xy_after = [(r["Country_Code"], r["Year"], r["x"], r["y"]) for r in v1[:50]]
assert xy_before == xy_after, "UMAP x,y must not change"

out_g1 = "const VIZ1_DATA = " + json.dumps(v1) + ";\n"
src_g1.write_text(out_g1, encoding="utf-8")
PROOF["G1_replaced"] = {
    "rows": len(v1),
    "h_updated": updated,
    "h_missing_no_panel": missing,
    "USA_2022_H_before": before_usa,
    "USA_2022_H_after": after_usa,
    "bytes": src_g1.stat().st_size,
    "xy_unchanged": True,
}
print("G1 OK: updated", updated, "missing", missing, "USA2022", before_usa, "->", after_usa)

# Spot-check more H values
for code, year in [("CHN", 2022), ("IND", 2022), ("GBR", 2022)]:
    pool_h = next(r["H_Index"] for r in v1 if r["Country_Code"] == code and r["Year"] == year)
    river_h = h_by_cy.get((code, year)) or (h_by_c[code][1] if code in h_by_c else None)
    print(f"  {code} {year}: pool={pool_h} river={river_h}")

# ---------------------------------------------------------------------------
# G5 spot-check
# ---------------------------------------------------------------------------
india_dir = DASH / "data" / "india_network"
manifest = india_dir / "manifest.json"
PROOF["G5"] = {
    "manifest_exists": manifest.exists(),
    "json_files": len(list(india_dir.glob("*.json"))),
    "action": "NO CHANGE — pipeline-backed spot-check only",
}
print("G5:", PROOF["G5"])

proof_path = RIVER.parent / "_poolfix_proof.json"
# Prefer notes under READY_FOR_TEAM
notes = RIVER / "_notes"
notes.mkdir(exist_ok=True)
proof_path = notes / "_poolfix_proof.json"
proof_path.write_text(json.dumps(PROOF, indent=2), encoding="utf-8")
print("PROOF written to", proof_path)
