#!/usr/bin/env python3
"""Export overview + full JSON payloads for the India network panel (prototype or final)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import (  # noqa: E402
    CORRIDOR_CITIES,
    EDGE_WEIGHT_MIN_FULL,
    EDGE_WEIGHT_MIN_OVERVIEW,
    FULL_NODE_CAP,
    HUB_COUNT,
    MAX_EDGES_FULL,
    MAX_EDGES_OVERVIEW,
    PROCESSED_DIR,
    PUBLIC_DIR,
    YEAR_MIN,
)

QUALITY_PATH = PROCESSED_DIR / "institution_quality_static.csv"
FUNDING_PATH = PROCESSED_DIR / "institution_funding.csv"
FUNDING_BY_YEAR_PATH = PROCESSED_DIR / "institution_funding_by_year.csv"
PATENTS_PATH = PROCESSED_DIR / "institution_patents.csv"
PATENTS_BY_YEAR_PATH = PROCESSED_DIR / "institution_patents_by_year.csv"
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
EDGES_PATH = PROCESSED_DIR / "collaboration_edges_full.csv"
HUBS_PATH = PROCESSED_DIR / "hub_flags.csv"
TRIADS_PATH = PROCESSED_DIR / "collaboration_triads.parquet"
DOMESTIC_WORKS_PATH = PROCESSED_DIR / "domestic_works.parquet"
SCIMAGEO_YEAR = 2019
from nirf_utils import (  # noqa: E402
    load_nirf_rankings_all_years,
    lookup_nirf_rank_for_institute,
    slider_year_to_funding_academic_year,
    slider_year_to_nirf_ranking_year,
    slider_year_to_patent_calendar_year,
)

LOSERS_PATH = PROCESSED_DIR / "nirf_match_losers.csv"

# Institutes sharing identical NIRF funding rows (informational — not join bugs).
# BHU campus family resolved by per-institute_id funding rows (01d); Panjab/NIT split at 3dp.
FUNDING_DUPLICATE_CLUSTER_BY_NAME: dict[str, str] = {}

OVERVIEW_NODE_KEYS = frozenset(
    {
        "id",
        "openalex_id",
        "name",
        "tier",
        "city",
        "state",
        "lat",
        "lon",
        "total_works",
        "is_hub",
        "color",
        "radius",
        "scimago_pct",
        "scimago_year",
        "nirf_rank",
        "nirf_ranking_category",
    }
)


def _tier_color(tier: str) -> str:
    return "#3b82f6" if tier == "premier" else "#a855f7"


def _node_radius(total_works: float) -> float:
    return max(4.0, min(18.0, math.sqrt(max(float(total_works or 0), 1)) * 0.04))


def load_quality() -> pd.DataFrame:
    if not QUALITY_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(QUALITY_PATH)


def edges_for_year(edges: pd.DataFrame, year: int | None) -> pd.DataFrame:
    if year is None:
        return edges.groupby(["inst_a", "inst_b", "openalex_a", "openalex_b"], as_index=False).agg(
            weight=("weight", "sum"), citation_weight=("citation_weight", "sum")
        )
    return edges[edges["year"] == year].copy()


def corridor_label(city: str | None) -> str | None:
    if not city or pd.isna(city):
        return None
    c = str(city).lower()
    for name, cities in CORRIDOR_CITIES.items():
        if any(x in c for x in cities):
            return name
    return None


def load_funding() -> pd.DataFrame:
    if not FUNDING_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(FUNDING_PATH)


def load_funding_by_year(slider_year: int | None) -> pd.DataFrame:
    """Return institution funding rows for the NIRF academic year mapped from slider year."""
    if not FUNDING_BY_YEAR_PATH.exists():
        df = load_funding()
        return df
    df = pd.read_csv(FUNDING_BY_YEAR_PATH)
    if df.empty or "academic_year" not in df.columns:
        return load_funding()
    target = slider_year_to_funding_academic_year(slider_year)
    sub = df[df["academic_year"].astype(str) == str(target)].copy()
    if sub.empty:
        return load_funding()
    return sub


def load_patents() -> pd.DataFrame:
    if not PATENTS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(PATENTS_PATH)


def load_patents_by_year(slider_year: int | None) -> pd.DataFrame:
    if not PATENTS_BY_YEAR_PATH.exists():
        df = load_patents()
        return df
    df = pd.read_csv(PATENTS_BY_YEAR_PATH)
    if df.empty or "patent_calendar_year" not in df.columns:
        return load_patents()
    target = slider_year_to_patent_calendar_year(slider_year)
    sub = df[df["patent_calendar_year"] == target].copy()
    if sub.empty:
        return load_patents()
    return sub


def load_nirf_losers() -> dict[str, str]:
    """canonical_name -> reason from nirf_match_losers.csv."""
    if not LOSERS_PATH.exists():
        return {}
    df = pd.read_csv(LOSERS_PATH)
    return {str(r["canonical_name"]): str(r["reason"]) for _, r in df.iterrows()}


def _nirf_match_status(name: str, nirf_id, losers: dict[str, str]) -> str:
    if pd.notna(nirf_id):
        return "matched"
    if name in losers:
        reason = losers[name]
        if reason == "id_blocked_by_uniqueness":
            return "blocked"
        return "unranked"
    return "unranked"


def _funding_status(name: str, funding_cr: float | None, nirf_rank, nirf_match_status: str) -> str:
    if nirf_match_status in ("unranked", "blocked"):
        return "unranked"
    if funding_cr is not None:
        return "reported"
    if pd.notna(nirf_rank):
        return "unavailable"
    return "unavailable"


def _patent_status(name: str, prow: pd.Series | None, nirf_match_status: str) -> str:
    if nirf_match_status in ("unranked", "blocked"):
        return "unranked"
    if prow is not None and pd.notna(prow.get("patent_status")):
        return str(prow["patent_status"])
    if prow is not None and pd.notna(prow.get("patents_published")):
        return "reported"
    return "unavailable"


def build_coverage_meta(nodes: list[dict], losers: dict[str, str]) -> dict:
    nirf_matched = sum(1 for n in nodes if n.get("nirf_match_status") == "matched")
    funding_reported = sum(1 for n in nodes if n.get("research_funding_cr") is not None)
    patents_reported = sum(1 for n in nodes if n.get("patents_published") is not None)
    return {
        "nirf_matched": nirf_matched,
        "nirf_losers": len(losers),
        "loser_names": sorted(losers.keys()),
        "funding_reported": funding_reported,
        "patents_reported": patents_reported,
        "institutions_total": len(nodes),
        "patent_ceiling_note": "Innovation PDF only; see data/logs/patent_coverage_gaps.json",
    }


def build_nodes(
    master: pd.DataFrame,
    hubs: pd.DataFrame,
    quality: pd.DataFrame,
    slider_year: int | None = None,
) -> list[dict]:
    hub_map = hubs.set_index("institution_id")["is_hub"].to_dict() if not hubs.empty else {}
    qmap = quality.set_index("institution_id") if not quality.empty and "institution_id" in quality.columns else None
    fmap = load_funding_by_year(slider_year)
    fmap = fmap.set_index("institution_id") if not fmap.empty and "institution_id" in fmap.columns else None
    pmap = load_patents_by_year(slider_year)
    pmap = pmap.set_index("institution_id") if not pmap.empty and "institution_id" in pmap.columns else None
    losers = load_nirf_losers()
    mapped_funding_year = slider_year_to_funding_academic_year(slider_year)
    mapped_patent_year = slider_year_to_patent_calendar_year(slider_year)
    mapped_ranking_year = slider_year_to_nirf_ranking_year(slider_year)
    nirf_all_years = load_nirf_rankings_all_years()

    nodes = []
    for _, r in master.iterrows():
        if pd.isna(r.get("latitude")) or pd.isna(r.get("longitude")):
            continue
        qrow = qmap.loc[r["institution_id"]] if qmap is not None and r["institution_id"] in qmap.index else None
        frow = fmap.loc[r["institution_id"]] if fmap is not None and r["institution_id"] in fmap.index else None
        prow = pmap.loc[r["institution_id"]] if pmap is not None and r["institution_id"] in pmap.index else None
        pct = None
        if qrow is not None and pd.notna(qrow.get("scimago_pct")):
            pct = float(qrow["scimago_pct"])
        funding_cr = None
        expenditure_cr = None
        sponsored_projects = None
        funding_year = None
        if frow is not None:
            if pd.notna(frow.get("research_funding_cr")):
                funding_cr = float(frow["research_funding_cr"])
            if pd.notna(frow.get("total_expenditure_cr")):
                expenditure_cr = float(frow["total_expenditure_cr"])
            if pd.notna(frow.get("sponsored_projects")):
                sponsored_projects = int(frow["sponsored_projects"])
            if funding_cr is not None or sponsored_projects is not None:
                if pd.notna(frow.get("funding_academic_year")):
                    funding_year = str(frow["funding_academic_year"])
                elif pd.notna(frow.get("academic_year")):
                    funding_year = str(frow["academic_year"])
                elif mapped_funding_year:
                    funding_year = mapped_funding_year
        patents_published = None
        patents_granted = None
        patent_year = None
        if prow is not None:
            if pd.notna(prow.get("patents_published")):
                patents_published = int(prow["patents_published"])
            if pd.notna(prow.get("patents_granted")):
                patents_granted = int(prow["patents_granted"])
            if pd.notna(prow.get("patent_calendar_year")):
                patent_year = int(prow["patent_calendar_year"])
        name = r["canonical_name"]
        nirf_id = r.get("nirf_institute_id")
        match_status = _nirf_match_status(name, nirf_id, losers)
        nirf_rank_val = int(r["nirf_rank"]) if pd.notna(r.get("nirf_rank")) else None
        nirf_cat_val = str(r["nirf_ranking_category"]) if pd.notna(r.get("nirf_ranking_category")) else None
        nirf_rank_season = int(r["nirf_year"]) if pd.notna(r.get("nirf_year")) else None
        if slider_year is not None and match_status == "matched":
            rank_lookup, cat_lookup, season_lookup = lookup_nirf_rank_for_institute(
                nirf_institute_id=str(nirf_id) if pd.notna(nirf_id) else None,
                canonical_name=name,
                ranking_year=mapped_ranking_year,
                nirf_all_years=nirf_all_years,
                inst_type=r.get("inst_type"),
                city=r.get("city"),
                state=r.get("state"),
            )
            if rank_lookup is not None:
                nirf_rank_val = rank_lookup
                nirf_cat_val = cat_lookup
                nirf_rank_season = season_lookup
        dup_cluster = FUNDING_DUPLICATE_CLUSTER_BY_NAME.get(name)
        node: dict = {
            "id": r["institution_id"],
            "openalex_id": r["openalex_id"],
            "name": name,
            "tier": r["tier"],
            "city": r.get("city"),
            "state": r.get("state"),
            "lat": float(r["latitude"]),
            "lon": float(r["longitude"]),
            "total_works": int(r.get("total_works") or 0),
            "is_hub": bool(hub_map.get(r["institution_id"], r.get("is_hub", False))),
            "color": _tier_color(str(r["tier"])),
            "radius": _node_radius(r.get("total_works")),
            "scimago_pct": pct,
            "scimago_year": SCIMAGEO_YEAR if pct is not None else None,
            "nirf_rank": nirf_rank_val,
            "nirf_ranking_category": nirf_cat_val,
            "nirf_ranking_season": nirf_rank_season,
            "nirf_rank_year_mismatch": (
                slider_year is not None
                and nirf_rank_season is not None
                and int(nirf_rank_season) != int(slider_year)
            ),
            "nirf_match_status": match_status,
            "research_funding_cr": funding_cr,
            "total_expenditure_cr": expenditure_cr,
            "sponsored_projects": sponsored_projects,
            "funding_academic_year": funding_year,
            "funding_status": _funding_status(name, funding_cr, r.get("nirf_rank"), match_status),
            "funding_year_mismatch": (
                slider_year is not None
                and funding_cr is not None
                and funding_year is not None
                and str(funding_year) != mapped_funding_year
            ),
            "patents_published": patents_published,
            "patents_granted": patents_granted,
            "patent_calendar_year": patent_year,
            "patent_status": _patent_status(name, prow, match_status),
            "patent_year_mismatch": (
                slider_year is not None
                and patents_published is not None
                and patent_year is not None
                and int(patent_year) != int(slider_year)
            ),
        }
        if dup_cluster:
            node["funding_duplicate_cluster"] = dup_cluster
        nodes.append(node)
    return nodes


def node_for_overview(node: dict) -> dict:
    """Strip funding/patent detail fields from overview payload (details-on-demand)."""
    return {k: node[k] for k in OVERVIEW_NODE_KEYS if k in node}


def build_edges(edge_df: pd.DataFrame, node_ids: set[str], min_weight: int, max_edges: int) -> list[dict]:
    edge_df = edge_df[(edge_df["weight"] >= min_weight) & edge_df["inst_a"].isin(node_ids) & edge_df["inst_b"].isin(node_ids)]
    edge_df = edge_df.sort_values("weight", ascending=False).head(max_edges)
    return [
        {
            "source": row["inst_a"],
            "target": row["inst_b"],
            "weight": int(row["weight"]),
            "citation_weight": int(row.get("citation_weight") or 0),
        }
        for _, row in edge_df.iterrows()
    ]


def tier_summary(nodes: list[dict]) -> list[dict]:
    rows = []
    for tier in ["premier", "state_affiliated"]:
        tier_nodes = [n for n in nodes if n["tier"] == tier]
        if not tier_nodes:
            continue
        works = [n["total_works"] for n in tier_nodes]
        pcts = [n["scimago_pct"] for n in tier_nodes if n.get("scimago_pct") is not None]
        fundings = [n["research_funding_cr"] for n in tier_nodes if n.get("research_funding_cr") is not None]
        rows.append(
            {
                "tier": tier,
                "institution_count": len(tier_nodes),
                "mean_total_works": round(sum(works) / len(works), 1),
                "mean_scimago_pct": round(sum(pcts) / len(pcts), 2) if pcts else None,
                "mean_research_funding_cr": round(sum(fundings) / len(fundings), 1) if fundings else None,
            }
        )
    return rows


def _sort_nodes_for_display(nodes: list[dict]) -> list[dict]:
    """Hubs first, then by total_works desc — deterministic overview/full selection."""
    return sorted(
        nodes,
        key=lambda n: (not n.get("is_hub", False), -int(n.get("total_works") or 0), str(n.get("name", ""))),
    )


def build_triads_payload(
    master: pd.DataFrame,
    year: int | None,
    node_ids: set[str],
) -> dict[str, list[list]]:
    """Per-focus partner-pair triads for 3+ institution papers (full payload only)."""
    cap = 15
    if TRIADS_PATH.exists():
        tri = pd.read_parquet(TRIADS_PATH)
        ykey = -1 if year is None else int(year)
        tri = tri[tri["year"] == ykey]
        tri = tri[
            tri["focus_id"].isin(node_ids)
            & tri["partner_a"].isin(node_ids)
            & tri["partner_b"].isin(node_ids)
        ]
        out: dict[str, list[list]] = {}
        for focus, grp in tri.groupby("focus_id"):
            sorted_triads = sorted(
                [[str(r.partner_a), str(r.partner_b), int(r.weight)] for r in grp.itertuples()],
                key=lambda x: -x[2],
            )
            out[str(focus)] = sorted_triads[:cap]
        return out

    if not DOMESTIC_WORKS_PATH.exists():
        return {}

    from triad_builder import build_triads_from_works, load_domestic_works, oa_map_from_master  # noqa: WPS433

    domestic = load_domestic_works(DOMESTIC_WORKS_PATH)
    oa_map = oa_map_from_master(master)
    triads_raw = build_triads_from_works(domestic, oa_map, year=year, node_ids=node_ids)
    out = {}
    for focus, rows in triads_raw.items():
        out[focus] = rows[:cap]
    return out


def hub_annotations(nodes: list[dict]) -> list[str]:
    labels = []
    for hub in [n for n in nodes if n.get("is_hub")][:HUB_COUNT]:
        corr = corridor_label(hub.get("city"))
        if corr and corr.title() not in labels:
            labels.append(f"{corr.title()} Hub")
    return labels[:3]


def temporal_metrics_note(slider_year: int | None) -> str:
    if slider_year is None:
        return (
            "All-years rollup for collaboration edges; NIRF funding/patents/ranks use latest available "
            f"seasons (funding {slider_year_to_funding_academic_year(None)}, patents "
            f"{slider_year_to_patent_calendar_year(None)}, ranks {slider_year_to_nirf_ranking_year(None)})."
        )
    fy = slider_year_to_funding_academic_year(slider_year)
    py = slider_year_to_patent_calendar_year(slider_year)
    ry = slider_year_to_nirf_ranking_year(slider_year)
    parts = [
        f"Collaboration edges: calendar year {slider_year}.",
        f"Sponsored research: NIRF academic year {fy}.",
        f"Patents: calendar year {py}.",
        f"NIRF rank: {ry} ranking season (nearest available to slider).",
    ]
    if slider_year < 2016:
        parts.append("Rankings before 2016 not published on nirfindia.org (404).")
    if slider_year < 2017:
        parts.append("Funding before 2017-18 uses earliest scraped academic year.")
    if slider_year > 2022:
        parts.append("Patent counts for 2023+ use 2022 — Innovation PDF only on 2024 CDN.")
    if slider_year > 2023:
        parts.append("Funding for 2024 uses 2022-23 — no 2023-24 academic year in PDFs.")
    return " ".join(parts)


def export_year(year: int | None, master: pd.DataFrame, edges: pd.DataFrame, hubs: pd.DataFrame, quality: pd.DataFrame) -> None:
    year_edges = edges_for_year(edges, year)
    nodes = _sort_nodes_for_display(build_nodes(master, hubs, quality, slider_year=year))
    hub_ids = {n["id"] for n in nodes if n.get("is_hub")}

    overview_candidates = [n for n in nodes if n.get("is_hub") or n["total_works"] >= 5000]
    overview_nodes = overview_candidates[:45]
    overview_node_ids = {n["id"] for n in overview_nodes}
    overview_hub_ids = hub_ids & overview_node_ids

    overview_edges = build_edges(
        year_edges[year_edges["inst_a"].isin(overview_hub_ids) & year_edges["inst_b"].isin(overview_hub_ids)],
        overview_node_ids,
        EDGE_WEIGHT_MIN_OVERVIEW,
        MAX_EDGES_OVERVIEW,
    )

    full_nodes = nodes[:FULL_NODE_CAP]
    full_node_ids = {n["id"] for n in full_nodes}
    full_edges = build_edges(year_edges, full_node_ids, EDGE_WEIGHT_MIN_FULL, MAX_EDGES_FULL)

    label = "all_years" if year is None else str(year)
    out_dir = PUBLIC_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    losers = load_nirf_losers()
    coverage = build_coverage_meta(nodes, losers)
    overview = {
        "year": year if year is not None else "all",
        "quality_year": SCIMAGEO_YEAR,
        "quality_note": "SCImago research impact % snapshot (2019 data); static across year slider",
        "funding_academic_year_mapped": slider_year_to_funding_academic_year(year),
        "patent_calendar_year_mapped": slider_year_to_patent_calendar_year(year),
        "nirf_ranking_season_mapped": slider_year_to_nirf_ranking_year(year),
        "temporal_metrics_note": temporal_metrics_note(year),
        "coverage": coverage,
        "nodes": [node_for_overview(n) for n in overview_nodes],
        "edges": overview_edges,
        "tier_summary": tier_summary(nodes),
        "annotations": hub_annotations(nodes),
    }
    full = {
        **overview,
        "nodes": full_nodes,
        "edges": full_edges,
        "triads": build_triads_payload(master, year, full_node_ids),
        "tier_panels": {
            "premier": next((t for t in tier_summary(nodes) if t["tier"] == "premier"), {}),
            "state_affiliated": next((t for t in tier_summary(nodes) if t["tier"] == "state_affiliated"), {}),
        },
    }

    overview_path = out_dir / f"{label}_overview.json"
    full_path = out_dir / f"{label}_full.json"
    overview_path.write_text(json.dumps(overview, indent=2), encoding="utf-8")
    full_path.write_text(json.dumps(full, indent=2), encoding="utf-8")
    print(f"  {label}: nodes={len(overview['nodes'])}/{len(full['nodes'])} edges={len(overview_edges)}/{len(full_edges)}")
    print(f"    -> {overview_path.name}, {full_path.name}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2024, help="Year slice (default 2024); use 0 for all-years rollup")
    args = parser.parse_args()

    for path in [MASTER_PATH, EDGES_PATH]:
        if not path.exists():
            raise FileNotFoundError(path)

    master = pd.read_csv(MASTER_PATH)
    edges = pd.read_csv(EDGES_PATH)
    hubs = pd.read_csv(HUBS_PATH) if HUBS_PATH.exists() else pd.DataFrame()
    quality = load_quality()

    year = None if args.year == 0 else args.year
    print(f"Exporting payloads to {PUBLIC_DIR}")
    export_year(year, master, edges, hubs, quality)


if __name__ == "__main__":
    main()
