"""Shared utilities for NIRF acquisition scripts."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

# scripts/india_network/acquisition/_common.py -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
EXTERNAL_DIR = RAW_DIR / "external"
CACHE_DIR = DATA_DIR / "cache" / "nirf" / "acquisition"
LOG_JSON = DATA_DIR / "logs" / "nirf_acquisition_attempts.json"
LOG_MD = PROJECT_ROOT / "docs" / "NIRF_DATA_ACQUISITION_LOG.md"

USER_AGENT = "CS661-IndiaNetwork/1.0 (mailto:bratadeeps24@iitk.ac.in; NIRF-acquisition)"
DEFAULT_SLEEP = 1.25


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def ensure_dirs() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
    LOG_JSON.parent.mkdir(parents=True, exist_ok=True)


def load_attempts() -> list[dict[str, Any]]:
    ensure_dirs()
    if not LOG_JSON.exists():
        return []
    try:
        return json.loads(LOG_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_attempts(records: list[dict[str, Any]]) -> None:
    ensure_dirs()
    LOG_JSON.write_text(json.dumps(records, indent=2), encoding="utf-8")


def attempt_key(method: str, source: str, detail: str = "") -> str:
    return f"{method}|{source}|{detail}"


def already_logged(records: list[dict[str, Any]], key: str) -> bool:
    return any(r.get("key") == key and r.get("status") in {"success", "partial", "fail"} for r in records)


def log_attempt(
    *,
    method: str,
    source: str,
    script: str,
    status: str,
    rows_recovered: int = 0,
    detail: str = "",
    why_failed: str = "",
    next_retry: str = "",
    extra: dict[str, Any] | None = None,
    force: bool = False,
) -> dict[str, Any]:
    """Append one attempt to JSON log (skip duplicate keys unless force=True)."""
    ensure_dirs()
    records = load_attempts()
    key = attempt_key(method, source, detail)
    if not force and already_logged(records, key):
        for r in records:
            if r.get("key") == key:
                return r

    entry: dict[str, Any] = {
        "key": key,
        "timestamp": utc_now_iso(),
        "method": method,
        "source": source,
        "script": script,
        "status": status,
        "rows_recovered": rows_recovered,
        "detail": detail,
        "why_failed": why_failed,
        "next_retry_hint": next_retry,
    }
    if extra:
        entry["extra"] = extra
    records.append(entry)
    save_attempts(records)
    append_md_entry(entry)
    return entry


def append_md_entry(entry: dict[str, Any]) -> None:
    """Append a single row to the markdown acquisition log."""
    ensure_dirs()
    line = (
        f"| {entry['timestamp']} | {entry['method']} | "
        f"{entry['source']} | {entry['script']} | "
        f"{entry.get('rows_recovered', 0)} | {entry['status']} | "
        f"{entry.get('why_failed', '') or '—'} | {entry.get('next_retry_hint', '') or '—'} |\n"
    )
    if not LOG_MD.exists():
        header = (
            "# NIRF Data Acquisition Log\n\n"
            "**Internal team memory — not for dashboard.**\n\n"
            "Chronological audit of every method attempted to fill Graph 5 historical NIRF gaps.\n\n"
            "| Timestamp (UTC) | Method | Source/URL | Script | Rows | Status | Why failed | Next retry |\n"
            "|-----------------|--------|------------|--------|------|--------|------------|------------|\n"
        )
        LOG_MD.write_text(header + line, encoding="utf-8")
    else:
        with LOG_MD.open("a", encoding="utf-8") as fh:
            fh.write(line)


def cache_path(name: str) -> Path:
    ensure_dirs()
    return CACHE_DIR / name


def cached_get(
    sess: requests.Session,
    url: str,
    *,
    cache_name: str | None = None,
    sleep: float = DEFAULT_SLEEP,
    method: str = "GET",
    timeout: int = 60,
) -> tuple[requests.Response | None, Path | None]:
    """GET/HEAD with disk cache; returns (response, cache_file)."""
    ensure_dirs()
    fname = cache_name or url.replace("://", "_").replace("/", "_").replace("?", "_")[:200]
    path = CACHE_DIR / fname
    if path.exists() and path.stat().st_size > 0:
        if method.upper() == "HEAD":
            # Reconstruct minimal response metadata from sidecar
            meta_path = path.with_suffix(".meta.json")
            if meta_path.exists():
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                r = requests.Response()
                r.status_code = meta.get("status_code", 200)
                r.headers = meta.get("headers", {})
                return r, path
        else:
            r = requests.Response()
            r.status_code = 200
            r._content = path.read_bytes()  # noqa: SLF001
            r.headers["Content-Type"] = "text/html"
            return r, path

    time.sleep(sleep)
    try:
        if method.upper() == "HEAD":
            resp = sess.head(url, timeout=timeout, allow_redirects=True)
            meta = {"status_code": resp.status_code, "headers": dict(resp.headers)}
            path.write_text("", encoding="utf-8")
            path.with_suffix(".meta.json").write_text(json.dumps(meta), encoding="utf-8")
            return resp, path
        resp = sess.get(url, timeout=timeout)
        if resp.status_code == 200 and resp.content:
            path.write_bytes(resp.content)
        return resp, path
    except requests.RequestException:
        return None, path
