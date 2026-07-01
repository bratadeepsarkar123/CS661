#!/usr/bin/env python3
"""Build works_raw.parquet from cached OpenAlex JSON pages (no API calls).

Memory modes (INDIA_ETL_MEMORY in .env or --memory flag):
  low  (default) — SQLite dedup + stream parquet + slim authorships (~0.5-0.8 GB)
  high (overnight) — in-memory dedup + larger batches; still streams (no batch list)

Safe to re-run while 05 fetch is running. Cache on disk is never modified.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import CACHE_DIR, PROCESSED_DIR, etl_batch_size, etl_memory_mode  # noqa: E402

WORKS_RAW = PROCESSED_DIR / "works_raw.parquet"
WORKS_RAW_TMP = PROCESSED_DIR / "works_raw.parquet.tmp"
MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
DEDUP_DB = PROCESSED_DIR / "_works_assemble_dedup.sqlite"

YEAR_PAGE_RE = re.compile(r"^works_(?P<inst>I\d+)_y(?P<year>\d{4})_page_(?P<page>\d+)\.json$")
LEGACY_PAGE_RE = re.compile(r"^works_(?P<inst>I\d+)_page_(?P<page>\d+)\.json$")

LOW_BATCH = 300
HIGH_BATCH = 1200
SQLITE_COMMIT_EVERY = 500


def inst_from_name(name: str) -> str | None:
    m = YEAR_PAGE_RE.match(name) or LEGACY_PAGE_RE.match(name)
    return m.group("inst") if m else None


def work_id_short(wid: str | None) -> str | None:
    if not wid:
        return None
    return wid.rsplit("/", 1)[-1] if wid.startswith("http") else wid


def slim_authorships_json(raw_authorships) -> str:
    """Minimal structure for filters.py (institution id + country_code only)."""
    slim = []
    for auth in raw_authorships or []:
        if not isinstance(auth, dict):
            continue
        insts = []
        for inst in auth.get("institutions") or []:
            if not isinstance(inst, dict):
                continue
            iid = inst.get("id")
            if iid:
                insts.append({"id": iid, "country_code": inst.get("country_code")})
        if insts:
            slim.append({"institutions": insts})
    return json.dumps(slim, separators=(",", ":"))


def slim_row(raw: dict, inst_id: str) -> dict:
    return {
        "id": raw.get("id"),
        "publication_year": raw.get("publication_year"),
        "cited_by_count": raw.get("cited_by_count") or 0,
        "type": raw.get("type"),
        "authorships": slim_authorships_json(raw.get("authorships")),
        "_source_institution": inst_id,
    }


class Deduper:
    def __init__(self, mode: str) -> None:
        self.mode = mode
        self._mem: set[str] = set()
        self._conn: sqlite3.Connection | None = None
        if mode == "low":
            PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(DEDUP_DB)
            self._conn.execute("CREATE TABLE IF NOT EXISTS seen (work_id TEXT PRIMARY KEY)")
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._pending = 0
        else:
            self._pending = 0

    def is_new(self, wid: str) -> bool:
        if self.mode == "high":
            if wid in self._mem:
                return False
            self._mem.add(wid)
            return True
        assert self._conn is not None
        cur = self._conn.execute("SELECT 1 FROM seen WHERE work_id=?", (wid,))
        if cur.fetchone():
            return False
        self._conn.execute("INSERT INTO seen VALUES (?)", (wid,))
        self._pending += 1
        if self._pending >= SQLITE_COMMIT_EVERY:
            self._conn.commit()
            self._pending = 0
        return True

    def close(self) -> None:
        if self._conn is not None:
            self._conn.commit()
            self._conn.close()


def write_batch(writer, batch: list[dict], schema_holder: list) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    df = pd.DataFrame(batch)
    table = pa.Table.from_pandas(df, preserve_index=False)
    if not schema_holder:
        schema_holder.append(table.schema)
        writer[0] = pq.ParquetWriter(WORKS_RAW_TMP, table.schema, compression="snappy")
    writer[0].write_table(table)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilot-top", type=int, default=0)
    parser.add_argument(
        "--memory",
        choices=("low", "high"),
        default=None,
        help="Override INDIA_ETL_MEMORY (low=laptop, high=overnight)",
    )
    args = parser.parse_args()
    mode = args.memory or etl_memory_mode()
    batch_size = etl_batch_size(mode) if mode == "high" else LOW_BATCH

    allowed: set[str] | None = None
    if args.pilot_top > 0 or MASTER_PATH.exists():
        master = pd.read_csv(MASTER_PATH)
        if args.pilot_top > 0:
            master = master[master["tier"] == "premier"].nlargest(args.pilot_top, "total_works")
        allowed = set(master["openalex_id"].astype(str))

    if mode == "low" and DEDUP_DB.exists():
        DEDUP_DB.unlink()

    deduper = Deduper(mode)
    batch: list[dict] = []
    files_read = 0
    total_rows = 0
    insts_seen: set[str] = set()

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    if WORKS_RAW_TMP.exists():
        WORKS_RAW_TMP.unlink()
    # Keep existing works_raw.parquet until a new file is fully written (safe to kill mid-run).

    import pyarrow.parquet as pq

    pq_writer: list = [None]
    schema_holder: list = []

    paths = sorted(CACHE_DIR.glob("works_*.json"), key=lambda p: p.stat().st_mtime)
    print(f"Mode={mode} batch={batch_size} | scanning {len(paths):,} cache files")

    try:
        for path in paths:
            inst_id = inst_from_name(path.name)
            if not inst_id or (allowed is not None and inst_id not in allowed):
                continue
            try:
                with path.open(encoding="utf-8") as fh:
                    data = json.load(fh)
            except (json.JSONDecodeError, OSError):
                continue
            files_read += 1
            for w in data.get("results") or []:
                wid = work_id_short(w.get("id"))
                if not wid or not deduper.is_new(wid):
                    continue
                batch.append(slim_row(w, inst_id))
                insts_seen.add(inst_id)
                if len(batch) >= batch_size:
                    write_batch(pq_writer, batch, schema_holder)
                    total_rows += len(batch)
                    batch = []
                    if files_read % 200 == 0:
                        print(f"  ... {total_rows:,} works from {files_read:,} files", flush=True)

        if batch:
            write_batch(pq_writer, batch, schema_holder)
            total_rows += len(batch)
    finally:
        if pq_writer[0] is not None:
            pq_writer[0].close()
        deduper.close()

    if total_rows == 0:
        if WORKS_RAW_TMP.exists():
            WORKS_RAW_TMP.unlink()
        raise SystemExit(f"No works assembled from {CACHE_DIR} (read {files_read} files)")

    WORKS_RAW_TMP.replace(WORKS_RAW)
    print(f"Assembled {total_rows:,} unique works from {files_read:,} cache files")
    print(f"  Institutions: {len(insts_seen)} | mode={mode}")
    print(f"  Wrote -> {WORKS_RAW}")


if __name__ == "__main__":
    main()
