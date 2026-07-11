#!/usr/bin/env python3
"""Continue audits for graphs 3-5 with deeper checks."""
from __future__ import annotations

import csv
import io
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent


def section(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


def load_js_json_var(path, var_name):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"(?:const|var|let)\s+{re.escape(var_name)}\s*=\s*", text)
    if not m:
        return None
    i = m.end()
    while i < len(text) and text[i] in " \t\r\n":
        i += 1
    depth = 0
    in_str = False
    esc = False
    quote = None
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
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0:
                return json.loads(text[i : j + 1])
    return None


def audit_viz2():
    section("GRAPH 2 reconfirm")
    data = load_js_json_var(BASE / "ridgeline_data.js", "REAL_RIDGELINE_DATA")
    rows = []
    for y, arr in data.items():
        for r in arr:
            rr = dict(r)
            rr["year"] = int(y)
            rows.append(rr)
    print(f"rows={len(rows)} years={min(r['year'] for r in rows)}..{max(r['year'] for r in rows)}")
    ratio_capped = sum(
        1
        for r in rows
        if r["q4"] and abs(r["ratio"] - 5.0) < 1e-9 and r["q1"] / r["q4"] > 5.01
    )
    print(
        f"ratio_capped={ratio_capped} q1+q4>total={sum(1 for r in rows if r['q1']+r['q4']>r['total']+1)} "
        f"q4>total={sum(1 for r in rows if r['q4']>r['total']+1)}"
    )
    for name in ("United States", "United Kingdom", "China", "India", "Taiwan"):
        rs = [r for r in rows if r["country"] == name]
        if not rs:
            print(f"  {name}: MISSING")
            continue
        last = max(rs, key=lambda r: r["year"])
        tr = last["q1"] / last["q4"] if last["q4"] else float("nan")
        print(
            f"  {name} {last['year']}: q1={last['q1']} q4={last['q4']} total={last['total']} "
            f"ratio={last['ratio']} true={tr:.2f}"
        )


def audit_viz3():
    section("GRAPH 3 CSV_DATA")
    text = (BASE / "viz3_data.js").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"window\.CSV_DATA\s*=\s*`", text)
    end = text.find("`;", m.end())
    rows = list(csv.DictReader(io.StringIO(text[m.end() : end])))
    for r in rows:
        r["year"] = int(r["year"])
        r["publications_count"] = int(float(r["publications_count"]))
    years = sorted({r["year"] for r in rows})
    topics = sorted({r["topic_name"] for r in rows})
    countries = {r["country_code"] for r in rows}
    print(f"rows={len(rows)} years={years[0]}..{years[-1]} ({len(years)}) topics={len(topics)} countries={len(countries)}")
    print("topics:", topics)

    # UI expects these topics
    expected = [
        "AI & Machine Learning",
        "CRISPR & Genomics",
        "Infectious Diseases",
        "Data Science & Big Data",
        "Renewable Energy",
        "Robotics & Automation",
        "Quantum Computing",
    ]
    print("UI topic coverage:", {t: (t in topics) for t in expected})
    print("extra topics in data:", [t for t in topics if t not in expected])

    # year gaps: UI loops 1950-2025
    missing_years_ui = [y for y in range(1950, 2026) if y not in years]
    print(f"years_missing_from_UI_range={missing_years_ui}")

    # duplicates
    keyc = Counter((r["year"], r["topic_name"], r["country_code"]) for r in rows)
    print(f"dups={sum(1 for v in keyc.values() if v>1)}")

    def series(topic, code):
        return sorted(
            (r["year"], r["publications_count"])
            for r in rows
            if r["topic_name"] == topic and r["country_code"] == code
        )

    # Global totals for AI by year (sum countries)
    for topic in expected:
        by_year = defaultdict(int)
        for r in rows:
            if r["topic_name"] == topic:
                by_year[r["year"]] += r["publications_count"]
        ys = sorted(by_year)
        if not ys:
            print(f"  {topic}: NO DATA")
            continue
        # check monotonic-ish growth 2010-2023
        modern = [(y, by_year[y]) for y in ys if 2010 <= y <= 2023]
        drops = [
            (modern[i - 1], modern[i])
            for i in range(1, len(modern))
            if modern[i][1] < 0.7 * modern[i - 1][1]
        ]
        print(
            f"  {topic}: {ys[0]}:{by_year[ys[0]]} -> {ys[-1]}:{by_year[ys[-1]]} "
            f"modern_drops>30%={len(drops)} ex={drops[:2]}"
        )

    # COVID bump infectious
    inf = defaultdict(int)
    for r in rows:
        if r["topic_name"] == "Infectious Diseases":
            inf[r["year"]] += r["publications_count"]
    for y in range(2018, 2025):
        print(f"  Infectious {y}: {inf.get(y, 0)}")

    # Top AI 2023
    y = 2023 if 2023 in years else max(years)
    top = sorted(
        [r for r in rows if r["year"] == y and r["topic_name"] == "AI & Machine Learning"],
        key=lambda r: -r["publications_count"],
    )[:12]
    print(f"\nTop AI {y}:")
    for r in top:
        print(f"  {r['country_name'][:45]:45} {r['publications_count']}")

    # China vs USA AI crossover
    us = dict(series("AI & Machine Learning", "US"))
    cn = dict(series("AI & Machine Learning", "CN"))
    flips = [y for y in sorted(set(us) & set(cn)) if cn[y] > us[y]]
    print(f"China>USA AI years: first={flips[0] if flips else None} count={len(flips)}")
    if 2023 in us and 2023 in cn:
        print(f"  2023 US={us[2023]} CN={cn[2023]}")

    # Quantum 2500 subfield - is it real?
    q_ids = {r["subfield_id"] for r in rows if r["topic_name"] == "Quantum Computing"}
    print(f"Quantum subfield_ids={q_ids}")

    # 2025 empty?
    print(f"rows_in_2025={sum(1 for r in rows if r['year']==2025)}")
    print(f"rows_in_2024={sum(1 for r in rows if r['year']==2024)}")

    # Belize etc noise in early years - fraction of tiny countries
    early = [r for r in rows if r["year"] <= 1960 and r["topic_name"] == "AI & Machine Learning"]
    print(f"AI<=1960 rows={len(early)} total_pubs={sum(r['publications_count'] for r in early)}")


