# Graph 3 Root Cause — 1950 AI vs Infectious spike

**Date:** 2026-07-12  
**Status:** FIXED (honesty trim + Machine Learning primary + API key auth)  
**ICM:** river keeps full extract; tap omits misleading early years; primary IDs only  
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
| **River** | Full CSV retained; ML `C119857082` **1950–2024**; Infectious **1950–2024** (1972–1999 hole filled); peers backfilled |
| **Tap** | Rebuilt `viz3_data.js` → **1974–2024** (largest shared complete window), **primary IDs only** |
| **Auth** | `fetch_topics_full.py` loads `OPENALEX_API_KEY` from `CS661/.env`; coordinated `--workers 2` with locked CSV writes |
| **UI** | Timeline / credits / footnote: window = 1974–2024 (derived from tap) |
| **Map** | AI primary = `C119857082` Machine learning; mega-concept demoted to alternate |

Backup of pre-trim tap: `dashboard/viz3_data_BEFORE_HONEST_TRIM.js`  
Proof: `topics_full/_g3_honest_rebuild_proof.json`

### After samples (tap, Machine Learning primary)

| Year | AI (ML `C119857082`) | Infectious |
|-----:|---------------------:|-----------:|
| 1950 | *(omitted)* | *(omitted)* |
| 1974 | **2 267** | **117** |
| 2000 | **20 614** | 1 552 |
| 2020 | **254 187** | 250 961 |

2020 AI ≈ Infectious order of magnitude — far more honest than the old mega-concept 754k vs 251k.

## Files changed

- `dashboard/viz3_data.js`
- `dashboard/viz3_data_BEFORE_HONEST_TRIM.js` (backup)
- `dashboard/app.js` (G3 years, stats, footnote, credit)
- `dashboard/index.html` (cache-bust)
- `CS661_Dataset/raw_vault/04_openalex/fetch_topics_full.py` (`--workers`, rate-limit stop, empty-year resume)
- `CS661_Dataset/raw_vault/04_openalex/topics_full/topic_id_map.json`
- `CS661_Dataset/raw_vault/04_openalex/topics_full/_rebuild_viz3_honest.py`
- `CS661_Dataset/raw_vault/04_openalex/G3_EXTRACT_STATUS.md`
- `docs/GRAPH3_DATA_ROOT_CAUSE.md` (this file)

**Not touched:** G1 / G5 payloads.

## Verify

```text
python CS661_Dataset/raw_vault/04_openalex/topics_full/_g3_verify_honest.py
# Expect: tap 1974-2024; Infectious 1972-1999 complete in pool; sample years match
python CS661_Dataset/raw_vault/04_openalex/topics_full/_rebuild_viz3_honest.py
# Idempotent rebuild → YEAR_MIN=1974
```

Open dashboard Graph 3 → slider min **1974**, footnote visible, no 1950 AI spike.

## Remaining blockers

1. ~~OpenAlex 429 / no API key~~ — **resolved**
2. ~~Infectious 1972–1999 pool hole~~ — **filled 2026-07-12**
3. Pre-1974 shared window **impossible** without inventing bars: CRISPR / Robotics / Quantum return 0 country groups in some early years
4. Cross-topic absolute levels remain imperfect (ML is still L1; Infectious is L3) — within-topic trends are the primary honest use

---

## India Infectious 2019→2020 cliff (audit 2026-07-12)

**User report:** India Infectious ~334 (2019) → ~13 395 (2020) (~40×). Suspected OpenAlex pollution / incomplete fetch / rate-limit holes.

### Proof (invent nothing — live API matched)

| Source | IN 2019 | IN 2020 |
|--------|--------:|--------:|
| Tap (`dashboard/viz3_data.js`) | 334 | 13 995 |
| River (`openalex_topic_country_year.csv`) | 334 | 13 995 |
| Live OpenAlex `concepts.id:C524204448,publication_year:Y,authorships.countries:IN` | 334 | 13 995 |
| Live OpenAlex `group_by=authorships.countries` cell IN | 334 | 13 995 |

Duplicate `(year, country)` rows for Infectious primary: **0**.

### Other-country Infectious YoY (tap = river = live group_by)

| CC | 2019 | 2020 | Ratio |
|----|-----:|-----:|------:|
| IN | 334 | 13 995 | **41.9×** |
| US | 2 327 | 51 033 | **21.9×** |
| CN | 703 | 16 830 | **23.9×** |
| GB | 676 | 20 273 | **30.0×** |

Global Infectious `meta.count`: **9 604** (2019) → **287 833** (2020). Country-group sum 2020 ≈ **250 961** (top-200 `per_page` cap + multi-country counting); matches prior G3 docs.

### Contrast — India AI (`C119857082`)

| | 2019 | 2020 | Ratio |
|--|-----:|-----:|------:|
| Tap / river / live | 10 121 | 14 271 | **1.41×** |

### Verdict

**Polluted river = real OpenAlex COVID-era tagging under Infectious disease (`C524204448`), not a tap leak or partial-year fetch hole.** All spot countries jump >20×; India AI does not. No re-fetch performed (would only re-copy the same cliff).

### Rate limit at audit time

Daily budget **not** exhausted: `daily_remaining_usd ≈ 0.964` / `$1`; credits remaining **9640**/10000; resets `2026-07-13T00:00:00.000Z`.

### Presentation remedies (optional — not a data bug)

- Annotate 2020–2022 as COVID-era Infectious spike
- Prefer **share mode** (country share of topic) so absolute cliffs are less misleading
- Do **not** invent a 2019 backfill or dampen 2020

### Audit script

`CS661_Dataset/raw_vault/04_openalex/topics_full/_g3_india_infectious_cliff_audit.py`

