#!/usr/bin/env python3
"""Hard audit of all dashboard visualization data payloads."""
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


def load_js_json_var(path: Path, var_name: str):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(rf"(?:const|var|let)\s+{re.escape(var_name)}\s*=\s*", text)
    if not m:
        return None
    i = m.end()
    while i < len(text) and text[i] in " \t\r\n":
        i += 1
    if i >= len(text) or text[i] not in "[{":
        return None
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


def section(title: str):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def audit_viz1():
    section("GRAPH 1 — VIZ1_DATA")
    data = load_js_json_var(BASE / "viz1_data.js", "VIZ1_DATA")
    assert isinstance(data, list), type(data)
    print(f"rows={len(data)} bytes={(BASE/'viz1_data.js').stat().st_size}")
    print("keys:", sorted(data[0].keys()))
    years = sorted({d["Year"] for d in data})
    codes = {d["Country_Code"] for d in data}
    names = {d["Country_Name"] for d in data}
    regions = Counter(d["Region"] for d in data)
    print(f"years={years[0]}..{years[-1]} ({len(years)}) countries={len(codes)} names={len(names)}")
    print("regions:", dict(regions))

    # null / nan
    nullish = Counter()
    for d in data:
        for k, v in d.items():
            if v is None or (isinstance(v, float) and math.isnan(v)):
                nullish[k] += 1
    print("nullish:", dict(nullish) or "none")

    # duplicates
    cy = Counter((d["Country_Code"], d["Year"]) for d in data)
    dups = [(k, v) for k, v in cy.items() if v > 1]
    print(f"dup_country_year={len(dups)}")

    # coverage
    incomplete = []
    for code in sorted(codes):
        ys = {d["Year"] for d in data if d["Country_Code"] == code}
        if len(ys) < len(years):
            incomplete.append((code, sorted(set(years) - ys)[:5], len(ys)))
    print(f"incomplete_coverage={len(incomplete)}/{len(codes)}")
    print(" incomplete ex:", incomplete[:8])

    # metric ranges
    for metric in ("Total_Docs", "H_Index", "GERD_Percent_GDP", "GDP_Per_Capita_PPP"):
        vals = [d[metric] for d in data if isinstance(d.get(metric), (int, float))]
        print(
            f"  {metric}: min={min(vals):.4g} med={statistics.median(vals):.4g} max={max(vals):.4g} "
            f"zeros={sum(1 for v in vals if v==0)} negs={sum(1 for v in vals if v<0)}"
        )

    # constant GERD across years for a country = imputed/static
    static_gerd = 0
    static_h = 0
    for code in list(codes)[:80]:
        rows = [d for d in data if d["Country_Code"] == code]
        g = {round(d["GERD_Percent_GDP"], 5) for d in rows}
        h = {round(d["H_Index"], 3) for d in rows}
        if len(g) == 1:
            static_gerd += 1
        if len(h) == 1:
            static_h += 1
    print(f"among_first_80_codes: static_GERD={static_gerd} static_H_Index={static_h}")

    # majors spot-check
    for code in ("USA", "CHN", "IND", "GBR", "DEU", "JPN", "TWN", "RUS"):
        rows = sorted(
            [d for d in data if d["Country_Code"] == code], key=lambda d: d["Year"]
        )
        if not rows:
            alt = {"USA": "United States", "CHN": "China", "IND": "India", "TWN": "Taiwan", "RUS": "Russia"}
            needle = alt.get(code, "___")
            rows = sorted(
                [
                    d
                    for d in data
                    if isinstance(d.get("Country_Name"), str) and needle in d["Country_Name"]
                ],
                key=lambda d: d["Year"],
            )
        if not rows:
            print(f"  {code}: MISSING")
            continue
        # coord reversals
        xrev = sum(
            1
            for i in range(1, len(rows) - 1)
            if (rows[i]["x"] - rows[i - 1]["x"]) * (rows[i + 1]["x"] - rows[i]["x"]) < 0
        )
        docs = [d["Total_Docs"] for d in rows]
        spikes = sum(
            1
            for i in range(1, len(docs))
            if docs[i] > 3 * max(docs[i - 1], 1) or docs[i] < docs[i - 1] / 3
        )
        # impossible: docs flat forever
        flat_docs = len(set(round(v, 1) for v in docs)) == 1
        last = rows[-1]
        first = rows[0]
        print(
            f"  {code} ({first['Country_Name']}): n={len(rows)} "
            f"docs {first['Total_Docs']:.0f}->{last['Total_Docs']:.0f} "
            f"GERD {first['GERD_Percent_GDP']:.3f}->{last['GERD_Percent_GDP']:.3f} "
            f"H {first['H_Index']:.0f}->{last['H_Index']:.0f} "
            f"xrev={xrev} doc_spikes={spikes} flat_docs={flat_docs}"
        )

    # Aruba-like constant Total_Docs (imputation smell)
    flat_doc_countries = 0
    for code in codes:
        docs = {round(d["Total_Docs"], 1) for d in data if d["Country_Code"] == code}
        if len(docs) == 1:
            flat_doc_countries += 1
    print(f"countries_with_flat_Total_Docs_all_years={flat_doc_countries}/{len(codes)}")

    # GDP sanity: USA should be high
    usa2022 = [d for d in data if d["Country_Code"] == "USA" and d["Year"] == 2022]
    chn2022 = [d for d in data if d["Country_Code"] == "CHN" and d["Year"] == 2022]
    ind2022 = [d for d in data if d["Country_Code"] == "IND" and d["Year"] == 2022]
    for label, rows in (("USA", usa2022), ("CHN", chn2022), ("IND", ind2022)):
        if rows:
            d = rows[0]
            print(
                f"  2022 {label}: docs={d['Total_Docs']:.0f} GDP_PPP={d['GDP_Per_Capita_PPP']:.0f} "
                f"GERD={d['GERD_Percent_GDP']:.3f} H={d['H_Index']:.0f} x={d['x']:.2f} y={d['y']:.2f}"
            )


