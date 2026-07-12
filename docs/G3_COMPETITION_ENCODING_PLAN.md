# Graph 3 — Competition Encoding Plan (presentation only)

**Date:** 2026-07-12  
**Status:** PLAN ONLY — no code/data changes required by this doc  
**ICM:** Layer 3 = presentation preferences below · Layer 4 = OpenAlex river/tap counts (immutable truth)

---

## Separation of concerns (ICM)

| Layer | What it is | Rule |
|-------|------------|------|
| **Layer 4 — data truth** | `openalex_topic_country_year.csv` (river) → `dashboard/viz3_data.js` (tap, 1974–2024, primary IDs) | Never silently scale, invent, or drop years to “make the race fair.” |
| **Layer 3 — presentation** | Axis mode, labels, callouts, optional redefinition of which concept IDs compete | Allowed if **labeled** and reversible; user can always see Absolute. |

**Course-honest principle:** Change *how attention is guided*, not *what the API returned*.

---

## Part A — Encoding options (ranked by honesty)

### Evidence snapshot (Layer 4, tap global sums)

| Year | AI (ML) | Infectious | AI share of 7 | Inf share | AI/Inf ratio |
|-----:|--------:|-----------:|--------------:|----------:|-------------:|
| 1974 | 2 267 | 117 | 75.2% | 3.9% | 19.4× |
| 2000 | 20 614 | 1 552 | 69.4% | 5.2% | 13.3× |
| **2020** | **254 187** | **250 961** | **39.3%** | **38.8%** | **1.01×** |
| 2024 | 257 472 | 120 824 | 48.0% | 22.5% | 2.13× |

**Already in Absolute:** 2020 is a photo finish. Competition UX is partly a *spotlight* problem, not only a scaling problem.

---

### 1. Share-of-selected-topics (recommended default) — honesty ★★★★★

| | |
|--|--|
| **What user sees** | Each year’s bars sum to 100% across the 7 selected topics. Axis = “% of selected-topic volume.” |
| **How rivalry appears** | Rank swaps and close contests (esp. 2020 AI 39.3% vs Infectious 38.8%). Early AI dominance becomes “share lead,” not an infinite absolute wall. |
| **Honesty risks** | Denominator is *only these 7* — not world science. Rising share ≠ rising absolute if total shrinks (2024 Infectious share drop partly absolute post-COVID). |
| **UI cost** | Low — transform in client; label axis + footnote: “Share of the seven dashboard topics (not of all science).” |

### 2. Index to base year (2000=100 preferred over 1974) — honesty ★★★★☆

| | |
|--|--|
| **What user sees** | Every topic starts at 100 in base year; bars = growth multiples. |
| **How rivalry appears** | CRISPR/Infectious “growth rockets” vs AI’s steadier climb (2020 CRISPR index ~15 900; Infectious ~16 170; AI ~1 233). |
| **Honesty risks** | Tiny 2000 CRISPR base (39) inflates later index — *mathematically true*, emotionally misleading without base-count footnote. 1974 base worse (CRISPR=1). |
| **UI cost** | Low–medium; pick **2000=100** and show “base N works” on hover. |

### 3. Log scale (Absolute) — honesty ★★★★★

| | |
|--|--|
| **What user sees** | Same counts, log₁₀ axis. |
| **How rivalry appears** | Compresses AI’s early lead so mid-tier topics stay readable; still Absolute truth. |
| **Honesty risks** | Viewers misread vertical distance as linear. Must label “log scale.” |
| **UI cost** | Low (axis transform + badge). |

### 4. Dual/triple mode toggle: Absolute | Share | Indexed — honesty ★★★★★

| | |
|--|--|
| **What user sees** | User chooses encoding; **default Share** for “competition,” Absolute for viva defense. |
| **How rivalry appears** | Same race, three honest lenses. |
| **Honesty risks** | None if default is disclosed and Absolute always one click away. |
| **UI cost** | Medium — one control + three axis titles + short mode blurb. |

### 5. Within-topic ranks / YoY % change race — honesty ★★★★☆

