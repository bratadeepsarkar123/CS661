#!/usr/bin/env python3
"""Source reconciliation: frontend bundled payloads vs CS661_Dataset (+ G5 processed)."""
from __future__ import annotations

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DS = ROOT / "CS661_Dataset"
DASH = ROOT / "dashboard"
OUT = DASH / "_recon_source_equality_out.txt"

CHECK_CODES = ["USA", "CHN", "IND", "GBR", "DEU"]
CHECK_YEARS = [2015, 2020, 2022, 2024]
NAME_TO_ISO3 = {
    "United States": "USA",
    "United States of America": "USA",
    "China": "CHN",
    "India": "IND",
    "United Kingdom": "GBR",
    "United Kingdom of Great Britain and Northern Ireland": "GBR",
    "Germany": "DEU",
}
ISO2_TO_ISO3 = {"US": "USA", "CN": "CHN", "IN": "IND", "GB": "GBR", "DE": "DEU"}


def load_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(encoding="utf-8", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return list(r.fieldnames or []), rows


def parse_js_const_array(path: Path, const_name: str):
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"(?:const|var|let)\s+{const_name}\s*=\s*", text)
    if not m:
        raise ValueError(f"{const_name} not found in {path}")
    i = m.end()
    while i < len(text) and text[i].isspace():
        i += 1
    if text[i] != "[":
        raise ValueError(f"{const_name} not an array")
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
                blob = text[start : j + 1]
                return json.loads(blob)
    raise ValueError(f"unclosed array for {const_name}")


def parse_js_const_obj(path: Path, const_name: str):
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"(?:const|var|let)\s+{const_name}\s*=\s*", text)
    if not m:
        raise ValueError(f"{const_name} not found")
    i = m.end()
    while i < len(text) and text[i].isspace():
        i += 1
    if text[i] != "{":
        raise ValueError(f"{const_name} not object")
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
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : j + 1])
    raise ValueError("unclosed object")


