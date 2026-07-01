#!/usr/bin/env python3
"""Shared NIRF matching helpers for india_network scripts."""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from config import DATA_DIR, RAW_DIR

NIRF_YEAR = 2024
NIRF_PDF_BASE = f"https://www.nirfindia.org/nirfpdfcdn/{NIRF_YEAR}/pdf"

CATEGORY_LETTER = {
    "Overall": "O",
    "University": "U",
    "Engineering": "E",
    "Management": "M",
    "Pharmacy": "P",
    "Medical": "MED",
    "College": "C",
    "Research": "R",
    "Law": "L",
    "Architecture": "A",
    "Dental": "D",
    "Agriculture": "AG",
    "Innovation": "I",
}

# Manual canonical_name -> nirf_institute_id when fuzzy match fails or is ambiguous.
NIRF_ID_OVERRIDES: dict[str, str] = {
    "Academy of Scientific and Innovative Research": "IR-R-U-0713",
    "Christian Medical College, Vellore": "IR-D-C-45654",
    "Christian Medical College": "IR-D-C-29209",
    "Koneru Lakshmaiah Education Foundation": "IR-O-U-0020",
    "Kasturba Medical College, Manipal": "IR-D-C-7242",
    "Bharati Vidyapeeth Deemed University": "IR-O-I-1361",
    "Indian Institute of Engineering Science and Technology, Shibpur": "IR-E-U-0584",
    "University of Petroleum and Energy Studies": "IR-O-U-0564",
    "Central University of Rajasthan": "IR-P-U-0392",
    "Government Medical College": "IR-D-C-48124",
    "Jawaharlal Nehru Technological University, Hyderabad": "IR-E-U-0017",
    "All India Institute of Medical Sciences Raipur": "IR-D-U-0690",
    "Post Graduate Institute of Medical Education and Research": "IR-O-U-0446",
    "Jawaharlal Institute of Post Graduate Medical Education and Research": "IR-O-U-0368",
}

# canonical_name -> preferred NIRF institute_name substring for funding join
FUNDING_NAME_ALIASES: dict[str, str] = {
    "Government Medical College": "Government Medical College, Thiruvananthapuram",
    "Christian Medical College": "Christian Medical College",
    "Bharati Vidyapeeth Deemed University": "Bharati Vidyapeeth",
    "Koneru Lakshmaiah Education Foundation": "Koneru Lakshmaiah Education Foundation",
    "University of Petroleum and Energy Studies": "UPES",
}


def norm_name(name: str) -> str:
    s = str(name or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm_name(a), norm_name(b)).ratio()


def pdf_institute_id(institute_id: str, category: str) -> str:
    parts = institute_id.split("-")
    if len(parts) >= 4 and category in CATEGORY_LETTER:
        letter = CATEGORY_LETTER[category]
        if letter != "MED":
            parts[1] = letter
    return "-".join(parts)


def candidate_pdf_urls(institute_id: str, categories: list[str]) -> list[tuple[str, str]]:
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for cat in categories:
        for pid in (pdf_institute_id(institute_id, cat), institute_id):
            url = f"{NIRF_PDF_BASE}/{cat}/{pid}.pdf"
            if url not in seen:
                seen.add(url)
                out.append((cat, url))
    overall_url = f"{NIRF_PDF_BASE}/Overall/{institute_id}.pdf"
    if overall_url not in seen:
        out.append(("Overall", overall_url))
    return out


def innovation_pdf_url(institute_id: str) -> str:
    inv_id = pdf_institute_id(institute_id, "Innovation")
    return f"{NIRF_PDF_BASE}/Innovation/{inv_id}.pdf"


def load_nirf_rankings() -> pd.DataFrame:
    path = RAW_DIR / "nirf_rankings.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_nirf_id_overrides() -> dict[str, str]:
    path = DATA_DIR / "nirf_institute_id_overrides.csv"
    overrides = dict(NIRF_ID_OVERRIDES)
    if path.exists():
        df = pd.read_csv(path)
        for _, row in df.iterrows():
            name = str(row.get("canonical_name", "")).strip()
            iid = str(row.get("nirf_institute_id", "")).strip()
            if name and iid:
                overrides[name] = iid
    return overrides


def load_nirf_categories() -> dict[str, list[str]]:
    """institute_id -> ranking categories (best first)."""
    df = load_nirf_rankings()
    if df.empty:
        return {}
    order = [
        "Engineering",
        "University",
        "Overall",
        "Research",
        "Management",
        "Medical",
        "Dental",
        "Pharmacy",
        "Innovation",
    ]
    out: dict[str, list[str]] = {}
    for iid, grp in df.groupby("institute_id"):
        cats = grp["ranking_category"].astype(str).tolist()
        cats_sorted = sorted(cats, key=lambda c: order.index(c) if c in order else 99)
        out[str(iid)] = cats_sorted
    return out


def best_nirf_match(
    canonical_name: str,
    city: str | None = None,
    state: str | None = None,
    nirf: pd.DataFrame | None = None,
) -> tuple[pd.Series | None, float]:
    overrides = load_nirf_id_overrides()
    if canonical_name in overrides:
        iid = overrides[canonical_name]
        if nirf is None:
            nirf = load_nirf_rankings()
        hits = nirf[nirf["institute_id"] == iid]
        if not hits.empty:
            best = hits.sort_values("rank").iloc[0]
            return best, 1.0

    if nirf is None:
        nirf = load_nirf_rankings()
    if nirf.empty:
        return None, 0.0

    preferred = nirf[nirf["ranking_category"] == "Overall"]
    if preferred.empty:
        preferred = nirf

    best_row = None
    best_score = 0.0
    for _, n in preferred.iterrows():
        score = name_similarity(canonical_name, n["institute_name"])
        if city and str(city).lower() == str(n.get("city", "")).lower():
            score += 0.08
        if state and str(state).lower() == str(n.get("state", "")).lower():
            score += 0.03
        if score > best_score:
            best_score = score
            best_row = n
    if best_row is not None and best_score >= 0.72:
        return best_row, best_score
    return None, best_score
