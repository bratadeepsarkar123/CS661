# Graph 5 Manual Verification Guide

Hard-test any value shown on the India Domestic HE Network dashboard by tracing it through **raw → processed → export JSON → UI**. Use `scripts/india_network/verify_graph5_display.py` for targeted checks; use `run_random_spot_check.py` for stratified regression sampling.

---

## Quick start

```bash
# Collaboration edge between two institutes (year slice + JSON rollup note)
python scripts/india_network/verify_graph5_display.py --pair "IIT Kanpur" "IIT Indore" --year 2024

# Direct partners for one institute
python scripts/india_network/verify_graph5_display.py --institute "IIT Kanpur" --year 2024 --field partners

# Scalar groups (year slider maps funding/patents; ranks static)
python scripts/india_network/verify_graph5_display.py --institute "IIT Kanpur" --field funding
python scripts/india_network/verify_graph5_display.py --institute "IIT Kharagpur" --field funding --year 2020
python scripts/india_network/verify_graph5_display.py --institute "IIT Kharagpur" --field funding --year 2023

# Optional machine-readable output
python scripts/india_network/verify_graph5_display.py --institute "IIT Hyderabad" --field funding --json-out data/logs/verify_funding.json
```

Institute names accept **UUID** (`institution_id`), full canonical names, or shorthand (**`IIT Kanpur`** expands to *Indian Institute of Technology Kanpur*).

---

## What each displayed metric maps to

| UI element | Processed source | Raw / upstream | Export JSON field | Year slider? |
|------------|------------------|----------------|-------------------|--------------|
| Map nodes (position) | `institution_master.csv` (`lat`/`lon` from `03b_apply_campus_geocoding.py`) | `india_higher_education.csv`, Nominatim | `nodes[].lat`, `nodes[].lon` | No |
| Node color (tier) | `institution_master.csv` `tier` | AISHE / manual overrides | `nodes[].tier`, `nodes[].color` | No |
| Node size (∝ √publications) | `institution_master.csv` `total_works` | OpenAlex institution works | `nodes[].radius` (export formula); **UI** `markerRadius()` in `india_network.js` uses a different formula | No |
| Hub ring | `hub_flags.csv` | `06_build_domestic_edges.py` degree + corridor rules | `nodes[].is_hub` | No |
| Collaboration edges / partner list | `collaboration_edges_full.csv` | `domestic_works.parquet` ← `works_raw.parquet` ← OpenAlex cache | `edges[]` (`source`, `target`, `weight`, `citation_weight`) | **Yes** — filtered by `year` in CSV; JSON loaded per `{year}_full.json` |
| Edge weight (co-publication count) | `collaboration_edges_full.csv` `weight` | Count of domestic filtered works with both institutes | `edges[].weight` | Yes |
| Citation weight | `collaboration_edges_full.csv` `citation_weight` | Sum of `cited_by_count` on those works | `edges[].citation_weight` | Yes |
| Triad++ sidebar | `collaboration_triads.parquet` | 3+ institution papers from `domestic_works` | `triads[focus_id]` | Yes |
| NIRF rank + category | `institution_master.csv` | `data/raw/nirf_rankings.csv` via `03a_enrich_institution_master.py` | `nodes[].nirf_rank`, `nirf_ranking_category`, `nirf_match_status` | No |
| Research funding (₹ Cr) | `institution_funding_by_year.csv` | `nirf_research_projects.csv` (+ PDF scrape `01e`) via `08_join_nirf_funding.py` | `nodes[].research_funding_cr`, `funding_academic_year`, `sponsored_projects`, `funding_status` | **Yes** — mapped academic year (2020-21 / 2021-22 / 2022-23) |
| Patents published / granted | `institution_patents_by_year.csv` | `nirf_patents_scraped.csv` via `08b_join_nirf_patents.py` | `nodes[].patents_*`, `patent_calendar_year`, `patent_status` | **Yes** — mapped calendar year (2020 / 2021 / 2022) |
| SCImago impact % | `institution_quality_static.csv` | `scimago_india.csv` via `07_join_scimago_quality.py` | `nodes[].scimago_pct`, `scimago_year` (2019) | No |
| Tier summary panel | Aggregated in `09_export_payloads.tier_summary()` | Same node fields | `tier_summary`, `tier_panels` | Funding/quality static; works/edges year-specific |

### Collaboration edge pipeline (trace chain)

```
OpenAlex works cache
  -> 05_fetch_openalex_works.py / 05b_assemble_works_from_cache.py
  -> data/processed/works_raw.parquet
  -> 06_build_domestic_edges.py (filters W1-W5, pair per publication year)
  -> data/processed/domestic_works.parquet
  -> data/processed/collaboration_edges_full.csv
  -> 09_export_payloads.py / 09b_export_year_slices.py
  -> dashboard/data/india_network/{year}_full.json
  -> dashboard/india_network.js (sort partners, draw edges)
```