def audit_viz4():
    section("GRAPH 4 VIZ4_DATA")
    data = load_js_json_var(BASE / "viz4_data.js", "VIZ4_DATA")
    print(f"n={len(data)}")
    print("regions", dict(Counter(d["region"] for d in data)))
    bad = [d for d in data if abs(d["gain"] - (d["international"] - d["domestic"])) > 0.11]
    lt = [d for d in data if d["international"] < d["domestic"]]
    print(f"gain_mismatch={len(bad)} intl<dom={len(lt)}")
    # all values *.1 precision?
    prec = sum(
        1
        for d in data
        if round(d["domestic"], 1) == d["domestic"] and round(d["international"], 1) == d["international"]
    )
    print(f"exact_0.1_precision={prec}/{len(data)}")
    # sorted by premium
    ranked = sorted(data, key=lambda d: -d["gain"])
    print("Top premium:")
    for d in ranked[:8]:
        print(f"  {d['name']}: dom={d['domestic']} intl={d['international']} gain={d['gain']}")
    print("Bottom premium:")
    for d in ranked[-5:]:
        print(f"  {d['name']}: dom={d['domestic']} intl={d['international']} gain={d['gain']}")
    # India/China/USA
    for n in ("United States", "China", "India", "Switzerland", "Saudi Arabia"):
        d = next(x for x in data if x["name"] == n)
        print(f"  spot {n}: {d}")

    # THE / SCImago typical cites/doc for domestic vs intl - values 5-30 look like cites/doc
    # Check if looks hand-tuned: very smooth region patterns
    by_reg = defaultdict(list)
    for d in data:
        by_reg[d["region"]].append(d["gain"])
    for reg, gains in by_reg.items():
        print(f"  region {reg}: mean_gain={statistics.mean(gains):.2f} n={len(gains)}")


