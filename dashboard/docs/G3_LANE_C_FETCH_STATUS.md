# G3 Lane C fetch status

**Date:** 2026-07-12  
**Lane:** `L3_college_cross_domain` (default live race)  
**Plan:** [`G3_SAME_LEVEL_COMPETITION_PLAN.md`](G3_SAME_LEVEL_COMPETITION_PLAN.md) · [`g3_level_sets.json`](g3_level_sets.json)

---

## Live pool now (exactly 7)

| # | Display name | Concept ID | Level | River | Pool years |
|--:|--------------|------------|------:|:-----:|:-----------|
| 1 | Infectious disease | `C524204448` | 3 | pre-existing | 1974–2024 |
| 2 | Robotics | `C34413123` | 3 | pre-existing | 1974–2024 |
| 3 | Quantum computer | `C58053490` | 3 | pre-existing | 1974–2024 |
| 4 | CRISPR | `C98108389` | 3 | pre-existing | 1974–2024 |
| 5 | Energy storage | `C73916439` | 3 | **fetched** | 1974–2024 |
| 6 | Photovoltaics | `C542589376` | 3 | **fetched** | 1974–2024 |
| 7 | Quantum information | `C169699857` | 3 | **fetched** | 1974–2024 (1975 empty = 0 works) |

**Dropped from live pool (still in river CSV for other lanes):**

| ID | Name | Why dropped |
|----|------|-------------|
| `C119857082` | Machine learning | L1 school-level |
| `C2522767166` | Data science | L1 school-level |
| `C188573790` | Renewable energy | L2 mid-college |
| `C154945302` | Artificial intelligence | forbidden mega-AI |

---

## Fetch completeness

| Metric | Value |
|--------|------:|
| Run | `fetch_topics_full.py --years 1974-2024 --topics "Energy storage,Photovoltaics,Quantum information" --workers 2 --sleep 0.45` |
| Queued / fetched | **153 / 153** |
| Rows appended this run | **6644** |
| Empty year pairs | **1** — `C169699857` / **1975** (0 country groups; treated as complete series with count 0) |
| Errors | **0** |
| Auth | KeyPool from `.env` (`OPENALEX_API_KEY` / `OPENALEX_API_KEYS`); auto-started on highest `daily_remaining_usd` (**key#2/3**); rotated on 429 |
| Remaining after run | ~**0.92** USD on active key (G4 expand left running) |
| Entity layer | OpenAlex **concepts** only (`concepts.id:C…`) — no ASJC / Topics scraper |

Resume-safe artifacts:

- `CS661_Dataset/raw_vault/04_openalex/topics_full/openalex_topic_country_year.csv`
- `…/fetched_empty.json`
- `…/progress.json`
- Synced → `READY_FOR_TEAM/openalex_topic_country_year.csv` (+ map + empty markers)

---

## Rebuild / UI

| Step | Status |
|------|:------:|
| `_river_to_pool_rebuild.py` allowlist → Lane C 7 IDs | done |
| Match river by **concept id** (old dashboard labels aliased) | done |
| `viz3_data.js` rebuilt | done (`year_min=1974`, 17882 pool rows) |
| `g3.js` names / colors / order / honesty + school-college note | done |
| `g3.css` `--g-pv` / `--g-qi` | done |
| Cache-bust `index.html` (`?v=20260712-lane-c-l3`) | done |
| G1 / G2 / G4 / G5 rebuild path still OK | verified this run |

**VIZ3_META highlights:** `lane_id=L3_college_cross_domain`, `openalex_level=3`, `same_field_required=false`, retrospective tagging note, `empty_fetched_years` includes `C169699857:1975`.

---

## Framing (product)

- Fairness = **same OpenAlex level**, not same scientific field.
- Metaphor: school (broader, e.g. L1) vs college (finer, e.g. L3) — this race is **college-only**.
- Infectious disease kept as COVID peer at L3.

---

## Verify checklist

- [x] Pool unique concept IDs = Lane C seven; no `C154945302`
- [x] No ML / Data science / Renewable in `viz3_data.js`
- [x] Infectious `C524204448` present
- [x] Continuous 1974–2024 for all seven (QI 1975 empty allowed)
- [x] Credits / subtitle mention L3 same-level + retrospective tags
- [x] `default_lane_id` in `g3_level_sets.json` = `L3_college_cross_domain`
