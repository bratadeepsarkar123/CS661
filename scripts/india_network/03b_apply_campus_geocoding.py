#!/usr/bin/env python3
"""Apply campus-level lat/lon via manual overrides + Nominatim (fixes OpenAlex city centroids)."""
from __future__ import annotations

import re
import sys
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402

MASTER_PATH = PROCESSED_DIR / "institution_master.csv"
CACHE_PATH = PROCESSED_DIR / "campus_coordinates.csv"
ALL_OVERRIDES_PATH = PROCESSED_DIR / "campus_all_overrides.csv"
NOMINATIM = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "CS661-IndiaNetwork/1.0 (campus-geocode; bratadeeps24@iitk.ac.in)"

# openalex_id -> (latitude, longitude, source)
MANUAL_CAMPUS: dict[str, tuple[float, float, str]] = {
    # Mumbai corridor (4 stacked on city centroid)
    "I162827531": (19.133602, 72.915631, "campus_powai_iitb"),
    "I169877490": (19.076090, 72.851498, "campus_kalina_mumbai_uni"),
    "I11947397": (18.907124, 72.804964, "campus_colaba_tifr"),
    "I200207707": (19.048400, 72.925400, "campus_anushakti_hbni"),
    # Delhi NCR (6 stacked)
    "I68891433": (28.545500, 77.192600, "campus_iit_delhi"),
    "I63739035": (28.566700, 77.209000, "campus_aiims"),
    "I110166357": (28.682900, 77.206500, "campus_du_north"),
    "I152429107": (28.538300, 77.166000, "campus_jnu"),
    "I59475050": (28.561700, 77.280000, "campus_jamia"),
    "I863896202": (28.750600, 77.117200, "campus_dtu"),
    # Chennai (4 stacked)
    "I85461943": (13.054900, 80.283200, "campus_saveetha"),
    "I33585257": (13.011600, 80.236200, "campus_anna_univ"),
    "I215927": (13.066100, 80.271300, "campus_madras_univ"),
    "I1330855593": (13.186800, 80.097200, "campus_veltech"),
    # Kolkata (4 stacked)
    "I106542073": (22.576300, 88.363900, "campus_calcutta_univ"),
    "I6498739": (22.525800, 88.366200, "campus_isi_kolkata"),
    "I165998391": (22.538600, 88.396400, "campus_iacs"),
    "I157674215": (22.775700, 88.364700, "campus_presidency"),
    # Chandigarh / Punjab (3 stacked)
    "I45294948": (30.764000, 76.775400, "campus_pgi"),
    "I51452335": (30.763900, 76.788500, "campus_panjab_univ"),
    "I74319210": (30.516500, 76.659800, "campus_chitkara"),
    # IIT Madras / Palakkad (OpenAlex lat/lon swap bug)
    "I24676775": (12.991500, 80.233700, "campus_iit_madras"),
    "I4210113248": (10.790500, 76.654800, "campus_iit_palakkad"),
    # Bhubaneswar (2 stacked)
    "I99729588": (20.296100, 85.824800, "campus_iit_bbs"),
    "I67357951": (20.355800, 85.813800, "campus_kiit"),
    # Vellore (2 stacked)
    "I876193797": (12.969200, 79.155900, "campus_vit"),
    "I172917736": (12.924900, 79.133600, "campus_cmc_vellore"),
    # Manipal (2 stacked)
    "I164861460": (13.352000, 74.786900, "campus_manipal"),
    "I76414455": (13.355000, 74.786200, "campus_kmc_manipal"),
    # Jaipur (2 stacked)
    "I99552915": (26.891200, 75.815300, "campus_rajasthan_univ"),
    "I83205935": (26.872700, 75.818700, "campus_mnit_jaipur"),
    # Coimbatore region (4 stacked across 2 pins)
    "I81556334": (10.902400, 76.902400, "campus_amrita_coimbatore"),
    "I134900695": (11.004400, 76.930800, "campus_tnau"),
    "I111575329": (11.038900, 77.035600, "campus_bharathiar"),
    "I65220239": (11.028200, 77.014300, "campus_karpagam"),
    # Pune (2 stacked)
    "I878213199": (18.553500, 73.825700, "campus_sp_pune"),
    "I244572783": (18.536400, 73.831400, "campus_symbiosis"),
    # Dehradun (2 stacked)
    "I60054993": (30.316500, 78.032200, "campus_graphic_era"),
    "I5847235": (30.295800, 77.995600, "campus_upes"),
    # Trichy (2 stacked)
    "I122964287": (10.758700, 78.804400, "campus_nit_trichy"),
    "I4076070": (10.679500, 78.709400, "campus_bharathidasan"),
    # Visakhapatnam (2 stacked)
    "I100887729": (17.732400, 83.326500, "campus_andhra_univ"),
    "I885392262": (17.778000, 83.377800, "campus_gitam"),
    # Pondicherry (2 stacked)
    "I175691731": (12.027100, 79.858700, "campus_pondicherry"),
    "I61923386": (11.956400, 79.805700, "campus_jipmer"),
    # Hyderabad (2 stacked)
    "I8975392": (17.419000, 78.526000, "campus_osmania"),
    "I10874241": (17.498200, 78.391600, "campus_jntu_hyd"),
    # Mangalore / Surathkal (2 stacked)
    "I11880225": (13.015600, 74.796300, "campus_nitk_surathkal"),
    "I19008122": (12.876700, 74.835600, "campus_mangalore_univ"),
}


