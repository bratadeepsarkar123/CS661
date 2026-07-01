"""Shared OpenAlex HTTP helpers (API key from .env, never hardcoded)."""
from __future__ import annotations

import time

import requests

from config import OPENALEX_BASE, OPENALEX_USER_AGENT, with_openalex_key


def openalex_get(
    path: str,
    params: dict | None = None,
    *,
    timeout: float = 90,
    max_retries: int = 5,
) -> requests.Response:
    """GET an OpenAlex endpoint with api_key injected from environment."""
    url = f"{OPENALEX_BASE}/{path.lstrip('/')}"
    headers = {"User-Agent": OPENALEX_USER_AGENT}
    base_params = with_openalex_key(dict(params or {}))

    for attempt in range(max_retries):
        resp = requests.get(url, params=base_params, headers=headers, timeout=timeout)
        if resp.status_code in (401, 403):
            raise SystemExit(
                "OpenAlex rejected the API key (HTTP "
                f"{resp.status_code}). Check OPENALEX_API_KEY in your local .env file."
            )
        if resp.status_code == 429:
            body = {}
            try:
                body = resp.json()
            except Exception:
                pass
            remaining = body.get("dailyRemainingUsd", body.get("creditsRemaining"))
            if remaining == 0:
                raise SystemExit(
                    "OpenAlex daily budget exhausted. Wait until midnight UTC, then re-run "
                    "(cached pages are skipped automatically)."
                )
            wait = int(body.get("retryAfter", 60))
            time.sleep(min(wait, 180))
            continue
        return resp

    return resp
