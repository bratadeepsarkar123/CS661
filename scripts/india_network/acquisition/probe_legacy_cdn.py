#!/usr/bin/env python3
"""Probe legacy nirfpdfcdn/{year}/{IRyy-...}.pdf URLs from 2016-2017 ranking pages."""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acquisition._common import CACHE_DIR, DEFAULT_SLEEP, log_attempt, session, utc_now_iso

LEGACY_PDF_RE = re.compile(
    r"https?://(?:www\.)?nirfindia\.org/nirfpdfcdn/(\d{4})/(IR\d{2}-[^\"']+\.pdf)",
    re.I,
)


def extract_legacy_pdfs_from_cache(year: int) -> list[str]:
    urls: set[str] = set()
    for path in CACHE_DIR.glob(f"wayback_*Rankings_{year}_*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        for m in LEGACY_PDF_RE.finditer(text):
            season, fname = m.group(1), m.group(2)
            urls.add(f"https://www.nirfindia.org/nirfpdfcdn/{season}/{fname}")
    return sorted(urls)


def probe_urls(urls: list[str], limit: int = 30) -> list[dict]:
    sess = session()
    results: list[dict] = []
    for url in urls[:limit]:
        cache = CACHE_DIR / f"legacy_cdn_{url.replace('://', '_').replace('/', '_')[:100]}.json"
        if cache.exists():
            results.append(json.loads(cache.read_text(encoding="utf-8")))
            continue
        time.sleep(DEFAULT_SLEEP)
        try:
            resp = sess.get(url, timeout=60)
            meta = {"url": url, "status": resp.status_code, "bytes": len(resp.content)}
        except requests.RequestException as exc:
            meta = {"url": url, "error": str(exc)}
        cache.write_text(json.dumps(meta), encoding="utf-8")
        results.append(meta)
    return results


def main() -> None:
    print(f"Legacy CDN probe — {utc_now_iso()}")
    for year in (2016, 2017):
        urls = extract_legacy_pdfs_from_cache(year)
        print(f"  {year}: {len(urls)} PDF URLs in wayback HTML")
        results = probe_urls(urls, limit=40)
        ok = sum(1 for r in results if r.get("status") == 200 and r.get("bytes", 0) > 1000)
        log_attempt(
            method="Legacy PDF CDN",
            source=f"nirfpdfcdn/{year}/IR{str(year)[-2:]}-*.pdf",
            script="probe_legacy_cdn.py",
            status="success" if ok > 5 else ("partial" if ok else "fail"),
            rows_recovered=ok,
            detail=f"urls_found={len(urls)} probed={len(results)} ok={ok}",
            why_failed="" if ok else "Legacy flat PDF path 404 or not in wayback HTML",
            next_retry="Parse funding tables from legacy PDFs if Overall contains sponsored research",
            force=True,
        )
        out = CACHE_DIR / f"legacy_cdn_probe_{year}.json"
        out.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
