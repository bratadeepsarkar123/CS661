#!/usr/bin/env python3
"""One-off analysis for patent + NIRF loser recovery candidates."""
from __future__ import annotations

import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_DIR, PROCESSED_DIR, RAW_DIR  # noqa: E402
from nirf_utils import (  # noqa: E402
    innovation_pdf_url,
    load_nirf_id_overrides,
    norm_name,
)

LOGS = DATA_DIR / "logs"


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, norm_name(a), norm_name(b)).ratio()


def analyze_nirf_losers() -> list[dict]:
    losers = pd.read_csv(PROCESSED_DIR / "nirf_match_losers.csv")
    master = pd.read_csv(PROCESSED_DIR / "institution_master.csv")
    rank24 = pd.read_csv(RAW_DIR / "nirf_rankings.csv")
    rank23_path = RAW_DIR / "nirf_rankings_2023.csv"
    rank23 = pd.read_csv(rank23_path) if rank23_path.exists() else pd.DataFrame()

    loser_meta = master[master["canonical_name"].isin(losers["canonical_name"])].set_index("canonical_name")
    out: list[dict] = []

    for _, row in losers.iterrows():
        name = row["canonical_name"]
        meta = loser_meta.loc[name] if name in loser_meta.index else None
        city = str(meta["city"]) if meta is not None and pd.notna(meta.get("city")) else ""
        state = str(meta["state"]) if meta is not None and pd.notna(meta.get("state")) else ""

        best_24 = None
        best_23 = None
        for label, df in [("2024", rank24), ("2023", rank23)]:
            if df.empty:
                continue
            for _, r in df.iterrows():
                rname = str(r["institute_name"])
                score = _sim(name, rname)
                rcity = str(r.get("city") or "")
                rstate = str(r.get("state") or "")
                if city and city.lower() in rcity.lower():
                    score += 0.08
                if state and state.lower() in rstate.lower():
                    score += 0.05
                # spelling aliases
                aliases = {
                    "pondicherry": "puducherry",
                    "allahabad": "prayagraj",
                    "mysore": "mysuru",
                    "mangalore": "mangaluru",
                }
                nn = norm_name(name)
                rn = norm_name(rname)
                for a, b in aliases.items():
                    if a in nn and b in rn:
                        score += 0.12
                    if b in nn and a in rn:
                        score += 0.12
                cand = {
                    "year": label,
                    "nirf_id": str(r["institute_id"]),
                    "nirf_name": rname,
                    "category": str(r.get("ranking_category", "")),
                    "city": rcity,
                    "state": rstate,
                    "score": round(score, 3),
                }
                if label == "2024":
                    if best_24 is None or cand["score"] > best_24["score"]:
                        best_24 = cand
                else:
                    if best_23 is None or cand["score"] > best_23["score"]:
                        best_23 = cand

        best = best_24 if best_24 and (not best_23 or best_24["score"] >= best_23["score"]) else best_23
        reason = row["reason"]
        blocked = row.get("blocked_by", "")

        if name == "University of Rajasthan":
            action = "accept_gap"
            note = "Distinct from Central University of Rajasthan (IR-P-U-0392 Kishangarh); no 2024 Overall/University row found"
        elif name == "SRM University":
            action = "accept_gap"
            note = "SRM University (Sonipat) is not S.R.M. Institute Chennai (IR-O-U-0473); no safe override"
        elif name == "Indian Institute of Technology Goa":
            action = "accept_gap"
            note = "IIT Goa not in NIRF 2024 rankings; fuzzy IIT Ropar is misleading"
        elif name == "Guru Nanak Dev University":
            action = "accept_gap"
            note = "Ranked in NIRF 2023 (IR-O-U-0376) but absent from 2024 master CSV"
        elif name == "Mangalore University":
            action = "accept_gap"
            note = "Do not map to Bangalore University (different city/entity)"
        elif name == "Shivaji University":
            action = "accept_gap"
            note = "Do not map to Shiv Nadar University (different entity)"
        elif name == "University of Allahabad":
            action = "accept_gap"
            note = "Prayagraj university not in NIRF 2024; Hyderabad match is false positive"
        elif best and best["year"] == "2024" and best["score"] >= 0.92:
            action = "override"
            note = f"Strong 2024 match: {best['nirf_name']} ({best['nirf_id']})"
        elif best and best["score"] >= 0.85:
            action = "manual_review"
            note = f"Possible match only ({best['score']}) — verify city/state"
        elif best and best["score"] >= 0.72:
            action = "manual_review"
            note = f"Weak match only ({best['score']})"
        else:
            action = "accept_gap"
            note = "No close NIRF 2024 row"

        if reason == "id_blocked_by_uniqueness" and name == "University of Rajasthan":
            action = "accept_gap"

        out.append(
            {
                "canonical_name": name,
                "reason": reason,
                "blocked_by": blocked if pd.notna(blocked) and blocked else None,
                "city": city or None,
                "state": state or None,
                "best_nirf_match": best,
                "best_nirf_match_2023": best_23,
                "recommended_action": action,
                "notes": note,
            }
        )
    return out


