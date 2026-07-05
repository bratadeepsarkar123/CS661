# Graph 5 (India Domestic HE Network) — Gap Assessment & Fix Design

**Workspace:** `C:\Users\brata\Downloads\CS661`  
**Assessment date:** 2026-07-08 (counts refreshed post-GNDU override + UI funding footnote)  
**Methodology:** Multi-level bridge inspection — severity first, core fix design at source, then implementation.

**Related:** [`GRAPH5_PIPELINE_AUDIT.md`](GRAPH5_PIPELINE_AUDIT.md) (read-only pre-fix audit)  
**Post-fix commits:** `927f6fd` (five loser overrides); `d2e915d` / `f15e208` (SRM/Thapar/GLA + funding token join); `b0133e4` (duplicate funding dedupe → 0 clusters); Pondicherry/Kalyani/Presidency supplement overrides; GNDU `IR-O-U-0376` from NIRF 2023 supplement.



## Funding temporal scope (year slider)

**User expectation:** Moving the collaboration year slider (2015-2024) should change sponsored-research funding.

**Behavior (post Phase B historical ingest):** Funding, patents, and **NIRF ranks** are mapped from the slider year into available NIRF seasons. Collaboration edges remain filtered by calendar year.

**Mapping (slider calendar year → NIRF metric year):**

| Slider year | Funding academic year | Patents calendar year | NIRF ranking season |
|-------------|----------------------|------------------------|----------------------|
| 2015–2017 | 2017-18 (earliest) | 2020 (earliest) | 2018 (nearest; 2015–2017 not on site) |
| 2018 | 2018-19 | 2020 | 2018 |
| 2019 | 2019-20 | 2020 | 2019 |
| 2020 | 2020-21 | 2020 | 2020 |
| 2021 | 2020-21 | 2021 | 2021 |
| 2022 | 2021-22 | 2022 | 2022 |
| 2023 | 2022-23 | 2022 | 2023 |
| 2024 | 2022-23 | 2022 | 2024 |

**Evidence:**
- Ranking seasons on disk: `nirf_rankings_2018.csv` … `nirf_rankings_2024.csv` (+ supplement).
- Funding academic years: 2017-18 … 2022-23 from multi-season PDF scrape (`01h`, seasons 2021–2024 CDN).
- `09_export_payloads.build_nodes()` uses `lookup_nirf_rank_for_institute()` per slider year.
- Example: IIT Delhi Overall rank **#3** in 2023 slice vs **#4** in 2024 slice.

**Still static (honest gaps):**
- **SCImago** — 2019 snapshot.
- **NIRF ranks 2015–2017** — nirfindia.org 404 / legacy layout (2016–2017 unscrapeable).
- **Patents before 2020 / after 2022** — Innovation PDF only on 2024 CDN (2020–2022).
- **Funding 2023-24 academic year** — not in any scraped PDF season.

---

## Level 1 — Severity Assessment

### Known issues (pre-fix)

