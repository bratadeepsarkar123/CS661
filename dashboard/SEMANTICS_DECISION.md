# Locked product decisions (2026-07-12)

## Goal
With data already in the pool, make pool + report + viz semantics consistent. Prefer upgrading data toward original intent only when CSVs already exist or are cheap; otherwise change report/viz to match the river.

## G2 — Q1/Q4
- **NOT doing:** multi-CSV author reconstruction (journal → authors → author country). Too heavy / not the route.
- **DOING:** treat metric as **documents in Q1 vs Q4 journals by publisher country** (SCImago journalrank aggregation already in pool).
- Report + TAP labels must say publisher-country publications, not author nationality.
- Pool already rebuilt from journalrank; teammate updates tap/report wording.

## G1
- Prefer: correct H from SCImago (done in pool); regen UMAP when ready so clusters match corrected features.
- Until UMAP regen: report that positions may still reflect old embedding.

## G3
- Prefer: OpenAlex concept extract already in pool (Quantum ≠ 2500). Tap should use new ids/names.
- Optional later: 1950–99 backfill when API allows.

## G4
- Prefer honesty: 20-country premium in pool. Do not invent 111-country FE without regen from OpenAlex dump.
- Tap/report: domestic vs intl mean citations (not FWCI unless proven).

## G5
- Keep pipeline data; fix labels for static/cumulative fields only.

## Rule of thumb
If we can link existing CSVs to get closer to original story → do it.
If not → rewrite viz + report to what the CSV measures.
