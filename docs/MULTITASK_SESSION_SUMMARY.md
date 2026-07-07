# CS661 Multitask Session — Results Summary

**Date:** 2026-07-07  
**Scope:** Graph 5 (India Domestic HE Network) + dashboard + docs + lecture assets  
**Status:** Multitask surveying concluded; core fixes pushed to `master`.

---

## Executive summary

This session integrated teammate visualizations, eradicated NIRF ID collisions at the pipeline source, repaired corrupt funding attribution, closed Graph 5 gap-assessment P0/P1 items, fixed triad map rendering, and published lecture/theory documentation with Git LFS image assets.

**Verification:** `18/18` checks pass (`data/processed/verification_report.md`) — includes duplicate-funding cluster detector (Phase 2).

---

## Commits on `master` (chronological)

| Commit | Summary |
|--------|---------|
| `d800a15` | Integrate teammate graph updates from `CS661 Project updated.zip` into `dashboard/` |
| `40a71aa` | Fix NIRF institute ID collisions — multi-category matching, uniqueness, name-first funding join |
| `2dd626d` | Repair NIRF funding at source — ID↔name validation in `01d`, PDF scrape, corrupt row rejection |
| `6ffb0c9` | Lecture markdown + **Git LFS** image assets (`docs/lectures/`, ~387 MB) |
| `9eaae0c` | Graph 5 gaps — Dharwad NIRF ID, rank category in UI, patent scrape expansion, verification cap |
| `d1ac9d8` | Fix triad map lines drifting when zoomed out (pixel-offset bug in `india_network.js`) |

---

## Workstream results

### 1. Teammate viz merge (`dashboard/`)

- Updated: `app.js`, `style.css`, `data.js`, `india_network.js`, bundled data JS files, `graph1.html`
- Kept local: `design-preview.html`, pipeline-exported JSON in `dashboard/data/india_network/`
- GitHub Pages redeploys from `master` via workflow

### 2. Graph 5 debugging — IITK patent withheld

- **Root cause:** IIT Jammu wrongly shared Kanpur's NIRF Overall ID `IR-O-I-1075`; patent dedupe kept Jammu alphabetically
- **Lesson:** Per-institute overrides were band-aids; led to source-level fix in `nirf_utils.py`

### 3. NIRF collision eradication (source fix)

| Metric | Before | After |
|--------|--------|-------|
| Duplicate NIRF ID groups | 21 (50 institutes) | **0** |
| `duplicate_resolved` patents | many | **0** |

- Rewrote `assign_nirf_matches()` — campus tokens, category preferences, greedy one-ID-per-institute
- Funding join uses name + token verification, not blind Dataful IDs

### 4. P0 funding repair

- Re-audit confirmed Bhilai/Jammu/Dharwad still corrupt **after** collision fix (Dataful CSV recycled wrong IDs)
- `01d` rejects ID↔name mismatches; `01e` PDF scrape authoritative for major IITs
- Delhi/Kanpur/Hyderabad/Madras now have PDF-sourced funding

### 5. Gap assessment & P0/P1 implementation

See [`GRAPH5_GAP_ASSESSMENT.md`](GRAPH5_GAP_ASSESSMENT.md).

| Metric | Before | After |
|--------|--------|-------|
| NIRF ID assigned | 97/120 | **98/120** |
| Mislabeled "Overall" ranks | ~40 | **0** |
| Patents reported | 42/120 | **51/120** |
| Funding reported | 83/120 | **84/120** |
| Verification | 16/17 | **17/17** |

### 6. Triad line rendering bug

- **Symptom:** Dashed orange triad lines pointed correctly when zoomed in but drifted 33–133 km when zoomed out
- **Cause:** `edgePathLatLngs` applied 14px screen offset → lat/lng conversion at low zoom
- **Fix:** Bind triads to raw institution coordinates like hub/star edges (`d1ac9d8`)

### 7. Documentation & lectures

| Artifact | Path |
|----------|------|
| Pipeline audit (read-only) | `docs/GRAPH5_PIPELINE_AUDIT.md` |
| Gap assessment + fix design | `docs/GRAPH5_GAP_ASSESSMENT.md` |
| Lecture theory → implementation | `docs/CS661_LECTURE_THEORY_TO_IMPLEMENTATION.md` |
| Image-rich lectures (19 PDFs) | `docs/lectures/` + LFS assets |
| Conversion script | `scripts/convert_lecture_pdfs.py` |

---

## Remaining P2 (Phase 2 — in progress)

See [`GRAPH5_GAP_ASSESSMENT.md`](GRAPH5_GAP_ASSESSMENT.md) Phase 2 section.

| Item | Status |
|------|--------|
| NIRF loser report (`nirf_match_losers.csv`) | **Done** — 22 losers logged |
| Duplicate funding detector in verification | **Done** — 6 clusters flagged, 18/18 pass |
| Review losers for valid overrides | Pending manual review |
| `01b` scrape gap diff | Pending |
| `hierarchy-app` fork dedup | Pending |
| Patent ceiling ~51/120 | Accept honest unavailable |

---

## Local dev

```powershell
cd C:\Users\brata\Downloads\CS661\dashboard
python -m http.server 8766
```

Open http://localhost:8766 → Viz 05 (India Network). Hard-refresh after data updates.

**LFS clone:** `git lfs install` then `git lfs pull` for lecture images.

---

## Key docs for agents

1. Start here: `docs/MULTITASK_SESSION_SUMMARY.md` (this file)
2. Data quality: `docs/GRAPH5_GAP_ASSESSMENT.md`
3. Full pipeline audit: `docs/GRAPH5_PIPELINE_AUDIT.md`
4. Course theory mapping: `docs/CS661_LECTURE_THEORY_TO_IMPLEMENTATION.md`
5. Lecture slides: `docs/lectures/README.md`

---

*Session concluded. Continue with Phase 2 gap fixes per `GRAPH5_GAP_ASSESSMENT.md`.*
