#!/usr/bin/env python3
"""Monitor OpenAlex works cache growth; detect stalls and API-limit stops.

Examples:
  python watch_openalex_fetch.py              # one snapshot
  python watch_openalex_fetch.py --loop 300   # every 5 minutes overnight
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import CACHE_DIR, PROCESSED_DIR, YEAR_MIN, YEAR_RANGE_JSON  # noqa: E402

LOG_DIR = PROCESSED_DIR.parent / "logs"
LOG_PATH = LOG_DIR / "openalex_watch.log"
STATUS_PATH = LOG_DIR / "openalex_watch_status.json"

YEAR_PAGE_RE = re.compile(r"^works_(?P<inst>I\d+)_y(?P<year>\d{4})_page_(?P<page>\d+)\.json$")


def load_year_max() -> int:
    if YEAR_RANGE_JSON.exists():
        return int(json.loads(YEAR_RANGE_JSON.read_text(encoding="utf-8"))["year_max"])
    return 2024


def snapshot() -> dict:
    files = list(CACHE_DIR.glob("works_*.json"))
    count = len(files)
    latest_mtime = max((f.stat().st_mtime for f in files), default=0.0)
    latest_name = ""
    if files:
        latest = max(files, key=lambda f: f.stat().st_mtime)
        latest_name = latest.name

    inst_years: dict[str, set[int]] = {}
    for f in files:
        m = YEAR_PAGE_RE.match(f.name)
        if not m:
            continue
        inst_years.setdefault(m.group("inst"), set()).add(int(m.group("year")))

    year_max = load_year_max()
    expected_years = year_max - YEAR_MIN + 1
    complete_insts = sum(1 for years in inst_years.values() if len(years) >= expected_years)

    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "cache_files": count,
        "latest_file": latest_name,
        "latest_mtime_utc": datetime.fromtimestamp(latest_mtime, tz=timezone.utc).isoformat()
        if latest_mtime
        else None,
        "institutions_with_any_cache": len(inst_years),
        "institutions_all_years_cached": complete_insts,
        "year_span": f"{YEAR_MIN}-{year_max}",
    }


def classify(prev: dict | None, curr: dict, stall_minutes: float) -> str:
    if prev is None:
        return "started"
    if curr["cache_files"] > prev["cache_files"]:
        delta = curr["cache_files"] - prev["cache_files"]
        return f"working (+{delta} files)"
    if not curr["latest_mtime_utc"]:
        return "no_cache"
    latest = datetime.fromisoformat(curr["latest_mtime_utc"])
    age_min = (datetime.now(timezone.utc) - latest).total_seconds() / 60.0
    if age_min >= stall_minutes:
        return f"STALLED ({age_min:.0f} min since last file — likely API limit or crashed process)"
    return f"idle ({age_min:.0f} min since last file — may be between institutions)"


def log_line(text: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}"
    print(line)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--loop", type=int, default=0, metavar="SECONDS", help="Repeat every N seconds (0 = once)")
    parser.add_argument("--stall-minutes", type=float, default=15.0, help="Minutes without new files = stalled")
    args = parser.parse_args()

    prev: dict | None = None
    if STATUS_PATH.exists():
        try:
            prev = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            prev = None

    while True:
        curr = snapshot()
        status = classify(prev, curr, args.stall_minutes)
        log_line(
            f"{status} | files={curr['cache_files']} | insts={curr['institutions_with_any_cache']} "
            f"| all-years={curr['institutions_all_years_cached']} | latest={curr['latest_file']}"
        )
        STATUS_PATH.write_text(json.dumps(curr, indent=2), encoding="utf-8")
        prev = curr
        if args.loop <= 0:
            break
        time.sleep(args.loop)


if __name__ == "__main__":
    main()