def fnum(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def nearly(a, b, rtol=1e-4, atol=1e-2):
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if math.isnan(a) or math.isnan(b):
        return False
    return abs(a - b) <= max(atol, rtol * max(abs(a), abs(b)))


def lines(buf, *args):
    s = " ".join(str(a) for a in args)
    buf.append(s)
    print(s)


def index_by(rows, code_key, year_key):
    d = {}
    for r in rows:
        c = r.get(code_key)
        y = r.get(year_key)
        if c is None or y is None or y == "":
            continue
        try:
            y = int(float(y))
        except Exception:
            continue
        d[(str(c), y)] = r
    return d


def recon_g1(buf):
    lines(buf, "\n" + "=" * 72)
    lines(buf, "GRAPH 1 — VIZ1_DATA vs master / raw_worldbank / sjr")
    lines(buf, "=" * 72)
    viz1 = parse_js_const_array(DASH / "viz1_data.js", "VIZ1_DATA")
    _, master = load_csv(DS / "master_dataset.csv")
    _, wb = load_csv(DS / "raw_worldbank.csv")
    _, sjr = load_csv(DS / "sjr_country_metrics.csv")
    _, oa = load_csv(DS / "raw_openalex_docs.csv")

    vidx = index_by(viz1, "Country_Code", "Year")
    midx = index_by(master, "Country_Code", "Year")
    widx = index_by(wb, "Country_Code", "Year")
    oidx = index_by(oa, "Country_Code", "Year")
    sjr_by = {r["Country_Code"]: r for r in sjr}

    fields_compare = [
        ("GDP_Per_Capita_PPP", "GDP_Per_Capita_PPP", "master"),
        ("GERD_Percent_GDP", "GERD_Percent_GDP", "master"),
        ("Total_Docs", "Total_Docs", "master"),
        ("H_Index", "H_Index", "master"),
    ]

    match_n = mismatch_n = missing_n = 0
    lines(buf, "Spot-check frontend vs master_dataset.csv:")
    for code in CHECK_CODES:
        for year in CHECK_YEARS:
            v = vidx.get((code, year))
            m = midx.get((code, year))
            if not v:
                lines(buf, f"  {code} {year}: MISSING in frontend")
                missing_n += 1
                continue
            if not m:
                lines(buf, f"  {code} {year}: MISSING in master")
                missing_n += 1
                continue
            diffs = []
            for vf, mf, _ in fields_compare:
                a, b = fnum(v.get(vf)), fnum(m.get(mf))
                if not nearly(a, b, atol=0.05 if "GDP" in vf else 0.01):
                    diffs.append(f"{vf}: FE={a} MASTER={b}")
            # also vs raw WB for GDP/GERD
            w = widx.get((code, year))
            wb_diffs = []
            if w:
                for f in ["GDP_Per_Capita_PPP", "GERD_Percent_GDP"]:
                    a, b = fnum(v.get(f)), fnum(w.get(f))
                    if a is not None and b is not None and not nearly(a, b, atol=0.05 if "GDP" in f else 0.01):
                        wb_diffs.append(f"{f}: FE={a} WB={b}")
            # OpenAlex docs vs Total_Docs
            o = oidx.get((code, year))
            oa_note = ""
            if o:
                a, b = fnum(v.get("Total_Docs")), fnum(o.get("Total_Docs_OA"))
                if a is not None and b is not None and not nearly(a, b, atol=1):
                    oa_note = f" | Total_Docs FE={a} OA={b} DIFF={a-b:.0f}"
            status = "MATCH" if not diffs else "MISMATCH"
            if diffs:
                mismatch_n += 1
            else:
                match_n += 1
            lines(
                buf,
                f"  {code} {year}: {status} name={v.get('Country_Name')!r} "
                f"docs={v.get('Total_Docs')} H={v.get('H_Index')} GERD={v.get('GERD_Percent_GDP')} "
                f"GDP={v.get('GDP_Per_Capita_PPP')}"
                + (f" DIFFS={diffs}" if diffs else "")
                + (f" WB_DIFFS={wb_diffs}" if wb_diffs else "")
                + oa_note,
            )

    # H_Index static check vs sjr
    lines(buf, "\nH_Index static vs sjr_country_metrics.csv (yearless):")
    for code in CHECK_CODES:
        years_h = []
        for year in range(1996, 2025):
            v = vidx.get((code, year))
            if v and v.get("H_Index") is not None:
                years_h.append(fnum(v["H_Index"]))
        uniq = sorted(set(years_h))
        s = sjr_by.get(code)
        sjr_h = fnum(s["H_Index"]) if s else None
        lines(buf, f"  {code}: FE unique H={uniq[:5]}{'...' if len(uniq)>5 else ''} n_unique={len(uniq)} sjr_H={sjr_h}")

    # Country_Name nulls
    null_names = sum(1 for r in viz1 if not r.get("Country_Name"))
    lines(buf, f"\nFrontend null Country_Name rows: {null_names}/{len(viz1)}")
    lines(buf, f"G1 FE vs master spot MATCH={match_n} MISMATCH={mismatch_n} MISSING={missing_n}")

    # Ireland vs USA H absurdity
    for code in ["IRL", "USA"]:
        v = vidx.get((code, 2022))
        if v:
            lines(buf, f"  absurdity check {code} 2022 H={v.get('H_Index')} docs={v.get('Total_Docs')}")

    return {
        "match": match_n,
        "mismatch": mismatch_n,
        "missing": missing_n,
        "null_names": null_names,
        "n": len(viz1),
    }


def recon_g2(buf):
    lines(buf, "\n" + "=" * 72)
    lines(buf, "GRAPH 2 — REAL_RIDGELINE_DATA vs master Q1/Q4 percents")
    lines(buf, "=" * 72)
    ridge = parse_js_const_obj(DASH / "ridgeline_data.js", "REAL_RIDGELINE_DATA")
    _, master = load_csv(DS / "master_dataset.csv")
    midx = index_by(master, "Country_Code", "Year")

    years = sorted(int(y) for y in ridge.keys())
    lines(buf, f"Years in ridgeline: {years[0]}..{years[-1]} ({len(years)})")
    total_rows = sum(len(v) for v in ridge.values())
    q1q4_gt = 0
    q4_gt = 0
    ratio_cap = 0
    for y, rows in ridge.items():
        for r in rows:
            q1, q4, tot = r["q1"], r["q4"], r["total"]
            if q1 + q4 > tot:
                q1q4_gt += 1
            if q4 > tot:
                q4_gt += 1
            if abs(r["ratio"] - 5.0) < 1e-9 or r["ratio"] >= 4.999:
                ratio_cap += 1
    lines(buf, f"rows={total_rows} q1+q4>total={q1q4_gt} q4>total={q4_gt} ratio~5={ratio_cap}")

    # Compare derived Q1% from counts vs master Q1_Percent for checklist
    lines(buf, "Spot-check: ridgeline counts vs master Q1_Percent/Q4_Percent:")
    name_map = {
        "United States": "USA",
        "China": "CHN",
        "India": "IND",
        "United Kingdom": "GBR",
        "Germany": "DEU",
    }
    match_n = mismatch_n = missing_n = no_master_q = 0
    for year in CHECK_YEARS:
        ys = str(year)
        if ys not in ridge:
            lines(buf, f"  year {year}: MISSING in ridgeline")
            missing_n += 5
            continue
        by_name = {r["country"]: r for r in ridge[ys]}
        for name, code in name_map.items():
            r = by_name.get(name)
            m = midx.get((code, year))
            if not r:
                lines(buf, f"  {name} {year}: MISSING in ridgeline")
                missing_n += 1
                continue
            q1, q4, tot = r["q1"], r["q4"], r["total"]
            # integrity
            integ = []
            if q1 + q4 > tot:
                integ.append(f"q1+q4={q1+q4}>total={tot}")
            if abs(r["ratio"] - min(5.0, (q1 / q4 if q4 else 0))) > 0.02 and q4:
                # ratio may be q1/q4 capped
                pass
            expected_ratio = min(5.0, (q1 / q4) if q4 else 0.0)
            ratio_ok = nearly(r["ratio"], expected_ratio, atol=0.02)
            mq1, mq4 = (fnum(m.get("Q1_Percent")), fnum(m.get("Q4_Percent"))) if m else (None, None)
            # master stores journal-share percents, not document counts — incomparable directly
            # But if we derive FE q1_pct = q1/(q1+q4)*100 when q1+q4>0
            fe_q1pct = (100.0 * q1 / (q1 + q4)) if (q1 + q4) else None
            note = ""
            if mq1 is None:
                no_master_q += 1
                note = "master Q1_Percent empty"
                status = "NO_MASTER_Q"
            else:
                # These are different units (doc counts vs journal %) — report both
                close = fe_q1pct is not None and nearly(fe_q1pct, mq1, atol=5.0)
                status = "PARTIAL_units_differ" if not close else "PCT_NEAR"
                if close:
                    match_n += 1
                else:
                    mismatch_n += 1
                note = f"FE_q1pct_of_q1q4={fe_q1pct:.2f} MASTER_Q1%={mq1} MASTER_Q4%={mq4}"
            lines(
                buf,
                f"  {name} {year}: {status} q1={q1} q4={q4} total={tot} ratio={r['ratio']} "
                f"ratio_ok={ratio_ok} integ={integ or 'ok'} {note}",
            )

    # UK vs USA Q1 2022
    for year in [2020, 2022]:
        ys = str(year)
        if ys not in ridge:
            continue
        by = {r["country"]: r for r in ridge[ys]}
        uk, us = by.get("United Kingdom"), by.get("United States")
        if uk and us:
            lines(buf, f"  UK vs USA {year}: UK_q1={uk['q1']} USA_q1={us['q1']} UK>USA={uk['q1']>us['q1']}")

    return {"rows": total_rows, "q1q4_gt": q1q4_gt, "years": years}


def recon_g3(buf):
    lines(buf, "\n" + "=" * 72)
    lines(buf, "GRAPH 3 — viz3 CSV_DATA (OpenAlex topics)")
    lines(buf, "=" * 72)
    text = (DASH / "viz3_data.js").read_text(encoding="utf-8")
    m = re.search(r"window\.CSV_DATA\s*=\s*`([\s\S]*?)`;", text)
    if not m:
        lines(buf, "CSV_DATA not found")
        return {}
    csv_text = m.group(1).strip()
    reader = csv.DictReader(csv_text.splitlines())
    rows = list(reader)
    lines(buf, f"rows={len(rows)} cols={reader.fieldnames}")
    years = sorted({int(r["year"]) for r in rows if r.get("year")})
    topics = sorted({r["topic_name"] for r in rows})
    lines(buf, f"years={years[0]}..{years[-1]} n_years={len(years)} topics({len(topics)}): {topics}")

    # Quantum ASJC check
    quantum = [r for r in rows if "Quantum" in (r.get("topic_name") or "")]
    if quantum:
        sid = {r["subfield_id"] for r in quantum}
        lines(buf, f"Quantum rows={len(quantum)} subfield_ids={sid}")
        # Materials Science ASJC 2500 is Materials; Quantum Physics often 3100s
        lines(buf, "  NOTE: ASJC 2500 = Materials Science (Scopus); Quantum Physics typically 3101/3107 area")

    # Spot check USA/China/India AI counts
    lines(buf, "Spot-check AI & Machine Learning publications:")
    for year in [2015, 2020, 2022]:
        for ccode, cname in [("US", "USA"), ("CN", "China"), ("IN", "India"), ("GB", "UK"), ("DE", "Germany")]:
            hits = [
                r
                for r in rows
                if r["year"] == str(year)
                and r["country_code"] == ccode
                and r["topic_name"] == "AI & Machine Learning"
            ]
            if hits:
                lines(buf, f"  {cname} {year}: pubs={hits[0]['publications_count']} subfield={hits[0]['subfield_id']}")
            else:
                lines(buf, f"  {cname} {year}: MISSING")

    # Local raw openalex is country-year totals only — not topic breakdown
    _, oa = load_csv(DS / "raw_openalex_docs.csv")
    lines(buf, f"Local raw_openalex_docs.csv has only country-year Total_Docs_OA ({len(oa)} rows) — NO topic/ASJC breakdown")
    lines(buf, "G3 status: NO_LOCAL_RAW for topic-country-year series (partner OpenAlex dump needed)")
    return {"rows": len(rows), "topics": topics, "years": years}


def recon_g4(buf):
    lines(buf, "\n" + "=" * 72)
    lines(buf, "GRAPH 4 — VIZ4_DATA vs collaboration_premium.csv")
    lines(buf, "=" * 72)
    viz4 = parse_js_const_array(DASH / "viz4_data.js", "VIZ4_DATA")
    _, prem = load_csv(DS / "collaboration_premium.csv")
    lines(buf, f"FE countries={len(viz4)} keys={list(viz4[0].keys())}")
    years = sorted({int(r["Year"]) for r in prem})
    lines(buf, f"premium years={years[0]}..{years[-1]} rows={len(prem)}")

    # Aggregate strategy candidates: mean / latest year / 2022
    by_code = defaultdict(list)
    for r in prem:
        by_code[r["Country_Code"]].append(r)

    name_to_code = {
        "United States": "US",  # wait — premium uses AU style ISO2? sample was AU
    }
    # Check code length
    sample_codes = list(by_code.keys())[:5]
    lines(buf, f"premium country code sample: {sample_codes}")

    # Map viz4 names to premium
    name_map = {
        "United States": "US",
        "United Kingdom": "GB",
        "Germany": "DE",
        "China": "CN",
        "India": "IN",
        "Canada": "CA",
        "France": "FR",
        "Japan": "JP",
        "Australia": "AU",
        "Switzerland": "CH",
    }
    # premium might use ISO2 or ISO3 — detect
    if "USA" in by_code:
        name_map = {
            "United States": "USA",
            "United Kingdom": "GBR",
            "Germany": "DEU",
            "China": "CHN",
            "India": "IND",
            "Canada": "CAN",
            "France": "FRA",
            "Japan": "JPN",
            "Australia": "AUS",
            "Switzerland": "CHE",
        }
    elif "US" in by_code:
        pass
    else:
        # try by Country_Name
        by_name = defaultdict(list)
        for r in prem:
            by_name[r["Country_Name"]].append(r)
        lines(buf, "Using Country_Name join")
        for fe in viz4:
            name = fe["name"]
            rows = by_name.get(name, [])
            if not rows:
                lines(buf, f"  {name}: NO_LOCAL row")
                continue
            # mean over years
            dom = sum(fnum(r["Domestic_Avg_Citations"]) or 0 for r in rows) / len(rows)
            intl = sum(fnum(r["International_Avg_Citations"]) or 0 for r in rows) / len(rows)
            gain = sum(fnum(r["Citation_Gain"]) or 0 for r in rows) / len(rows)
            # latest
            latest = max(rows, key=lambda r: int(r["Year"]))
            # 2022
            y2022 = next((r for r in rows if r["Year"] == "2022"), None)
            lines(
                buf,
                f"  {name}: FE dom={fe['domestic']} intl={fe['international']} gain={fe['gain']} | "
                f"MEAN dom={dom:.2f} intl={intl:.2f} gain={gain:.2f} | "
                f"LATEST({latest['Year']}) dom={latest['Domestic_Avg_Citations']} intl={latest['International_Avg_Citations']} gain={latest['Citation_Gain']}"
                + (
                    f" | 2022 dom={y2022['Domestic_Avg_Citations']} intl={y2022['International_Avg_Citations']} gain={y2022['Citation_Gain']}"
                    if y2022
                    else " | 2022 MISSING"
                ),
            )
            # precision check
            for k in ["domestic", "international", "gain"]:
                val = fe[k]
                if abs(val * 10 - round(val * 10)) > 1e-6:
                    lines(buf, f"    non-0.1 precision on {k}={val}")
        # check if FE equals round(mean,1) or round(latest,1)
        lines(buf, "\nEquality tests (atol=0.05):")
        for fe in viz4:
            name = fe["name"]
            rows = by_name.get(name, [])
            if not rows:
                continue
            for label, pick in [
                ("mean_all", None),
                ("latest", max(rows, key=lambda r: int(r["Year"]))),
                ("y2022", next((r for r in rows if r["Year"] == "2022"), None)),
                ("y2020", next((r for r in rows if r["Year"] == "2020"), None)),
                ("y2015", next((r for r in rows if r["Year"] == "2015"), None)),
            ]:
                if label == "mean_all":
                    dom = sum(fnum(r["Domestic_Avg_Citations"]) or 0 for r in rows) / len(rows)
                    intl = sum(fnum(r["International_Avg_Citations"]) or 0 for r in rows) / len(rows)
                    gain = sum(fnum(r["Citation_Gain"]) or 0 for r in rows) / len(rows)
                elif pick is None:
                    continue
                else:
                    dom = fnum(pick["Domestic_Avg_Citations"])
                    intl = fnum(pick["International_Avg_Citations"])
                    gain = fnum(pick["Citation_Gain"])
                ok = (
                    nearly(fe["domestic"], round(dom, 1), atol=0.05)
                    and nearly(fe["international"], round(intl, 1), atol=0.05)
                    and nearly(fe["gain"], round(gain, 1), atol=0.05)
                )
                ok_raw = nearly(fe["domestic"], dom, atol=0.15) and nearly(fe["international"], intl, atol=0.15)
                if ok or ok_raw:
                    lines(buf, f"  {name} matches {label}? round1={ok} near_raw={ok_raw} FE={fe['domestic']}/{fe['international']}/{fe['gain']} SRC={dom:.3f}/{intl:.3f}/{gain:.3f}")
        return {"fe_n": len(viz4), "prem_n": len(prem)}

    # ISO path
    by_name = defaultdict(list)
    for r in prem:
        by_name[r["Country_Name"]].append(r)
    for fe in viz4[:5]:
        lines(buf, fe)
    return {}


def recon_g5(buf):
    lines(buf, "\n" + "=" * 72)
    lines(buf, "GRAPH 5 — india_network payloads vs processed CSVs")
    lines(buf, "=" * 72)
    man = json.loads((DASH / "data/india_network/manifest.json").read_text(encoding="utf-8"))
    lines(buf, f"manifest keys={list(man.keys())}")
    lines(buf, json.dumps(man, indent=2)[:1500])

    overview = json.loads((DASH / "data/india_network/all_years_overview.json").read_text(encoding="utf-8"))
    full = json.loads((DASH / "data/india_network/all_years_full.json").read_text(encoding="utf-8"))
    nodes = overview.get("nodes") or overview.get("institutions") or []
    edges = overview.get("edges") or overview.get("links") or []
    lines(buf, f"overview type keys={list(overview.keys())}")
    if "meta" in overview:
        lines(buf, f"meta={overview['meta']}")
    lines(buf, f"overview nodes={len(nodes)} edges={len(edges)}")
    if nodes:
        lines(buf, f"node0 keys={list(nodes[0].keys())}")
        lines(buf, f"node0 sample={ {k:nodes[0].get(k) for k in list(nodes[0].keys())[:12]} }")
    if edges:
        lines(buf, f"edge0={edges[0]}")

    # processed local
    candidates = [
        ROOT / "CS661 Project/data/processed/institution_master.csv",
        ROOT / "CS661 Project/data/processed/collaboration_edges_full.csv",
        ROOT / "CS661 Project/data/processed/institution_funding.csv",
        ROOT / "CS661 Project/data/processed/institution_patents.csv",
        ROOT / "data/processed/institution_master.csv",
        ROOT / "dashboard/data/processed/institution_master.csv",
    ]
    found = [p for p in candidates if p.exists()]
    lines(buf, f"processed candidates found: {[str(p) for p in found]}")

    # Also search
    for p in [
        ROOT / "CS661 Project/data/processed",
        ROOT / "data",
    ]:
        if p.exists():
            for f in sorted(p.rglob("*.csv"))[:30]:
                lines(buf, f"  csv: {f.relative_to(ROOT)} ({f.stat().st_size})")

    # Spot-check scimago_pct static
    scimago_years = {n.get("scimago_year") for n in nodes if isinstance(n, dict)}
    scimago_pcts = [n.get("scimago_pct") for n in nodes if isinstance(n, dict) and n.get("scimago_pct") is not None]
    lines(buf, f"scimago_years={scimago_years} n_with_pct={len(scimago_pcts)}")

    # Year slice edge counts
    for year in [2015, 2020, 2022, 2024]:
        p = DASH / f"data/india_network/{year}_overview.json"
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            nn = len(d.get("nodes") or [])
            ee = len(d.get("edges") or [])
            meta = d.get("meta")
            lines(buf, f"  {year}_overview: nodes={nn} edges={ee} meta={meta}")

    # Compare to collaboration_edges if present
    edge_csv = ROOT / "CS661 Project/data/processed/collaboration_edges_full.csv"
    if edge_csv.exists():
        _, erows = load_csv(edge_csv)
        lines(buf, f"collaboration_edges_full rows={len(erows)} cols={list(erows[0].keys()) if erows else []}")
        # IITK-IITI if present
        for r in erows[:3]:
            lines(buf, f"  edge sample: {r}")

    master_csv = ROOT / "CS661 Project/data/processed/institution_master.csv"
    if master_csv.exists():
        _, mrows = load_csv(master_csv)
        lines(buf, f"institution_master rows={len(mrows)} cols={list(mrows[0].keys()) if mrows else []}")

    # CS661_Dataset has NO india network raw
    lines(buf, "CS661_Dataset: no India/NIRF/OpenAlex institution files — G5 raw lives under scripts pipeline / CS661 Project/data")
    return {"overview_nodes": len(nodes), "overview_edges": len(edges)}


def inventory(buf):
    lines(buf, "=" * 72)
    lines(buf, "INVENTORY — CS661_Dataset")
    lines(buf, "=" * 72)
    for p in sorted(DS.iterdir()):
        if p.is_file():
            lines(buf, f"{p.name:40s} {p.stat().st_size:10d} bytes")
    # year coverage master
    _, master = load_csv(DS / "master_dataset.csv")
    years = sorted({int(r["Year"]) for r in master})
    codes = {r["Country_Code"] for r in master}
    lines(buf, f"master_dataset: rows={len(master)} countries={len(codes)} years={years[0]}..{years[-1]}")
    # fill rates
    for col in ["GDP_Per_Capita_PPP", "GERD_Percent_GDP", "Total_Docs", "H_Index", "Q1_Percent", "Q4_Percent"]:
        filled = sum(1 for r in master if r.get(col) not in (None, ""))
        lines(buf, f"  fill {col}: {filled}/{len(master)} ({100*filled/len(master):.1f}%)")


def main():
    buf = []
    inventory(buf)
    g1 = recon_g1(buf)
    g2 = recon_g2(buf)
    g3 = recon_g3(buf)
    g4 = recon_g4(buf)
    g5 = recon_g5(buf)
    lines(buf, "\nDONE")
    OUT.write_text("\n".join(buf), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
