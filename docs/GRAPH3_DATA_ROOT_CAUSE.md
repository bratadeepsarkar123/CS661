# Graph 3 Root Cause — 1950 AI vs Infectious spike

**Date:** 2026-07-12  
**Status:** FIXED (honesty trim) — tap no longer shows pre-2000  
**ICM:** river keeps full extract; tap omits misleading early years  
**Pattern:** A implementer

---

## User symptom

Dashboard at **1950** showed ~**878** AI & Machine Learning papers vs ~**24** Infectious Diseases — historically unbelievable (AI as a named field ≈1956; infectious-disease literature was large).

## Tap numbers (before honesty fix)

Global sum of `publications_count` in `dashboard/viz3_data.js`:

| Year | AI & Machine Learning | Infectious Diseases |
|-----:|----------------------:|--------------------:|
| 1950 | 878 | 24 |
| 1960 | 2 522 | 40 |
| 2000 | 101 247 | 1 552 |
| 2020 | 754 116 | 250 961 |

`BEFORE_POOLFIX` (old ASJC-like FE) was more balanced at 1950: AI **218** / Inf **343**.

## Pool vs tap

**Pool = tap exactly** (`delta=0` for all key years).  
`_poolfix_rebuild.py` faithfully copied `openalex_topic_country_year.csv` → `viz3_data.js`.  
**Not** a join bug, not silent scaling, not undated→1950 invention.

## Raw OpenAlex truth

Request log (`topics_full/request_log.jsonl`) for 1950:

| Topic | Concept ID | `meta.count` (all works) | Country-group sum (tap) | Groups |
|-------|------------|-------------------------:|------------------------:|-------:|
| AI | `C154945302` | **3 826** | **878** | 39 |
| Infectious | `C524204448` | **113** | **24** | 5 |

Country sum < `meta.count` because many works lack `authorships.countries` — expected for `group_by=authorships.countries`, not a year mis-join.

Live concept metadata (2026-07-12 probe, concept endpoint):

| ID | display_name | Level | `works_count` |
|----|--------------|------:|--------------:|
| `C154945302` | Artificial intelligence | **1** | **~36.4 M** |
| `C119857082` | Machine learning | 1 | ~5.1 M |
| `C524204448` | Infectious disease (medical specialty) | **3** | ~1.4 M |

## Root cause (ranked)

1. **Incomparable ontology levels (primary):** AI uses a **mega L1 concept** (~36M works) with heavy **retrospective tagging**. Infectious uses a **narrow L3 medical specialty**. Absolute cross-topic bars at 1950 are apples-to-oranges.
2. **Partial 1950–1999 backfill (secondary):** AI complete 1950–2024; Infectious missing **1972–1999**; Data/Renewable/Robotics/Quantum only **2000–2024**. Slider at 1950 showed AI fully while peers were thin/absent.
3. **HTTP 429** stopped finishing a comparable early-year extract (`dailyRemainingUsd: 0`).
4. **Not cumulative counts** — each row is yearly `publication_year` filter.
5. **Not country vs global mix-up** — global = sum of country groups (under-counts works with no country).

## Fix applied (honesty first, no silent scaling)

| Layer | Action |
|-------|--------|
| **River** | Kept full `openalex_topic_country_year.csv` (26 609 rows) including pre-2000 |
| **Tap** | Rebuilt `viz3_data.js` → **2000–2024 only** (20 882 rows); pre-2000 **omitted** |
| **UI** | Timeline / credits / footnote: window = 2000–2024; explain mega-concept + withhold |
| **Map** | `topic_id_map.json`: warn on AI mega-concept; prefer `C119857082` for future re-extract |

Backup of pre-trim tap: `dashboard/viz3_data_BEFORE_HONEST_TRIM.js`  
Proof: `topics_full/_g3_honest_rebuild_proof.json`

### After samples (tap)

| Year | AI | Infectious |
|-----:|---:|-----------:|
| 1950 | *(omitted)* | *(omitted)* |
| 2000 | 101 247 | 1 552 |
| 2020 | 754 116 | 250 961 |

Absolute AI ≫ Infectious in 2000+ remains (same mega-concept). Footnote states **cross-topic absolute levels are not comparable**; within-topic trends are the honest use.

## Files changed

- `dashboard/viz3_data.js`
- `dashboard/viz3_data_BEFORE_HONEST_TRIM.js` (backup)
- `dashboard/app.js` (G3 years, stats, footnote, credit)
- `dashboard/index.html` (cache-bust)
- `CS661_Dataset/raw_vault/04_openalex/topics_full/topic_id_map.json`
- `CS661_Dataset/raw_vault/04_openalex/topics_full/_rebuild_viz3_honest.py`
- `CS661_Dataset/raw_vault/04_openalex/G3_EXTRACT_STATUS.md` (this section + status)
- `docs/GRAPH3_DATA_ROOT_CAUSE.md` (this file)

**Not touched:** G1 / G5 payloads.

## Verify

```text
python CS661_Dataset/raw_vault/04_openalex/topics_full/_g3_audit.py
# Expect: no 1950 rows in tap; 2000/2020 AI & Inf match pool
python CS661_Dataset/raw_vault/04_openalex/topics_full/_rebuild_viz3_honest.py
# Idempotent rebuild
```

Open dashboard Graph 3 → slider min **2000**, footnote visible, no 1950 AI spike.

## Remaining blockers

1. **OpenAlex 429 / $0 daily budget** — cannot re-extract with `C119857082` (Machine learning) or finish Infectious 1972–1999 yet.
2. After budget reset: re-fetch AI with ML concept (or Topics fine-grain), finish Infectious gap, optionally CRISPR start ≥2012; then rebuild tap.
3. Cross-topic absolute bar heights remain imperfect until concept levels are aligned.

## Resume commands (after midnight UTC)

```text
cd CS661_Dataset/raw_vault/04_openalex
python fetch_topics_full.py --years 1972-1999 --topics "Infectious Diseases" --sleep 0.5
# After switching topic_id_map AI primary → C119857082 and clearing old AI pairs:
# python fetch_topics_full.py --years 2000-2024 --topics "AI & Machine Learning" --sleep 0.5
python topics_full/_rebuild_viz3_honest.py
```