def audit_viz2():
    section("GRAPH 2 — REAL_RIDGELINE_DATA (reconfirm)")
    data = load_js_json_var(BASE / "ridgeline_data.js", "REAL_RIDGELINE_DATA")
    # may be list or dict
    if isinstance(data, dict):
        rows = []
        for y, arr in data.items():
            if isinstance(arr, list):
                for r in arr:
                    rr = dict(r)
                    rr["year"] = int(y)
                    rows.append(rr)
        data = rows
    print(f"rows={len(data)} keys={sorted(data[0].keys())}")
    ratio_capped = sum(
        1
        for r in data
        if r.get("q4")
        and abs(r.get("ratio", 0) - 5.0) < 1e-9
        and (r["q1"] / r["q4"]) > 5.01
    )
    qsum_gt = sum(1 for r in data if r["q1"] + r["q4"] > r["total"] + 1)
    q4_gt = sum(1 for r in data if r["q4"] > r["total"] + 1)
    print(f"ratio_capped={ratio_capped} q1+q4>total={qsum_gt} q4>total={q4_gt}")
    for name in ("United States", "United Kingdom", "China", "India", "Taiwan"):
        rows = [r for r in data if r.get("country") == name]
        if not rows:
            print(f"  {name}: MISSING")
            continue
        last = max(rows, key=lambda r: r["year"])
        tr = last["q1"] / last["q4"] if last["q4"] else float("nan")
        print(
            f"  {name} {last['year']}: q1={last['q1']} q4={last['q4']} total={last['total']} "
            f"stored_ratio={last['ratio']} true_ratio={tr:.2f}"
        )