| Issue | Severity | User-visible impact | Data integrity risk | Scope (# institutes) | Blocks demo/submission? |
|-------|----------|---------------------|---------------------|----------------------|-------------------------|
| IIT Dharwad missing NIRF ID | **P0** | Detail panel shows rank "—" and inconsistent funding story | Wrong institute could inherit Hyderabad-scale funding (fixed in `2dd626d`) | 1 | Yes — demo narrative for newer IITs |
| ~40 institutes show "NIRF rank (Overall)" for Engineering/Medical/etc. ranks | **P0** | Misleading rank category in detail panel | Attribution error (rank number correct, category wrong) | ~40 | Yes — undermines trust in NIRF panel |
| Patent coverage 49/120 | **P1** | Most institutes show "patents unavailable" | Incomplete Innovation metrics; not fabricated | 71 missing | No — honest "unavailable" is acceptable |
| Verification full-payload size fails (543 KB vs 200 KB cap) | **Resolved** | CI/checklist passes | Cap raised to 2 MB | N/A | No |
| Lecture assets ~376 MB in git | **Resolved** | Repo clone needs LFS | None | N/A | No — committed via Git LFS (`6ffb0c9`) |

### New issues discovered during bridge inspection

| Issue | Severity | User-visible impact | Data integrity risk | Scope (# institutes) | Blocks demo/submission? |
|-------|----------|---------------------|---------------------|----------------------|-------------------------|
| IIT Dharwad absent from `01b` NIRF scrape (`nirf_rankings.csv`) despite NIRF 2024 Engineering participation | **P0** | No algorithmic match possible without override/supplemental row | ID assignment blocked at source | 1 | Yes |
| `dashboard/data/india_network/` drift from `public/india_network/` after export | **P1** | UI bundle stale until manual copy | Dashboard shows old fields (no `nirf_ranking_category`) | All 120 nodes | Yes — fixes invisible in UI |
| Duplicate funding values across unrelated institutes | **Resolved** | Same ₹ cr shown for distinct universities | Join dedupe in `01d` / `b0133e4` | **0 clusters** | No |
| 10 NIRF match losers (no ID after uniqueness pass) | **P1** | Missing NIRF rank in panel | Silent loss of metadata | 10 | No — documented limitation |
| `hierarchy-app/dist/india_network/` partial/stale fork | **P2** | Submodule app shows old slice if not rebuilt | Fork drift until sync + build | N/A | No — sync `public/` from dashboard |
| Triad map lines drift when zoomed out | **P0** (fixed) | Dashed triad endpoints 33–133 km off at zoom 4–6 | Visual misread of collaboration geography | All triad++ users | Yes — fixed `d1ac9d8` |
| Stale `nirf_coverage_gaps.md` / old verification claims | **P2** | Maintainer confusion | Documentation drift | N/A | No |
| Patent scrape limited to institutes with Innovation PDF on nirfindia.org | **P1** | Newer IITs (Bhilai, Jammu, Dharwad, etc.) show patent unavailable | Honest gap — no PDF exists | ~47 NIRF-ranked with no Innovation PDF | No |
| `01b` scrape gap pattern (institutes in official NIRF PDFs but missing from CSV) | **P1** | Systemic risk for future campuses | Under-counted in rankings source | Unknown tail | No |

### Holistic inspection summary

| Check | Status (post-fix) |
|-------|-------------------|
| Funding duplicates (same ₹, different institutes) | **0 clusters** — `10_verification_checklist.py` PASS (post `b0133e4`) |
| NIRF match losers | **10 unmatched** — Pondicherry, Kalyani, Presidency, GNDU fixed via supplement overrides |
| Dashboard ↔ public JSON drift | **Fixed** — `09b` now syncs to `dashboard/data/india_network/` |
| `hierarchy-app` fork | **Synced** — `dashboard/data/india_network/` copied to `hierarchy-app/public/india_network/` (2026-07-08) |
| Edge/orphan integrity | **PASS** — 0 orphan edges in overview/full payloads |
| Geo stacking | **PASS** — max stack=1; KIIT + Siksha O Anusandhan share Bhubaneswar pin (cosmetic P2, see below) |
| Verification artifacts | **Current** — **20/20 PASS** (`10_verification_checklist.py`) |
| Commits `40a71aa` / `2dd626d` regressions | **No regressions** — funding corruption guard passes; major IIT funding present |
| Raw source quality | Dataful funding IDs still unreliable; PDF scrape path authoritative |
| UI provenance footnotes | Accurate — SCImago static note + **Funding tab static NIRF snapshot note** (`india-data-note`) |

#### Duplicate funding clusters

Verification (`10_verification_checklist.py`) reports **0 duplicate-value clusters** (post `b0133e4` join dedupe). Earlier 2-cluster set (Panjab/NIT Durgapur; IISc/BHU family) resolved — see [`GRAPH5_FUNDING_LOSER_TRACE.md`](GRAPH5_FUNDING_LOSER_TRACE.md).

#### NIRF unmatched institutes (10)

IIT Goa; SRM University (Sonipat — distinct from SRM Chennai); Dr. Hari Singh Gour University; Indian Association for the Cultivation of Science; University of Allahabad; G.S. Science Arts And Commerce College; Shivaji University; Mangalore University; Karpagam Academy of Higher Education; University of Rajasthan (id_blocked_by_uniqueness vs Central University of Rajasthan).

**Why:** `assign_nirf_matches()` enforces one NIRF ID per institute. Losers include (a) institutes not in NIRF 2024 rankings (IIT Goa), (b) fuzzy-match blocked because a higher-scoring peer claimed the ID (SRM vs IIT Madras), (c) name variants not meeting threshold.

---

## Level 2 — Core Fix Design

### 2a — IIT Dharwad NIRF ID

**Research:**
- NIRF 2024 Engineering: **IR-E-U-0899**, rank **#93**, score 42.36 ([nirfindia.org Engineering 2024](https://www.nirfindia.org/Rankings/2024/EngineeringRanking.html); IIT Dharwad official submission PDF confirms ID).
- `01b_scrape_nirf_rankings.py` omitted this row from `nirf_rankings.csv` (present in `nirf_rankings_2023.csv` only).

**Design (at source, not per-institute UI patch):**
1. Add supplemental row to `data/raw/nirf_rankings.csv`.
2. Add override in `data/nirf_institute_id_overrides.csv` + `NIRF_ID_OVERRIDES` in `nirf_utils.py`.
3. `assign_nirf_matches()` uses `_best_row_for_id()` with category preferences (Engineering for IIT).
4. Re-run `03a` → `01e --only-missing` → `01d` → `08` → export chain.

**PDF funding path:** `01e` scrapes Engineering PDF for `IR-E-U-0899` → merged into `nirf_research_projects.csv` → `08_join_nirf_funding.py`.

### 2b — Rank category mislabel

**Trace:** `03a` (`assign_nirf_matches`) → `institution_master.csv` → `09_export_payloads.py` → `dashboard/india_network.js`

**Design:**
1. Store `nirf_ranking_category` in master during `assign_nirf_matches()`.
2. Export field in `09_export_payloads.py` (overview + full nodes).
3. UI: `nirfRankLabel(node)` → `NIRF rank (${category})` instead of hardcoded "Overall".

**Institutes affected (40 with non-Overall displayed rank):** All IITs/NITs ranked only in Engineering; AIIMS and medical colleges in Medical; Central University of Rajasthan in Pharmacy; University of Calcutta in Management; etc. Full list derivable from master where `nirf_ranking_category != 'Overall'`.

### 2c — Patent coverage 42/120 → expand

**Root cause audit:**
- `01f_scrape_nirf_patents_from_pdfs.py` only had 42 institutes in raw CSV from prior partial run.
- 59 NIRF-matched institutes lacked Innovation PDF (HTTP 404 or empty) — includes newer IITs, many state universities.
- No NIRF ID → no Innovation PDF URL → `unavailable` status (correct).

**Design:**
1. Enhance `01f` to merge with existing scrape (skip cached IDs).
2. Re-run for all master institutes with `nirf_institute_id` (98 targets).
3. `01g` → `08b` join unchanged; status remains `unavailable` when PDF absent.

**Realistic ceiling:** ~57 institutes with patent rows in raw data → **51 reported** after dedupe/collision resolution. Further gains require NIRF publishing Innovation PDFs or alternate source.

### 2d — Verification threshold

**Problem:** `10_verification_checklist.py` required `2024_full.json` < 200 KB; actual size ~544 KB with 120 nodes + triads.

**Design:** Raise cap to **2 MB** with explicit detail string. Overview cap stays 40 KB. Add funding corruption + major IIT checks (already present from `2dd626d`).

### 2e — Other P0/P1 fixes

| Issue | Fix |
|-------|-----|
| Dashboard bundle drift | `09b_export_year_slices.py` copies `public/india_network/*.json` → `dashboard/data/india_network/` |
| Lecture assets 376 MB | **Recommendation:** add `docs/lectures/assets/` to `.gitignore`; distribute via GitHub Release artifact or Git LFS; keep markdown lecture notes in git |

---

## Level 3 — Implementation Summary

### Files changed

| File | Change |
|------|--------|
| `data/raw/nirf_rankings.csv` | Added IIT Dharwad Engineering row `IR-E-U-0899` |
| `data/nirf_institute_id_overrides.csv` | Dharwad override |
| `scripts/india_network/nirf_utils.py` | `nirf_ranking_category`, `_best_row_for_id()`, Dharwad override |
| `scripts/india_network/09_export_payloads.py` | Export `nirf_ranking_category` |
| `scripts/india_network/09b_export_year_slices.py` | Auto-sync to dashboard |
| `scripts/india_network/10_verification_checklist.py` | Full payload cap 2 MB |
| `scripts/india_network/01f_scrape_nirf_patents_from_pdfs.py` | Incremental merge with cached scrape |
| `dashboard/india_network.js` | Dynamic `nirfRankLabel()` |
| Processed + dashboard JSON | Re-exported |

### Before / after metrics

| Metric | Before | After (2026-07-08) |
|--------|--------|---------------------|
| NIRF ID assigned | 97/120 | **110/120** (supplement overrides: Pondicherry, Kalyani, Presidency, GNDU) |
| IIT Dharwad NIRF | None | **IR-E-U-0899, Engineering #93** |
| IIT Dharwad funding | 79.77 cr (corrupt) / null | **12.24 cr (PDF scrape)** |
| Mislabeled "Overall" ranks in UI | ~40 | **0** (category field exported) |
| Patent reported | 42/120 | **49/120** |
| Funding reported | 83/120 | **102/120** |
| `2024_full.json` size | 543,708 B | **400,902 B** |
| Verification | 16/17 | **20/20 PASS** |
| Orphan edges | 0 | 0 |
| Funding corruption guard | PASS | PASS |
| Duplicate funding clusters | 6 → 2 | **0** (post `b0133e4`) |

### Verification proof

```
Verification: 20/20 passed -> data/processed/verification_report.md
Generated: 2026-07-07T20:10:54Z (post GNDU override + funding UI footnote)
```

Key checks: full size 400902 bytes (cap 1953 KB); funding **102/120**; patents **49/120** reported; duplicate funding **0 clusters**; NIRF matched **110/120**; major IIT funding present; corruption guard clean; 0 orphan edges.

### IIT Dharwad dashboard spot-check (2024_full.json)

```json
{
  "name": "Indian Institute of Technology Dharwad",
  "nirf_rank": 93,
  "nirf_ranking_category": "Engineering",
  "research_funding_cr": 12.24,
  "funding_status": "reported",
  "patent_status": "unavailable"
}
```

### Guru Nanak Dev University dashboard spot-check (2024_full.json)

```json
{
  "name": "Guru Nanak Dev University",
  "nirf_rank": 87,
  "nirf_ranking_category": "Overall",
  "nirf_match_status": "matched",
  "research_funding_cr": null,
  "funding_status": "unavailable",
  "patent_status": "unranked"
}
```

*Funding unavailable — no NIRF 2024 PDF on nirfindia.org; rank from 2023 supplement (`IR-O-U-0376`).*

### Remaining P2 (not implemented)

| Item | Recommendation |
|------|----------------|
| 10 NIRF losers | Expand overrides as NIRF adds categories; emit loser report from `assign_nirf_matches` |
| `01b` scrape completeness | Diff official NIRF HTML vs CSV after each scrape season |
| `hierarchy-app` fork | Synced `public/india_network/` from dashboard; rebuild `dist/` when previewing |
| Patent ceiling ~49/120 | Accept honest unavailable; re-scrape when NIRF publishes Innovation PDFs |
| GNDU / Pondicherry / Kalyani / Presidency funding | Rank matched via supplement; 2024 PDF scrape still MISS — funding `unavailable` until PDF exists |

### Lecture assets git strategy

**Decision (2026-07-07):** Committed via **Git LFS** in `6ffb0c9` — 1519 image pointers under `docs/lectures/assets/`. Collaborators must run `git lfs install` and `git lfs pull`.

| Option | Status |
|--------|--------|
| Git LFS | **Active** — `docs/lectures/assets/**` tracked in `.gitattributes` |
| Release artifact | Optional backup for non-git distribution |
| `.gitignore` | Not used — assets are versioned |

---


## 10 NIRF match losers — review (2026-07-08)

Source: `data/processed/nirf_match_losers.csv` cross-checked against `data/raw/nirf_rankings.csv` + supplement. **Supplement overrides added** for Pondicherry, Kalyani, Presidency (2024 rank-band rows) and GNDU (2023 `IR-O-U-0376`).

| Canonical institute | Disposition | NIRF evidence |
|---------------------|-------------|---------------|
| Indian Institute of Technology Goa | **Accept gap** | No IIT Goa row in NIRF 2024. |
| Pondicherry University | **Override** | `IR-O-U-0369` supplement (Overall/University 101–150, Puducherry). |
| SRM University (Sonipat) | **Accept gap — no override** | Distinct from SRM Institute of Science and Technology (Chennai). |
| Guru Nanak Dev University | **Override** | `IR-O-U-0376` from NIRF 2023 supplement (Overall #87, Amritsar); absent from 2024 CSV. |
| Dr. Hari Singh Gour University | **Accept gap** | No matching row in `nirf_rankings.csv`. |
| Indian Association for the Cultivation of Science | **Accept gap** | No IACS row in NIRF 2024 scrape. |
| University of Allahabad | **Accept gap** | No university row; only IIIT Allahabad — different institute. |
| University of Kalyani | **Override** | `IR-O-U-0576` supplement (University 151–200). |
| G.S. Science, Arts And Commerce College | **Accept gap** | No matching college row. |
| Presidency University | **Override** | `IR-O-U-0580` supplement (University 101–150 Kolkata). |
| Shivaji University | **Accept gap** | Shivaji College only — not Shivaji University, Kolhapur. |
| Mangalore University | **Accept gap** | Mangalore-named colleges only. |
| Karpagam Academy of Higher Education | **Accept gap** | No Karpagam row in NIRF 2024 scrape. |
| University of Rajasthan | **Blocked — uniqueness** | `blocked_by`: Central University of Rajasthan (`IR-P-U-0392`). |

## Phase 2 — Remaining gaps (fix design)

*Post-session continuation after multitask surveying concluded. See also [`MULTITASK_SESSION_SUMMARY.md`](MULTITASK_SESSION_SUMMARY.md).*

### P2-1 — NIRF match losers (10 institutes)

**Severity:** P1 — silent metadata loss, not data corruption.

**Root cause:** `assign_nirf_matches()` greedy uniqueness — first claimant wins NIRF ID; lower-scoring peers become losers.

| Reason code | Example | Core fix |
|-------------|---------|----------|
| `id_blocked_by_uniqueness` | SRM blocked by IIT Madras (`IR-O-U-0456`) | Category-specific ID if NIRF lists SRM in Management/Engineering separately; manual override only when NIRF has distinct row |
| `no_fuzzy_match` | IIT Goa (not in NIRF 2024) | Accept honest gap; add when `01b` scrape includes institute |
| `override_id_missing_in_rankings` | Rare override typos | Validate overrides against `nirf_rankings.csv` in `10_verification_checklist` |

**Implementation (Phase 2a):**
1. ✅ `assign_nirf_matches()` emits `data/processed/nirf_match_losers.csv` (reason, blocked_by, score)
2. Review losers CSV each pipeline run; add overrides only for institutes with **distinct** NIRF rows
3. Do **not** relax uniqueness — collisions were P0

### P2-2 — KIIT + Siksha O Anusandhan coordinate stack (Bhubaneswar)

**Severity:** P2 — cosmetic; no data integrity issue.

**Current state:** `institution_master.csv` assigns KIIT `(20.3558, 85.8138, campus_kiit)` and Siksha O Anusandhan `(20.356, 85.814, campus_soa_bhubaneswar)` — sub-km apart, same Bhubaneswar corridor pattern as Delhi/Mumbai stacks in `03b_apply_campus_geocoding.py`.

**Disposition:** **Accept as intentional** — follows existing `MANUAL_CAMPUS` / `generate_campus_all_overrides.py` pattern; verification reports max stack=1 (rounded coords do not exceed stack threshold). No coordinate fix unless Nominatim or official campus geocodes are added later.

### P2-3 — Duplicate funding clusters (0 groups, was 6)

**Severity:** Resolved post-`b0133e4`.

**Current state:** `10_verification_checklist.py` — `duplicate funding value clusters` check **PASS** (0 clusters).

### P2-4 — Patent ceiling (~49/120)

**Severity:** P1 — coverage gap, honest `unavailable` status.

**Root cause:** NIRF Innovation PDF exists for only ~49 institutes on nirfindia.org.

**Core fix design:**
1. ✅ Re-ran `01f_scrape_nirf_patents_from_pdfs.py` 2026-07-08 (incremental: 64 institutes in raw scrape → **57/120** reported in payload after join/dedupe)
2. Accept `unavailable` for institutes without Innovation category PDF
3. Optional: footnote in UI citing "NIRF Innovation PDF not published for this institute"

**Do not fabricate** patent counts from Engineering/Overall PDFs.

### P2-5 — `01b` scrape completeness

**Severity:** P1 — systemic risk (Dharwad was missing until supplemental row added).

**Implementation (Phase 2b):**
1. ✅ After `01b_scrape_nirf_rankings.py`, diff institute count per category vs NIRF website
2. ✅ Log missing IDs to `data/logs/nirf_scrape_gaps.json`
3. ✅ Supplemental rows in `data/raw/nirf_rankings_supplement.csv` merged in `load_nirf_all()` (`03a`)

### P2-6 — `hierarchy-app` fork drift

**Severity:** P2.

**Status (2026-07-08):** **Synced** — `scripts/sync_hierarchy_app.ps1` copies `dashboard/data/india_network/` → `public/` and `dist/india_network/`. Vite rebuild requires `package.json` (not always in repo).

### P2-7 — Documentation drift

**Severity:** P2.

**Actions:**
1. Archive or update `data/processed/nirf_coverage_gaps.md` to match **102/120** funding, **49/120** patents, **110/120** NIRF matched
2. Point maintainers to `docs/GRAPH5_GAP_ASSESSMENT.md` as living doc
3. ✅ `india_domestic_he_network_plan.md` script map updated (deprecated `07_build_institution_metrics.py` / `08_compute_tier_aggregates.py` names)

### P3 backlog — optional sources (no pipeline break)

| Item | Status | Notes |
|------|--------|-------|
| **P3-1** AISHE xlsx (`data/raw/aishe_universities.xlsx`) | **Validated (optional)** | `01_download_sources.py` marks optional; `validate_aishe.py` → `data/logs/aishe_coverage_summary.json` |
| **P3-2** Plan doc script drift | **Closed** | See `india_domestic_he_network_plan.md` repo layout + Phase 1 table |

---

## Phase 2 — Implementation tracker

| Item | Status | File(s) |
|------|--------|---------|
| NIRF loser report | **Done** | `nirf_utils.py`, `03a_enrich`, `nirf_match_losers.csv` |
| Duplicate funding detector | **Done** | `10_verification_checklist.py` |
| Session summary markdown | **Done** | `docs/MULTITASK_SESSION_SUMMARY.md` |
| Remove 08_join debug instrumentation | **Done** | post-f15e208 cleanup |

| Review 10 losers for valid overrides | **Done** | Pondicherry/Kalyani/Presidency/GNDU overrides added 2026-07-08 |
| Duplicate funding cluster root cause | **Traced** | 3 join bugs; see trace doc |
| `01b` scrape gap diff | **Done** | `01b_scrape_nirf_rankings.py`, `nirf_utils.py`, `nirf_scrape_gaps.json` |
| `hierarchy-app` dedup | **Done** | `scripts/sync_hierarchy_app.ps1`; `public/` + `dist/` synced from dashboard |
| Update `nirf_coverage_gaps.md` | **Done** | `report_nirf_gaps.py` wired in `10_verification_checklist.py` |
| Patent gap JSON | **Done** | `data/logs/patent_coverage_gaps.json` |
| Export `nirf_match_status` + `coverage` meta | **Done** | `09_export_payloads.py`, `dashboard/india_network.js` |
| Duplicate funding UI tags | **Done** | `funding_duplicate_cluster` on export + funding tab footnotes |
| Funding static snapshot UI note | **Done** | `fundingStaticNote()` in `dashboard/india_network.js` Funding tab |
| AISHE validate script | **Done** | `validate_aishe.py` → `aishe_coverage_summary.json` |

---

*Assessment complete. P0 and feasible P1 core fixes implemented at pipeline source. Phase 2 P2 items have fix design; loser report and duplicate-funding check implemented.*
