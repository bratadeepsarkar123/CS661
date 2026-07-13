# G3 AI 1979→1980 jump audit

**Date:** 2026-07-12  
**Concept (live primary):** `C119857082` — OpenAlex **Machine learning**  
**Forbidden mega-AI (in river, never pool primary):** `C154945302` — **Artificial intelligence**  
**River CSV:** `CS661_Dataset/raw_vault/READY_FOR_TEAM/openalex_topic_country_year.csv`  
**Pool:** `dashboard/viz3_data.js` (built by `_river_to_pool_rebuild.py`)

---

## One-paragraph verdict

**The cartoon cliff (1979 = n/a, 1980 = 3000+ papers) was our honesty floor, not OpenAlex.** In the raw river, Machine learning (`C119857082`) already has **~3,182** global works in **1979** and **~3,396** in **1980** (+6.7% — a gentle step, not a birth). The pool used to **hard-zero** AI before 1980 for an AI-winter narrative, so the UI showed `n/a before 1980` then suddenly dumped the full ~3.4k series — looking like inventing a field overnight. Spot-checked country cells (US 1548→1689, GB 311→322, IN 105→83) match the same continuous series. **Fix applied:** AI honesty floor softened **1980 → 1974** (shared scrubber start); chart now shows the real OpenAlex ML time series with a retrospective-tagging disclaimer. **Follow-up same day:** CRISPR / Data Science / Quantum / Robotics milestone floors had the same bug class and were softened to **1974** as well — see [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md).

---

## How OpenAlex marks a paper as “AI” / ML

OpenAlex **legacy Concepts** (deprecated in favor of Topics, but still served on works) come from a **MAG-derived** hierarchy. A machine-learning tagger assigns one or more concepts to each work from **title and abstract** text (V1 titles-only; V2/V3 add abstracts; V3 also fills parent concepts so every tag has a path up the tree). Tags are **retrospective**: a 1975 paper about pattern recognition or statistical learning can receive concept `C119857082` (*Machine learning*) even if the authors never wrote the modern buzzword “AI.” Hierarchy is multi-level (level 0–5); parent concepts can be attached along with leaf concepts.

**Cited:**

| Source | URL |
|--------|-----|
| OpenAlex help — Concepts | https://ourresearch.gitbook.io/help.openalex.org/how-it-works/concepts |
| Concept tagging repo (V1/V2/V3) | https://github.com/ourresearch/openalex-concept-tagging |
| Developers — Concepts deprecated | https://developers.openalex.org/api-reference/concepts |
| MAG concept tagging / hierarchy paper | https://ar5iv.labs.arxiv.org/html/1805.12216 |
| Independent note on noisy hierarchy | https://doi.org/10.29173/cais1978 |

**Dashboard label** “AI & Machine Learning” is locked to **Machine learning** `C119857082`, **not** mega-AI `C154945302` (which is ~5× larger and still present in the river for audit only).

---

## Method (not blind py filter trust)

1. Read river columns: `year, country_iso2, …, openalex_id, topic_display_name, works_count`.
2. Filter cells where `openalex_id == C119857082`.
3. **Sum cells** per year (global = sum of all country rows; also US/CN/IN/GB).
4. Spot-print top country rows for 1978 / 1979 / 1980.
5. Compare to pool `viz3_data.js` (`window.CSV_DATA`) after honesty floors.
6. Calculator script: `dashboard/docs/_audit_g3_ai_1980_jump.py` → `_audit_g3_ai_1980_jump.json`.

---

## Year table — raw river vs pool (concept `C119857082`)