| | |
|--|--|
| **What user sees** | Bars = YoY %Δ or rank-by-growth this year (not counts). |
| **How rivalry appears** | “Who gained this year” — e.g. 2015–18 CRISPR YoY leaders; **2020 Infectious +2509%** (pandemic); 2022 Renewable +12.7%. |
| **Honesty risks** | Volatile for small bases; 2020 Infectious looks like a cartoon spike. Pair with Absolute tooltip. |
| **UI cost** | Medium (derived series + rank animation). |

### 6. Matched ontology depth (redefine river) — honesty ★★★☆☆ *if labeled*

| | |
|--|--|
| **What user sees** | Narrower ML/Data IDs (Topics API / L2–L3) so absolute bars compete with CRISPR/Robotics L3. |
| **How rivalry appears** | Fairer absolute race *by construction*. |
| **Honesty risks** | **Changes the river definition** — not “presentation,” a new dataset. Must rename (“ML algorithms subset”) and keep old series as alternate. |
| **UI cost** | High — re-extract, new map, dual credit line. Defer unless viva demands apples-to-apples Absolute. |

### 7. Small multiples (own y-scale per topic) — honesty ★★★★★

| | |
|--|--|
| **What user sees** | Seven sparklines / mini races, each auto-scaled. |
| **How rivalry appears** | Trend shapes compete (rise/fall/crossover timing) without shared-axis lie. |
| **Honesty risks** | Cross-topic *level* comparison is impossible — say so. |
| **UI cost** | Medium–high (layout redesign); great as secondary view. |

### 8. Footnotes / “AI is L1 mega-tag” callouts — honesty ★★★★★ (mandatory companion)

| | |
|--|--|
| **What user sees** | Persistent note: ML=`C119857082` L1; CRISPR/Infectious/Robotics/Quantum = L3; Data Science L1; Renewable L2. Retrospective tagging inflates early CS. |
| **How rivalry appears** | Doesn’t create rivalry alone; **prevents grader distrust** when Absolute still shows AI tall early. |
| **Honesty risks** | None if short and always visible. |
| **UI cost** | Low — already partially in credit/footnote (`app.js`). |

---

## Honesty ranking (summary)

| Rank | Option | Use when |
|-----:|--------|----------|
| 1 | Share + footnote | Default “competition” demo |
| 1-tie | Absolute + log toggle | Viva / “don’t hide the numbers” |
| 2 | Dual mode Absolute \| Share \| Indexed | Best product answer |
| 3 | Small multiples | Trend storytelling secondary panel |
| 4 | YoY / rank race | Highlight years only (not full timeline default) |
| 5 | Index 2000=100 | Growth narrative mode |
| 6 | Ontology rematch | Only as labeled alternate extract |

**Do not do:** silent divide-by-max, fake jitter, truncating AI, or inventing pre-1974 CRISPR bars.

---

## Narrative beats (guide attention, don’t invent data)

Use callout chips / chapter markers on the year slider (Share or Absolute):

1. **1974–2000 — Uneven ontology, not “AI invented science.”**  
   AI ~70% of *selected* volume; footnote L1 vs L3.

2. **~2012–2015 — CRISPR ignition.**  
   Tap CRISPR: 2012=386 → 2015=1 886; live `meta.count` 2012=361 → 2013=728 → 2015=1 940 (matches CRISPR literature takeoff ~2012).

3. **2015–2019 — Quiet share chess.**  
   YoY leaders often CRISPR/Quantum; AI share drifts ~61–63%.

4. **2020 — Photo finish (Messi vs Ronaldo).**  
   Absolute **254 187 vs 250 961**; Share **39.3% vs 38.8%**. Auto-pause / highlight.

5. **2021 — Infectious peak YoY continuation** (+24.8%); then **2022–24 Infectious retreat**, AI share recovers to 48% by 2024.

6. **Decade card (2014 → 2024 share):**  
   AI 62.2%→48.0%; Infectious 4.3%→22.5%; CRISPR 0.6%→1.3%; Data 22.6%→19.9%.

Optional HUD: “YoY leader,” “share gainer this decade,” “closest Absolute race year.”

---

## Recommended product default

