#!/usr/bin/env python3
"""Emit campus_all_overrides.csv — 120 locked campus-level coordinates (campus_* sources)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR  # noqa: E402

SRC = PROCESSED_DIR / "campus_coordinates.csv"
OUT = PROCESSED_DIR / "campus_all_overrides.csv"

# Campus fixes for former openalex_normalized (city-centroid) rows
CAMPUS_FIXES: dict[str, tuple[float, float, str]] = {
    "I27674431": (23.2155, 72.6858, "campus_iit_gandhinagar"),
    "I189109744": (23.7956, 86.4302, "campus_iit_dhanbad"),
    "I4210121466": (21.2540, 81.5540, "campus_iit_bhilai"),
    "I145286018": (12.8236, 80.0442, "campus_srm_chennai"),
    "I171210897": (27.9159, 78.0812, "campus_amu"),
    "I99364266": (28.6545, 77.4545, "campus_acsir_ghaziabad"),
    "I101407740": (30.7320, 76.7310, "campus_chandigarh_university"),
    "I74796645": (28.3672, 75.6035, "campus_bits_pilani"),
    "I875944469": (16.5075, 80.6466, "campus_kl_university"),
    "I193073490": (20.3560, 85.8140, "campus_soa_bhubaneswar"),
    "I162030827": (30.3390, 76.3922, "campus_thapar_patiala"),
    "I8977528": (23.8280, 78.7715, "campus_dhsgsu_sagar"),
    "I170558118": (13.6360, 79.3930, "campus_svu_tirupati"),
    "I4210144496": (20.7161, 76.5619, "campus_gs_college_khamgaon"),
    "I98365261": (22.5550, 88.3510, "campus_iiest_shibpur"),
    "I19716509": (28.5165, 77.2498, "campus_jamia_hamdard"),
    "I82571370": (27.6030, 77.2940, "campus_gla_mathura"),
    "I115715567": (23.3432, 85.3094, "campus_bit_mesra"),
    "I20107917": (13.0415, 80.1440, "campus_sri_ramachandra"),
    "I155125381": (28.4961, 77.5360, "campus_galgotias"),
}


def _slug(name: str, oid: str) -> str:
    if name.startswith("campus_"):
        return name
    base = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    if len(base) > 40:
        base = base[:40].rstrip("_")
    return f"campus_{base or oid.lower()}"


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)
    df = pd.read_csv(SRC)
    rows = []
    for _, r in df.iterrows():
        oid = str(r["openalex_id"])
        if oid in CAMPUS_FIXES:
            lat, lon, src = CAMPUS_FIXES[oid]
        else:
            lat, lon = float(r["latitude"]), float(r["longitude"])
            src = str(r["geo_source"])
            if src.startswith("campus_"):
                pass
            elif src.startswith("nominatim"):
                src = _slug(r["canonical_name"], oid)
            else:
                src = _slug(r["canonical_name"], oid)
        rows.append(
            {
                "openalex_id": oid,
                "canonical_name": r["canonical_name"],
                "latitude": lat,
                "longitude": lon,
                "geo_source": src,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT, index=False)
    campus_only = out["geo_source"].str.startswith("campus_").sum()
    print(f"Wrote {OUT} ({len(out)} rows, campus_* sources: {campus_only})")


if __name__ == "__main__":
    main()
