#!/usr/bin/env python3
"""Dedupe works, apply W1–W5, build collaboration_edges + hub flags."""
from __future__ import annotations

import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import (  # noqa: E402
    CORRIDOR_CITIES,
    EDGE_WEIGHT_MIN_FULL,
    HUB_COUNT,
    PROCESSED_DIR,
)
from filters import master_institution_ids_on_work, openalex_id, work_passes_filters  # noqa: E402

WORKS_RAW = PROCESSED_DIR / "works_raw.parquet"
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
DOMESTIC_WORKS_PATH = PROCESSED_DIR / "domestic_works.parquet"
EDGES_PATH = PROCESSED_DIR / "collaboration_edges_full.csv"
HUBS_PATH = PROCESSED_DIR / "hub_flags.csv"


def _parse_authorships(raw):
    if raw is None:
        return []
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return []
    return raw


def load_works_jsonish(df: pd.DataFrame) -> list[dict]:
    works: list[dict] = []
    for row in df.to_dict(orient="records"):
        wid = row.get("id") or row.get("id", "")
        if isinstance(wid, str) and wid.startswith("http"):
            wid = wid.rsplit("/", 1)[-1]
        works.append(
            {
                "id": wid,
                "publication_year": row.get("publication_year"),
                "cited_by_count": row.get("cited_by_count") or 0,
                "type": row.get("type"),
                "authorships": _parse_authorships(row.get("authorships")),
            }
        )
    return works


def build_edges(domestic_df: pd.DataFrame, id_map: dict[str, str]) -> pd.DataFrame:
    """id_map: openalex_id -> institution_id"""
    pair_counts: dict[tuple[str, str, int], dict] = defaultdict(lambda: {"weight": 0, "citation_weight": 0})

    for _, row in domestic_df.iterrows():
        year = int(row["year"])
        cited = int(row.get("cited_by_count") or 0)
        inst_ids = row["institution_ids"]
        for a, b in itertools.combinations(sorted(inst_ids), 2):
            key = (a, b, year)
            pair_counts[key]["weight"] += 1
            pair_counts[key]["citation_weight"] += cited

    rows = []
    for (oa_a, oa_b, year), metrics in pair_counts.items():
        if metrics["weight"] < EDGE_WEIGHT_MIN_FULL:
            continue
        rows.append(
            {
                "inst_a": id_map[oa_a],
                "inst_b": id_map[oa_b],
                "openalex_a": oa_a,
                "openalex_b": oa_b,
                "year": year,
                "weight": metrics["weight"],
                "citation_weight": metrics["citation_weight"],
            }
        )
    return pd.DataFrame(rows)


def compute_hubs(edges: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:
    degree: dict[str, int] = defaultdict(int)
    for _, e in edges.iterrows():
        degree[e["inst_a"]] += e["weight"]
        degree[e["inst_b"]] += e["weight"]

    hub_df = master[["institution_id", "openalex_id", "city"]].copy()
    hub_df["degree"] = hub_df["institution_id"].map(lambda i: degree.get(i, 0))
    hub_df["is_hub"] = False

    top = hub_df.nlargest(HUB_COUNT, "degree")
    hub_df.loc[hub_df["institution_id"].isin(top["institution_id"]), "is_hub"] = True

    def city_in_corridor(city: str, keywords: list[str]) -> bool:
        c = (city or "").lower()
        return any(k in c for k in keywords)

    for _name, keywords in CORRIDOR_CITIES.items():
        corridor = hub_df[hub_df["city"].apply(lambda c: city_in_corridor(c, keywords))]
        if corridor.empty:
            continue
        best = corridor.nlargest(1, "degree").iloc[0]["institution_id"]
        hub_df.loc[hub_df["institution_id"] == best, "is_hub"] = True

    return hub_df[["institution_id", "openalex_id", "degree", "is_hub"]]


def main() -> None:
    if not WORKS_RAW.exists():
        raise FileNotFoundError(f"Run 05_fetch_openalex_works.py first: {WORKS_RAW}")
    master = pd.read_csv(MASTER_PATH)
    oa_to_inst = dict(zip(master["openalex_id"], master["institution_id"]))
    master_oa_ids = set(master["openalex_id"])

    raw = pd.read_parquet(WORKS_RAW)
    if "id" in raw.columns:
        raw = raw.drop_duplicates(subset=["id"])
    elif "id" in raw.columns.astype(str):
        pass

    works = load_works_jsonish(raw)
    domestic_rows = []
    for w in works:
        if not work_passes_filters(w, master_oa_ids):
            continue
        inst_oa_ids = sorted(master_institution_ids_on_work(w["authorships"], master_oa_ids))
        domestic_rows.append(
            {
                "work_id": w["id"],
                "year": w["publication_year"],
                "cited_by_count": w["cited_by_count"],
                "institution_ids": inst_oa_ids,
            }
        )

    domestic_df = pd.DataFrame(domestic_rows)
    domestic_df.to_parquet(DOMESTIC_WORKS_PATH, index=False)
    print(f"Domestic works: {len(domestic_df)} -> {DOMESTIC_WORKS_PATH}")

    edges = build_edges(domestic_df, oa_to_inst)
    edges.to_csv(EDGES_PATH, index=False)
    print(f"Edges (weight>={EDGE_WEIGHT_MIN_FULL}): {len(edges)} -> {EDGES_PATH}")

    hubs = compute_hubs(edges, master)
    hubs.to_csv(HUBS_PATH, index=False)
    hub_count = hubs["is_hub"].sum()
    print(f"Hubs marked: {hub_count} -> {HUBS_PATH}")


if __name__ == "__main__":
    main()
