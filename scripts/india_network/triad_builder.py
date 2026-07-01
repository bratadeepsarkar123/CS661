"""Build per-focus triad partner-pair counts from domestic_works (3+ institution papers)."""
from __future__ import annotations

import itertools
from collections import defaultdict

import pandas as pd

TRIADS_PATH_SUFFIX = "collaboration_triads.parquet"


def build_triads_from_works(
    domestic_df: pd.DataFrame,
    oa_to_inst: dict[str, str],
    year: int | None = None,
    node_ids: set[str] | None = None,
) -> dict[str, list[list]]:
    """
    Return compact triads dict for JSON export:
      { focus_id: [[partner_a, partner_b, weight], ...], ... }
    Only partner-partner pairs where a paper includes focus + both partners.
    """
    if year is not None:
        domestic_df = domestic_df[domestic_df["year"] == year]

    counts: dict[str, dict[tuple[str, str], int]] = defaultdict(lambda: defaultdict(int))

    for inst_ids in domestic_df["institution_ids"]:
        mapped = []
        for oid in inst_ids:
            oid = str(oid)
            iid = oa_to_inst.get(oid)
            if iid:
                mapped.append(iid)
        unique = sorted(set(mapped))
        if len(unique) < 3:
            continue
        for focus in unique:
            if node_ids is not None and focus not in node_ids:
                continue
            others = [x for x in unique if x != focus]
            for a, b in itertools.combinations(others, 2):
                pair = (a, b) if a < b else (b, a)
                counts[focus][pair] += 1

    out: dict[str, list[list]] = {}
    for focus, pairs in counts.items():
        rows = [[a, b, int(w)] for (a, b), w in pairs.items() if w >= 1]
        if node_ids is not None:
            rows = [r for r in rows if r[0] in node_ids and r[1] in node_ids]
        if rows:
            rows.sort(key=lambda r: -r[2])
            out[focus] = rows
    return out


def load_domestic_works(path) -> pd.DataFrame:
    return pd.read_parquet(path)


def oa_map_from_master(master: pd.DataFrame) -> dict[str, str]:
    return dict(zip(master["openalex_id"].astype(str), master["institution_id"].astype(str)))
