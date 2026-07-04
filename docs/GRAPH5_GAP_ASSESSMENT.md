# Graph 5 (India Domestic HE Network) — Gap Assessment & Fix Design

**Workspace:** `C:\Users\brata\Downloads\CS661`  
**Assessment date:** 2026-07-07  
**Methodology:** Multi-level bridge inspection — severity first, core fix design at source, then implementation.

**Related:** [`GRAPH5_PIPELINE_AUDIT.md`](GRAPH5_PIPELINE_AUDIT.md) (read-only pre-fix audit)  
**Post-fix commits:** This work builds on `40a71aa` (NIRF collision fix) and `2dd626d` (funding ID validation + PDF scrape).

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
| Duplicate funding values across unrelated institutes | **P1** | Same ₹ cr shown for distinct universities | Possible join/source duplication | 6 clusters (12 institutes) | No — suspicious but not corrupt |
| 22 NIRF match losers (no ID after uniqueness pass) | **P1** | Missing NIRF rank in panel | Silent loss of metadata | 22 | No — documented limitation |
| `hierarchy-app/dist/india_network/` partial/stale fork | **P2** | Submodule app shows old 2024 slice only | Fork drift | N/A | No |
| Triad map lines drift when zoomed out | **P0** (fixed) | Dashed triad endpoints 33–133 km off at zoom 4–6 | Visual misread of collaboration geography | All triad++ users | Yes — fixed `d1ac9d8` |
| Stale `nirf_coverage_gaps.md` / old verification claims (116/120 funding) | **P2** | Maintainer confusion | Documentation drift | N/A | No |
| Patent scrape limited to institutes with Innovation PDF on nirfindia.org | **P1** | Newer IITs (Bhilai, Jammu, Dharwad, etc.) show patent unavailable | Honest gap — no PDF exists | ~47 NIRF-ranked with no Innovation PDF | No |
| `01b` scrape gap pattern (institutes in official NIRF PDFs but missing from CSV) | **P1** | Systemic risk for future campuses | Under-counted in rankings source | Unknown tail | No |

### Holistic inspection summary

