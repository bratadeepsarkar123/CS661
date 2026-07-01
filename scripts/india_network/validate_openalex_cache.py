#!/usr/bin/env python3
"""Read-only OpenAlex cache validation — no API calls, no re-downloads."""
from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import importlib

_fetch = importlib.import_module("05_fetch_openalex_works")
from config import CACHE_DIR, PROCESSED_DIR, YEAR_MIN, YEAR_RANGE_JSON  # noqa: E402

LOG_DIR = PROCESSED_DIR.parent / "logs"
REPORT_MD = LOG_DIR / "cache_validation_report.md"
REPORT_JSON = LOG_DIR / "cache_validation_report.json"


def load_year_max() -> int:
    if YEAR_RANGE_JSON.exists():
        return int(json.loads(YEAR_RANGE_JSON.read_text(encoding="utf-8"))["year_max"])
    return 2024


def validate_institution(inst_id: str, name: str, year_max: int) -> dict:
    issues: list[str] = []
    years_ok = 0
    years_partial = 0
    missing_pages: list[str] = []

    for year in range(YEAR_MIN, year_max + 1):
        p1 = _fetch.cache_path(inst_id, year, 1)
        if not p1.exists():
            issues.append(f"{year}: no page 1")
            continue
        tp = _fetch.total_pages_for_year(inst_id, year)
        if tp <= 0:
            issues.append(f"{year}: bad meta on page 1")
            continue
        if _fetch.year_is_cached(inst_id, year):
            years_ok += 1
        else:
            years_partial += 1
            for page in range(1, tp + 1):
                if not _fetch.cache_path(inst_id, year, page).exists():
                    missing_pages.append(f"{year}/page_{page}")

    status = "COMPLETE" if years_ok == (year_max - YEAR_MIN + 1) else (
        "PARTIAL" if years_ok or years_partial else "EMPTY"
    )
    return {
        "institution_id": inst_id,
        "name": name,
        "status": status,
        "years_complete": years_ok,
        "years_partial": years_partial,
        "missing_pages": missing_pages[:20],
        "missing_page_count": len(missing_pages),
        "issues": issues[:10],
    }


def sample_json_integrity(n: int = 12) -> list[str]:
    files = list(CACHE_DIR.glob("works_*.json"))
    if not files:
        return ["No cache files"]
    sample = random.sample(files, min(n, len(files)))
    problems: list[str] = []
    for path in sample:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            results = data.get("results") or []
            if not results and data.get("meta", {}).get("count", 0) > 0:
                problems.append(f"{path.name}: empty results but meta.count>0")
                continue
            w = results[0]
            if results and not w.get("id"):
                problems.append(f"{path.name}: missing work id")
            auth = (w.get("authorships") or [{}])[0] if results else {}
            insts = auth.get("institutions") or []
            if results and not insts:
                pass  # some works lack affiliations — OK
        except (json.JSONDecodeError, OSError) as exc:
            problems.append(f"{path.name}: {exc}")
    return problems or ["OK — sampled files parse cleanly"]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--full-master", action="store_true", help="Validate all 120 master rows")
    parser.add_argument("--pilot-top", type=int, default=0)
    args = parser.parse_args()

    master = pd.read_csv(PROCESSED_DIR / "institution_master.csv")
    if args.pilot_top > 0:
        master = master[master["tier"] == "premier"].nlargest(args.pilot_top, "total_works")
    elif not args.full_master:
        master = master[master["tier"] == "premier"].nlargest(30, "total_works")

    year_max = load_year_max()
    rows = []
    for _, r in master.iterrows():
        rows.append(validate_institution(str(r["openalex_id"]), r["canonical_name"], year_max))

    complete = sum(1 for x in rows if x["status"] == "COMPLETE")
    partial = sum(1 for x in rows if x["status"] == "PARTIAL")
    integrity = sample_json_integrity()

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "institutions_checked": len(rows),
        "complete": complete,
        "partial": partial,
        "empty": len(rows) - complete - partial,
        "cache_files": len(list(CACHE_DIR.glob("works_*.json"))),
        "json_sample": integrity,
        "institutions": rows,
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = [
        "# OpenAlex cache validation (read-only)",
        "",
        f"Generated: {summary['generated_at']}",
        f"Institutions: {complete}/{len(rows)} COMPLETE, {partial} PARTIAL",
        f"Cache files: {summary['cache_files']:,}",
        "",
        "## JSON sample check",
        *[f"- {x}" for x in integrity],
        "",
        "## Per institution",
        "| Status | Name | Years OK | Missing pages |",
        "|--------|------|----------|---------------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['status']} | {row['name'][:40]} | {row['years_complete']}/{year_max - YEAR_MIN + 1} | {row['missing_page_count']} |"
        )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Complete: {complete}/{len(rows)} | Partial: {partial} | Cache files: {summary['cache_files']:,}")
    print(f"Report -> {REPORT_MD}")
    if partial > 0 or complete < len(rows):
        print("Some institutions need fetch resume (missing pages only — no full re-download).")


if __name__ == "__main__":
    main()
