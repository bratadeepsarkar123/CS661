#!/usr/bin/env python3
"""Report institutions missing NIRF funding/patents after pipeline."""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROC = ROOT / "data" / "processed"

master = pd.read_csv(PROC / "institution_master.csv")
funding = pd.read_csv(PROC / "institution_funding.csv")
patents = pd.read_csv(PROC / "institution_patents.csv")

miss_fund = funding[funding["research_funding_cr"].isna()].merge(
    master[["institution_id", "nirf_institute_id", "city", "state"]], on="institution_id"
)
miss_pat = patents[patents["patents_published"].isna()].merge(
    master[["institution_id", "nirf_institute_id"]], on="institution_id"
)

lines = [
    "# NIRF data coverage gaps",
    "",
    f"Funding joined: {funding['research_funding_cr'].notna().sum()} / {len(funding)}",
    f"Patents joined: {patents['patents_published'].notna().sum()} / {len(patents)}",
    "",
    "## Missing funding",
    "",
]
for _, r in miss_fund.iterrows():
    reason = "Not in NIRF 2024 rankings" if pd.isna(r["nirf_institute_id"]) else "No sponsored-research table in NIRF PDF"
    lines.append(f"- **{r['canonical_name']}** ({r.get('city')}, {r.get('state')}): {reason}")

lines.extend(["", "## Missing patents", ""])
for _, r in miss_pat.iterrows():
    reason = (
        "Not in NIRF 2024 rankings"
        if pd.isna(r["nirf_institute_id"])
        else "No Innovation-category PDF on nirfindia.org (patents only in Innovation PDFs)"
    )
    lines.append(f"- **{r['canonical_name']}**: {reason}")

out = PROC / "nirf_coverage_gaps.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(out)
print(f"Funding: {funding['research_funding_cr'].notna().sum()}/{len(funding)}")
print(f"Patents: {patents['patents_published'].notna().sum()}/{len(patents)}")
