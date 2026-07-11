#!/usr/bin/env python3
"""Extra deep checks for Viz1 H-index and related."""
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
t = (BASE / "viz1_data.js").read_text(encoding="utf-8")
m = re.search(r"VIZ1_DATA\s*=\s*", t)
i = m.end()
depth = 0
in_s = False
esc = False
q = None
for j in range(i, len(t)):
    ch = t[j]
    if in_s:
        if esc:
            esc = False
        elif ch == "\\":
            esc = True
        elif ch == q:
            in_s = False
        continue
    if ch in "\"'":
        in_s = True
        q = ch
        continue
    if ch in "[{":
        depth += 1
    elif ch in "]}":
        depth -= 1
        if depth == 0:
            data = json.loads(t[i : j + 1])
            break

h_by = {}
for d in data:
    h_by.setdefault(d["Country_Code"], set()).add(round(d["H_Index"], 3))
static = sum(1 for s in h_by.values() if len(s) == 1)
varying = sum(1 for s in h_by.values() if len(s) > 1)
print("H_Index static countries", static, "varying", varying)

last = {}
for d in data:
    if d["Year"] == 2024:
        last[d["Country_Code"]] = (d["Country_Name"], d["H_Index"], d["Total_Docs"])
print("Top H_Index 2024:")
for n, h, docs in sorted(last.values(), key=lambda x: -x[1])[:15]:
    print(f"  {n}: H={h} docs={docs}")

nulls = [(d["Country_Code"], d["Year"]) for d in data if d["Country_Name"] is None]
print("null names", len(nulls), nulls[:10])

g_by = {}
for d in data:
    g_by.setdefault(d["Country_Code"], set()).add(round(d["GERD_Percent_GDP"], 5))
print("GERD fully static", sum(1 for s in g_by.values() if len(s) == 1))

# USA vs known SCImago-ish docs order 2024
print("\n2024 docs ranking top 10:")
for n, h, docs in sorted(last.values(), key=lambda x: -x[2])[:10]:
    print(f"  {n}: docs={docs:.0f} H={h}")
