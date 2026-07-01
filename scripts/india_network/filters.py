"""Work-level filters for domestic collaboration pipeline."""
from __future__ import annotations

from typing import Any

import numpy as np

from config import WORK_TYPES, YEAR_MIN, YEAR_MAX


def openalex_id(value: str | None) -> str | None:
    if not value:
        return None
    return value.rsplit("/", 1)[-1]


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, list):
        return value
    return [value]


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if hasattr(value, "to_dict"):
        return value.to_dict()
    return {}


def institutions_on_work(authorships: Any) -> list[dict[str, Any]]:
    insts: list[dict[str, Any]] = []
    for auth in _as_list(authorships):
        auth = _as_dict(auth)
        for inst in _as_list(auth.get("institutions")):
            inst = _as_dict(inst)
            if inst.get("id"):
                insts.append(inst)
    return insts


def is_domestic_work(authorships: list[dict[str, Any]]) -> bool:
    """W3: every listed institution must be IN; exclude unaffiliated authors."""
    insts = institutions_on_work(authorships)
    if not insts:
        return False
    return all(inst.get("country_code") == "IN" for inst in insts)


def master_institution_ids_on_work(
    authorships: list[dict[str, Any]],
    master_openalex_ids: set[str],
) -> set[str]:
    ids: set[str] = set()
    for inst in institutions_on_work(authorships):
        oid = openalex_id(inst.get("id"))
        if oid and oid in master_openalex_ids:
            ids.add(oid)
    return ids


def work_passes_filters(
    work: dict[str, Any],
    master_openalex_ids: set[str],
    year_min: int = YEAR_MIN,
    year_max: int = YEAR_MAX,
) -> bool:
    """Apply W1–W5."""
    year = work.get("publication_year")
    if year is None or year < year_min or year > year_max:
        return False

    work_type = work.get("type")
    if work_type and work_type not in WORK_TYPES:
        return False

    authorships = work.get("authorships")
    if authorships is None:
        authorships = []
    if not is_domestic_work(authorships):
        return False

    if len(master_institution_ids_on_work(authorships, master_openalex_ids)) < 2:
        return False

    return True
