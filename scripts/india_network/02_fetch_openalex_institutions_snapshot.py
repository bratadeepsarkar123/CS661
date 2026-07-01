#!/usr/bin/env python3
"""Download OpenAlex institutions snapshot (~177 MB gzip) and filter IN education."""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent))
from config import CACHE_DIR, PROCESSED_DIR  # noqa: E402

MANIFEST_URL = "https://openalex.s3.amazonaws.com/data/institutions/manifest"
OUT_PATH = PROCESSED_DIR / "openalex_institutions.parquet"
SNAPSHOT_DIR = CACHE_DIR / "institutions_snapshot"


def s3_to_https(s3_url: str) -> str:
    # s3://openalex/data/institutions/... -> https://openalex.s3.amazonaws.com/data/institutions/...
    path = s3_url.replace("s3://openalex/", "")
    return f"https://openalex.s3.amazonaws.com/{path}"


def download_parts() -> list[Path]:
    manifest = requests.get(MANIFEST_URL, timeout=60).json()
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    for entry in tqdm(manifest["entries"], desc="Downloading institution parts"):
        url = s3_to_https(entry["url"])
        name = entry["url"].split("/")[-2] + "_" + entry["url"].split("/")[-1]
        dest = SNAPSHOT_DIR / name
        if not dest.exists() or dest.stat().st_size == 0:
            resp = requests.get(url, timeout=300)
            resp.raise_for_status()
            dest.write_bytes(resp.content)
        paths.append(dest)
    return paths


def flatten_institution(row: dict) -> dict | None:
    if row.get("country_code") != "IN":
        return None
    if row.get("type") != "education":
        return None
    geo = row.get("geo") or {}
    ror = (row.get("ids") or {}).get("ror") or row.get("ror")
    if isinstance(ror, str) and ror.startswith("http"):
        ror = ror.rsplit("/", 1)[-1]
    return {
        "openalex_id": (row.get("id") or "").rsplit("/", 1)[-1],
        "display_name": row.get("display_name"),
        "ror_id": ror,
        "works_count": row.get("works_count") or 0,
        "cited_by_count": row.get("cited_by_count") or 0,
        "city": geo.get("city"),
        "region": geo.get("region"),
        "latitude": geo.get("latitude"),
        "longitude": geo.get("longitude"),
        "type": row.get("type"),
    }


def parse_gz_files(paths: list[Path]) -> pd.DataFrame:
    rows: list[dict] = []
    for path in tqdm(paths, desc="Parsing JSONL"):
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                flat = flatten_institution(json.loads(line))
                if flat:
                    rows.append(flat)
    return pd.DataFrame(rows)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    parts = download_parts()
    df = parse_gz_files(parts)
    df = df.drop_duplicates(subset=["openalex_id"])
    df.to_parquet(OUT_PATH, index=False)
    print(f"Wrote {len(df)} IN education institutions → {OUT_PATH}")


if __name__ == "__main__":
    main()
