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

CATEGORY_ORDER_DEFAULT = [
    "Overall",
    "University",
    "Engineering",
    "Research",
    "Medical",
    "Management",
    "Pharmacy",
    "Dental",
    "Law",
    "Architecture",
    "Agriculture",
    "College",
    "Innovation",
]

# Prefer Engineering for tech institutes that may lack an Overall NIRF row.
CATEGORY_ORDER_BY_INST_TYPE: dict[str, list[str]] = {
    "IIT": ["Overall", "Engineering", "Research"],
    "NIT": ["Engineering", "Overall"],
    "IIIT": ["Engineering", "Overall", "University"],
}

CATEGORY_ORDER_BY_NAME_PATTERN: list[tuple[re.Pattern[str], list[str]]] = [
    (re.compile(r"\bmedical\b|\baiims\b|\bims\b", re.I), ["Medical", "Overall"]),
    (re.compile(r"\bpharmacy\b", re.I), ["Pharmacy", "Overall"]),
    (re.compile(r"\blaw\b", re.I), ["Law", "Overall"]),
    (re.compile(r"\bdental\b", re.I), ["Dental", "Overall"]),
    (re.compile(r"indian institute of technology", re.I), ["Overall", "Engineering", "Research"]),
    (re.compile(r"national institute of technology", re.I), ["Engineering", "Overall"]),
    (re.compile(r"institute of technology", re.I), ["Engineering", "Overall", "University"]),
]

NAME_STOP_TOKENS = frozenset(
    {
        "indian",
        "institute",
        "of",
        "technology",
        "the",
        "and",
        "university",
        "national",
        "college",
        "academy",
        "higher",
        "education",
        "deemed",
        "sciences",
        "science",
        "government",
        "technical",
        "management",
        "fundamental",
        "social",
        "medical",
        "post",
        "graduate",
        "school",
        "mines",
        "banaras",
        "hindu",
        "varanasi",
        "bhu",
        "ism",
        "dhanbad",
    }
)

CITY_ALIASES: dict[str, set[str]] = {
    "prayagraj": {"allahabad", "prayagraj"},
    "allahabad": {"allahabad", "prayagraj"},
    "bengaluru": {"bengaluru", "bangalore"},
    "bangalore": {"bengaluru", "bangalore"},
    "mysuru": {"mysuru", "mysore"},
    "mysore": {"mysuru", "mysore"},
    "mumbai": {"mumbai", "bombay"},
    "bombay": {"mumbai", "bombay"},
    "chennai": {"chennai", "madras"},
    "madras": {"chennai", "madras"},
    "new delhi": {"new delhi", "delhi"},
    "delhi": {"new delhi", "delhi"},
    "sonipat": {"sonipat", "sonīpat"},
    "sonīpat": {"sonipat", "sonīpat"},
    "kolhapur": {"kolhapur", "kolhāpur"},
    "kolhāpur": {"kolhapur", "kolhāpur"},
    "patia": {"patiala", "patiāla"},
    "patiala": {"patiala", "patiāla"},
    "patiāla": {"patiala", "patiāla"},
}

# Manual canonical_name -> nirf_institute_id for names that cannot be resolved algorithmically.
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

MATCH_THRESHOLD = 0.78
MATCH_THRESHOLD_WITH_TOKENS = 0.72


def norm_name(name: str) -> str:
    s = str(name or "").lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, norm_name(a), norm_name(b)).ratio()


def _city_aliases(city: str | None) -> set[str]:
    if not city or pd.isna(city):
        return set()
    key = norm_name(str(city))
    return CITY_ALIASES.get(key, {key})


def extract_distinguishing_tokens(canonical_name: str) -> set[str]:
    """Location or campus tokens that must align with a NIRF row."""
    norm = norm_name(canonical_name)
    tokens = {t for t in norm.split() if len(t) > 2 and t not in NAME_STOP_TOKENS}
    return tokens


def _token_overlap(canonical_tokens: set[str], nirf_name: str, city: str | None = None) -> bool:
    if not canonical_tokens:
        return True
    nirf_tokens = set(norm_name(nirf_name).split())
    if canonical_tokens & nirf_tokens:
        return True
    for alias_set in (_city_aliases(city),):
        if alias_set & nirf_tokens:
            return True
        if any(a in norm_name(nirf_name) for a in alias_set):
            return True
    return False


def category_preferences(canonical_name: str, inst_type: str | None = None) -> list[str]:
    if inst_type and str(inst_type).strip() in CATEGORY_ORDER_BY_INST_TYPE:
        return CATEGORY_ORDER_BY_INST_TYPE[str(inst_type).strip()]
    for pattern, order in CATEGORY_ORDER_BY_NAME_PATTERN:
        if pattern.search(canonical_name):
            return order
    return CATEGORY_ORDER_DEFAULT


