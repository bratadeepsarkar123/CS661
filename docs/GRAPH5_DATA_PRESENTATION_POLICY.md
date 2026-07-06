# Graph 5 Data Presentation Policy

**Audience:** Dashboard users (public/demo) vs maintainers (internal).  
**Principle:** Never show a misleading partial time series without an explicit footnote.  
**Last updated:** 2026-07-08 (post acquisition marathon)

---

## 1. Core rules

1. **Never fabricate** institute-level ranks, funding, or patents for years where NIRF did not publish data we have scraped.
2. **Collaboration edges** always reflect the **calendar year** selected on the slider (2015–2024).
3. **NIRF-derived metrics** (rank, funding, patents) use **mapped** seasons/years — show the mapped value *and* label when it differs from the slider year.
4. **Grey out / unavailable** beats wrong numbers. Prefer `—` or “Unavailable” with a one-line reason.
5. **Internal gap docs** (`GRAPH5_GAP_ASSESSMENT.md`, `NIRF_DATA_ACQUISITION_LOG.md`) are **not** shown in the dashboard; users see only honest footnotes.

---

## 2. Per-metric coverage (actual data on disk)

| Metric | Years we actually have | Slider behavior | UI when outside range |
|--------|------------------------|-----------------|------------------------|
| **NIRF rank** | Ranking seasons **2016–2024** on disk (2016–2017 via acquisition marathon); **2015** not published | Slider 2015 → **2016**; 2016 → 2016; 2017 → 2017; 2018–2024 → matching season | Footnote when slider ≠ season. Legacy IR17-* IDs resolved by name fuzzy match. |
| **Research funding** | Academic years **2017-18 … 2022-23** from PDF scrape | Slider 2015–2017 → **2017-18**; 2018–2023 → mapped year; 2024 → **2022-23** | Static snapshot note on Funding tab (already implemented). Show `research_funding_cr` only when `funding_status=reported`. |
| **Patents** | Calendar years **2020, 2021, 2022** (Innovation PDF, 2024 CDN) | Slider &lt; 2020 → **2020**; 2020–2022 → exact year; &gt; 2022 → **2022** | `patent_status=unavailable` → “Patents not published in NIRF Innovation PDF for this institute.” |
| **SCImago quality** | **2019** snapshot only | Static across all slider years | Existing quality note (static 2019). |

---

## 3. Slider carry behavior (earliest / latest)

When the user moves the slider to an edge year:

| Slider | Funding shown | Patents shown | Rank season shown |
|--------|---------------|---------------|-------------------|
| 2015 | 2017-18 (earliest) | 2020 (earliest) | **2016** (nearest) |
| 2016 | 2017-18 | 2020 | **2016** |
| 2017 | 2017-18 | 2020 | **2017** |
| 2018 | 2018-19 | 2020 | 2018 |
| 2024 | 2022-23 (latest) | 2022 (latest) | 2024 |

**UI requirement:** When mapped year ≠ slider year, show a **carry indicator** (e.g. small “↔ 2018 season” or footnote line in the detail panel).

---

## 4. What the dashboard SHOULD show

- Collaboration network **changes by year** (edges, weights, triads).
- NIRF rank **when matched**, with **correct category** (`nirf_ranking_category`).
- Funding/patents **only when sourced** from NIRF PDFs; otherwise explicit unavailable state.
- Global footer notes:
  - SCImago static 2019.
  - Funding/patent/rank temporal mapping summary (expandable “About this data”).
- Coverage meta from export (`funding_academic_year_mapped`, `patent_calendar_year_mapped`, `nirf_ranking_season_mapped`) — use for footnotes, not raw slider year alone.

---

## 5. What stays internal-only

- Full acquisition attempt log (`docs/NIRF_DATA_ACQUISITION_LOG.md`).
- Third-party reference list (`data/logs/third_party_nirf_reference.json`).
- CDN probe matrices, Wayback CDX failures, data.gov.in CKAN metadata.
- NIRF match losers CSV and override rationale.

---

## 6. Example user-facing copy (footnotes)

**Funding tab (global):**
> Sponsored research amounts come from NIRF Overall/Engineering PDFs. We have academic years 2017-18 through 2022-23. Moving the year slider maps earlier/later collaboration years to the nearest available NIRF academic year.

**Detail panel — rank carry:**
> NIRF rank: #42 (Engineering, **2020 season**). Collaboration year 2019 — rank shown from nearest published NIRF season.

**Detail panel — funding unavailable:**
> Research funding: Unavailable — NIRF did not publish a downloadable PDF for this institute in our scraped seasons.

**Detail panel — patents unavailable:**
> Patents: Unavailable — NIRF Innovation category PDF not found for this institute (not inferred from Overall/Engineering PDFs).

**Detail panel — patent year carry:**
> Patents (published/granted): 2021 values shown. Collaboration year 2023 — patent data only available through calendar year 2022 in NIRF Innovation PDFs.

---

## 7. Policy on alternate sources

| Source | Use in dashboard |
|--------|------------------|
| nirfindia.org PDFs / HTML | **Primary** — only source for institute-level funding/patents/ranks |
| Wayback Machine recovered HTML | **Primary for ranks** if parsed and verified; same display rules |
| data.gov.in aggregate stats | **Not** for institute-level charts unless institute-keyed CSV verified |
| Shiksha / Careers360 | **Reference only** — never ingest without IR-* ID crosswalk |
| OpenAlex / university websites | **Cross-validation only** — never fill missing NIRF metrics |

---

## 8. Verification alignment

`10_verification_checklist.py` must PASS before demo. Presentation policy does not override verification — if a metric is `unavailable` in JSON, UI must not show a fabricated number.

---

*Maintainers: update Section 2 when `data/logs/nirf_historical_coverage.json` changes after acquisition runs.*
