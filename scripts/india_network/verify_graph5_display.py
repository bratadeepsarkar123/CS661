#!/usr/bin/env python3
"""Manual hard-test harness: trace Graph 5 dashboard values to backend sources.

Compares processed CSVs and export JSON (and notes UI-only transforms in india_network.js)
for institute scalars, partner lists, and collaboration edge pairs.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import uuid
from dataclasses import dataclass, field as dc_field
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR  # noqa: E402
from nirf_utils import (  # noqa: E402
    load_nirf_rankings_all_years,
    lookup_nirf_rank_for_institute,
    name_similarity,
    slider_year_to_funding_academic_year,
    slider_year_to_nirf_ranking_year,
)

# Reuse spot-check helpers for raw NIRF tracing.
from run_random_spot_check import (  # noqa: E402
    _load_losers,
    _norm,
    _processed_values,
    _raw_funding_rows,
    _raw_patent_rows,
    _raw_rank_row,
    _values_match,
)

DASHBOARD_DIR = PROJECT_ROOT / "dashboard" / "data" / "india_network"

EDGE_CHAIN = (
    "OpenAlex works (data/cache/openalex/*.json) "
    "-> 05_fetch_openalex_works.py / 05b_assemble_works_from_cache.py "
    "-> works_raw.parquet "
    "-> 06_build_domestic_edges.py (W1-W5 filters, co-auth pairs per year) "
    "-> domestic_works.parquet + collaboration_edges_full.csv "
    "-> 09_export_payloads.py / 09b_export_year_slices.py "
    "-> dashboard/data/india_network/{year}_full.json "
    "-> dashboard/india_network.js (partner list sort, marker radius)"
)

SCALAR_GROUPS: dict[str, list[str]] = {
    "funding": [
        "research_funding_cr",
        "total_expenditure_cr",
        "sponsored_projects",
        "funding_academic_year",
        "funding_status",
    ],
    "patents": [
        "patents_published",
        "patents_granted",
        "patent_calendar_year",
        "patent_status",
    ],
    "nirf_rank": [
        "nirf_rank",
        "nirf_ranking_category",
        "nirf_match_status",
    ],
    "scimago": ["scimago_pct", "scimago_year"],
    "node": ["total_works", "is_hub", "radius", "tier"],
}

PROCESSED_PATHS = {
    "master": PROCESSED_DIR / "institution_master.csv",
    "edges": PROCESSED_DIR / "collaboration_edges_full.csv",
    "funding": PROCESSED_DIR / "institution_funding.csv",
    "funding_by_year": PROCESSED_DIR / "institution_funding_by_year.csv",
    "patents": PROCESSED_DIR / "institution_patents.csv",
    "patents_by_year": PROCESSED_DIR / "institution_patents_by_year.csv",
    "quality": PROCESSED_DIR / "institution_quality_static.csv",
    "hubs": PROCESSED_DIR / "hub_flags.csv",
    "domestic_works": PROCESSED_DIR / "domestic_works.parquet",
}


@dataclass
class VerifyRow:
    layer: str
    source_file: str
    value: Any
    match: str  # yes | no | n/a | warn
    note: str = ""


@dataclass
class VerifyResult:
    query: str
    institute_id: str | None = None
    institute_name: str | None = None
    year: int | None = None
    field: str | None = None
    edge_chain: str = EDGE_CHAIN
    rows: list[VerifyRow] = dc_field(default_factory=list)
    warnings: list[str] = dc_field(default_factory=list)
    passed: bool = True

    def add(self, layer: str, source: str, value: Any, match: str, note: str = "") -> None:
        self.rows.append(VerifyRow(layer, source, value, match, note))
        if match == "no":
            self.passed = False

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def _is_uuid(val: str) -> bool:
    try:
        uuid.UUID(val)
        return True
    except ValueError:
        return False


def _expand_iit_shorthand(query: str) -> list[str]:
    """Return alternate search strings for common IIT abbreviations."""
    q = query.strip()
    alts = [q]
    m = re.match(r"^IIT[\s-]+(.+)$", q, re.I)
    if m:
        city = m.group(1).strip()
        alts.append(f"Indian Institute of Technology {city}")
        alts.append(f"Indian Institute of Technology, {city}")
    if re.match(r"^IISc\b", q, re.I):
        alts.append("Indian Institute of Science")
    return alts


def resolve_institute(master: pd.DataFrame, query: str) -> pd.Series:
    """Resolve institute by UUID institution_id or fuzzy canonical_name match."""
    if _is_uuid(query):
        hit = master[master["institution_id"] == query]
        if hit.empty:
            raise SystemExit(f"No institution_id={query} in institution_master.csv")
        return hit.iloc[0]

    candidates = _expand_iit_shorthand(query)
    for cand in candidates:
        q = cand.strip().lower()
        exact = master[master["canonical_name"].str.lower() == q]
        if len(exact) == 1:
            return exact.iloc[0]

        contains = master[master["canonical_name"].str.contains(re.escape(cand), case=False, na=False)]
        if len(contains) == 1:
            return contains.iloc[0]
        if len(contains) > 1:
            # Prefer IIT over university when shorthand used
            if cand.lower().startswith("indian institute of technology"):
                iit_only = contains[
                    contains["canonical_name"].str.contains("Indian Institute of Technology", case=False, na=False)
                ]
                if len(iit_only) == 1:
                    return iit_only.iloc[0]
            names = "\n".join(f"  - {r.canonical_name} ({r.institution_id})" for r in contains.itertuples())
            raise SystemExit(f"Ambiguous name '{query}'. Matches:\n{names}")

        tokens = [t for t in re.split(r"[^a-z0-9]+", q) if len(t) > 2]
        if tokens:
            mask = pd.Series(True, index=master.index)
            for tok in tokens:
                mask &= master["canonical_name"].str.lower().str.contains(re.escape(tok), na=False)
            token_hits = master[mask]
            if len(token_hits) == 1:
                return token_hits.iloc[0]

    scored = []
    for _, row in master.iterrows():
        score = max(name_similarity(alt, str(row["canonical_name"])) for alt in candidates)
        if score >= 0.40:
            scored.append((score, row))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        raise SystemExit(f"No institute matching '{query}' in institution_master.csv")
    if len(scored) > 1 and scored[0][0] - scored[1][0] < 0.06:
        names = "\n".join(f"  - {r['canonical_name']} (score={s:.2f})" for s, r in scored[:5])
        raise SystemExit(f"Ambiguous fuzzy match for '{query}':\n{names}")
    best_score, best = scored[0]
    if best_score < 0.65:
        print(f"Note: fuzzy match '{best['canonical_name']}' (score={best_score:.2f})", file=sys.stderr)
    return best


def load_json_payload(year: int | None, variant: str = "full") -> tuple[dict, Path]:
    if year is None:
        fname = f"all_years_{variant}.json"
    else:
        fname = f"{year}_{variant}.json"
    path = DASHBOARD_DIR / fname
    if not path.exists():
        raise SystemExit(f"Missing export payload: {path}")
    return json.loads(path.read_text(encoding="utf-8")), path


def json_year_note(requested: int | None, payload: dict) -> str | None:
    py = payload.get("year")
    if requested is None:
        return None
    if py == requested:
        return None
    return f"Payload year={py!r} does not match requested year={requested}"


def node_from_json(payload: dict, inst_id: str) -> dict | None:
    for node in payload.get("nodes", []):
        if node.get("id") == inst_id:
            return node
    return None


def edges_for_inst_processed(
    edges: pd.DataFrame, inst_id: str, year: int | None, *, rollup: bool = False
) -> pd.DataFrame:
    sub = edges[(edges["inst_a"] == inst_id) | (edges["inst_b"] == inst_id)].copy()
    if year is not None and not rollup:
        sub = sub[sub["year"] == year]
    if rollup and year is not None:
        sub = (
            sub.groupby(["inst_a", "inst_b"], as_index=False)
            .agg(weight=("weight", "sum"), citation_weight=("citation_weight", "sum"))
        )
    return sub


def partner_map_from_edges(edge_df: pd.DataFrame, inst_id: str) -> dict[str, dict[str, int]]:
    partners: dict[str, dict[str, int]] = {}
    for _, row in edge_df.iterrows():
        partner = row["inst_b"] if row["inst_a"] == inst_id else row["inst_a"]
        partners[str(partner)] = {
            "weight": int(row["weight"]),
            "citation_weight": int(int(row.get("citation_weight") or 0)),
        }
    return partners


def partners_from_json(payload: dict, inst_id: str) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for edge in payload.get("edges", []):
        src, tgt = edge["source"], edge["target"]
        if src == inst_id:
            out[tgt] = {"weight": int(edge["weight"]), "citation_weight": int(edge.get("citation_weight") or 0)}
        elif tgt == inst_id:
            out[src] = {"weight": int(edge["weight"]), "citation_weight": int(edge.get("citation_weight") or 0)}
    return out


def pair_edge_processed(
    edges: pd.DataFrame, id_a: str, id_b: str, year: int | None, *, rollup: bool = False
) -> dict[str, Any] | None:
    sub = edges[
        ((edges["inst_a"] == id_a) & (edges["inst_b"] == id_b))
        | ((edges["inst_a"] == id_b) & (edges["inst_b"] == id_a))
    ]
    if year is not None and not rollup:
        sub = sub[sub["year"] == year]
    if sub.empty:
        return None
    if rollup or year is None:
        return {
            "weight": int(sub["weight"].sum()),
            "citation_weight": int(sub["citation_weight"].sum()),
            "years": sorted(sub["year"].unique().tolist()),
        }
    row = sub.iloc[0]
    return {
        "weight": int(row["weight"]),
        "citation_weight": int(row["citation_weight"]),
        "year": int(row["year"]),
        "csv_row": int(row.name) + 2,
    }


def pair_edge_json(payload: dict, id_a: str, id_b: str) -> dict[str, int] | None:
    for edge in payload.get("edges", []):
        pair = {edge["source"], edge["target"]}
        if pair == {id_a, id_b}:
            return {
                "weight": int(edge["weight"]),
                "citation_weight": int(edge.get("citation_weight") or 0),
            }
    return None


def export_radius(total_works: float) -> float:
    return round(max(4.0, min(18.0, math.sqrt(max(float(total_works or 0), 1)) * 0.04)), 3)


def ui_marker_radius(total_works: float, is_hub: bool) -> float:
    works = total_works or 0
    if is_hub:
        return round(min(14, max(7, 5 + math.sqrt(works) * 0.015)), 3)
    return round(min(9, max(4, 3 + math.sqrt(works) * 0.008)), 3)


def load_context() -> dict[str, Any]:
    ctx: dict[str, Any] = {}
    for key, path in PROCESSED_PATHS.items():
        if path.exists():
            if path.suffix == ".parquet":
                ctx[key] = pd.read_parquet(path)
            else:
                ctx[key] = pd.read_csv(path)
        else:
            ctx[key] = None
    ctx["losers"] = _load_losers()
    ctx["research_raw"] = (
        pd.read_csv(RAW_DIR / "nirf_research_projects.csv")
        if (RAW_DIR / "nirf_research_projects.csv").exists()
        else pd.DataFrame()
    )
    patents_raw_path = RAW_DIR / "nirf_patents_scraped.csv"
    if not patents_raw_path.exists():
        patents_raw_path = RAW_DIR / "nirf_patents_by_institute.csv"
    ctx["patents_raw"] = pd.read_csv(patents_raw_path) if patents_raw_path.exists() else pd.DataFrame()
    ctx["nirf_all"] = load_nirf_rankings_all_years()
    return ctx


def processed_scalar_values(
    ctx: dict[str, Any], master_row: pd.Series, field_group: str, year: int | None = None
) -> dict[str, Any]:
    inst_id = str(master_row["institution_id"])
    fund_df = ctx["funding_by_year"] if year is not None and ctx.get("funding_by_year") is not None else ctx["funding"]
    pat_df = ctx["patents_by_year"] if year is not None and ctx.get("patents_by_year") is not None else ctx["patents"]
    quality_df = ctx["quality"]
    fund_row = None
    pat_row = None
    if fund_df is not None:
        fidx = fund_df.set_index("institution_id")
        if inst_id in fidx.index:
            if year is not None and "academic_year" in fund_df.columns:
                target = slider_year_to_funding_academic_year(year)
                hits = fund_df[
                    (fund_df["institution_id"] == inst_id)
                    & (fund_df["academic_year"].astype(str) == str(target))
                ]
                fund_row = hits.iloc[0] if not hits.empty else fidx.loc[inst_id]
            else:
                fund_row = fidx.loc[inst_id]
            if isinstance(fund_row, pd.DataFrame):
                fund_row = fund_row.iloc[0]
    if pat_df is not None:
        pidx = pat_df.set_index("institution_id")
        if inst_id in pidx.index:
            if year is not None and "patent_calendar_year" in pat_df.columns:
                from nirf_utils import slider_year_to_patent_calendar_year  # noqa: WPS433

                target = slider_year_to_patent_calendar_year(year)
                hits = pat_df[
                    (pat_df["institution_id"] == inst_id)
                    & (pat_df["patent_calendar_year"] == target)
                ]
                pat_row = hits.iloc[0] if not hits.empty else pidx.loc[inst_id]
            else:
                pat_row = pidx.loc[inst_id]
            if isinstance(pat_row, pd.DataFrame):
                pat_row = pat_row.iloc[0]

    base = _processed_values(master_row, fund_row, pat_row, ctx["losers"])
    if fund_row is not None and pd.notna(fund_row.get("academic_year")):
        base["funding_academic_year"] = str(fund_row["academic_year"])
    if pat_row is not None and pd.notna(pat_row.get("patent_calendar_year")):
        base["patent_calendar_year"] = int(pat_row["patent_calendar_year"])
    else:
        base["patent_calendar_year"] = None
    # quality / node extras
    if quality_df is not None and inst_id in quality_df.set_index("institution_id").index:
        qrow = quality_df.set_index("institution_id").loc[inst_id]
        base["scimago_pct"] = _norm(qrow.get("scimago_pct"))
        base["scimago_year"] = 2019 if pd.notna(qrow.get("scimago_pct")) else None
    else:
        base["scimago_pct"] = None
        base["scimago_year"] = None

    base["total_works"] = int(master_row.get("total_works") or 0)
    base["tier"] = str(master_row.get("tier", ""))
    hub_df = ctx["hubs"]
    is_hub = bool(master_row.get("is_hub", False))
    if hub_df is not None and inst_id in hub_df.set_index("institution_id").index:
        is_hub = bool(hub_df.set_index("institution_id").loc[inst_id].get("is_hub", is_hub))
    base["is_hub"] = is_hub
    base["radius"] = export_radius(base["total_works"])

    # funding_status / patent_status derived in export (mirror 09_export_payloads)
    name = str(master_row["canonical_name"])
    nirf_id = master_row.get("nirf_institute_id")
    match_status = base.get("nirf_match_status")
    funding_cr = base.get("research_funding_cr")
    if match_status in ("unranked", "blocked"):
        base["funding_status"] = "unranked"
    elif funding_cr is not None:
        base["funding_status"] = "reported"
    elif pd.notna(master_row.get("nirf_rank")):
        base["funding_status"] = "unavailable"
    else:
        base["funding_status"] = "unavailable"

    if field_group == "funding":
        return {k: base.get(k) for k in SCALAR_GROUPS["funding"]}
    if field_group == "patents":
        return {k: base.get(k) for k in SCALAR_GROUPS["patents"]}
    if field_group == "nirf_rank":
        return {k: base.get(k) for k in SCALAR_GROUPS["nirf_rank"]}
    if field_group == "scimago":
        return {k: base.get(k) for k in SCALAR_GROUPS["scimago"]}
    if field_group == "node":
        return {k: base.get(k) for k in SCALAR_GROUPS["node"]}
    if field_group in SCALAR_GROUPS:
        return {k: base.get(k) for k in SCALAR_GROUPS[field_group]}
    return {field_group: base.get(field_group)}


def raw_scalar_trace(
    ctx: dict[str, Any], master_row: pd.Series, scalar: str, processed: dict[str, Any]
) -> tuple[Any, str]:
    nirf_id = master_row.get("nirf_institute_id")
    category = master_row.get("nirf_ranking_category")
    if scalar in ("nirf_rank", "nirf_ranking_category"):
        ranking_year = processed.get("nirf_ranking_season") or slider_year_to_nirf_ranking_year(
            processed.get("slider_year")
        )
        season_df = ctx["nirf_all"]
        if ranking_year and not season_df.empty:
            season_df = season_df[season_df["nirf_year"] == int(ranking_year)]
        raw_rank, ref = _raw_rank_row(season_df if not season_df.empty else ctx["nirf_all"], nirf_id, category)
        if raw_rank is None and ranking_year:
            rank_val, cat_val, _ = lookup_nirf_rank_for_institute(
                nirf_institute_id=str(nirf_id) if pd.notna(nirf_id) else None,
                canonical_name=str(master_row["canonical_name"]),
                ranking_year=int(ranking_year),
                nirf_all_years=ctx["nirf_all"],
                inst_type=master_row.get("inst_type"),
                city=master_row.get("city"),
                state=master_row.get("state"),
            )
            if rank_val is not None:
                raw_rank = {
                    "rank": rank_val,
                    "ranking_category": cat_val,
                    "institute_id": str(nirf_id) if pd.notna(nirf_id) else "",
                    "nirf_year": int(ranking_year),
                }
                ref = f"nirf_rankings_{ranking_year}.csv (name/ID lookup)"
        if scalar == "nirf_rank":
            return (raw_rank["rank"] if raw_rank else None, ref)
        return (raw_rank["ranking_category"] if raw_rank else None, ref)
    if scalar in ("research_funding_cr", "sponsored_projects", "funding_academic_year", "total_expenditure_cr"):
        raw_funding = _raw_funding_rows(
            ctx["research_raw"], nirf_id, processed.get("funding_academic_year")
        )
        if scalar == "total_expenditure_cr":
            return (None, "institution_funding.csv — expenditure from NIRF PDF via 08_join_nirf_funding.py")
        item = raw_funding.get(scalar, (None, "nirf_research_projects.csv"))
        return item[0], item[1]
    if scalar in ("patents_published", "patents_granted", "patent_calendar_year"):
        patent_year = processed.get("patent_calendar_year") or 2022
        raw_patents = _raw_patent_rows(ctx["patents_raw"], nirf_id, patent_year)
        if scalar == "patent_calendar_year":
            return (patent_year, f"nirf_patents_scraped.csv (calendar_year={patent_year})")
        return raw_patents.get(scalar, (None, "nirf_patents_scraped.csv"))
    if scalar == "scimago_pct":
        return (processed.get("scimago_pct"), "scimago_india.csv via 07_join_scimago_quality.py")
    if scalar in ("funding_status", "patent_status", "nirf_match_status"):
        return (None, "derived in 09_export_payloads.py (not in raw CSV)")
    if scalar == "radius":
        return (processed.get("radius"), "derived in 09_export_payloads._node_radius()")
    if scalar == "total_works":
        return (processed.get("total_works"), "OpenAlex institution works count in institution_master.csv")
    return (None, "no raw trace configured")


def verify_pair(
    ctx: dict[str, Any], name_a: str, name_b: str, year: int | None, variant: str
) -> VerifyResult:
    master = ctx["master"]
    edges = ctx["edges"]
    row_a = resolve_institute(master, name_a)
    row_b = resolve_institute(master, name_b)
    id_a, id_b = str(row_a["institution_id"]), str(row_b["institution_id"])
    label_a, label_b = str(row_a["canonical_name"]), str(row_b["canonical_name"])

    result = VerifyResult(
        query=f"pair {label_a} <-> {label_b}",
        institute_id=f"{id_a} <-> {id_b}",
        institute_name=f"{label_a} <-> {label_b}",
        year=year,
        field="collaboration_edge",
    )

    payload, json_path = load_json_payload(year, variant)
    note = json_year_note(year, payload)
    if note:
        result.warn(note)
    use_rollup = False

    proc = pair_edge_processed(edges, id_a, id_b, year, rollup=False)
    proc_roll = pair_edge_processed(edges, id_a, id_b, year, rollup=True) if use_rollup else None
    json_edge = pair_edge_json(payload, id_a, id_b)

    if proc:
        src = f"collaboration_edges_full.csv row {proc.get('csv_row', '?')} (year={proc.get('year', 'rollup')})"
        result.add("Processed", src, f"weight={proc['weight']}, citation_weight={proc['citation_weight']}", "n/a")
    else:
        result.add("Processed", "collaboration_edges_full.csv", "no edge (year slice)", "n/a")

    if proc_roll:
        result.add(
            "Processed (all-years rollup)",
            "collaboration_edges_full.csv (sum years)",
            f"weight={proc_roll['weight']}, citation_weight={proc_roll['citation_weight']}, years={proc_roll['years']}",
            "n/a",
        )

    if json_edge:
        match = "n/a"
        if proc_roll and use_rollup:
            match = "yes" if _values_match(proc_roll["weight"], json_edge["weight"]) else "no"
        elif proc and not use_rollup:
            match = "yes" if _values_match(proc["weight"], json_edge["weight"]) else "no"
        elif proc and use_rollup:
            match = "warn"
            result.warn("JSON is all-years; year-slice processed weight differs from JSON (expected for 2024 panel file)")
        result.add(
            "Export JSON",
            str(json_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
            f"weight={json_edge['weight']}, citation_weight={json_edge['citation_weight']}",
            match,
        )
    else:
        result.add("Export JSON", str(json_path.relative_to(PROJECT_ROOT)).replace("\\", "/"), "edge absent", "n/a")
        if proc or proc_roll:
            result.passed = False
            result.rows[-1].match = "no"

    # Raw trace: count domestic works linking both institutes for year
    dom = ctx.get("domestic_works")
    raw_count = None
    if dom is not None and not dom.empty:
        oa_a, oa_b = str(row_a["openalex_id"]), str(row_b["openalex_id"])
        hits = 0
        for _, w in dom.iterrows():
            if year is not None and int(w.get("year", -1)) != year:
                continue
            insts = w.get("institution_ids")
            if isinstance(insts, str):
                insts = json.loads(insts)
            if oa_a in insts and oa_b in insts:
                hits += 1
        raw_count = hits
    result.add(
        "Raw (domestic works)",
        "domestic_works.parquet",
        f"co-authored works={raw_count}" if raw_count is not None else "file missing",
        "yes" if proc and raw_count is not None and raw_count >= proc["weight"] else ("n/a" if raw_count is None else "warn"),
        "Edge weight counts papers with both institutes (weight may exceed unique works after filters)",
    )

    result.add(
        "UI-only",
        "dashboard/india_network.js",
        "edge thickness ~ weight; partner list sorted desc by weight",
        "n/a",
        "UI-only transform",
    )
    return result


def verify_institute_field(
    ctx: dict[str, Any], institute: str, field: str, year: int | None, variant: str
) -> VerifyResult:
    master = ctx["master"]
    row = resolve_institute(master, institute)
    inst_id = str(row["institution_id"])
    name = str(row["canonical_name"])

    result = VerifyResult(
        query=f"{name} - {field}",
        institute_id=inst_id,
        institute_name=name,
        year=year,
        field=field,
    )

    if field == "partners":
        return _verify_partners(ctx, result, inst_id, year, variant)

    group = field if field in SCALAR_GROUPS else field
    fields = SCALAR_GROUPS.get(group, [field])
    payload, json_path = load_json_payload(year, variant)
    note = json_year_note(year, payload)
    if note:
        result.warn(note)
    json_node = node_from_json(payload, inst_id)
    processed = processed_scalar_values(ctx, row, group if group in SCALAR_GROUPS else field, year=year)

    for scalar in fields:
        proc_val = _norm(processed.get(scalar))
        json_val = _norm(json_node.get(scalar)) if json_node else None
        raw_val, raw_ref = raw_scalar_trace(ctx, row, scalar, processed)
        raw_val = _norm(raw_val)

        proc_src = {
            "research_funding_cr": "institution_funding_by_year.csv" if year else "institution_funding.csv",
            "total_expenditure_cr": "institution_funding_by_year.csv" if year else "institution_funding.csv",
            "sponsored_projects": "institution_funding_by_year.csv" if year else "institution_funding.csv",
            "funding_academic_year": "institution_funding_by_year.csv" if year else "institution_funding.csv",
            "patents_published": "institution_patents_by_year.csv" if year else "institution_patents.csv",
            "patents_granted": "institution_patents_by_year.csv" if year else "institution_patents.csv",
            "patent_calendar_year": "institution_patents_by_year.csv" if year else "institution_patents.csv",
            "nirf_rank": "institution_master.csv",
            "nirf_ranking_category": "institution_master.csv",
            "scimago_pct": "institution_quality_static.csv",
            "total_works": "institution_master.csv",
            "is_hub": "hub_flags.csv",
        }.get(scalar, "institution_master.csv / derived")

        match_json = "yes" if _values_match(proc_val, json_val) else ("no" if json_node else "n/a")
        result.add("Processed", proc_src, proc_val, match_json)

        if raw_ref and not raw_ref.startswith("derived"):
            raw_match = "yes" if _values_match(proc_val, raw_val) else ("n/a" if raw_val is None else "no")
            result.add("Raw", raw_ref.split(" row")[0], raw_val, raw_match, raw_ref)
        elif scalar in ("funding_status", "patent_status", "nirf_match_status"):
            result.add("Derived (export)", "09_export_payloads.py", proc_val, "n/a", raw_ref)

        result.add("Export JSON", f"{json_path.name} -> nodes[].{scalar}", json_val, match_json)

        if scalar == "radius":
            ui_r = ui_marker_radius(processed.get("total_works", 0), processed.get("is_hub", False))
            result.add(
                "UI-only",
                "india_network.js markerRadius()",
                ui_r,
                "n/a",
                f"Export radius={proc_val} (payload); map marker uses different formula",
            )

    return result


def _verify_partners(
    ctx: dict[str, Any], result: VerifyResult, inst_id: str, year: int | None, variant: str
) -> VerifyResult:
    edges = ctx["edges"]
    master = ctx["master"]
    id_to_name = dict(zip(master["institution_id"], master["canonical_name"]))

    payload, json_path = load_json_payload(year, variant)
    note = json_year_note(year, payload)
    if note:
        result.warn(note)
    use_rollup = False

    proc_edges = edges_for_inst_processed(edges, inst_id, year, rollup=False)
    proc_partners = partner_map_from_edges(proc_edges, inst_id)

    proc_roll_partners: dict[str, dict[str, int]] = {}
    if use_rollup:
        roll_edges = edges_for_inst_processed(edges, inst_id, year, rollup=True)
        proc_roll_partners = partner_map_from_edges(roll_edges, inst_id)

    json_partners = partners_from_json(payload, inst_id)

    result.add(
        "Processed",
        f"collaboration_edges_full.csv (year={year})",
        f"{len(proc_partners)} partners",
        "n/a",
    )
    if use_rollup:
        result.add(
            "Processed (all-years rollup)",
            "collaboration_edges_full.csv (sum years)",
            f"{len(proc_roll_partners)} partners",
            "n/a",
        )
    result.add(
        "Export JSON",
        str(json_path.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        f"{len(json_partners)} partners in payload edges",
        "n/a",
    )

    compare_set = proc_roll_partners if use_rollup else proc_partners
    only_proc = set(compare_set) - set(json_partners)
    only_json = set(json_partners) - set(compare_set)
    common = set(compare_set) & set(json_partners)

    weight_mismatches = [
        p
        for p in common
        if not _values_match(compare_set[p]["weight"], json_partners[p]["weight"])
    ]

    # Export caps global edges (MAX_EDGES_FULL=300); missing partners in JSON is expected.
    export_cap_note = (
        "09_export_payloads.build_edges() keeps top 300 edges network-wide; "
        "institutes with many partners will show fewer in JSON than in processed CSV."
    )
    set_match = not weight_mismatches
    result.add(
        "Match summary",
        "processed vs JSON (common partners)",
        f"common={len(common)}, only_processed={len(only_proc)}, only_json={len(only_json)}, weight_mismatches={len(weight_mismatches)}",
        "yes" if set_match else "no",
        export_cap_note if only_proc else "",
    )

    if only_proc:
        sample = sorted(only_proc, key=lambda p: -compare_set[p]["weight"])[:5]
        result.warn(
            f"In processed only ({len(only_proc)} total, export edge cap): "
            f"{[id_to_name.get(p, p) for p in sample]} ..."
        )
    if only_json:
        sample = sorted(only_json, key=lambda p: -json_partners[p]["weight"])[:5]
        result.warn(f"In JSON only (top): {[id_to_name.get(p, p) for p in sample]}")
    if weight_mismatches[:3]:
        for p in weight_mismatches[:3]:
            result.warn(
                f"Weight mismatch {id_to_name.get(p, p)}: processed={compare_set[p]['weight']} json={json_partners[p]['weight']}"
            )

    # Top 5 partner table rows
    top = sorted(compare_set.items(), key=lambda x: -x[1]["weight"])[:5]
    for pid, metrics in top:
        jm = json_partners.get(pid)
        jw = jm["weight"] if jm else None
        match = "yes" if jm and _values_match(metrics["weight"], jw) else ("no" if jm else "missing")
        result.add(
            "Partner",
            id_to_name.get(pid, pid),
            f"proc weight={metrics['weight']}, json weight={jw}",
            match,
        )

    result.add("UI-only", "india_network.js", "partner sidebar sorted by weight desc", "n/a")
    return result


def format_table(result: VerifyResult) -> str:
    lines = [
        f"# Graph 5 verify: {result.query}",
        "",
        f"Institute: {result.institute_name or '-'} (`{result.institute_id or '-'}`)",
        f"Year: {result.year if result.year is not None else 'all'} | Field: {result.field or '-'}",
        f"**Result: {'PASS' if result.passed else 'FAIL'}**",
        "",
        "## Edge / data chain",
        "",
        result.edge_chain,
        "",
    ]
    if result.warnings:
        lines.append("## Warnings")
        lines.append("")
        for w in result.warnings:
            lines.append(f"- {w}")
        lines.append("")

    lines.extend(
        [
            "## Trace table",
            "",
            "| Layer | Source file | Value | Match? |",
            "|-------|-------------|-------|--------|",
        ]
    )
    for row in result.rows:
        val = str(row.value).replace("|", "\\|")
        note = f" ({row.note})" if row.note else ""
        lines.append(f"| {row.layer} | {row.source_file} | {val}{note} | {row.match} |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trace Graph 5 dashboard values to backend CSV/JSON sources.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/india_network/verify_graph5_display.py --pair "IIT Kanpur" "IIT Indore" --year 2024
  python scripts/india_network/verify_graph5_display.py --institute "IIT Kanpur" --year 2024 --field partners
  python scripts/india_network/verify_graph5_display.py --institute "IIT Kanpur" --field funding
  python scripts/india_network/verify_graph5_display.py --institute "IIT Hyderabad" --field funding
  python scripts/india_network/verify_graph5_display.py --institute "IIT Palakkad" --field patents
        """,
    )
    parser.add_argument("--pair", nargs=2, metavar=("A", "B"), help="Two institute names or UUIDs")
    parser.add_argument("--institute", help="Institute name or institution_id UUID")
    parser.add_argument(
        "--field",
        choices=["partners", "funding", "patents", "nirf_rank", "scimago", "node", "edge"],
        help="Scalar group or partners list",
    )
    parser.add_argument("--year", type=int, default=None, help="Year slice for edges/partners (e.g. 2024)")
    parser.add_argument("--variant", choices=["full", "overview"], default="full", help="JSON payload variant")
    parser.add_argument("--json-out", type=Path, help="Write machine-readable JSON result")
    args = parser.parse_args()

    if args.pair and args.institute:
        raise SystemExit("Use --pair OR --institute, not both")
    if not args.pair and not args.institute:
        parser.error("Provide --pair or --institute")
    if args.institute and not args.field:
        parser.error("--institute requires --field")

    ctx = load_context()
    if ctx["master"] is None:
        raise SystemExit(f"Missing {PROCESSED_PATHS['master']}")

    if args.pair:
        result = verify_pair(ctx, args.pair[0], args.pair[1], args.year, args.variant)
    else:
        field = args.field or "funding"
        if field == "edge":
            raise SystemExit("Use --pair for edge checks, not --institute --field edge")
        result = verify_institute_field(ctx, args.institute, field, args.year, args.variant)

    text = format_table(result)
    sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "query": result.query,
            "institute_id": result.institute_id,
            "institute_name": result.institute_name,
            "year": result.year,
            "field": result.field,
            "passed": result.passed,
            "warnings": result.warnings,
            "edge_chain": result.edge_chain,
            "rows": [r.__dict__ for r in result.rows],
        }
        args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote {args.json_out}")

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