def analyze_patent_gaps() -> list[dict]:
    gaps = json.loads((LOGS / "patent_coverage_gaps.json").read_text(encoding="utf-8"))
    master = pd.read_csv(PROCESSED_DIR / "institution_master.csv")
    overrides = load_nirf_id_overrides()
    patents_raw = RAW_DIR / "nirf_patents.csv"
    patents_df = pd.read_csv(patents_raw) if patents_raw.exists() else pd.DataFrame()
    scraped_path = RAW_DIR / "nirf_patents_scraped.csv"
    scraped_df = pd.read_csv(scraped_path) if scraped_path.exists() else pd.DataFrame()
    rank24 = pd.read_csv(RAW_DIR / "nirf_rankings.csv")

    id_in_scraped = set()
    if not scraped_df.empty and "institute_id" in scraped_df.columns:
        id_in_scraped = set(scraped_df["institute_id"].astype(str).str.strip())

    id_in_dataful = set()
    if not patents_df.empty and "institute_id" in patents_df.columns:
        id_in_dataful = set(patents_df["institute_id"].astype(str).str.strip())

    out: list[dict] = []
    session = requests.Session()
    session.headers.update({"User-Agent": "CS661-recovery-analysis/1.0"})

    for item in gaps["unavailable"]:
        name = item["canonical_name"]
        iid = item.get("nirf_institute_id")
        if not iid:
            iid = overrides.get(name)
        reason = item.get("reason", "unknown")

        mrow = master[master["canonical_name"] == name]
        city = str(mrow.iloc[0]["city"]) if not mrow.empty and pd.notna(mrow.iloc[0].get("city")) else ""
        state = str(mrow.iloc[0]["state"]) if not mrow.empty and pd.notna(mrow.iloc[0].get("state")) else ""

        pdf_status = None
        if iid:
            url = innovation_pdf_url(str(iid))
            try:
                resp = session.head(url, timeout=20, allow_redirects=True)
                pdf_status = resp.status_code
            except requests.RequestException as exc:
                pdf_status = str(exc)

        # Search rankings for alternate spellings
        alt_matches = []
        for _, r in rank24.iterrows():
            score = _sim(name, str(r["institute_name"]))
            if city and city.lower() in str(r.get("city") or "").lower():
                score += 0.08
            if score >= 0.75:
                alt_matches.append(
                    {
                        "nirf_id": str(r["institute_id"]),
                        "nirf_name": str(r["institute_name"]),
                        "category": str(r.get("ranking_category", "")),
                        "score": round(score, 3),
                    }
                )
        alt_matches.sort(key=lambda x: x["score"], reverse=True)

        recoverable = False
        fix = None
        evidence = []

        if iid and str(iid) in id_in_scraped:
            recoverable = True
            fix = "already_in_scraped_rejoin"
            evidence.append(f"{iid} present in nirf_patents_scraped.csv but join missed")

        if pdf_status == 200:
            recoverable = True
            fix = fix or "rescrape_innovation_pdf"
            evidence.append(f"Innovation PDF HTTP 200 for {iid}")
        elif pdf_status == 404:
            evidence.append(f"Innovation PDF 404 for {iid}")
        elif pdf_status:
            evidence.append(f"Innovation PDF status {pdf_status} for {iid}")

        if reason == "no_innovation_pdf" and pdf_status == 404:
            fix = fix or "accept_gap_no_innovation_pdf"
            evidence.append("Patents only in Innovation category PDFs per NIRF schema")

        # Do not suggest cross-institute overrides (Goa→Ropar, SRM→SR Univ, Mangalore→Bangalore).
        blocked_patent_overrides = {
            "Indian Institute of Technology Goa",
            "SRM University",
            "Mangalore University",
        }
        if not iid and alt_matches and name not in blocked_patent_overrides:
            top = alt_matches[0]
            if top["score"] >= 0.95 and city and city.lower() in str(
                rank24.loc[rank24["institute_id"] == top["nirf_id"], "city"].astype(str).str.lower()
            ).any():
                recoverable = True
                fix = fix or "nirf_id_override_then_scrape"
                evidence.append(f"Alternate NIRF id {top['nirf_id']} via rankings ({top['nirf_name']})")

        if name in {"Guru Nanak Dev University", "Dr. Hari Singh Gour University", "Indian Association for the Cultivation of Science"}:
            fix = "accept_gap_unranked"
            recoverable = False
            evidence.append("Marked unranked in 08b_join_nirf_patents.py")

        out.append(
            {
                "canonical_name": name,
                "nirf_institute_id": iid,
                "reason": reason,
                "city": city or None,
                "state": state or None,
                "innovation_pdf_http": pdf_status,
                "in_scraped_csv": bool(iid and str(iid) in id_in_scraped),
                "alternate_nirf_matches": alt_matches[:3],
                "recoverable": recoverable,
                "recommended_fix": fix,
                "evidence": evidence,
            }
        )
    return out


def main() -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    loser_path = LOGS / "nirf_loser_recovery_candidates.json"
    patent_path = LOGS / "patent_recovery_candidates.json"

    losers = analyze_nirf_losers()
    loser_path.write_text(json.dumps({"candidates": losers}, indent=2), encoding="utf-8")
    print(f"Wrote {loser_path} ({len(losers)} losers)")

    patents = analyze_patent_gaps()
    patent_path.write_text(
        json.dumps(
            {
                "generated_from": "_recovery_analysis.py",
                "total_unavailable": len(patents),
                "recoverable_count": sum(1 for p in patents if p["recoverable"]),
                "candidates": patents,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {patent_path} ({len(patents)} patent gaps, {sum(1 for p in patents if p['recoverable'])} recoverable)")


if __name__ == "__main__":
    main()
