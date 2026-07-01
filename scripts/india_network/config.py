"""Shared paths and thresholds for India Domestic HE Network ETL."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CACHE_DIR = DATA_DIR / "cache" / "openalex"
PROCESSED_DIR = DATA_DIR / "processed"
PUBLIC_DIR = PROJECT_ROOT / "public" / "india_network"

MANUAL_OVERRIDES_CSV = DATA_DIR / "manual_institution_overrides.csv"
YEAR_RANGE_JSON = PROCESSED_DIR / "year_range.json"

ENV_FILE = PROJECT_ROOT / ".env"

OPENALEX_BASE = "https://api.openalex.org"
OPENALEX_USER_AGENT = "CS661-IndiaNetwork/1.0 (mailto:bratadeeps24@iitk.ac.in)"


def _load_dotenv(path: Path) -> None:
    """Load KEY=VALUE lines from .env into os.environ (does not override existing)."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(ENV_FILE)


def get_openalex_api_key() -> str:
    key = os.environ.get("OPENALEX_API_KEY", "").strip()
    if key and key not in {"paste_your_key_here", "your_key_here"}:
        return key
    raise SystemExit(
        "OpenAlex API key missing.\n\n"
        "  1. Copy .env.example → .env  (project root: CS661/.env)\n"
        "  2. Open .env and set:  OPENALEX_API_KEY=your_key_from_openalex.org/settings/api\n"
        "  3. Verify:  python scripts/india_network/check_openalex_key.py\n"
        "  4. Re-run your fetch script\n\n"
        ".env is gitignored — do not commit it or paste the key into chat."
    )


def with_openalex_key(params: dict) -> dict:
    out = dict(params)
    out["api_key"] = get_openalex_api_key()
    return out


def openalex_key_configured() -> bool:
    try:
        get_openalex_api_key()
        return True
    except SystemExit:
        return False


def etl_memory_mode() -> str:
    """low = laptop-friendly (~0.5-0.8 GB for 05b). high = larger batches if RAM allows."""
    mode = os.environ.get("INDIA_ETL_MEMORY", "low").strip().lower()
    return "high" if mode == "high" else "low"


def etl_ram_cap_mb() -> int:
    """Soft cap for ETL on 12 GB laptops. Default 3584 (~30%) when RESOURCE_CAP=active."""
    default = "3584" if resource_cap_active() else "4608"
    try:
        return int(os.environ.get("ETL_RAM_CAP_MB", default))
    except ValueError:
        return int(default)


def resource_cap_active() -> bool:
    """User at desk: fetch + light export only; no incremental 05b/06."""
    return os.environ.get("RESOURCE_CAP", "").strip().lower() in {"active", "1", "true", "yes"}


def openalex_fetch_delay_sec() -> float:
    if resource_cap_active():
        return float(os.environ.get("OPENALEX_FETCH_DELAY", "0.35"))
    return float(os.environ.get("OPENALEX_FETCH_DELAY", "0.12"))


def etl_batch_size(memory_mode: str) -> int:
    cap = etl_ram_cap_mb()
    if resource_cap_active() or (memory_mode != "high" and cap <= 4096):
        return 200
    if memory_mode != "high" and cap <= 5120:
        return 300
    if cap <= 7168:
        return 800
    return 1200


def is_overnight_etl() -> bool:
    return etl_memory_mode() == "high"

YEAR_MIN = 2015
# Overwritten by 00_detect_year_range.py → year_range.json
YEAR_MAX = 2024

WORK_TYPES = {"article", "review", "book-chapter"}
WORK_SELECT = "id,publication_year,cited_by_count,authorships,type"

PREMIER_WORKS_MIN = 50
STATE_WORKS_MIN = 10
PREMIER_CAP = 60
STATE_CAP = 60

EDGE_WEIGHT_MIN_FULL = 2
EDGE_WEIGHT_MIN_OVERVIEW = 5
MAX_EDGES_OVERVIEW = 40
MAX_EDGES_FULL = 200
HUB_COUNT = 12

CORRIDOR_CITIES = {
    "ncr": ["delhi", "new delhi", "noida", "gurgaon", "gurugram", "ghaziabad"],
    "bengaluru": ["bengaluru", "bangalore"],
    "mumbai": ["mumbai", "powai"],
    "chennai": ["chennai", "madras"],
}

SOURCE_URLS = {
    "nirf_rankings": "https://dataful.in/datasets/19320/",
    "nirf_patents": "https://dataful.in/datasets/20551/",
    "scimago_india": "https://www.scimagoir.com/rankings.php?ranking=Research&country=IND",
    "aishe_universities": "https://aikosh.indiaai.gov.in/home/datasets/details/all_universities_as_per_aishe_dashboard.html",
    "india_he_geo": "https://github.com/notrueindian/india-higher-ed-db",
}
