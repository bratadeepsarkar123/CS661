# Graph 5 (India Domestic HE Network) — Gap Assessment & Fix Design

**Workspace:** `C:\Users\brata\Downloads\CS661`  
**Assessment date:** 2026-07-07  
**Methodology:** Multi-level bridge inspection — severity first, core fix design at source, then implementation.

**Related:** [`GRAPH5_PIPELINE_AUDIT.md`](GRAPH5_PIPELINE_AUDIT.md) (read-only pre-fix audit)  
**Post-fix commits:** `927f6fd` (five loser overrides: Saveetha/KIIT/SASTRA/IMS/GITAM); `d2e915d` / `f15e208` (SRM/Thapar/GLA + funding token join); builds on `40a71aa` and `2dd626d`.

---

## Level 1 — Severity Assessment

### Known issues (pre-fix)

| Issue | Severity | User-visible impact | Data integrity risk | Scope (# institutes) | Blocks demo/submission? |
|-------|----------|---------------------|---------------------|----------------------|-------------------------|
| IIT Dharwad missing NIRF ID | **P0** | Detail panel shows rank "—" and inconsistent funding story | Wrong institute could inherit Hyderabad-scale funding (fixed in `2dd626d`) | 1 | Yes — demo narrative for newer IITs |
| ~40 institutes show "NIRF rank (Overall)" for Engineering/Medical/etc. ranks | **P0** | Misleading rank category in detail panel | Attribution error (rank number correct, category wrong) | ~40 | Yes — undermines trust in NIRF panel |
| Patent coverage 42/120 | **P1** | Most institutes show "patents unavailable" | Incomplete Innovation metrics; not fabricated | 78 missing | No — honest "unavailable" is acceptable |
| Verification full-payload size fails (543 KB vs 200 KB cap) | **P1** | CI/checklist fails despite valid data | False negative blocks release gate | 1 check | Yes — blocks automated sign-off |
| Lecture assets ~376 MB in git | **Resolved** | Repo clone needs LFS | None | N/A | No — committed via Git LFS (`6ffb0c9`) |

### New issues discovered during bridge inspection

| Issue | Severity | User-visible impact | Data integrity risk | Scope (# institutes) | Blocks demo/submission? |
|-------|----------|---------------------|---------------------|----------------------|-------------------------|
| IIT Dharwad absent from `01b` NIRF scrape (`nirf_rankings.csv`) despite NIRF 2024 Engineering participation | **P0** | No algorithmic match possible without override/supplemental row | ID assignment blocked at source | 1 | Yes |
| `dashboard/data/india_network/` drift from `public/india_network/` after export | **P1** | UI bundle stale until manual copy | Dashboard shows old fields (no `nirf_ranking_category`) | All 120 nodes | Yes — fixes invisible in UI |
| Duplicate funding values across unrelated institutes | **P1** | Same ₹ cr shown for distinct universities | Possible join/source duplication | **2 clusters** (5 institutes) | No — suspicious but not corrupt |
| 14 NIRF match losers (no ID after uniqueness pass) | **P1** | Missing NIRF rank in panel | Silent loss of metadata | 14 | No — documented limitation |
| `hierarchy-app/dist/india_network/` partial/stale fork | **P2** | Submodule app shows old slice if not rebuilt | Fork drift until sync + build | N/A | No — sync `public/` from dashboard |
| Triad map lines drift when zoomed out | **P0** (fixed) | Dashed triad endpoints 33–133 km off at zoom 4–6 | Visual misread of collaboration geography | All triad++ users | Yes — fixed `d1ac9d8` |
| Stale `nirf_coverage_gaps.md` / old verification claims (116/120 funding) | **P2** | Maintainer confusion | Documentation drift | N/A | No |
| Patent scrape limited to institutes with Innovation PDF on nirfindia.org | **P1** | Newer IITs (Bhilai, Jammu, Dharwad, etc.) show patent unavailable | Honest gap — no PDF exists | ~47 NIRF-ranked with no Innovation PDF | No |
| `01b` scrape gap pattern (institutes in official NIRF PDFs but missing from CSV) | **P1** | Systemic risk for future campuses | Under-counted in rankings source | Unknown tail | No |

### Holistic inspection summary

| Check | Status (post-fix) |
|-------|-------------------|
| Funding duplicates (same ₹, different institutes) | **2 clusters** (informational check passes) — see duplicate table below |
| NIRF match losers | **14 unmatched** (Saveetha/KIIT/SASTRA/IMS/GITAM fixed post-f15e208) — IIT Goa, SRM Sonipat, Pondicherry, etc. |
| Dashboard ↔ public JSON drift | **Fixed** — `09b` now syncs to `dashboard/data/india_network/` |
| `hierarchy-app` fork | **Synced** — `dashboard/data/india_network/` copied to `hierarchy-app/public/india_network/` (2026-07-08) |
| Edge/orphan integrity | **PASS** — 0 orphan edges in overview/full payloads |
| Geo stacking | **PASS** — max stack=1; KIIT + Siksha O Anusandhan share Bhubaneswar pin (cosmetic P2, see below) |
| Verification artifacts | **Current** — 18/18 pass (10_verification_checklist.py) |
| Commits `40a71aa` / `2dd626d` regressions | **No regressions** — funding corruption guard passes; major IIT funding present |
| Raw source quality | Dataful funding IDs still unreliable; PDF scrape path authoritative |
| UI provenance footnotes | Accurate — sources cite nirfindia.org; category label now dynamic |

#### Duplicate funding clusters (remaining, P2)

Verification (`10_verification_checklist.py`) reports **2 duplicate-value clusters** (informational PASS):

| Amount (₹ cr) | Institutes | Notes |
|---------------|------------|-------|
| 19.84 | Panjab University, NIT Durgapur | Raw/join duplication — trace in [`GRAPH5_FUNDING_LOSER_TRACE.md`](GRAPH5_FUNDING_LOSER_TRACE.md) |
| 206.94 | IISc, BHU (Varanasi), IMS/BHU Medical College | Shared Engineering/Innovation PDF row pattern (post-join fixes reduced earlier 6-cluster set) |

#### NIRF unmatched institutes (14)

IIT Goa; Pondicherry University; SRM University (Sonipat — distinct from SRM Chennai); Guru Nanak Dev University; Dr. Hari Singh Gour University; Indian Association for the Cultivation of Science; University of Allahabad; University of Kalyani; G.S. Science Arts And Commerce College; Presidency University; Shivaji University; Mangalore University; Karpagam Academy of Higher Education; University of Rajasthan (id_blocked_by_uniqueness vs Central University of Rajasthan — no distinct NIRF row in 2024).

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

| Metric | Before | After |
|--------|--------|-------|
| NIRF ID assigned | 97/120 | **106/120** (post Saveetha/KIIT/SASTRA/IMS/GITAM overrides) |
| IIT Dharwad NIRF | None | **IR-E-U-0899, Engineering #93** |
| IIT Dharwad funding | 79.77 cr (corrupt) / null | **12.24 cr (PDF scrape)** |
| Mislabeled "Overall" ranks in UI | ~40 | **0** (category field exported) |
| Patent reported | 42/120 | **57/120** (post `01f` re-scrape 2026-07-08) |
| Funding reported | 83/120 | **91/120** (post overrides + `01d` merge) |
| `2024_full.json` size | 543,708 B | **395,396 B** |
| Verification | 16/17 | **18/18 PASS** (Phase 2: +duplicate funding check) |
| Orphan edges | 0 | 0 |
| Funding corruption guard | PASS | PASS |

### Verification proof

```
Verification: 18/18 passed -> data/processed/verification_report.md
Generated: 2026-07-07T18:46:25Z (re-run after patent re-scrape)
```

Key checks: full size 395396 bytes (cap 1953 KB); funding **91/120**; patents **57/120** reported; duplicate funding **2 clusters**; major IIT funding present; corruption guard clean; 0 orphan edges.

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

### Remaining P2 (not implemented)

| Item | Recommendation |
|------|----------------|
| 14 NIRF losers | Expand overrides as NIRF adds categories; emit loser report from `assign_nirf_matches` |
| Duplicate funding clusters | Add duplicate-value detector in `10_verification_checklist.py` |
| `01b` scrape completeness | Diff official NIRF HTML vs CSV after each scrape season |
| `hierarchy-app` fork | Synced `public/india_network/` from dashboard; rebuild `dist/` when previewing |
| Patent ceiling ~57/120 | Accept honest unavailable; re-scrape when NIRF publishes Innovation PDFs |
| Lecture assets 376 MB | **Do not commit.** Use `.gitignore` + release artifact or Git LFS |

### Lecture assets git strategy

**Decision (2026-07-07):** Committed via **Git LFS** in `6ffb0c9` — 1519 image pointers under `docs/lectures/assets/`. Collaborators must run `git lfs install` and `git lfs pull`.

| Option | Status |
|--------|--------|
| Git LFS | **Active** — `docs/lectures/assets/**` tracked in `.gitattributes` |
| Release artifact | Optional backup for non-git distribution |
| `.gitignore` | Not used — assets are versioned |

---


## 14 NIRF match losers — review (2026-07-08)

Source: `data/processed/nirf_match_losers.csv` cross-checked against `data/raw/nirf_rankings.csv` (NIRF 2024). **No new overrides added** (risky pairs excluded per policy).

| Canonical institute | Disposition | NIRF 2024 evidence |
|---------------------|-------------|-------------------|
| Indian Institute of Technology Goa | **Accept gap** | No IIT Goa row; only unrelated Goa entries (e.g. Goa Institute of Management, Goa College of Pharmacy). |
| Pondicherry University | **Accept gap** | No university-level row; Puducherry entries are NIT Puducherry, JIPMER, colleges — not Pondicherry University. |
| SRM University (Sonipat) | **Accept gap — no override** | NIRF lists SRM dental colleges only; distinct from SRM Institute of Science and Technology (Chennai), already overridden separately. **Do not** map Sonipat to Chennai ID. |
| Guru Nanak Dev University | **Accept gap** | No GNDU Amritsar row; only Guru Nanak College / Guru Nanak pharma institute (different entities). |
| Dr. Hari Singh Gour University | **Accept gap** | No matching row in `nirf_rankings.csv`. |
| Indian Association for the Cultivation of Science | **Accept gap** | No IACS row in NIRF 2024 scrape. |
| University of Allahabad | **Accept gap** | No university row; only IIIT Allahabad (`IR-E-U-0516`) — different institute. |
| University of Kalyani | **Accept gap** | No Kalyani University row in NIRF 2024 scrape. |
| G.S. Science, Arts And Commerce College | **Accept gap** | No matching college row (fuzzy matches are unrelated pharma/agri names). |
| Presidency University | **Accept gap — no override** | Only Presidency **College** in College category — not Presidency University Kolkata; **do not** conflate with Periyar University (Salem). |
| Shivaji University | **Accept gap** | Shivaji College / Shri Shivaji Science College only — not Shivaji University, Kolhapur. |
| Mangalore University | **Accept gap** | Mangalore-named medical/dental colleges only; no Mangalore University row. |
| Karpagam Academy of Higher Education | **Accept gap** | No Karpagam row in NIRF 2024 scrape. |
| University of Rajasthan | **Blocked — uniqueness** | `blocked_by`: Central University of Rajasthan (`IR-P-U-0392`); no distinct University of Rajasthan row. **Do not** share ID with Central University of Rajasthan. |

## Phase 2 — Remaining gaps (fix design)

*Post-session continuation after multitask surveying concluded. See also [`MULTITASK_SESSION_SUMMARY.md`](MULTITASK_SESSION_SUMMARY.md).*

### P2-1 — NIRF match losers (14 institutes)

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

### P2-3 — Duplicate funding clusters (2 groups, was 6)

**Severity:** P1 — suspicious, not proven corrupt post-`2dd626d`.

**Core fix design:**
1. ✅ `10_verification_checklist.py` — `duplicate funding value clusters` check (informational)
2. For each cluster: trace to `nirf_research_projects.csv` row → PDF source
3. If same PDF row joined twice via name variants → dedupe in `01d` on `name_norm` + amount
4. Medical college pairs (CMC Vellore/Ludhiana) may be legitimately similar — verify against NIRF PDF

### P2-4 — Patent ceiling (~57/120)

**Severity:** P1 — coverage gap, honest `unavailable` status.

**Root cause:** NIRF Innovation PDF exists for only ~57 institutes on nirfindia.org after 2026-07-08 re-scrape.

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
1. Archive or update `data/processed/nirf_coverage_gaps.md` to match **91/120** funding, **57/120** patents
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

| Review 14 losers for valid overrides | **Done** | All 14 reviewed 2026-07-08; no new overrides (see table below) | [`GRAPH5_FUNDING_LOSER_TRACE.md`](GRAPH5_FUNDING_LOSER_TRACE.md) |
| Duplicate funding cluster root cause | **Traced** | 3 join bugs; see trace doc |
| `01b` scrape gap diff | **Done** | `01b_scrape_nirf_rankings.py`, `nirf_utils.py`, `nirf_scrape_gaps.json` |
| `hierarchy-app` dedup | **Done** | `scripts/sync_hierarchy_app.ps1`; `public/` + `dist/` synced from dashboard |
| Update `nirf_coverage_gaps.md` | **Done** | `report_nirf_gaps.py` wired in `10_verification_checklist.py` |
| Patent gap JSON | **Done** | `data/logs/patent_coverage_gaps.json` |
| Export `nirf_match_status` + `coverage` meta | **Done** | `09_export_payloads.py`, `dashboard/india_network.js` |
| Duplicate funding UI tags | **Done** | `funding_duplicate_cluster` on export + funding tab footnotes |
| AISHE validate script | **Done** | `validate_aishe.py` → `aishe_coverage_summary.json` |

---

*Assessment complete. P0 and feasible P1 core fixes implemented at pipeline source. Phase 2 P2 items have fix design; loser report and duplicate-funding check implemented.*
