#!/usr/bin/env python3
"""Shared NIRF matching helpers for india_network scripts."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from config import DATA_DIR, RAW_DIR

NIRF_RANKING_CATEGORIES = [
    "Overall",
    "University",
    "College",
    "Research",
    "Engineering",
    "Management",
    "Pharmacy",
    "Medical",
    "Dental",
    "Law",
    "Architecture",
    "Agriculture",
    "Innovation",
]

NIRF_SUPPLEMENT_PATH = RAW_DIR / "nirf_rankings_supplement.csv"
NIRF_SCRAPE_GAPS_PATH = DATA_DIR / "logs" / "nirf_scrape_gaps.json"

NIRF_YEAR = 2024


def nirf_pdf_base(season: int | None = None) -> str:
    """CDN base for NIRF institute PDFs (ranking season year)."""
    return f"https://www.nirfindia.org/nirfpdfcdn/{season or NIRF_YEAR}/pdf"

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
    "Indian Institute of Technology Dharwad": "IR-E-U-0899",
    "SRM Institute of Science and Technology": "IR-O-U-0473",
    "Thapar Institute of Engineering & Technology": "IR-E-I-1480",
    "GLA University": "IR-P-U-0513",
    "Saveetha University": "IR-O-I-1441",
    "KIIT University": "IR-O-U-0356",
    "SASTRA University": "IR-O-U-0476",
    "Institute of Medical Sciences": "IR-D-U-0500",
    "GITAM University": "IR-P-U-0011",
    "Pondicherry University": "IR-O-U-0369",
    "University of Kalyani": "IR-O-U-0576",
    "Presidency University": "IR-O-U-0580",
    "Guru Nanak Dev University": "IR-O-U-0376",
}

# canonical_name -> preferred NIRF institute_name substring for funding join
FUNDING_NAME_ALIASES: dict[str, str] = {
    "Government Medical College": "Government Medical College, Thiruvananthapuram",
    "Christian Medical College": "Christian Medical College",
    "Bharati Vidyapeeth Deemed University": "Bharati Vidyapeeth",
    "Koneru Lakshmaiah Education Foundation": "Koneru Lakshmaiah Education Foundation",
    "University of Petroleum and Energy Studies": "UPES",
    "Indian Institute of Science": "Indian Institute of Science, Bengaluru",
    "Indian Institute of Technology (BHU) Varanasi": "Indian Institute of Technology (Banaras Hindu University) Varanasi",
    "Institute of Medical Sciences": "Banaras Hindu University",
    "Indian Institute of Technology (ISM) Dhanbad": "Indian Institute of Technology (Indian School of Mines) Dhanbad",
    "Thapar Institute of Engineering & Technology": "Thapar Institute of Engineering and Technology (Deemed-to-be-university)",
    "GLA University": "G. L. A. University",
    "SRM Institute of Science and Technology": "S.R.M. Institute of Science and Technology",
    "Saveetha University": "Saveetha Institute of Medical and Technical Sciences",
    "KIIT University": "Kalinga Institute of Industrial Technology",
    "SASTRA University": "Shanmugha Arts Science Technology and Research Academy",
    "GITAM University": "Gandhi Institute of Technology and Management",
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


def _spaced_acronyms(norm: str) -> set[str]:
    """Collapse single-letter runs (e.g. s r m -> srm) from NIRF dotted abbreviations."""
    parts = norm.split()
    out: set[str] = set()
    buf: list[str] = []
    for part in parts:
        if len(part) == 1 and part.isalpha():
            buf.append(part)
        else:
            if len(buf) >= 2:
                out.add("".join(buf))
            buf = []
    if len(buf) >= 2:
        out.add("".join(buf))
    return out


def extract_distinguishing_tokens(canonical_name: str) -> set[str]:
    """Location or campus tokens that must align with a NIRF row."""
    norm = norm_name(canonical_name)
    tokens = {t for t in norm.split() if len(t) > 2 and t not in NAME_STOP_TOKENS}
    tokens |= _spaced_acronyms(norm)
    return tokens


def funding_campus_compatible(
    inst_name: str,
    funding_name: str,
    city: str | None = None,
) -> bool:
    """Reject cross-institute fuzzy funding matches (IISc→AIIMS, IIT campus swaps)."""
    cn = norm_name(inst_name)
    fn = norm_name(funding_name)
    city_n = norm_name(city) if city and not pd.isna(city) else ""

    if name_similarity(inst_name, funding_name) >= 0.95:
        return True

    if cn == "indian institute of science":
        if "medical" in fn:
            return False
        return "bengaluru" in fn or "bangalore" in fn or cn in fn or "iisc" in fn

    if cn == "institute of medical sciences":
        if "all india institute" in fn and "varanasi" not in fn and "banaras" not in fn:
            return False
        if city_n and city_n in fn:
            return True
        return "banaras" in fn or "varanasi" in fn

    if "indian institute of technology" in cn:
        cross = [
            ("dhanbad", "dharwad"),
            ("dharwad", "dhanbad"),
            ("varanasi", "bhilai"),
            ("bhilai", "varanasi"),
        ]
        for a, b in cross:
            if (a in cn or a == city_n) and b in fn:
                return False
        if city_n:
            city_parts = {t for t in city_n.split() if len(t) > 2}
            if city_parts & set(fn.split()):
                return True
            if "banaras" in fn and ("bhu" in cn or "varanasi" in cn or city_n == "varanasi"):
                return True
            if "delhi" in cn and "delhi" in fn:
                return True
            if "madras" in cn and ("madras" in fn or city_n == "chennai"):
                return True
            return False
    return True


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


def candidate_pdf_urls(
    institute_id: str, categories: list[str], *, season: int | None = None
) -> list[tuple[str, str]]:
    base = nirf_pdf_base(season)
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for cat in categories:
        for pid in (pdf_institute_id(institute_id, cat), institute_id):
            url = f"{base}/{cat}/{pid}.pdf"
            if url not in seen:
                seen.add(url)
                out.append((cat, url))
    overall_url = f"{base}/Overall/{institute_id}.pdf"
    if overall_url not in seen:
        out.append(("Overall", overall_url))
    return out


def innovation_pdf_url(institute_id: str, *, season: int | None = None) -> str:
    inv_id = pdf_institute_id(institute_id, "Innovation")
    return f"{nirf_pdf_base(season)}/Innovation/{inv_id}.pdf"


def load_nirf_rankings() -> pd.DataFrame:
    path = RAW_DIR / "nirf_rankings.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_nirf_all() -> pd.DataFrame:
    """Load canonical rankings CSV merged with optional supplement rows."""
    base = load_nirf_rankings()
    if NIRF_SUPPLEMENT_PATH.exists():
        supp = pd.read_csv(NIRF_SUPPLEMENT_PATH)
        required = {
            "institute_id",
            "institute_name",
            "city",
            "state",
            "score",
            "rank",
            "ranking_category",
            "nirf_year",
        }
        missing = required - set(supp.columns)
        if missing:
            raise ValueError(f"{NIRF_SUPPLEMENT_PATH} missing columns: {sorted(missing)}")
        if not supp.empty:
            base = pd.concat([base, supp], ignore_index=True)
    if base.empty:
        return base
    base = base.drop_duplicates(
        subset=["institute_id", "ranking_category", "nirf_year"], keep="first"
    )
    base["name_norm"] = base["institute_name"].map(norm_name)
    return base


def build_nirf_scrape_gaps_report(
    scraped_df: pd.DataFrame,
    *,
    website_ids_by_category: dict[str, set[str]] | None = None,
    master: pd.DataFrame | None = None,
    year: int = NIRF_YEAR,
    source: str = "01b_scrape_nirf_rankings",
) -> dict:
    """Compare scraped CSV rows against live NIRF page IDs and master coverage."""
    category_counts: dict[str, dict[str, int]] = {}
    missing_from_csv: list[dict[str, str]] = []

    if website_ids_by_category:
        for cat, web_ids in website_ids_by_category.items():
            if scraped_df.empty:
                csv_ids: set[str] = set()
            else:
                csv_ids = set(
                    scraped_df.loc[
                        scraped_df["ranking_category"] == cat, "institute_id"
                    ].astype(str)
                )
            category_counts[cat] = {"website": len(web_ids), "csv": len(csv_ids)}
            for iid in sorted(web_ids - csv_ids):
                missing_from_csv.append({"institute_id": iid, "ranking_category": cat})

    master_institutes_without_nirf_match: list[str] = []
    master_nirf_matched = 0
    master_total = 0
    if master is not None and not master.empty:
        master_total = len(master)
        if "nirf_institute_id" in master.columns:
            master_nirf_matched = int(master["nirf_institute_id"].notna().sum())
            master_institutes_without_nirf_match = (
                master.loc[master["nirf_institute_id"].isna(), "canonical_name"]
                .astype(str)
                .sort_values()
                .tolist()
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "nirf_year": year,
        "missing_from_csv": missing_from_csv,
        "category_counts": category_counts,
        "master_institutes_without_nirf_match": master_institutes_without_nirf_match,
        "master_nirf_matched": master_nirf_matched,
        "master_total": master_total,
        "csv_rows": len(scraped_df),
        "csv_unique_institutes": int(scraped_df["institute_id"].nunique())
        if not scraped_df.empty
        else 0,
    }


def write_nirf_scrape_gaps(report: dict, path: Path | None = None) -> Path:
    out = path or NIRF_SCRAPE_GAPS_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return out


def update_master_in_scrape_gaps(master: pd.DataFrame, year: int = NIRF_YEAR) -> Path:
    """Refresh master coverage fields in an existing scrape-gaps report."""
    existing: dict = {}
    if NIRF_SCRAPE_GAPS_PATH.exists():
        existing = json.loads(NIRF_SCRAPE_GAPS_PATH.read_text(encoding="utf-8"))
    report = build_nirf_scrape_gaps_report(
        pd.DataFrame(),
        master=master,
        year=year,
        source="03a_enrich_institution_master",
    )
    existing.update(
        {
            "generated_at": report["generated_at"],
            "source": report["source"],
            "master_institutes_without_nirf_match": report["master_institutes_without_nirf_match"],
            "master_nirf_matched": report["master_nirf_matched"],
            "master_total": report["master_total"],
        }
    )
    return write_nirf_scrape_gaps(existing)


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


def load_nirf_id_canonical_names(*, prefer_category: str = "Overall") -> dict[str, str]:
    """Map NIRF institute_id -> canonical institute_name from rankings."""
    df = load_nirf_all()
    if df.empty:
        return {}
    out: dict[str, str] = {}
    for iid, grp in df.groupby("institute_id"):
        iid = str(iid).strip()
        preferred = grp[grp["ranking_category"] == prefer_category]
        row = preferred.sort_values("rank").iloc[0] if not preferred.empty else grp.sort_values("rank").iloc[0]
        out[iid] = str(row["institute_name"]).strip()
    return out


def funding_row_id_name_valid(
    institute_id: str,
    institute_name: str,
    id_to_name: dict[str, str],
    *,
    threshold: float = 0.88,
) -> bool:
    """True when row name aligns with the institute_id's NIRF canonical name."""
    canonical = id_to_name.get(str(institute_id).strip())
    if not canonical:
        return True
    if norm_name(institute_name) == norm_name(canonical):
        return True
    alias = FUNDING_NAME_ALIASES.get(str(institute_name).strip())
    if alias and norm_name(alias) == norm_name(canonical):
        return True
    score = name_similarity(institute_name, canonical)
    if alias:
        score = max(score, name_similarity(alias, canonical))
    if score < threshold and score < 0.72:
        return False
    if score < threshold and score >= 0.72:
        # Master short names (e.g. "Indian Institute of Science") vs NIRF PDF labels
        if not funding_campus_compatible(institute_name, canonical):
            return False
    canon_tokens = extract_distinguishing_tokens(canonical)
    if canon_tokens and not _token_overlap(canon_tokens, institute_name):
        if alias and _token_overlap(canon_tokens, alias):
            pass
        else:
            return False
    row_tokens = extract_distinguishing_tokens(institute_name)
    if row_tokens and not _token_overlap(row_tokens, canonical):
        if alias and _token_overlap(row_tokens, alias):
            pass
        else:
            return False
    return True


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
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Assign NIRF ids/ranks with one-id-per-institute uniqueness.

    Returns (master, losers_df) where losers_df lists institutes that could not
    claim an ID (blocked by uniqueness, missing override row, or no fuzzy match).
    """
    master = master.copy()
    for col in ["nirf_institute_id", "nirf_rank", "nirf_score", "nirf_year", "nirf_ranking_category"]:
        if col not in master.columns:
            master[col] = pd.NA
        else:
            master[col] = pd.NA

    overrides = load_nirf_id_overrides()
    claimed_ids: set[str] = set()
    id_to_name: dict[str, str] = {}
    candidates: list[tuple[int, pd.Series, float]] = []
    losers: list[dict[str, object]] = []

    for idx, row in master.iterrows():
        name = row["canonical_name"]
        if name in overrides:
            iid = overrides[name]
            hits = nirf_all[nirf_all["institute_id"] == iid]
            if hits.empty:
                losers.append(
                    {
                        "canonical_name": name,
                        "reason": "override_id_missing_in_rankings",
                        "best_nirf_id": iid,
                        "best_nirf_name": "",
                        "match_score": "",
                        "blocked_by": "",
                    }
                )
                continue
            if iid in claimed_ids:
                losers.append(
                    {
                        "canonical_name": name,
                        "reason": "override_id_already_claimed",
                        "best_nirf_id": iid,
                        "best_nirf_name": hits.iloc[0].get("institute_name", ""),
                        "match_score": "",
                        "blocked_by": id_to_name.get(iid, ""),
                    }
                )
                continue
            prefs = category_preferences(name, inst_type=row.get("inst_type"))
            best = _best_row_for_id(hits, prefs)
            claimed_ids.add(iid)
            id_to_name[iid] = name
            master.at[idx, "nirf_institute_id"] = best["institute_id"]
            master.at[idx, "nirf_rank"] = int(best["rank"])
            master.at[idx, "nirf_score"] = float(best["score"])
            master.at[idx, "nirf_year"] = int(best["nirf_year"])
            master.at[idx, "nirf_ranking_category"] = str(best["ranking_category"])
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
        else:
            losers.append(
                {
                    "canonical_name": name,
                    "reason": "no_fuzzy_match",
                    "best_nirf_id": "",
                    "best_nirf_name": "",
                    "match_score": round(score, 3),
                    "blocked_by": "",
                }
            )

    candidates.sort(key=lambda item: item[2], reverse=True)
    for idx, match, score in candidates:
        iid = str(match["institute_id"])
        if iid in claimed_ids:
            row = master.loc[idx]
            losers.append(
                {
                    "canonical_name": row["canonical_name"],
                    "reason": "id_blocked_by_uniqueness",
                    "best_nirf_id": iid,
                    "best_nirf_name": match.get("institute_name", ""),
                    "match_score": round(score, 3),
                    "blocked_by": id_to_name.get(iid, ""),
                }
            )
            continue
        claimed_ids.add(iid)
        id_to_name[iid] = str(master.at[idx, "canonical_name"])
        master.at[idx, "nirf_institute_id"] = match["institute_id"]
        master.at[idx, "nirf_rank"] = int(match["rank"])
        master.at[idx, "nirf_score"] = float(match["score"])
        master.at[idx, "nirf_year"] = int(match["nirf_year"])
        master.at[idx, "nirf_ranking_category"] = str(match["ranking_category"])

    losers_df = pd.DataFrame(losers)
    return master, losers_df


def _best_row_for_id(hits: pd.DataFrame, category_prefs: list[str]) -> pd.Series:
    """Pick the ranking row for an institute_id using category preference order."""
    for cat in category_prefs:
        pool = hits[hits["ranking_category"] == cat]
        if not pool.empty:
            return pool.sort_values("rank").iloc[0]
    return hits.sort_values("rank").iloc[0]


# Academic years from merged NIRF PDF seasons (2021–2024 CDN) + Dataful scrape.
FUNDING_ACADEMIC_YEARS: tuple[str, ...] = (
    "2017-18",
    "2018-19",
    "2019-20",
    "2020-21",
    "2021-22",
    "2022-23",
)
PATENT_CALENDAR_YEARS: tuple[int, ...] = (2020, 2021, 2022)


def discover_nirf_ranking_years(raw_dir: Path | None = None) -> list[int]:
    """Ranking seasons available as data/raw/nirf_rankings_{year}.csv."""
    root = raw_dir or RAW_DIR
    years: list[int] = []
    for path in sorted(root.glob("nirf_rankings_*.csv")):
        stem = path.stem.replace("nirf_rankings_", "")
        if stem.isdigit():
            years.append(int(stem))
    if not years and (root / "nirf_rankings.csv").exists():
        try:
            yr = int(pd.read_csv(root / "nirf_rankings.csv", usecols=["nirf_year"])["nirf_year"].iloc[0])
            years.append(yr)
        except (ValueError, KeyError, IndexError):
            pass
    return sorted(set(years))


def load_nirf_rankings_for_year(year: int, raw_dir: Path | None = None) -> pd.DataFrame:
    """Load one NIRF ranking season CSV (year file or canonical fallback)."""
    root = raw_dir or RAW_DIR
    year_path = root / f"nirf_rankings_{year}.csv"
    path = year_path if year_path.exists() else root / "nirf_rankings.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "nirf_year" not in df.columns:
        df["nirf_year"] = year
    else:
        df["nirf_year"] = df["nirf_year"].fillna(year).astype(int)
    df["name_norm"] = df["institute_name"].map(norm_name)
    return df


def load_nirf_rankings_all_years(raw_dir: Path | None = None) -> pd.DataFrame:
    """Concat all per-season ranking CSVs plus supplement rows."""
    root = raw_dir or RAW_DIR
    years = discover_nirf_ranking_years(root)
    frames: list[pd.DataFrame] = []
    for yr in years:
        part = load_nirf_rankings_for_year(yr, root)
        if not part.empty:
            frames.append(part)
    if not frames:
        base = load_nirf_all()
        return base
    combined = pd.concat(frames, ignore_index=True)
    if NIRF_SUPPLEMENT_PATH.exists():
        supp = pd.read_csv(NIRF_SUPPLEMENT_PATH)
        if not supp.empty:
            supp["name_norm"] = supp["institute_name"].map(norm_name)
            combined = pd.concat([combined, supp], ignore_index=True)
    combined = combined.drop_duplicates(
        subset=["institute_id", "ranking_category", "nirf_year"], keep="first"
    )
    combined["name_norm"] = combined["institute_name"].map(norm_name)
    return combined


def nearest_nirf_ranking_year(slider_year: int | None, available: list[int] | None = None) -> int:
    """Pick closest NIRF ranking season for a collaboration slider year."""
    avail = available or discover_nirf_ranking_years()
    if not avail:
        return NIRF_YEAR
    if slider_year is None:
        return avail[-1]
    return min(avail, key=lambda y: (abs(y - slider_year), -y))


def slider_year_to_nirf_ranking_year(slider_year: int | None) -> int:
    return nearest_nirf_ranking_year(slider_year)


def lookup_nirf_rank_for_institute(
    *,
    nirf_institute_id: str | None,
    canonical_name: str,
    ranking_year: int,
    nirf_all_years: pd.DataFrame | None = None,
    inst_type: str | None = None,
    city: str | None = None,
    state: str | None = None,
) -> tuple[int | None, str | None, int | None]:
    """Return (rank, ranking_category, nirf_ranking_season) for one institute and season."""
    pool = nirf_all_years if nirf_all_years is not None else load_nirf_rankings_all_years()
    if pool.empty:
        return None, None, None
    season = pool[pool["nirf_year"] == ranking_year]
    if season.empty:
        ranking_year = nearest_nirf_ranking_year(ranking_year, sorted(pool["nirf_year"].unique()))
        season = pool[pool["nirf_year"] == ranking_year]
    if season.empty:
        return None, None, None

    prefs = category_preferences(canonical_name, inst_type=inst_type)
    if nirf_institute_id and pd.notna(nirf_institute_id):
        hits = season[season["institute_id"] == str(nirf_institute_id).strip()]
        if hits.empty:
            hits = season[season["institute_id"].str.endswith(str(nirf_institute_id).split("-")[-1], na=False)]
        if not hits.empty:
            row = _best_row_for_id(hits, prefs)
            return int(row["rank"]), str(row["ranking_category"]), int(row["nirf_year"])

    best_row: pd.Series | None = None
    best_score = 0.0
    best_pref = 99
    threshold = _threshold_for(canonical_name)
    for cat in prefs:
        cat_pool = season[season["ranking_category"] == cat]
        if cat_pool.empty:
            continue
        pref_rank = prefs.index(cat)
        for _, row in cat_pool.iterrows():
            score = score_nirf_row_match(canonical_name, row, city=city, state=state)
            if score < threshold:
                continue
            if score > best_score or (score == best_score and pref_rank < best_pref):
                best_score = score
                best_row = row
                best_pref = pref_rank
    if best_row is None:
        return None, None, int(ranking_year)
    return int(best_row["rank"]), str(best_row["ranking_category"]), int(best_row["nirf_year"])


def slider_year_to_funding_academic_year(slider_year: int | None) -> str:
    """Map collaboration slider calendar year to best NIRF sponsored-research academic year."""
    if slider_year is None:
        return FUNDING_ACADEMIC_YEARS[-1]
    mapping = {
        2015: "2017-18",
        2016: "2017-18",
        2017: "2017-18",
        2018: "2018-19",
        2019: "2019-20",
        2020: "2020-21",
        2021: "2020-21",
        2022: "2021-22",
        2023: "2022-23",
        2024: "2022-23",
    }
    if slider_year in mapping:
        return mapping[slider_year]
    if slider_year < 2017:
        return FUNDING_ACADEMIC_YEARS[0]
    if slider_year > 2024:
        return FUNDING_ACADEMIC_YEARS[-1]
    return FUNDING_ACADEMIC_YEARS[-1]


def slider_year_to_patent_calendar_year(slider_year: int | None) -> int:
    """Map collaboration slider calendar year to best NIRF Innovation patent calendar year."""
    if slider_year is None:
        return PATENT_CALENDAR_YEARS[-1]
    if slider_year < PATENT_CALENDAR_YEARS[0]:
        return PATENT_CALENDAR_YEARS[0]
    if slider_year > PATENT_CALENDAR_YEARS[-1]:
        return PATENT_CALENDAR_YEARS[-1]
    return int(slider_year)


def funding_year_matches_slider(slider_year: int | None, funding_academic_year: str | None) -> bool:
    if slider_year is None or not funding_academic_year:
        return True
    return str(funding_academic_year) == slider_year_to_funding_academic_year(slider_year)


def patent_year_matches_slider(slider_year: int | None, patent_calendar_year: int | None) -> bool:
    if slider_year is None or patent_calendar_year is None:
        return True
    return int(patent_calendar_year) == slider_year_to_patent_calendar_year(slider_year)