def audit_viz3():
    section("GRAPH 3 — window.CSV_DATA (topic race CSV)")
    text = (BASE / "viz3_data.js").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"window\.CSV_DATA\s*=\s*`", text)
    if not m:
        print("FAIL: no CSV_DATA template")
        return
    end = text.find("`;", m.end())
    csv_text = text[m.end() : end]
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    print(f"rows={len(rows)} fields={reader.fieldnames}")

    # types
    for r in rows:
        r["year"] = int(r["year"])
        r["publications_count"] = int(float(r["publications_count"]))
        r["subfield_id"] = r["subfield_id"]

    years = sorted({r["year"] for r in rows})
    topics = sorted({r["topic_name"] for r in rows})
    countries = {r["country_code"] for r in rows}
    print(f"years={years[0]}..{years[-1]} ({len(years)}) topics={len(topics)} countries={len(countries)}")
    print("topics:", topics)

    # null/neg
    negs = sum(1 for r in rows if r["publications_count"] < 0)
    zeros = sum(1 for r in rows if r["publications_count"] == 0)
    print(f"neg={negs} zero={zeros}")

    # duplicate year-topic-country
    keyc = Counter((r["year"], r["topic_name"], r["country_code"]) for r in rows)
    dups = sum(1 for v in keyc.values() if v > 1)
    print(f"dup_year_topic_country={dups}")

    # global totals by year for AI
    def series(topic, code):
        return sorted(
            [
                (r["year"], r["publications_count"])
                for r in rows
                if r["topic_name"] == topic and r["country_code"] == code
            ]
        )

    for topic in topics:
        for code in ("US", "CN", "IN", "GB"):
            s = series(topic, code)
            if not s:
                continue
            # early years tiny is ok for 1950; check modern
            modern = [p for y, p in s if y >= 2015]
            spikes = sum(
                1
                for i in range(1, len(s))
                if s[i][1] > 5 * max(s[i - 1][1], 1) or (s[i - 1][1] > 20 and s[i][1] < s[i - 1][1] / 5)
            )
            if code == "US" or (modern and modern[-1] > 100):
                print(
                    f"  {topic[:28]:28} {code}: {s[0]} -> {s[-1]} modern_last={modern[-1] if modern else 'n/a'} spikes={spikes}"
                )

    # China overtaking USA in AI?
    for topic in topics:
        us = dict(series(topic, "US"))
        cn = dict(series(topic, "CN"))
        common = sorted(set(us) & set(cn))
        flips = [y for y in common if y >= 2000 and cn[y] > us[y]]
        if flips:
            print(f"  China>USA in {topic}: first_flip={flips[0]} last={flips[-1]} n={len(flips)}")

    # Top countries 2023 AI
    for topic in topics[:1]:
        y = max(years)
        top = sorted(
            [r for r in rows if r["year"] == y and r["topic_name"] == topic],
            key=lambda r: -r["publications_count"],
        )[:10]
        print(f"\nTop 10 {topic} in {y}:")
        for r in top:
            print(f"  {r['country_name'][:40]:40} {r['publications_count']}")

    # Check if 1950 AI counts look like OpenAlex/Scopus artifact
    early = [r for r in rows if r["year"] == 1950 and r["topic_name"] == topics[0]]
    print(f"1950 rows for {topics[0]}: {len(early)} total_pubs={sum(r['publications_count'] for r in early)}")

    # Year gaps per topic-country
    gap_examples = []
    for topic in topics:
        for code in ("US", "CN", "IN"):
            s = series(topic, code)
            if len(s) < 10:
                continue
            ys = [y for y, _ in s]
            gaps = [ys[i] - ys[i - 1] for i in range(1, len(ys)) if ys[i] - ys[i - 1] > 1]
            if gaps:
                gap_examples.append((topic, code, max(gaps), len(gaps)))
    print(f"series_with_year_gaps={len(gap_examples)} ex={gap_examples[:6]}")