| Setting | Choice |
|---------|--------|
| **Default encoding** | **Share-of-7** |
| **Always available** | Absolute (linear) |
| **Advanced** | Absolute (log), Indexed (2000=100), optional YoY highlight track |
| **Secondary layout** | Small multiples for “within-topic story” |
| **Mandatory** | L1/L2/L3 + “share of selected topics” footnotes |
| **Not default** | Ontology rematch (Layer 4 change) |

---

## Part B — OpenAlex skepticism verdict

### B1. Are 1974 / 2020 gaps real OpenAlex for primary IDs?

**Yes.** Provenance:

| Check | Result |
|-------|--------|
| `_g3_1974_honesty_probe.json` | Live `group_by` country_sum **==** tap **==** river primary-id for all 7 in 1974 |
| Live re-probe 2020 (this plan, key loaded, key not logged) | country_sum **==** tap for all 7 |
| Probe verdict (1974 file) | `FETCHED_CORRECTLY_BUT_CROSS_TOPIC_SKEWED_BY_CONCEPT_BREADTH` |

Notable: AI/Infectious/Robotics often hit **200 country groups** (API `per_page` cap) — long-tail countries truncated; does not invent the AI lead.

### B2. Cross-source sanity

| Source | What it shows | Use |
|--------|---------------|-----|
| **BEFORE_POOLFIX** (ASJC-like FE) | 1950 AI 218 vs Inf 343 (more “balanced”); 1974 CRISPR 4 213 (Molecular Biology proxy, not CRISPR); Quantum under ASJC **2500 Materials** | Different ontology → different race. **Not** proof OpenAlex is wrong; proof **label→ID mapping** drives absolute levels. |
| **Dimensions** | Not available in workspace | Skip |
| **Wikipedia / history** | CRISPR gene-editing papers take off ~2012 | Aligns with OpenAlex CRISPR `meta` ramp 2010→2013 |
| **OpenAlex spot-check (G1 docs)** | Country×year totals within 1% of live | Index itself is stable for aggregates |

### B3. Why ML/Data look huge in the 1970s

1. **Retrospective tagging** — modern concept classifiers apply “Machine learning” / “Data science” to older statistical/CS/pattern-recognition works.  
2. **Ontology breadth** — ML & Data Science are **L1**; CRISPR, Infectious specialty, Robotics, Quantum computer are **L3**; Renewable **L2**.  
3. **Concept age vs name age** — “CRISPR” as a named gene-editing boom is post-2012; sparse earlier tags are expected. Robotics/Quantum also sparse early in country groups.  
4. **Not a join bug** — pool=tap; yearly `publication_year` filters (see `docs/GRAPH3_DATA_ROOT_CAUSE.md`).

### B4. Is OpenAlex “wrong” or “wrong concept choice for a fair race”?

**Wrong concept choice for a fair Absolute race across topics — not a broken fetch.**

- For the chosen primary IDs, OpenAlex returns consistent, reproducible counts.  
- Cross-topic Absolute comparison remains **apples-to-oranges** while L1 sits beside L3.  
- Within-topic trends and Share-of-selected-topics are the honest competition frames.  
- Rematching to narrower Topics API IDs is optional Layer 4 work, only if labeled as a new series.

---

## Implementation sketch (when coding is allowed later)

1. Client-side `mode ∈ {absolute, share, index2000, log}` — no CSV rewrite.  
2. Axis title + one-line mode description.  
3. Year markers at 2012, 2020, 2024.  
4. Keep existing OpenAlex credit; add “Share = among 7 topics only” when mode=share.  
5. Optional later: Topics-API alternate pack behind “Fair Absolute (matched depth)” toggle.

---

## Proof captured for this plan

- Tap aggregates from `dashboard/viz3_data.js` (1974–2024).  
- Live OpenAlex 2020 country_sum match (7/7).  
- CRISPR live meta ramp 2005–2020.  
- BEFORE_POOLFIX ASJC contrast.  
- Prior: `_g3_1974_honesty_probe.json`, `GRAPH3_DATA_ROOT_CAUSE.md`.

**Not verified here:** Dimensions; full SCImago ASJC rebuild for same seven labels; browser UI mock of Share mode.