def audit_viz5():
    section("GRAPH 5 india_network JSON")
    netdir = BASE / "data" / "india_network"
    man = json.loads((netdir / "manifest.json").read_text(encoding="utf-8"))
    print("manifest:", man)

    for year in range(2015, 2025):
        blob = json.loads((netdir / f"{year}_full.json").read_text(encoding="utf-8"))
        nodes = blob.get("nodes") or []
        edges = blob.get("edges") or blob.get("links") or []
        year_field = blob.get("year")
        print(f"  {year}: nodes={len(nodes)} edges={len(edges)} year_field={year_field}")

    b15 = json.loads((netdir / "2015_full.json").read_text(encoding="utf-8"))
    b20 = json.loads((netdir / "2020_full.json").read_text(encoding="utf-8"))
    b23 = json.loads((netdir / "2023_full.json").read_text(encoding="utf-8"))
    b24 = json.loads((netdir / "2024_full.json").read_text(encoding="utf-8"))

    print("\nnode0 keys 2024:", sorted(b24["nodes"][0].keys()))
    print("node0 sample:", {k: b24["nodes"][0][k] for k in list(b24["nodes"][0])[:15]})
    if b24.get("edges"):
        print("edge0:", b24["edges"][0])

    # funding variance
    def fund_map(blob):
        out = {}
        for n in blob["nodes"]:
            fid = n.get("id")
            out[fid] = n.get("funding") or n.get("research_funding_cr") or n.get("funding_cr")
        return out

    f20, f23 = fund_map(b20), fund_map(b23)
    common = [k for k in f20 if k in f23 and f20[k] is not None and f23[k] is not None]
    changed = sum(1 for k in common if f20[k] != f23[k])
    same = sum(1 for k in common if f20[k] == f23[k])
    print(f"funding 2020 vs 2023: common={len(common)} changed={changed} same={same}")

    # NIRF rank variance
    def rank_map(blob):
        out = {}
        for n in blob["nodes"]:
            out[n.get("id")] = n.get("nirf_rank") or n.get("rank") or n.get("nirf")
        return out

    r20, r23 = rank_map(b20), rank_map(b23)
    common_r = [k for k in r20 if k in r23 and r20[k] is not None and r23[k] is not None]
    changed_r = sum(1 for k in common_r if r20[k] != r23[k])
    print(f"nirf/rank 2020 vs 2023: common={len(common_r)} changed={changed_r}")

    # geo bbox
    bad = []
    for n in b24["nodes"]:
        lat = n.get("lat", n.get("latitude"))
        lon = n.get("lon", n.get("lng", n.get("longitude")))
        if lat is None or lon is None:
            bad.append(("missing", n.get("name"), n.get("id")))
        elif not (6 <= float(lat) <= 37 and 68 <= float(lon) <= 98):
            bad.append(("oob", n.get("name"), lat, lon))
    print(f"geo_issues={len(bad)} ex={bad[:8]}")

    # dangling
    ids = {n["id"] for n in b24["nodes"]}
    edges = b24.get("edges") or b24.get("links") or []
    dang = sum(1 for e in edges if e.get("source") not in ids or e.get("target") not in ids)
    print(f"dangling_edges_2024={dang}/{len(edges)}")

    # IITK-IITI
    print("\nKanpur-Indore:")
    for year, blob in [(2015, b15), (2020, b20), (2023, b23), (2024, b24)]:
        nodes = blob["nodes"]
        edges = blob.get("edges") or blob.get("links") or []
        aids = [n["id"] for n in nodes if "Kanpur" in str(n.get("name", ""))]
        bids = [n["id"] for n in nodes if "Indore" in str(n.get("name", ""))]
        w = 0
        for e in edges:
            s, t = e.get("source"), e.get("target")
            if (s in aids and t in bids) or (s in bids and t in aids):
                w += e.get("weight") or 0
        print(f"  {year}: w={w} a={aids[:1]} b={bids[:1]}")

    # overview vs full
    ov = json.loads((netdir / "2024_overview.json").read_text(encoding="utf-8"))
    print(f"\n2024 overview nodes={len(ov.get('nodes',[]))} edges={len(ov.get('edges') or ov.get('links') or [])}")

    # 2024 == all_years?
    allf = json.loads((netdir / "all_years_full.json").read_text(encoding="utf-8"))
    print(f"all_years_full nodes={len(allf.get('nodes',[]))} edges={len(allf.get('edges') or allf.get('links') or [])} year={allf.get('year')}")

    # SCImago static fields?
    def sci_map(blob):
        out = {}
        for n in blob["nodes"]:
            out[n["id"]] = (
                n.get("scimago_impact")
                or n.get("research_impact")
                or n.get("impact")
                or n.get("normalized_impact")
            )
        return out

    s15, s24 = sci_map(b15), sci_map(b24)
    if any(v is not None for v in s24.values()):
        common_s = [k for k in s15 if k in s24 and s15[k] is not None]
        same_s = sum(1 for k in common_s if s15[k] == s24[k])
        print(f"impact-like field static? common={len(common_s)} same={same_s}")
    else:
        # print available numeric fields that are identical across years
        keys = set(b24["nodes"][0])
        print("checking static numeric fields across 2015 vs 2024...")
        for key in sorted(keys):
            if key in ("id", "name", "lat", "lon", "latitude", "longitude", "lng"):
                continue
            vals15 = {n["id"]: n.get(key) for n in b15["nodes"]}
            vals24 = {n["id"]: n.get(key) for n in b24["nodes"]}
            common = [i for i in vals15 if i in vals24 and isinstance(vals24[i], (int, float))]
            if len(common) < 20:
                continue
            same = sum(1 for i in common if vals15[i] == vals24[i])
            pct = same / len(common)
            if pct > 0.9:
                print(f"  STATIC-ish {key}: {same}/{len(common)} identical ({pct:.0%})")
            elif pct < 0.5:
                print(f"  VARIES {key}: {same}/{len(common)} identical ({pct:.0%})")


if __name__ == "__main__":
    audit_viz2()
    audit_viz3()
    audit_viz4()
    audit_viz5()
    print("\nDONE")
