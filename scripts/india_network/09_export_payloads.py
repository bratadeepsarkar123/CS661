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
    HUB_COUNT,
    MAX_EDGES_FULL,
    MAX_EDGES_OVERVIEW,
    PROCESSED_DIR,
    PUBLIC_DIR,
    YEAR_MIN,
)

QUALITY_PATH = PROCESSED_DIR / "institution_quality_static.csv"
FUNDING_PATH = PROCESSED_DIR / "institution_funding.csv"
PATENTS_PATH = PROCESSED_DIR / "institution_patents.csv"
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
EDGES_PATH = PROCESSED_DIR / "collaboration_edges_full.csv"
HUBS_PATH = PROCESSED_DIR / "hub_flags.csv"
SCIMAGEO_YEAR = 2019

UNRANKED_NIRF_NAMES = {
    "Guru Nanak Dev University",
    "Dr. Hari Singh Gour University",
    "Indian Association for the Cultivation of Science",
    "G.S. Science, Arts And Commerce College",
}

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


def load_patents() -> pd.DataFrame:
    if not PATENTS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(PATENTS_PATH)


def _funding_status(name: str, funding_cr: float | None, nirf_rank) -> str:
    if name in UNRANKED_NIRF_NAMES:
        return "unranked"
    if funding_cr is not None:
        return "reported"
    if pd.notna(nirf_rank):
        return "unavailable"
    return "unavailable"


def _patent_status(name: str, prow: pd.Series | None) -> str:
    if name in UNRANKED_NIRF_NAMES:
        return "unranked"
    if prow is not None and pd.notna(prow.get("patent_status")):
        return str(prow["patent_status"])
    if prow is not None and pd.notna(prow.get("patents_published")):
        return "reported"
    return "unavailable"


def build_nodes(master: pd.DataFrame, hubs: pd.DataFrame, quality: pd.DataFrame) -> list[dict]:
    hub_map = hubs.set_index("institution_id")["is_hub"].to_dict() if not hubs.empty else {}
    qmap = quality.set_index("institution_id") if not quality.empty and "institution_id" in quality.columns else None
    fmap = load_funding()
    fmap = fmap.set_index("institution_id") if not fmap.empty and "institution_id" in fmap.columns else None
    pmap = load_patents()
    pmap = pmap.set_index("institution_id") if not pmap.empty and "institution_id" in pmap.columns else None

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
            if pd.notna(frow.get("funding_academic_year")):
                funding_year = str(frow["funding_academic_year"])
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
        nodes.append(
            {
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
                "nirf_rank": int(r["nirf_rank"]) if pd.notna(r.get("nirf_rank")) else None,
                "research_funding_cr": funding_cr,
                "total_expenditure_cr": expenditure_cr,
                "sponsored_projects": sponsored_projects,
                "funding_academic_year": funding_year,
                "funding_status": _funding_status(name, funding_cr, r.get("nirf_rank")),
                "patents_published": patents_published,
                "patents_granted": patents_granted,
                "patent_calendar_year": patent_year,
                "patent_status": _patent_status(name, prow),
            }
        )
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


def hub_annotations(nodes: list[dict]) -> list[str]:
    labels = []
    for hub in [n for n in nodes if n.get("is_hub")][:HUB_COUNT]:
        corr = corridor_label(hub.get("city"))
        if corr and corr.title() not in labels:
            labels.append(f"{corr.title()} Hub")
    return labels[:3]


def export_year(year: int | None, master: pd.DataFrame, edges: pd.DataFrame, hubs: pd.DataFrame, quality: pd.DataFrame) -> None:
    year_edges = edges_for_year(edges, year)
    nodes = build_nodes(master, hubs, quality)
    node_ids = {n["id"] for n in nodes}
    hub_ids = {n["id"] for n in nodes if n.get("is_hub")}

    overview_edges = build_edges(
        year_edges[year_edges["inst_a"].isin(hub_ids) & year_edges["inst_b"].isin(hub_ids)],
        node_ids,
        EDGE_WEIGHT_MIN_OVERVIEW,
        MAX_EDGES_OVERVIEW,
    )
    full_edges = build_edges(year_edges, node_ids, EDGE_WEIGHT_MIN_FULL, MAX_EDGES_FULL)

    label = "all_years" if year is None else str(year)
    out_dir = PUBLIC_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    overview_node_source = [n for n in nodes if n.get("is_hub") or n["total_works"] >= 5000][:45]
    overview = {
        "year": year if year is not None else "all",
        "quality_year": SCIMAGEO_YEAR,
        "quality_note": "SCImago research impact % snapshot (2019 data); static across year slider",
        "nodes": [node_for_overview(n) for n in overview_node_source],
        "edges": overview_edges,
        "tier_summary": tier_summary(nodes),
        "annotations": hub_annotations(nodes),
    }
    full = {
        **overview,
        "nodes": nodes[:80],
        "edges": full_edges,
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

    label = "all_years" if year is None else str(year)
    if label != "2024":
        import shutil

        shutil.copy(PUBLIC_DIR / f"{label}_overview.json", PUBLIC_DIR / "2024_overview.json")
        shutil.copy(PUBLIC_DIR / f"{label}_full.json", PUBLIC_DIR / "2024_full.json")
        print("Panel copies -> 2024_overview.json, 2024_full.json")


if __name__ == "__main__":
    main()
