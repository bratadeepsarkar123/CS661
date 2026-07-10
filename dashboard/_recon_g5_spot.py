#!/usr/bin/env python3
from pathlib import Path
import json
import csv
import re

ROOT = Path(__file__).resolve().parents[1]
iitk = "129be347-f8df-4fd2-b553-37ff0fd31af1"
iiti = "92004806-cba2-4966-9ebf-9f31bc5a9597"

for fn in ["all_years_full.json", "2024_full.json", "2024_overview.json"]:
    d = json.loads((ROOT / "dashboard/data/india_network" / fn).read_text(encoding="utf-8"))
    edges = d.get("edges", [])
    hit = [e for e in edges if {e["source"], e["target"]} == {iitk, iiti}]
    print(fn, "nodes", len(d.get("nodes", [])), "edges", len(edges), "IITK-IITI", hit)

full = json.loads((ROOT / "dashboard/data/india_network/all_years_full.json").read_text(encoding="utf-8"))
iisc = next(n for n in full["nodes"] if n.get("openalex_id") == "I59270414")
print("IISc", {k: iisc.get(k) for k in ["scimago_pct", "scimago_year", "total_works", "nirf_rank", "name"]})

fund = list(csv.DictReader((ROOT / "CS661 Project/data/processed/institution_funding.csv").open(encoding="utf-8")))
print("funding cols", list(fund[0].keys()), "n", len(fund))
iisc_f = [r for r in fund if r.get("institution_id") == iisc["id"] or "Indian Institute of Science" in str(r)]
print("IISc funding rows", len(iisc_f), iisc_f[:2] if iisc_f else None)

# viz1 GERD trail
text = (ROOT / "dashboard/viz1_data.js").read_text(encoding="utf-8")
m = re.search(r"const VIZ1_DATA\s*=\s*", text)
i = m.end()
while text[i].isspace():
    i += 1
depth = 0
start = i
in_str = False
esc = False
quote = ""
for j in range(i, len(text)):
    ch = text[j]
    if in_str:
        if esc:
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == quote:
            in_str = False
        continue
    if ch in "\"'":
        in_str = True
        quote = ch
        continue
    if ch == "[":
        depth += 1
    elif ch == "]":
        depth -= 1
        if depth == 0:
            viz = json.loads(text[start : j + 1])
            break

for code in ["USA", "CHN", "IND", "GBR", "DEU"]:
    rows = sorted([r for r in viz if r["Country_Code"] == code], key=lambda r: r["Year"])
    print(code, "GERD last5", [(r["Year"], r.get("GERD_Percent_GDP")) for r in rows[-5:]])
    print(code, "docs last5", [(r["Year"], r.get("Total_Docs")) for r in rows[-5:]])

# Compare FE USA 2015 domestic to premium 2015
print("Note: G4 FE values are 0.1 precision and gain=intl-dom always")
