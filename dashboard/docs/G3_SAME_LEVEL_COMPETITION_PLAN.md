# G3 same-level competition plan

**Date:** 2026-07-12 (reframed same day)  
**Scope:** Graph 3 only — fair topic races at **one OpenAlex concept abstraction level**. No full multi-level UI in this pass.  
**Related:** [`G3_FIX_PLAN.md`](G3_FIX_PLAN.md), [`RIVER_OWNERS.md`](RIVER_OWNERS.md), stub [`g3_level_sets.json`](g3_level_sets.json).

---

## Plain-language goal (school / college metaphor)

Think of OpenAlex `level` like school vs college course catalogs:

| Metaphor | Meaning | OpenAlex |
|----------|---------|----------|
| **School level** | Broad subjects (Science, EVS, Math) | Higher / broader levels (e.g. **L1**) |
| **College level** | Finer subjects (Calculus, Genomics, Electronics) | Deeper levels (e.g. **L2 / L3**) |

**Wrong:** Mix school with college in one race — e.g. Machine learning (**L1**) vs CRISPR (**L3**). That is “comparing school vs college,” not a fair competition.

**Right:** Either show a **full school-level set** (all same broader `level`) **or** a **full college-level set** (all same deeper `level`). Each race = **one abstraction only**.

### What “same level” does *not* mean

- **Same scientific field is NOT required.** Cross-field at the same abstraction is **good and intentional**.
- Example: a 2020 COVID biology boost (Infectious disease) competing with Robotics / Quantum / CRISPR at **the same OpenAlex `level`** is valuable storytelling — not misleading.
- **Do NOT** drop Infectious (or other high-volume peers) solely because their `works_count` band differs from CRISPR, **if they share the same OpenAlex `level`**.
- Works-count can still inform curation within a lane, but **level match is the fairness rule**; volume band is secondary, not a veto.

**Rule (hard):** Every race uses sibling concepts at the **same OpenAlex `level` (0–5)**.  
**Rule (soft):** Prefer peers that make country/time divergence interesting — including cross-domain event spikes (COVID, energy transitions, quantum race).

Honesty stays: counts = **retrospective OpenAlex concept tags**; shared scrubber **1974**; **no fake milestone floors**; **no mega-AI** (`C154945302`); **no ASJC / friend-scraper path**.

---

## What OpenAlex hierarchy actually is (2026)

| Fact | Detail |
|------|--------|
| Legacy Concepts | MAG/Wikidata taxonomy, **~65k** concepts, **6 levels (L0–L5)** |
| L0 | ~19 broad disciplines (e.g. Computer science `C41008148`) |
| L1–L5 | Progressively narrower; poly-hierarchical (multiple parents historically) |
| Status | **Deprecated** — OpenAlex prefers Topics (domain → field → subfield → topic) |
| Still usable for G3 | `concepts.id` on works still works; `fetch_topics_full.py` already uses concepts |
| Broken on live API | `ancestors` / `related_concepts` return **null**; `filter=ancestors.id:…` returns **0 children** |
| Fairness rule we use | Same numeric **`level`** (required). Cross-domain OK. Works-count is secondary curation only. |