| Year | Raw global | Raw US | Raw CN | Raw IN | Raw GB | Pool BEFORE fix (floor 1980) | Pool AFTER fix (floor 1974) |
|-----:|-----------:|-------:|-------:|-------:|-------:|-----------------------------:|----------------------------:|
| 1970 | 2006 | 1002 | 9 | 81 | 206 | 0 (zeroed) | outside scrubber |
| 1971 | 1748 | 1051 | 5 | 34 | 148 | 0 (zeroed) | outside scrubber |
| 1972 | 2034 | 1161 | 3 | 57 | 202 | 0 (zeroed) | outside scrubber |
| 1973 | 2084 | 1107 | 6 | 72 | 207 | 0 (zeroed) | outside scrubber |
| 1974 | 2267 | 1199 | 6 | 70 | 238 | 0 (zeroed) | **2267** |
| 1975 | 2436 | 1315 | 5 | 53 | 242 | 0 (zeroed) | **2436** |
| 1976 | 2628 | 1409 | 12 | 68 | 253 | 0 (zeroed) | **2628** |
| 1977 | 2956 | 1493 | 9 | 80 | 300 | 0 (zeroed) | **2956** |
| 1978 | 2963 | 1488 | 9 | 63 | 267 | 0 (zeroed) | **2963** |
| **1979** | **3182** | **1548** | **11** | **105** | **311** | **0 (n/a)** | **3182** |
| **1980** | **3396** | **1689** | **16** | **83** | **322** | **3396** | **3396** |
| 1981 | 3836 | 1886 | 37 | 97 | 356 | 3836 | 3836 |
| 1982 | 3921 | 1903 | 43 | 92 | 340 | 3921 | 3921 |
| 1983 | 4244 | 2057 | 49 | 93 | 394 | 4244 | 4244 |
| 1984 | 4516 | 2212 | 55 | 92 | 402 | 4516 | 4516 |
| 1985 | 4897 | 2327 | 63 | 92 | 443 | 4897 | 4897 |
| 1986 | 5487 | 2627 | 69 | 109 | 442 | 5487 | 5487 |
| 1987 | 6072 | 2882 | 103 | 91 | 501 | 6072 | 6072 |
| 1988 | 6648 | 3118 | 128 | 98 | 557 | 6648 | 6648 |
| 1989 | 7659 | 3605 | 170 | 98 | 599 | 7659 | 7659 |
| 1990 | 8425 | 3931 | 184 | 124 | 644 | 8425 | 8425 |

**Read the cliff:** raw 1979→1980 is +214 works (+6.7%). Pool-before was 0→3396. Pool-after matches river (3182→3396). That old gap was **100% display policy**.

### Spot-check (printed river rows)

**1979 top countries (77 rows, global 3182):** US 1548, GB 311, CA 181, JP 155, DE 145, IN 105, AU 97, FR 81, …  
**1980 top countries (78 rows, global 3396):** US 1689, GB 322, CA 188, JP 155, DE 113, AU 104, FR 88, IN 83, …

Mega-AI `C154945302` also exists continuously in the river (1979 global **16910**, 1980 **18428**) — larger umbrella; **not** used as G3 primary.

---

## Plain-language explanation (angry-user edition)

OpenAlex does **not** wait for someone to invent the phrase “machine learning” in 1980 and then start counting. A classifier reads titles/abstracts of old papers and sticks today’s concept IDs on them. So 1975 pattern-recognition / statistics / cybernetics-adjacent work can land under *Machine learning*. Our dashboard then labeled that series “AI & Machine Learning” and — to avoid looking like we claimed an “AI boom” during the first AI winter — **deleted every year before 1980**. Result: scrubber at 1979 said **n/a**, scrubber at 1980 said **three thousand papers**. That is a **lie by omission**, not a discovery in the data. The river was already humming along at ~2–3k ML-tagged works through the 1970s.

---

## Policy change (implemented)

| Topic | Old floor | New floor | Why |
|-------|----------:|----------:|-----|
| **AI & Machine Learning** | 1980 | **1974** | Raw series continuous; hard wall created fake cliff. Pool after rebuild: 1979=3182, 1980=3396 (matches river). |
| Robotics / Quantum / Data Science / CRISPR | milestone floors | **1974** (same-day follow-up) | Same bug class — continuous raw volume before floors. See [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md). |

**UI:** honesty note says all seven topics show real OpenAlex concept series from 1974; modern labels are retrospective tags.

**Rebuild:** `_river_to_pool_rebuild.py` → `viz3_data.js` with AI (and later all live-7) rows from 1974 inclusive.

---

## What we did *not* do

- Did **not** invent new counts.
- Did **not** switch primary to mega-AI `C154945302`.
- Did **not** claim 1970s papers used the modern “AI” marketing term.