def audit_viz4():
    section("GRAPH 4 — VIZ4_DATA")
    data = load_js_json_var(BASE / "viz4_data.js", "VIZ4_DATA")
    print(f"rows={len(data)} keys={sorted(data[0].keys())}")
    regions = Counter(d["region"] for d in data)
    print("regions:", dict(regions))
    bad_gain = [
        d
        for d in data
        if abs(d["gain"] - (d["international"] - d["domestic"])) > 0.11
    ]
    intl_lt = [d for d in data if d["international"] < d["domestic"]]
    print(f"gain_mismatch={len(bad_gain)} intl<dom={len(intl_lt)}")
    if intl_lt:
        print(" intl<dom:", intl_lt)
    vals_d = [d["domestic"] for d in data]
    vals_i = [d["international"] for d in data]
    print(
        f"domestic range {min(vals_d):.1f}-{max(vals_d):.1f} "
        f"intl {min(vals_i):.1f}-{max(vals_i):.1f}"
    )
    # suspiciously round?
    roundish = sum(
        1
        for d in data
        if abs(d["domestic"] * 10 - round(d["domestic"] * 10)) < 1e-9
        and abs(d["international"] * 10 - round(d["international"] * 10)) < 1e-9
    )
    print(f"values_at_0.1_precision={roundish}/{len(data)}")

    for name in (
        "United States",
        "China",
        "India",
        "Switzerland",
        "Saudi Arabia",
        "Russia",
    ):
        hits = [d for d in data if d["name"] == name]
        print(f"  {name}: {hits[0] if hits else 'MISSING'}")

    # compare fallback
    fb = load_js_json_var(BASE / "data.js", "COLLAB_DATA")
    if fb:
        print(f"fallback COLLAB_DATA n={len(fb)}")
        close = 0
        for d in data:
            m = next((x for x in fb if x["name"] == d["name"]), None)
            if m and abs(m["domestic"] - d["domestic"]) < 0.5:
                close += 1
        print(f"approx_match_fallback_dom={close}")


def audit_viz5():
    section("GRAPH 5 — INDIA_NETWORK_DATA / JSON files")
    # Prefer on-disk JSON (same content, easier)
    netdir = BASE / "data" / "india_network"
    if not netdir.exists():
        # try project copy
        alt = BASE.parent / "CS661 Project" / "data" / "india_network"
        netdir = alt if alt.exists() else None
    print("netdir:", netdir)

    if netdir and netdir.exists():
        files = sorted(netdir.glob("*.json"))
        print(f"json_files={len(files)}")
        man_path = netdir / "manifest.json"
        if man_path.exists():
            man = json.loads(man_path.read_text(encoding="utf-8"))
            print("manifest keys:", list(man.keys()) if isinstance(man, dict) else type(man))
            print(json.dumps(man, indent=2)[:1200])

        for fname in ("2024_full.json", "2024_overview.json", "2015_full.json", "all_years_full.json"):
            p = netdir / fname
            if not p.exists():
                print(f" MISSING {fname}")
                continue
            blob = json.loads(p.read_text(encoding="utf-8"))
            audit_net(fname, blob)

        # year-over-year node/edge counts
        print("\nYoY coverage:")
        for year in range(2015, 2025):
            p = netdir / f"{year}_full.json"
            if not p.exists():
                print(f"  {year}: missing full")
                continue
            blob = json.loads(p.read_text(encoding="utf-8"))
            nodes = blob.get("nodes") or []
            edges = blob.get("edges") or blob.get("links") or []
            print(f"  {year}: nodes={len(nodes)} edges={len(edges)}")

        # IITK-IITI
        print("\nIIT Kanpur <-> IIT Indore weights:")
        for year in range(2015, 2025):
            p = netdir / f"{year}_full.json"
            if not p.exists():
                continue
            blob = json.loads(p.read_text(encoding="utf-8"))
            w = pair_weight(blob, "Kanpur", "Indore")
            print(f"  {year}: {w}")

        # funding static check
        print("\nFunding change 2015 vs 2024 (sample):")
        b15 = json.loads((netdir / "2015_full.json").read_text(encoding="utf-8"))
        b24 = json.loads((netdir / "2024_full.json").read_text(encoding="utf-8"))
        f15 = {n.get("id") or n.get("name"): n.get("funding") for n in b15.get("nodes", [])}
        f24 = {n.get("id") or n.get("name"): n.get("funding") for n in b24.get("nodes", [])}
        common = [k for k in f15 if k in f24 and f15[k] is not None and f24[k] is not None]
        same = sum(1 for k in common if f15[k] == f24[k])
        print(f"  nodes_with_funding_both={len(common)} identical_funding={same}")
        # lat/lon out of India bbox
        bad_geo = []
        for n in b24.get("nodes", []):
            lat = n.get("lat") if n.get("lat") is not None else n.get("latitude")
            lon = n.get("lon") if n.get("lon") is not None else n.get("lng", n.get("longitude"))
            if lat is None or lon is None:
                continue
            if not (6 <= lat <= 37 and 68 <= lon <= 98):
                bad_geo.append((n.get("name") or n.get("id"), lat, lon))
        print(f"  nodes_outside_India_bbox={len(bad_geo)} ex={bad_geo[:8]}")
        return

    # fallback: parse bundled JS (slow/large)
    print("No JSON dir; attempting bundled JS parse (may be slow)...")
    data = load_js_json_var(BASE / "india_network_data.js", "INDIA_NETWORK_DATA")
    print("parsed keys:", len(data) if isinstance(data, dict) else data)