def score_nirf_row_match(
    canonical_name: str,
    nirf_row: pd.Series,
    *,
    city: str | None = None,
    state: str | None = None,
) -> float:
    score = name_similarity(canonical_name, nirf_row["institute_name"])
    canon_tokens = extract_distinguishing_tokens(canonical_name)
    nirf_name = str(nirf_row.get("institute_name", ""))

    if canon_tokens and not _token_overlap(canon_tokens, nirf_name, city=city):
        return 0.0

    nirf_city = str(nirf_row.get("city", "") or "")
    nirf_state = str(nirf_row.get("state", "") or "")
    city_norm = norm_name(city) if city and not pd.isna(city) else ""
    state_norm = norm_name(state) if state and not pd.isna(state) else ""

    if city_norm and nirf_city:
        city_match = city_norm == norm_name(nirf_city)
        if not city_match:
            city_match = bool(_city_aliases(city) & _city_aliases(nirf_city))
        if not city_match and city_norm not in norm_name(nirf_city) and norm_name(nirf_city) not in city_norm:
            score -= 0.12
        else:
            score += 0.12

    if state_norm and nirf_state:
        if state_norm == norm_name(nirf_state):
            score += 0.06
        elif state_norm not in norm_name(nirf_state):
            score -= 0.05

    return score


def _threshold_for(canonical_name: str) -> float:
    tokens = extract_distinguishing_tokens(canonical_name)
    return MATCH_THRESHOLD_WITH_TOKENS if tokens else MATCH_THRESHOLD


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
    order = CATEGORY_ORDER_DEFAULT
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
    inst_type: str | None = None,
) -> tuple[pd.Series | None, float]:
    """Return the best NIRF row for one institution (no global uniqueness)."""
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

    prefs = category_preferences(canonical_name, inst_type=inst_type)
    threshold = _threshold_for(canonical_name)

    best_row: pd.Series | None = None
    best_score = 0.0
    best_pref = 99

    for cat in prefs:
        pool = nirf[nirf["ranking_category"] == cat]
        if pool.empty:
            continue
        pref_rank = prefs.index(cat)
        for _, row in pool.iterrows():
            score = score_nirf_row_match(canonical_name, row, city=city, state=state)
            if score < threshold:
                continue
            if score > best_score or (score == best_score and pref_rank < best_pref):
                best_score = score
                best_row = row
                best_pref = pref_rank

    if best_row is not None:
        return best_row, best_score
    return None, best_score


def assign_nirf_matches(
    master: pd.DataFrame,
    nirf_all: pd.DataFrame,
) -> pd.DataFrame:
    """Assign NIRF ids/ranks with one-id-per-institute uniqueness."""
    master = master.copy()
    for col in ["nirf_institute_id", "nirf_rank", "nirf_score", "nirf_year"]:
        if col not in master.columns:
            master[col] = pd.NA
        else:
            master[col] = pd.NA

    overrides = load_nirf_id_overrides()
    claimed_ids: set[str] = set()
    candidates: list[tuple[int, pd.Series, float]] = []

    for idx, row in master.iterrows():
        name = row["canonical_name"]
        if name in overrides:
            iid = overrides[name]
            hits = nirf_all[nirf_all["institute_id"] == iid]
            if hits.empty:
                continue
            if iid in claimed_ids:
                continue
            best = hits.sort_values("rank").iloc[0]
            claimed_ids.add(iid)
            master.at[idx, "nirf_institute_id"] = best["institute_id"]
            master.at[idx, "nirf_rank"] = int(best["rank"])
            master.at[idx, "nirf_score"] = float(best["score"])
            master.at[idx, "nirf_year"] = int(best["nirf_year"])
            continue

        match, score = best_nirf_match(
            name,
            city=row.get("city"),
            state=row.get("state"),
            nirf=nirf_all,
            inst_type=row.get("inst_type"),
        )
        if match is not None:
            candidates.append((idx, match, score))

    candidates.sort(key=lambda item: item[2], reverse=True)
    for idx, match, _score in candidates:
        iid = str(match["institute_id"])
        if iid in claimed_ids:
            continue
        claimed_ids.add(iid)
        master.at[idx, "nirf_institute_id"] = match["institute_id"]
        master.at[idx, "nirf_rank"] = int(match["rank"])
        master.at[idx, "nirf_score"] = float(match["score"])
        master.at[idx, "nirf_year"] = int(match["nirf_year"])

    return master
