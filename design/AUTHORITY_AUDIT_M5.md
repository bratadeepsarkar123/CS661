# Module 5 Authority Audit — Resolution Log

**Initial verdict (Sonnet 4.6 medium):** FAIL  
**Final verdict:** PASS (after fixes below)  
**Verification:** 14/14 passed (`data/processed/verification_report.md`)

## Issues fixed

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | 55 orphan edges in `2024_full.json` | Sort nodes hubs-first; slice 80; rebuild edges on sliced IDs |
| 2 | CRITICAL | 11 orphan edges in overview JSON | Overview edges filtered to `overview_node_ids` (45 nodes, all hubs included) |
| 3 | HIGH | `setYear()` overwrote `cache.full` | Write only to `cache.byYear`; keep 2024 anchor |
| 4 | HIGH | Year slider 404 for missing years | Ran `09b_export_year_slices.py`; `manifest.json` with 10 years |
| 5 | HIGH | Patent dedup grouped on count triple | Dedup by `nirf_patent_source_id` (NIRF institute ID) |
| 6 | MEDIUM | Verification missed payload integrity | Added orphan-edge + manifest checks (11 → 14 checks) |
| 7 | LOW | NIRF rank missing from Publications tab | Added stat row in `buildDetailPanelHtml` |
| 8 | LOW | Stale copy / edge styling | Removed "pilot" text; neutral edge color; focus+context opacity |

## Deferred (design phase, not data bugs)

- Global year slider wiring across all 5 panels (parent dashboard integration)
- Phase 3 plan doc still mentions `2022_*` filenames in one checklist row — update when editing plan

## Recommended Module 5 design choice

**M5-03 Focus Fisheye** + optional **M5-08 integrity header** — see `design/MODULE5_INDEX.md`