def audit_net(label, blob):
    print(f"\n--- {label} ---")
    print("top_keys:", list(blob.keys())[:15])
    nodes = blob.get("nodes") or blob.get("institutions") or []
    edges = blob.get("edges") or blob.get("links") or []
    print(f"nodes={len(nodes)} edges={len(edges)}")
    if not nodes:
        return
    print("node_keys:", sorted(nodes[0].keys()))
    print("node0:", {k: nodes[0][k] for k in list(nodes[0])[:12]})
    if edges:
        print("edge_keys:", sorted(edges[0].keys()))
        print("edge0:", edges[0])
    ids = [n.get("id") for n in nodes]
    print(f"dup_ids={sum(1 for c in Counter(ids).values() if c>1)}")
    idset = set(ids)
    if edges and "source" in edges[0]:
        dang = sum(
            1
            for e in edges
            if e.get("source") not in idset or e.get("target") not in idset
        )
        print(f"dangling={dang}/{len(edges)}")
        ws = [e.get("weight", 0) for e in edges]
        print(f"weight min/med/max={min(ws)}/{statistics.median(ws)}/{max(ws)}")


def pair_weight(blob, a_sub, b_sub):
    nodes = blob.get("nodes") or []
    edges = blob.get("edges") or blob.get("links") or []
    aids = [n["id"] for n in nodes if a_sub.lower() in str(n.get("name", "")).lower()]
    bids = [n["id"] for n in nodes if b_sub.lower() in str(n.get("name", "")).lower()]
    if not aids or not bids:
        return f"not_found a={aids} b={bids}"
    total = 0
    for e in edges:
        s, t = e.get("source"), e.get("target")
        if (s in aids and t in bids) or (s in bids and t in aids):
            total += e.get("weight") or 0
    return {"weight": total, "a": aids[:2], "b": bids[:2]}


def audit_cross():
    section("CROSS-CUTTING — what UI uses vs what data.js claims")
    app = (BASE / "app.js").read_text(encoding="utf-8", errors="replace")
    print("Hero badges claim: World Bank API, UNESCO UIS, SCImago, THE, NIRF")
    print("data.js header claims: World Bank API live + fallbacks")
    print()
    print("Actual render paths:")
    print("  G1: VIZ1_DATA (real file) + MA/EMA smoother in app.js")
    print("  G2: REAL_RIDGELINE_DATA + getCountryMetrics() SYNTHETIC GDP/R&D")
    print("  G3: window.CSV_DATA via Papa.parse")
    print("  G4: VIZ4_DATA (else COLLAB_DATA hardcoded)")
    print("  G5: INDIA.render / INDIA_NETWORK_DATA (else getIndiaNetwork demo)")
    print()
    print(f"  getCountryMetrics present: {'getCountryMetrics' in app}")
    print(f"  getTopicsForYear used in app: {app.count('getTopicsForYear')}")
    print(f"  getCountriesForYear used in app: {app.count('getCountriesForYear')}")
    print(f"  getIndiaNetwork used in app: {app.count('getIndiaNetwork')}")
    # bubble size field
    if "Total_Docs" in app:
        print("  Viz1 size field references Total_Docs: yes")
    if "Publications" in app and "Total_Docs" in app:
        print("  Viz1 also mentions Publications string (check mapping)")


def main():
    audit_viz1()
    audit_viz2()
    audit_viz3()
    audit_viz4()
    audit_viz5()
    audit_cross()
    section("DONE")


if __name__ == "__main__":
    main()
