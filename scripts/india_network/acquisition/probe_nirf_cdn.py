#!/usr/bin/env python3
"""Probe nirfpdfcdn/{2015..2024}/pdf for Innovation, Overall, Engineering PDF availability.

Uses sample institute IDs from nirf_rankings_2024.csv + known IDs.
Logs per-season/category/institute HTTP status to acquisition JSON.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from acquisition._common import (  # noqa: E402
    CACHE_DIR,
    DEFAULT_SLEEP,
    RAW_DIR,
    log_attempt,
    session,
    utc_now_iso,
)
from nirf_utils import candidate_pdf_urls, innovation_pdf_url, nirf_pdf_base  # noqa: E402

DEFAULT_SEASONS = list(range(2015, 2026))
DEFAULT_CATEGORIES = ["Innovation", "Overall", "Engineering"]
SAMPLE_IDS = [
    "IR-O-U-0306",  # IIT Bombay Overall
    "IR-E-U-0306",  # IIT Bombay Engineering
    "IR-O-U-0456",  # IIT Madras Overall
    "IR-O-U-0220",  # Delhi University
    "IR-O-U-0108",  # JNU
    "IR-O-U-0376",  # GNDU
    "IR-E-U-0899",  # IIT Dharwad
    "IR-O-N-0045",  # NIT Trichy (typical NIT)
]


def load_sample_ids(limit: int = 12) -> list[str]:
    path = RAW_DIR / "nirf_rankings_2024.csv"
    ids = list(SAMPLE_IDS)
    if path.exists():
        df = pd.read_csv(path)
        for iid in df["institute_id"].dropna().astype(str).unique()[:limit]:
            if iid not in ids:
                ids.append(iid)
    return ids[:limit]


def probe_season(season: int, institute_ids: list[str], categories: list[str]) -> dict:
    sess = session()
    results: dict = {"season": season, "base": nirf_pdf_base(season), "probes": []}
    hits = 0
    for iid in institute_ids:
        for cat in categories:
            if cat == "Innovation":
                url = innovation_pdf_url(iid, season=season)
                urls = [(cat, url)]
            else:
                urls = [(c, u) for c, u in candidate_pdf_urls(iid, [cat], season=season)]
            for cat_name, url in urls:
                cache_name = f"cdn_probe_{season}_{cat_name}_{iid}.meta.json"
                meta_path = CACHE_DIR / cache_name
                if meta_path.exists():
                    meta = json.loads(meta_path.read_text(encoding="utf-8"))
                    results["probes"].append(meta)
                    if meta.get("status") == 200 and meta.get("content_length", 0) > 500:
                        hits += 1
                    continue
                time.sleep(DEFAULT_SLEEP)
                try:
                    resp = sess.get(url, timeout=45, allow_redirects=True)
                    clen = len(resp.content)
                    meta = {
                        "institute_id": iid,
                        "category": cat_name,
                        "url": url,
                        "status": resp.status_code,
                        "content_length": clen,
                    }
                    meta_path.write_text(json.dumps(meta), encoding="utf-8")
                    results["probes"].append(meta)
                    if meta["status"] == 200 and meta["content_length"] > 500:
                        hits += 1
                except Exception as exc:  # noqa: BLE001
                    meta = {"institute_id": iid, "category": cat_name, "url": url, "error": str(exc)}
                    meta_path.write_text(json.dumps(meta), encoding="utf-8")
                    results["probes"].append(meta)
    results["hit_count"] = hits
    return results


def summarize_all(all_results: list[dict]) -> dict:
    by_season: dict[int, dict[str, int]] = {}
    for r in all_results:
        season = r["season"]
        by_season.setdefault(season, {})
        for p in r["probes"]:
            cat = p.get("category", "?")
            ok = p.get("status") == 200 and p.get("content_length", 0) > 500
            by_season[season][cat] = by_season[season].get(cat, 0) + (1 if ok else 0)
    return by_season


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe NIRF PDF CDN seasons")
    parser.add_argument("--seasons", type=str, default="2015-2024")
    parser.add_argument("--sample", type=int, default=12)
    args = parser.parse_args()
    if "-" in args.seasons:
        lo, hi = args.seasons.split("-", 1)
        seasons = list(range(int(lo), int(hi) + 1))
    else:
        seasons = [int(s.strip()) for s in args.seasons.split(",") if s.strip().isdigit()]

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    ids = load_sample_ids(args.sample)
    print(f"CDN probe — {utc_now_iso()} — {len(ids)} sample IDs, seasons {seasons[0]}–{seasons[-1]}")

    all_results: list[dict] = []
    for season in seasons:
        print(f"  Season {season} ...")
        res = probe_season(season, ids, DEFAULT_CATEGORIES)
        all_results.append(res)
        print(f"    hits={res['hit_count']}/{len(res['probes'])}")

    summary = summarize_all(all_results)
    out_path = CACHE_DIR / "cdn_probe_summary.json"
    out_path.write_text(json.dumps({"summary": summary, "details": all_results}, indent=2), encoding="utf-8")

    # Log per season
    for season, cats in summary.items():
        total_hits = sum(cats.values())
        status = "success" if total_hits > 0 else "fail"
        log_attempt(
            method="PDF CDN probe",
            source=f"nirfpdfcdn/{season}/pdf/",
            script="probe_nirf_cdn.py",
            status=status if total_hits > 3 else ("partial" if total_hits else "fail"),
            rows_recovered=total_hits,
            detail=json.dumps(cats),
            why_failed="" if total_hits else "No PDFs >500B for sample IDs",
            next_retry="Expand sample IDs; GET full Innovation PDF for patent year columns",
            extra={"season": season},
        )

    log_attempt(
        method="PDF CDN probe",
        source="nirfpdfcdn aggregate",
        script="probe_nirf_cdn.py",
        status="partial" if any(summary.values()) else "fail",
        rows_recovered=sum(sum(c.values()) for c in summary.values()),
        detail=f"summary -> {out_path.name}",
        extra={"by_season": summary},
    )
    print(f"Summary -> {out_path}")


if __name__ == "__main__":
    main()
