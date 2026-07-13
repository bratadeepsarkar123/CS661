# G3 fix plan (plain language)

**Date:** 2026-07-12 (floors revised same day)  
**Scope:** Graph 3 only (OpenAlex concept topic race). G1 / G2 / G4 / G5 untouched.

---

## What’s wrong

OpenAlex tags old papers with **modern concept labels** (retrospective ML tagging from titles/abstracts). That is normal for the API — but our race used those labels as if the *buzzword field* existed then.

**Also wrong (fixed):** Hard “honesty floors” (CRISPR 2012, Data Science 2001, Quantum 1994, Robotics/AI 1980) **zeroed continuous raw series**, creating cartoon `n/a → spike` cliffs. That was display policy lying about the river — same bug class as the AI 1980 floor.

**Wrong interpretation:** “People published CRISPR gene-editing papers in 1974.”  
**Right interpretation:** “OpenAlex’s tagger assigned concept ID X to some 1974 works; read the bar as concept-tagged volume, not as a modern named field being ‘born.’”

---

## What’s NOT wrong

| Piece | Status |
|-------|--------|
| Canonical **concept river** (`concepts.id` × country × year via `fetch_topics_full.py`) | OK as OpenAlex concept volume |
| Friend script `scrape_openalex_data.py` (ASJC / Topics subfield path, Quantum=`2500`) | **Wrong** for G3 — different measurement system; must not overwrite the pool |
| UI “OpenAlex concept-tagged works” copy | Right product honesty (labeling, not zeroing) |

---

## The live 7 topics (pool + UI)

Only these concept IDs may appear in `viz3_data.js`. Mega-AI `C154945302` may stay in the **river CSV for audit** but is **forbidden in the pool**.

| # | Display name | Concept ID | Honesty start |
|--:|--------------|------------|--------------:|
| 1 | Infectious Diseases | `C524204448` | 1974 |
| 2 | Renewable Energy | `C188573790` | 1974 |
| 3 | AI & Machine Learning | `C119857082` (Machine learning) | 1974 |
| 4 | Robotics & Automation | `C34413123` | 1974 |
| 5 | Quantum Computing | `C58053490` | 1974 |
| 6 | Data Science & Big Data | `C2522767166` | 1974 |
| 7 | CRISPR & Genomics | `C98108389` | 1974 |

### Display order chosen

**Live-7 narrative order** (Infectious → Renewable → AI → Robotics → Quantum → Data Science → CRISPR). All floors share scrubber start **1974**; order is no longer “milestone entry year.”

Insight cards / trend legend follow this order. The animated race still **ranks by volume** within the active year.

---

## Plan (what we do)

1. **Seven topics only → pool** — rebuild `viz3_data.js` from the concept river; drop mega-AI and any other extras even if the river CSV still has them.
2. **Rebuild guard** — `_river_to_pool_rebuild.py` refuses to emit any concept ID outside the allowlist of 7.
3. **Soft honesty floors** — all live-7 start at **1974**; pool matches continuous raw river (no fake cliffs). Details: [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md).
4. **UI labels** — counts = OpenAlex concept-tagged works (retrospective), not “field coined that year.”
5. **Canonical fetch** — `CS661_Dataset/raw_vault/04_openalex/fetch_topics_full.py` → river CSV → `_river_to_pool_rebuild.py` → `viz3_data.js`.
6. **Reorder UI** — `g3.js` topic list matches the table above / `VIZ3_META.display_order`.

---

## What we will NOT do

- Integrate `scrape_openalex_data.py` ASJC / Topics-subfield path into the live G3 pool.
- Use mega-AI `C154945302` as the AI primary.
- Use ASJC `2500` (Materials Science) for Quantum.
- Invent Lucy/Altair-style historical milestone charts.
- Change G1, G2, G4, or G5 pools or charts in this pass.
- Pretend early OpenAlex counts are “fake API years” — they are real tags; the bug was **display interpretation** (and hard floors that hid them).

---

## Verify (quick)

- Pool unique `subfield_id`s = exactly the 7 IDs above; no `C154945302`.
- At year **1974**, all seven topics active (pool matches river); CRISPR/Data Science no longer `n/a` until milestone years.
- Pre-cliff globals present: CRISPR 2011, Data Science 2000, Quantum 1993, AI 1979.
- Credits / subtitle still mention retrospective concept tagging.

Details / citations: [`G3_HISTORICAL_HONESTY.md`](G3_HISTORICAL_HONESTY.md), [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md). Owners: [`RIVER_OWNERS.md`](RIVER_OWNERS.md).
