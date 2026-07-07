#!/usr/bin/env python3
"""Search data.gov.in for NIRF / HE funding / patent datasets; save downloads to data/raw/external/."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import quote

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acquisition._common import (  # noqa: E402
    CACHE_DIR,
    DEFAULT_SLEEP,
    EXTERNAL_DIR,
    cached_get,
    log_attempt,
    session,
    utc_now_iso,
)

SEARCH_QUERIES = [
    "NIRF",
    "National Institutional Ranking Framework",
    "MHRD university",
    "Ministry of Education higher education",
    "R&D expenditure university",
    "patents granted university India",
    "UGC research projects",
    "AISHE",
]

# data.gov.in CKAN API
CKAN_BASE = "https://data.gov.in/api/3/action/package_search"
METABASE_SEARCH = "https://data.gov.in/api/3/action/package_search"


def search_ckan(query: str, rows: int = 10) -> list[dict]:
    sess = session()
    params = {"q": query, "rows": rows}
    cache_name = f"datagov_search_{quote(query)[:60]}.json"
    path = CACHE_DIR / cache_name
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data.get("result", {}).get("results", [])
        except json.JSONDecodeError:
            pass
    time.sleep(DEFAULT_SLEEP)
    try:
        resp = sess.get(CKAN_BASE, params=params, timeout=90)
        resp.raise_for_status()
        data = resp.json()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return data.get("result", {}).get("results", [])
    except (requests.RequestException, json.JSONDecodeError):
        return []


def try_download_resource(resource: dict, pkg_title: str) -> int:
    url = resource.get("url") or ""
    fmt = (resource.get("format") or "").lower()
    if not url or fmt not in {"csv", "xlsx", "xls", "json", "zip"}:
        return 0
    if "nirf" not in url.lower() and "nirf" not in pkg_title.lower() and fmt == "csv":
        # Still save if query matched
        pass
    safe = re_sub(r"[^\w\-]+", "_", pkg_title[:40])
    ext = fmt if fmt in {"csv", "json", "zip"} else "bin"
    out = EXTERNAL_DIR / f"datagov_{safe}_{resource.get('id', 'res')[:8]}.{ext}"
    if out.exists() and out.stat().st_size > 100:
        return 0
    sess = session()
    time.sleep(DEFAULT_SLEEP)
    try:
        resp = sess.get(url, timeout=120)
        if resp.status_code == 200 and len(resp.content) > 100:
            out.write_bytes(resp.content)
            return len(resp.content)
    except requests.RequestException:
        pass
    return 0


def re_sub(pattern: str, repl: str, s: str) -> str:
    import re
    return re.sub(pattern, repl, s)


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe data.gov.in for NIRF-related datasets")
    parser.add_argument("--queries", type=str, default="", help="Comma-separated override queries")
    args = parser.parse_args()
    queries = [q.strip() for q in args.queries.split(",") if q.strip()] or SEARCH_QUERIES

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"data.gov.in probe — {utc_now_iso()}")

    all_packages: list[dict] = []
    bytes_saved = 0
    for query in queries:
        results = search_ckan(query)
        print(f"  '{query}': {len(results)} packages")
        for pkg in results:
            all_packages.append({"query": query, "title": pkg.get("title"), "name": pkg.get("name")})
            for res in pkg.get("resources") or []:
                nbytes = try_download_resource(res, pkg.get("title") or query)
                bytes_saved += nbytes
        log_attempt(
            method="data.gov.in search",
            source=f"data.gov.in?q={query}",
            script="probe_data_gov.py",
            status="partial" if results else "fail",
            rows_recovered=len(results),
            detail=f"{len(results)} CKAN packages",
            why_failed="" if results else "No packages in CKAN search",
            next_retry="Try manual portal browse; RTI for institute-level funding",
        )

    index_path = EXTERNAL_DIR / "datagov_search_index.json"
    index_path.write_text(json.dumps(all_packages, indent=2), encoding="utf-8")
    log_attempt(
        method="data.gov.in search",
        source="data.gov.in aggregate",
        script="probe_data_gov.py",
        status="partial" if all_packages else "fail",
        rows_recovered=len(all_packages),
        detail=f"index -> {index_path.name}, bytes_downloaded={bytes_saved}",
        why_failed="" if all_packages else "All queries returned 0",
        next_retry="Metadata saved for manual review; no institute-level NIRF CSV found automatically",
    )
    print(f"Index -> {index_path} ({len(all_packages)} packages, {bytes_saved} bytes downloaded)")


if __name__ == "__main__":
    main()