| Check | Status (post-fix) |
|-------|-------------------|
| Funding duplicates (same ₹, different institutes) | **6 clusters remain** — see duplicate table below |
| NIRF match losers | **22 unmatched** — IIT Goa, SRM, Saveetha, KIIT, etc. |
| Dashboard ↔ public JSON drift | **Fixed** — `09b` now syncs to `dashboard/data/india_network/` |
| `hierarchy-app` fork | **Stale** — only 3 files under `hierarchy-app/public/india_network/` |
| Edge/orphan integrity | **PASS** — 0 orphan edges in overview/full payloads |
| Geo stacking | **PASS** — max stack=1 (improved from audit's stack=2 note) |
| Verification artifacts | **Current** — `data/logs/verification_report.json` 17/17 pass |
| Commits `40a71aa` / `2dd626d` regressions | **No regressions** — funding corruption guard passes; major IIT funding present |
| Raw source quality | Dataful funding IDs still unreliable; PDF scrape path authoritative |
| UI provenance footnotes | Accurate — sources cite nirfindia.org; category label now dynamic |

#### Duplicate funding clusters (remaining, P2)

| Amount (₹ cr) | Institutes | Likely cause |
|---------------|------------|--------------|
| 197.08 | IISc, AIIMS Delhi, IMS Varanasi | Shared raw row / name collision |
| 35.37 | IIT BHU Varanasi, IIT Bhilai | Engineering PDF pattern overlap |
| 19.84 | Panjab University, NIT Durgapur | Raw duplication |
| 18.53 | CMC Vellore, CMC Ludhiana | Related medical colleges |
| 15.65 | IIT Mandi, IIT ISM Dhanbad | Scrape/join overlap |
| 0.62 | University of Rajasthan, Central Univ. Rajasthan | Entity confusion |

#### NIRF unmatched institutes (22)

IIT Goa; Saveetha University; SRM Institute of Science & Technology; University of Rajasthan; Institute of Medical Sciences; KIIT University; Pondicherry University; SRM University; Thapar Institute; Guru Nanak Dev University; Dr. Hari Singh Gour University; GITAM University; IACS Kolkata; University of Allahabad; University of Kalyani; G.S. Science Arts And Commerce College; Presidency University; GLA University; Shivaji University; SASTRA University; Mangalore University; Karpagam Academy of Higher Education.

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
| NIRF ID assigned | 97/120 | **98/120** |
| IIT Dharwad NIRF | None | **IR-E-U-0899, Engineering #93** |
| IIT Dharwad funding | 79.77 cr (corrupt) / null | **12.24 cr (PDF scrape)** |
| Mislabeled "Overall" ranks in UI | ~40 | **0** (category field exported) |
| Patent reported | 42/120 | **51/120** |
| Funding reported | 83/120 | **84/120** |
| `2024_full.json` size | 543,708 B | **395,396 B** |
| Verification | 16/17 | **18/18 PASS** (Phase 2: +duplicate funding check) |
| Orphan edges | 0 | 0 |
| Funding corruption guard | PASS | PASS |

### Verification proof

```
Verification: 17/17 passed -> data/processed/verification_report.md
Generated: 2026-07-07T17:22:39Z
```

Key checks: full size 395396 bytes (cap 1953 KB); funding 84/120; major IIT funding present; corruption guard clean; 0 orphan edges.

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
| 22 NIRF losers | Expand overrides as NIRF adds categories; emit loser report from `assign_nirf_matches` |
| Duplicate funding clusters | Add duplicate-value detector in `10_verification_checklist.py` |
| `01b` scrape completeness | Diff official NIRF HTML vs CSV after each scrape season |
| `hierarchy-app` fork | Point at `dashboard/data/india_network` or remove duplicate |
| Patent ceiling ~51/120 | Accept honest unavailable; re-scrape when NIRF publishes Innovation PDFs |
| Lecture assets 376 MB | **Do not commit.** Use `.gitignore` + release artifact or Git LFS |

### Lecture assets git strategy

**Decision (2026-07-07):** Committed via **Git LFS** in `6ffb0c9` — 1519 image pointers under `docs/lectures/assets/`. Collaborators must run `git lfs install` and `git lfs pull`.

| Option | Status |
|--------|--------|
| Git LFS | **Active** — `docs/lectures/assets/**` tracked in `.gitattributes` |
| Release artifact | Optional backup for non-git distribution |
| `.gitignore` | Not used — assets are versioned |

---

## Phase 2 — Remaining gaps (fix design)

*Post-session continuation after multitask surveying concluded. See also [`MULTITASK_SESSION_SUMMARY.md`](MULTITASK_SESSION_SUMMARY.md).*

### P2-1 — NIRF match losers (22 institutes)

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

### P2-2 — Duplicate funding clusters (6 groups)

**Severity:** P1 — suspicious, not proven corrupt post-`2dd626d`.

**Core fix design:**
1. ✅ `10_verification_checklist.py` — `duplicate funding value clusters` check (informational)
2. For each cluster: trace to `nirf_research_projects.csv` row → PDF source
3. If same PDF row joined twice via name variants → dedupe in `01d` on `name_norm` + amount
4. Medical college pairs (CMC Vellore/Ludhiana) may be legitimately similar — verify against NIRF PDF

### P2-3 — Patent ceiling (~51/120)

**Severity:** P1 — coverage gap, honest `unavailable` status.

**Root cause:** NIRF Innovation PDF exists for only ~51 institutes on nirfindia.org.

**Core fix design:**
1. Re-run `01f_scrape_nirf_patents_from_pdfs.py` each pipeline season (incremental merge already implemented)
2. Accept `unavailable` for institutes without Innovation category PDF
3. Optional: footnote in UI citing "NIRF Innovation PDF not published for this institute"

**Do not fabricate** patent counts from Engineering/Overall PDFs.

### P2-4 — `01b` scrape completeness

**Severity:** P1 — systemic risk (Dharwad was missing until supplemental row added).

**Implementation (Phase 2b):**
1. ✅ After `01b_scrape_nirf_rankings.py`, diff institute count per category vs NIRF website
2. ✅ Log missing IDs to `data/logs/nirf_scrape_gaps.json`
3. ✅ Supplemental rows in `data/raw/nirf_rankings_supplement.csv` merged in `load_nirf_all()` (`03a`)

### P2-5 — `hierarchy-app` fork drift

**Severity:** P2.

**Core fix design:**
1. **Preferred:** Remove duplicate `hierarchy-app/public/india_network/`; document that `dashboard/` is canonical
2. **Alternative:** Symlink or build step copying `dashboard/data/india_network/` → hierarchy-app

### P2-6 — Documentation drift

**Severity:** P2.

**Actions:**
1. Archive or update `data/processed/nirf_coverage_gaps.md` to match 84/120 funding, 51/120 patents
2. Point maintainers to `docs/GRAPH5_GAP_ASSESSMENT.md` as living doc

---

## Phase 2 — Implementation tracker

| Item | Status | File(s) |
|------|--------|---------|
| NIRF loser report | **Done** | `nirf_utils.py`, `03a_enrich`, `nirf_match_losers.csv` |
| Duplicate funding detector | **Done** | `10_verification_checklist.py` |
| Session summary markdown | **Done** | `docs/MULTITASK_SESSION_SUMMARY.md` |
| Review 22 losers for valid overrides | **Traced** | [`GRAPH5_FUNDING_LOSER_TRACE.md`](GRAPH5_FUNDING_LOSER_TRACE.md) — 5 overrides recommended |
| Duplicate funding cluster root cause | **Traced** | 3 join bugs; see trace doc |
| `01b` scrape gap diff | **Done** | `01b_scrape_nirf_rankings.py`, `nirf_utils.py`, `nirf_scrape_gaps.json` |
| `hierarchy-app` dedup | Pending | remove stale fork |
| Update `nirf_coverage_gaps.md` | Pending | `data/processed/` |

---

*Assessment complete. P0 and feasible P1 core fixes implemented at pipeline source. Phase 2 P2 items have fix design; loser report and duplicate-funding check implemented.*
