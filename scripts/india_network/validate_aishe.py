#!/usr/bin/env python3
"""Validate optional AISHE universities xlsx and emit coverage summary JSON."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
LOGS = ROOT / "data" / "logs"
AISHE_PATH = RAW / "aishe_universities.xlsx"
OUT_PATH = LOGS / "aishe_coverage_summary.json"


def run_validate() -> dict:
    LOGS.mkdir(parents=True, exist_ok=True)
    if not AISHE_PATH.exists():
        payload = {
            "present": False,
            "path": str(AISHE_PATH),
            "note": "optional — tier narrative uses NSTMIS/AISHE report aggregates; pipeline runs without it",
        }
        OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload

    df = pd.read_excel(AISHE_PATH)
    state_col = next((c for c in df.columns if "state" in str(c).lower()), None)
    type_col = next(
        (c for c in df.columns if "type" in str(c).lower() or "category" in str(c).lower()),
        None,
    )
    state_counts: dict[str, int] = {}
    type_counts: dict[str, int] = {}
    if state_col:
        state_counts = (
            df[state_col].astype(str).value_counts().head(10).astype(int).to_dict()
        )
    if type_col:
        type_counts = df[type_col].astype(str).value_counts().head(10).astype(int).to_dict()

    payload = {
        "present": True,
        "path": str(AISHE_PATH),
        "row_count": int(len(df)),
        "columns": [str(c) for c in df.columns.tolist()],
        "state_counts_top10": state_counts,
        "type_counts_top10": type_counts,
        "note": "not joined to institution_master — enrollment join is future work",
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> None:
    payload = run_validate()
    print(OUT_PATH)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