### Export caps (important for partner checks)

`09_export_payloads.build_edges()` keeps at most **300** edges (`MAX_EDGES_FULL`) network-wide, sorted by weight. An institute may have dozens of processed partners but only the **top edges present in the payload** appear in JSON. The verify script compares **weights for common partners** and warns about cap-related omissions — it does not fail solely because JSON has fewer partners.

### Year slider: `2024_full.json`

`09b_export_year_slices.py` writes per-year files including a **true calendar-year 2024 slice** (`year: 2024`). `all_years_full.json` remains the cumulative rollup. Default panel loads `2024_full.json`.

Funding and patents **change with the slider** within available NIRF years (see mapping table in [`GRAPH5_GAP_ASSESSMENT.md`](GRAPH5_GAP_ASSESSMENT.md)). NIRF rank and SCImago remain static.

**Worked example — funding varies by slider:**

| Institute | 2020 slice | 2023 slice |
|-----------|------------|------------|
| IIT Kharagpur | ₹102.7 Cr (2020-21) | ₹193.8 Cr (2022-23) |

```bash
python scripts/india_network/verify_graph5_display.py --institute "IIT Kharagpur" --field funding --year 2020
python scripts/india_network/verify_graph5_display.py --institute "IIT Kharagpur" --field funding --year 2023
```

---

## Worked example: IIT Kanpur ↔ IIT Indore (2024)

```bash
python scripts/india_network/verify_graph5_display.py --pair "IIT Kanpur" "IIT Indore" --year 2024
```

**Summary (2026-07-08 run): PASS**

| Layer | Source | Value | Match? |
|-------|--------|-------|--------|
| Processed (year 2024) | `collaboration_edges_full.csv` row 7365 | weight=6, citation_weight=19 | n/a |
| Processed (all-years rollup) | CSV sum across years | weight=95, citation_weight=1742 | n/a |
| Export JSON | `dashboard/data/india_network/2024_full.json` | weight=95, citation_weight=1742 | **yes** |
| Raw | `domestic_works.parquet` | 6 co-authored works in 2024 | yes |
| UI-only | `india_network.js` | edge thickness ~ weight | n/a |

Calendar-year 2024 co-publications: **6 papers**. The dashboard file `2024_full.json` shows the **all-years** weight (95) because of the panel-default copy noted above.

---

## Verification runs (deliverable checklist)

| Check | Command | Result |
|-------|---------|--------|
| IITK ↔ IITI edge | `--pair "IIT Kanpur" "IIT Indore" --year 2024` | **PASS** |
| IIT Hyderabad funding | `--institute "IIT Hyderabad" --field funding` | **PASS** (₹79.775 Cr, 315 sponsored projects, AY 2022-23) |
| IIT Palakkad patents | `--institute "IIT Palakkad" --field patents` | **PASS** (2 published, 2 granted, calendar year 2022) |

No pipeline bugs found during this harness build; the IITK–IITI year-slice vs JSON rollup behavior is **by design** in `09b_export_year_slices.py`, not a data error.

---

## How this complements `run_random_spot_check.py`

| Tool | Purpose |
|------|---------|
| **`verify_graph5_display.py`** | **Manual, deterministic** trace for a named institute, field, or pair. Prints layer table and exit code 0/1. Use when debugging a specific UI number or answering "where does this come from?" |
| **`run_random_spot_check.py`** | **Stratified random** sample (12 institutes × 9 fields) with raw NIRF PDF row refs. Use after pipeline changes for regression confidence. |

Spot-check seed is logged in `data/logs/random_spot_check_report.md`. Re-run with the same `--seed` to reproduce.

---

## Metrics covered by `--field`

| `--field` | Subfields checked |
|-----------|-------------------|
| `partners` | Partner set + weights (processed vs JSON, cap-aware) |
| `funding` | `research_funding_cr`, `total_expenditure_cr`, `sponsored_projects`, `funding_academic_year`, `funding_status` |
| `patents` | `patents_published`, `patents_granted`, `patent_calendar_year`, `patent_status` |
| `nirf_rank` | `nirf_rank`, `nirf_ranking_category`, `nirf_match_status` |
| `scimago` | `scimago_pct`, `scimago_year` |
| `node` | `total_works`, `is_hub`, `radius`, `tier` (+ UI `markerRadius` note) |

Pair mode checks `weight` and `citation_weight` for a single edge.

---

## Related docs

- [`GRAPH5_GAP_ASSESSMENT.md`](GRAPH5_GAP_ASSESSMENT.md) — known gaps and fix status  
- [`GRAPH5_PIPELINE_AUDIT.md`](GRAPH5_PIPELINE_AUDIT.md) — historical pipeline map  
- [`data/processed/verification_report.md`](../data/processed/verification_report.md) — automated 20-check checklist  