def _in_india(lat: float, lon: float) -> bool:
    return 6.0 <= lat <= 38.0 and 68.0 <= lon <= 98.0


def _normalize_india(lat: float, lon: float) -> tuple[float, float]:
    """Swap lat/lon when clearly reversed for India."""
    if _in_india(lat, lon):
        return lat, lon
    if _in_india(lon, lat):
        return lon, lat
    return lat, lon


def _query_nominatim(name: str, city: str | None, state: str | None) -> tuple[float, float, str] | None:
    parts = [str(name)]
    if city and pd.notna(city):
        parts.append(str(city))
    if state and pd.notna(state):
        parts.append(str(state))
    parts.append("India")
    q = ", ".join(parts)
    try:
        resp = requests.get(
            NOMINATIM,
            params={"q": q, "format": "json", "limit": 1},
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return None
        hit = data[0]
        lat, lon = _normalize_india(float(hit["lat"]), float(hit["lon"]))
        if not _in_india(lat, lon):
            return None
        return lat, lon, f"nominatim:{hit.get('osm_type', '')}/{hit.get('osm_id', '')}"
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return None


def _load_cache() -> dict[str, dict]:
    if not CACHE_PATH.exists():
        return {}
    df = pd.read_csv(CACHE_PATH)
    if df.empty or "openalex_id" not in df.columns:
        return {}
    return df.set_index("openalex_id")[["latitude", "longitude", "geo_source"]].to_dict("index")


def _load_all_overrides() -> dict[str, tuple[float, float, str]]:
    """Authoritative 120-row campus lockfile (run generate_campus_all_overrides.py)."""
    if not ALL_OVERRIDES_PATH.exists():
        return {}
    df = pd.read_csv(ALL_OVERRIDES_PATH)
    out: dict[str, tuple[float, float, str]] = {}
    for _, row in df.iterrows():
        out[str(row["openalex_id"])] = (
            float(row["latitude"]),
            float(row["longitude"]),
            str(row["geo_source"]),
        )
    return out


def main() -> None:
    if not MASTER_PATH.exists():
        raise FileNotFoundError(f"Run 03_build_institution_master.py first: {MASTER_PATH}")

    master = pd.read_csv(MASTER_PATH)
    cache_map = _load_cache()
    locked = _load_all_overrides()
    if locked:
        MANUAL_CAMPUS.update(locked)
    rows: list[dict] = []
    nominatim_calls = 0
    updated = 0

    for _, inst in master.iterrows():
        oid = str(inst["openalex_id"])
        name = inst["canonical_name"]
        city = inst.get("city")
        state = inst.get("state")
        old_lat, old_lon = float(inst["latitude"]), float(inst["longitude"])

        if oid in MANUAL_CAMPUS:
            lat, lon, src = MANUAL_CAMPUS[oid]
        elif oid in cache_map and pd.notna(cache_map[oid].get("latitude")):
            lat = float(cache_map[oid]["latitude"])
            lon = float(cache_map[oid]["longitude"])
            src = str(cache_map[oid]["geo_source"])
        else:
            hit = _query_nominatim(name, city, state)
            nominatim_calls += 1
            time.sleep(1.05)
            if hit:
                lat, lon, src = hit
            else:
                lat, lon = _normalize_india(old_lat, old_lon)
                src = "openalex_normalized" if _in_india(lat, lon) else "openalex_unverified"

        lat, lon = _normalize_india(lat, lon)
        if abs(lat - old_lat) > 0.01 or abs(lon - old_lon) > 0.01:
            updated += 1

        rows.append(
            {
                "openalex_id": oid,
                "latitude": lat,
                "longitude": lon,
                "geo_source": src,
            }
        )

    geo = pd.DataFrame(rows)
    geo.to_csv(CACHE_PATH, index=False)

    audit = master[["openalex_id", "canonical_name"]].merge(geo, on="openalex_id", how="left")
    audit.to_csv(PROCESSED_DIR / "campus_coordinates_audit.csv", index=False)

    master = master.drop(columns=[c for c in ("latitude", "longitude", "geo_source") if c in master.columns])
    master = master.merge(geo, on="openalex_id", how="left")
    master.to_csv(MASTER_PATH, index=False)

    rounded = master.apply(
        lambda r: (round(float(r["latitude"]), 4), round(float(r["longitude"]), 4)),
        axis=1,
    )
    stacks = {k: v for k, v in Counter(rounded).items() if v > 1}

    print(f"Wrote {CACHE_PATH} ({len(geo)} rows)")
    print(f"  Manual campus overrides: {len(MANUAL_CAMPUS)}")
    if locked:
        print(f"  Locked campus_all_overrides.csv: {len(locked)} rows")
    print(f"  Nominatim calls this run: {nominatim_calls}")
    print(f"  Coordinates moved (>0.01 deg): {updated}")
    print(f"  Remaining duplicate stacks: {len(stacks)}")
    if stacks:
        worst = max(stacks.items(), key=lambda x: x[1])
        print(f"  Worst stack: {worst[1]} at {worst[0]}")


if __name__ == "__main__":
    main()