Sources: [OpenAlex deprecations](https://developers.openalex.org/guides/deprecations) (Concepts → Topics; Concepts = 6 levels / MAG); concept `level` + `works_count` via `GET /concepts/https://openalex.org/C…` (short `/concepts/C…` 404s).

**We stay on Concepts** for this redesign (existing river + fetch script). Topics migration is out of scope; ASJC is forbidden.

---

## Diagnosis of the live 7

| Display name | Concept ID | Level | Works (API ~2026-07-12) | In river CSV? |
|--------------|------------|------:|------------------------:|:-------------:|
| Infectious Diseases | `C524204448` | **3** | ~1.39M | yes |
| Renewable Energy | `C188573790` | **2** | ~1.30M | yes |
| AI & Machine Learning | `C119857082` | **1** | ~5.14M | yes |
| Robotics & Automation | `C34413123` | **3** | ~227k | yes |
| Quantum Computing | `C58053490` | **3** | ~183k | yes |
| Data Science & Big Data | `C2522767166` | **1** | ~2.93M | yes |
| CRISPR & Genomics | `C98108389` | **3** | ~81k | yes |

**Problem:** Levels **1 + 2 + 3** in one race — school mixed with college.  
**Not the problem:** Infectious vs CRISPR both being L3 but different works-count — that is same-college, cross-domain (allowed; COVID signal is a feature).

River already has these eight IDs (seven live + mega-AI audit):  
`C119857082`, `C2522767166`, `C188573790`, `C524204448`, `C34413123`, `C58053490`, `C98108389`, `C154945302` (audit only).

---

## Recommended default for the live dashboard

### Default lane: **L3 — College-level cross-domain race** *(includes COVID peer)*

**Metaphor:** Full **college** catalog race — finer specialties across domains, all OpenAlex **level 3**.

**Why this default**

- Fixes the real unfairness: **L1/L2 umbrellas mixed with L3 specialties**.
- **Same field not required** — biology (Infectious, CRISPR) races tech (Robotics, Quantum) and energy methods (storage, PV) at one abstraction.
- Keeps **Infectious disease** so a 2020 COVID spike can compete visibly with robotics/quantum/CRISPR — high-signal cross-domain story.
- Four of seven already in the river; three need one `fetch_topics_full.py` pass.
- Country races diverge (CN robotics/PV; US/EU quantum; global CRISPR; pandemic epidemiology surge).

| # | Display name | Concept ID | Level | Works ~ | River |
|--:|--------------|------------|------:|--------:|:-----:|
| 1 | Infectious disease | `C524204448` | 3 | 1.39M | **yes** |
| 2 | Robotics | `C34413123` | 3 | 227k | **yes** |
| 3 | Quantum computer | `C58053490` | 3 | 183k | **yes** |
| 4 | CRISPR | `C98108389` | 3 | 81k | **yes** |
| 5 | Energy storage | `C73916439` | 3 | 279k | need fetch |
| 6 | Photovoltaics | `C542589376` | 3 | 94k | need fetch |
| 7 | Quantum information | `C169699857` | 3 | 123k | need fetch |

**Explicitly not in this default**

| Dropped from live mix | Why |
|----------------------|-----|
| Machine learning `C119857082` | **L1 school-level** — moves to Lane A |
| Data science `C2522767166` | **L1 school-level** — moves to Lane A |
| Renewable energy `C188573790` | **L2** — moves to Lane B / E |
| Mega-AI `C154945302` | Forbidden primary |
| Supervised learning `C136389625` | Still L3 peer candidate for alt tech-heavy set; swapped out of default 7 to keep Infectious (COVID) + QI |

**Not dropped:** Infectious disease — **same L3 as CRISPR/Robotics**; larger works-count is OK. Dropping it for volume would erase the COVID competition the product wants.

**UI copy (when swapped):** “OpenAlex concept-tagged works — seven **level-3** peers (same college abstraction; cross-domain by design).” Retrospective tagging disclaimer unchanged. Floors stay soft **1974**.

**Phase status:** Plan + JSON only. **No live pool swap in this pass.** Fetch still required for missing IDs before Phase 1.

---

## Full menu of lanes (ready for later UI)

Each lane = **one abstraction only** (school *or* college depth — never mixed). Cross-field within a lane is encouraged. Machine-readable twin: [`g3_level_sets.json`](g3_level_sets.json).

| Lane | Metaphor | Level | Role |
|------|----------|------:|------|
| **A** | School | L1 | Broader method subjects |
| **B** | College (mid) | L2 | Applied mid-fields |
| **C** | College (fine) | L3 | **DEFAULT** — cross-domain incl. Infectious |
| **C-tech** | College (fine) | L3 | Alt: tighter tech/methods set (no Infectious) |
| **D** | College (narrower) | L4 | True narrow siblings (partial) |
| **E** | College (mid) | L2 | Energy sub-race |

### Lane A — L1 School-level methods  
*(broad subjects — “Science / Math” class)*

| # | Name | ID | Level | Works ~ | River |
|--:|------|-----|------:|--------:|:-----:|
| 1 | Machine learning | `C119857082` | 1 | 5.1M | **yes** |
| 2 | Computer vision | `C31972630` | 1 | 5.6M | need fetch |
| 3 | Natural language processing | `C204321447` | 1 | 2.2M | need fetch |
| 4 | Data science | `C2522767166` | 1 | 2.9M | **yes** |
| 5 | Computer security | `C38652104` | 1 | 5.7M | need fetch |
| 6 | Bioinformatics | `C60644358` | 1 | 1.6M | need fetch |
| 7 | Biotechnology | `C150903083` | 1 | 2.3M | need fetch |

**Why fair:** All L1 (same school abstraction). Cross-domain methods (compute + bio) are intentional.  
**Exclude:** Artificial intelligence `C154945302` (~36M), Data mining / Statistics (too broad/noisy).  
**Race interest:** CN strength in CV/ML vs US/EU in NLP/security/bioinformatics over time.  
**Do not race against:** Any L2/L3 set in the same UI mode.

---

### Lane B — L2 College mid-fields  
*(applied mid-depth)*

| # | Name | ID | Level | Works ~ | River |
|--:|------|-----|------:|--------:|:-----:|
| 1 | Renewable energy | `C188573790` | 2 | 1.30M | **yes** |
| 2 | Climate change | `C132651083` | 2 | 1.86M | need fetch |
| 3 | Epidemiology | `C107130276` | 2 | 1.37M | need fetch |
| 4 | Sustainable development | `C552854447` | 2 | 1.00M | need fetch |
| 5 | Deep learning | `C108583219` | 2 | 739k | need fetch |
| 6 | Automation | `C115901376` | 2 | 720k | need fetch |
| 7 | Internet of Things | `C81860439` | 2 | 334k | need fetch |

**Why fair:** All L2. Cross-domain (climate + epi + digital systems) is a feature.  
**Alt energy-only 7:** see Lane E.  
**Do not mix with:** Pattern recognition (psychology) `C153180895` — wrong sense of “pattern recognition” for a CS peer; also do not mix L2 with L1/L3 in one race.

---

### Lane C — L3 College cross-domain *(DEFAULT)*  

See table in **Recommended default** above.

**Why fair:** Same OpenAlex level 3 only. **Same field not required.** Infectious stays for COVID vs robotics/quantum/CRISPR competition.  
**Volume note:** Infectious (~1.4M) vs CRISPR (~81k) differ in works-count; that is **not** a reason to exclude Infectious when `level` matches.

---

### Lane C-tech — L3 College tech/methods alt *(optional)*

Same level as default C, but a **tech-heavier** peer set if a demo wants less medical volume dominance — **not** because Infectious is “wrong level.”

| # | Name | ID | Level | Works ~ | River |
|--:|------|-----|------:|--------:|:-----:|
| 1 | Robotics | `C34413123` | 3 | 227k | **yes** |
| 2 | Quantum computer | `C58053490` | 3 | 183k | **yes** |
| 3 | CRISPR | `C98108389` | 3 | 81k | **yes** |
| 4 | Energy storage | `C73916439` | 3 | 279k | need fetch |
| 5 | Photovoltaics | `C542589376` | 3 | 94k | need fetch |
| 6 | Quantum information | `C169699857` | 3 | 123k | need fetch |
| 7 | Supervised learning | `C136389625` | 3 | 88k | need fetch |

Use when product wants a tighter works-count cluster; default remains **Lane C with Infectious**.

---

### Lane D — L4 Narrower college topics  
*(true “narrow method” layer — Genomics / QIS class)*

| # | Name | ID | Level | Works ~ | River |
|--:|------|-----|------:|--------:|:-----:|
| 1 | Genomics | `C189206191` | 4 | 360k | need fetch (mapped as CRISPR alternate) |
| 2 | Quantum information science | `C5320026` | 4 | 46k | need fetch (mapped as Quantum alternate) |
| 3 | Hydrogen economy | `C39380314` | 4 | 18k | need fetch |
| 4–7 | *TBD* | — | 4 | — | need lookup |

**Status:** Partial — OpenAlex API budget hit mid-research (2026-07-12). Complete to 5–7 L4 peers when credits reset.  
**Why this lane exists:** Deeper college abstraction than L3. Stay L4-only; cross-field OK once filled. Note Genomics (L4, 360k) volume ≠ CRISPR (L3, 81k) — **never race L4 Genomics against L3 CRISPR** (school/college mismatch).

---

### Lane E — L2 Energy sub-race  

Same level as Renewable; energy/materials-adjacent story:

| # | Name | ID | Level | Works ~ | River |
|--:|------|-----|------:|--------:|:-----:|
| 1 | Renewable energy | `C188573790` | 2 | 1.30M | **yes** |
| 2 | Solar energy | `C541104983` | 2 | 431k | need fetch |
| 3 | Wind power | `C78600449` | 2 | 385k | need fetch |
| 4 | Biofuel | `C53991642` | 2 | 218k | need fetch |
| 5 | Graphene | `C30080830` | 2 | 405k | need fetch |
| 6 | Fuel cells | `C2987658370` | 2 | 138k | need fetch |
| 7 | Smart grid | `C10558101` | 2 | 104k | need fetch |

**Why fair:** All L2. Volume spread within level is acceptable; level match is the gate.

---

## Data readiness

### Already in concept river (`openalex_topic_country_year.csv`)

| ID | Name | Usable in lanes |
|----|------|-----------------|
| `C119857082` | Machine learning | A |
| `C2522767166` | Data science | A |
| `C188573790` | Renewable energy | B, E |
| `C34413123` | Robotics | **C default**, C-tech |
| `C58053490` | Quantum computer | **C default**, C-tech |
| `C98108389` | CRISPR | **C default**, C-tech |
| `C524204448` | Infectious disease | **C default** (COVID peer) |
| `C154945302` | Artificial intelligence | **audit only — never pool** |

### Need `fetch_topics_full.py` (extend `topic_id_map.json` first)

**Default Lane C (3 IDs):**  
`C73916439`, `C542589376`, `C169699857`

**Lane C-tech add-on:**  
`C136389625` (plus the three above if C-tech is chosen instead)

**Lane A (5 IDs):**  
`C31972630`, `C204321447`, `C38652104`, `C60644358`, `C150903083`

**Lane B / E / D:** see tables above (all marked need fetch).

### Fetch / rebuild path (unchanged)

```
topic_id_map.json  →  fetch_topics_full.py  →  openalex_topic_country_year.csv
                   →  _river_to_pool_rebuild.py  →  viz3_data.js
```

- Allowlist = **active lane’s 7 IDs only** (rebuild guard).  
- Entity type remains **`concept`** (`concepts.id:C…`).  
- Years: resume-safe; prefer full scrubber window **1974–2024** (or 1950–2024 if backfill budget allows).  
- Do **not** use friend `scrape_openalex_data.py` / ASJC.

### API note (research day)

Concept metadata lookups burned daily OpenAlex credit near end of session. Works group_by fetches for new IDs should wait for budget reset or prepaid credits. Hierarchy fields (`ancestors`) are unavailable — do not block the plan on them.

---

## Implementation phases (do not all ship now)

| Phase | Work | UI? |
|------:|------|-----|
| **0 (this doc)** | Peer sets + JSON stub + default recommendation | No |
| **1** | Extend `topic_id_map.json` with Lane C seven; fetch missing three; rebuild pool; update `g3.js` labels / `VIZ3_META` | Swap live race to Lane C only |
| **2** | Fetch Lane A (+ optionally B/E/C-tech); keep sets in `g3_level_sets.json` | Still single race, or hidden config switch |
| **3** | Level picker UI (dropdown: L1 school / L2 college mid / L3 college default / L4 narrow / L2 energy) | Yes — later |
| **4** | Complete Lane D to 5–7 IDs | Later |

**This pass:** Phase 0 only (plan + stub). **No live pool swap.** Phase 1 is the next coding step when fetch budget allows — **do not fight a concurrent G4 expand agent**.

---

## Honesty / product constraints (carry forward)

1. Label bars as **OpenAlex concept-tagged works** (retrospective), not “field invented that year.”  
2. Soft shared start **1974** — no CRISPR-2012 / ML-1980 style cliffs.  
3. No mega-AI primary.  
4. No ASJC scraper into the pool.  
5. G1 / G2 / G4 / G5 untouched.  
6. **Same field not required; same OpenAlex `level` is required.** Cross-domain event races (e.g. COVID) are in-scope.

---

## Verify (when Phase 1 lands)

- [ ] Pool unique concept IDs = exactly Lane C seven; no `C154945302`.  
- [ ] All seven have `level == 3` on OpenAlex concept object.  
- [ ] Infectious `C524204448` is in the default pool (COVID peer retained).  
- [ ] Pool years continuous from 1974 (matches river, no hard floors).  
- [ ] Credits/subtitle mention same-level (college) peers + cross-domain OK + retrospective tagging.  
- [ ] `g3_level_sets.json` `default_lane_id` matches live pool.

---

## Summary

| Item | Choice |
|------|--------|
| **Fairness rule** | **Same OpenAlex `level` required; same scientific field NOT required** |
| **Metaphor** | School (broader, e.g. L1) vs college (deeper, e.g. L2/L3) — never mix in one race |
| **Live default** | **Lane C — L3 college cross-domain** (Infectious, Robotics, Quantum computer, CRISPR, Energy storage, Photovoltaics, Quantum information) |
| **Why Infectious stays** | Same L3; enables COVID vs tech competition; works-count alone is not a drop reason |
| **Menu ready** | A (L1 school), B (L2), C (L3 default), C-tech (L3 alt), D (L4 partial), E (L2 energy) |
| **Already river-ready for default** | 4/7 (`C524204448`, `C34413123`, `C58053490`, `C98108389`) |
| **Fetch before live swap** | 3 IDs: `C73916439`, `C542589376`, `C169699857` |
| **UI multi-level picker** | Deferred (Phase 3) |
| **This pass** | Docs + JSON only — **no live pool swap** |
