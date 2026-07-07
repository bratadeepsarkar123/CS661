#!/usr/bin/env python3
"""Report institutions missing NIRF funding/patents after pipeline."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"
LOGS = ROOT / "data" / "logs"
LOSERS_PATH = PROC / "nirf_match_losers.csv"


def _patent_gap_reason(nirf_id) -> str:
    if pd.isna(nirf_id):
        return "no_nirf_id"
    return "no_innovation_pdf"


def _funding_gap_reason(nirf_id) -> str:
    if pd.isna(nirf_id):
        return "no_nirf_id"
    return "no_sponsored_research_pdf"


def load_loser_names() -> dict[str, str]:
    """canonical_name -> reason (no_fuzzy_match | id_blocked_by_uniqueness)."""
    if not LOSERS_PATH.exists():
        return {}
    df = pd.read_csv(LOSERS_PATH)
    return {str(r["canonical_name"]): str(r["reason"]) for _, r in df.iterrows()}


def run_report() -> dict:
    """Write nirf_coverage_gaps.md and patent_coverage_gaps.json; return summary counts."""
    master = pd.read_csv(PROC / "institution_master.csv")
    funding = pd.read_csv(PROC / "institution_funding.csv")
    patents = pd.read_csv(PROC / "institution_patents.csv")

    fund_count = int(funding["research_funding_cr"].notna().sum())
    patent_count = int(patents["patents_published"].notna().sum())
    nirf_matched = int(master["nirf_institute_id"].notna().sum())
    losers = load_loser_names()

    miss_fund = funding[funding["research_funding_cr"].isna()].merge(
        master[["institution_id", "nirf_institute_id", "city", "state"]], on="institution_id"
    )
    miss_pat = patents[patents["patents_published"].isna()].merge(
        master[["institution_id", "nirf_institute_id"]], on="institution_id"
    )

    patent_gaps: list[dict] = []
    for _, r in miss_pat.iterrows():
        reason = _patent_gap_reason(r["nirf_institute_id"])
        patent_gaps.append(
            {
                "canonical_name": str(r["canonical_name"]),
                "nirf_institute_id": None if pd.isna(r["nirf_institute_id"]) else str(r["nirf_institute_id"]),
                "reason": reason,
            }
        )

    lines = [
        "# NIRF data coverage gaps",
        "",
        f"Funding joined: {fund_count} / {len(funding)}",
        f"Patents joined: {patent_count} / {len(patents)}",
        f"NIRF IDs assigned: {nirf_matched} / {len(master)}",
        f"NIRF match losers: {len(losers)}",
        "",
        "## Missing funding",
        "",
    ]
    for _, r in miss_fund.iterrows():
        reason = (
            "Not in NIRF 2024 rankings"
            if pd.isna(r["nirf_institute_id"])
            else "No sponsored-research table in NIRF PDF"
        )
        lines.append(f"- **{r['canonical_name']}** ({r.get('city')}, {r.get('state')}): {reason}")

    lines.extend(["", "## Missing patents", ""])
    for gap in patent_gaps:
        if gap["reason"] == "no_nirf_id":
            label = "Not in NIRF 2024 rankings"
        else:
            label = "No Innovation-category PDF on nirfindia.org (patents only in Innovation PDFs)"
        lines.append(f"- **{gap['canonical_name']}**: {label}")

    md_out = PROC / "nirf_coverage_gaps.md"
    md_out.write_text("\n".join(lines), encoding="utf-8")

    LOGS.mkdir(parents=True, exist_ok=True)
    json_out = LOGS / "patent_coverage_gaps.json"
    json_payload = {
        "generated_from": "report_nirf_gaps.py",
        "patents_reported": patent_count,
        "patents_total": len(patents),
        "funding_reported": fund_count,
        "nirf_matched": nirf_matched,
        "nirf_losers": len(losers),
        "unavailable": patent_gaps,
        "by_reason": {
            "no_nirf_id": sum(1 for g in patent_gaps if g["reason"] == "no_nirf_id"),
            "no_innovation_pdf": sum(1 for g in patent_gaps if g["reason"] == "no_innovation_pdf"),
        },
    }
    json_out.write_text(json.dumps(json_payload, indent=2), encoding="utf-8")

    summary = {
        "funding_reported": fund_count,
        "funding_total": len(funding),
        "patents_reported": patent_count,
        "patents_total": len(patents),
        "nirf_matched": nirf_matched,
        "nirf_losers": len(losers),
        "loser_names": sorted(losers.keys()),
        "md_path": str(md_out),
        "json_path": str(json_out),
    }
    return summary


def main() -> None:
    summary = run_report()
    print(summary["md_path"])
    print(f"Funding: {summary['funding_reported']}/{summary['funding_total']}")
    print(f"Patents: {summary['patents_reported']}/{summary['patents_total']}")
    print(f"Patent gaps JSON: {summary['json_path']}")


if __name__ == "__main__":
    main()
