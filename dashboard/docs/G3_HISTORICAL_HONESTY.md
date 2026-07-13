# Graph 3 historical honesty

**Date:** 2026-07-12  
**Scope:** G3 only (OpenAlex topic race). No Lucy/Altair milestone charts.

**Related:** trim/reorder / “7 topics only” product plan → [`G3_FIX_PLAN.md`](G3_FIX_PLAN.md).

---

## Plan (what we did)

1. **Web research** on OpenAlex concept tagging + real field milestones (cited below).
2. **Audit** friend scraper `scrape_openalex_data.py` vs canonical river fetch.
3. **Decide:** river concept extract is OK; interpretation/UI window was wrong. Scraper is **not** the canonical path and must not overwrite the pool.
4. **Implement:** per-topic honesty floors + UI copy that counts are OpenAlex concept-tagged works.

---

## What was wrong (product)

At early scrubber years (e.g. **1974**), the race showed modern **dashboard labels** (CRISPR & Genomics, Data Science & Big Data, AI & Machine Learning) as if those named fields were booming then. That reads as fake:

| Label | Why 1970s look impossible |
|-------|---------------------------|
| CRISPR & Genomics | Gene-editing CRISPR-Cas9 crystallizes **2012** (Doudna/Charpentier). |
| Data Science & Big Data | Modern “data science” / “big data” discourse is late **1990s–2001+**. |
| AI & Machine Learning | First **AI winter** narrative sits around **1974–1980** (Lighthill 1973); a 1974 “AI boom” bar contradicts that story. |

**Important:** Early OpenAlex *counts* are often real classifier outputs — they are **not** “people published CRISPR gene-editing papers in 1974.” They are works the MAG-derived tagger assigns to a modern concept ID from title/abstract.

---

## How OpenAlex concepts work (retrospective)

- Legacy **Concepts** are a MAG-derived hierarchy assigned by an ML tagger from **titles and abstracts** (later V2/V3 also use abstracts; parent concepts filled for hierarchy).  
  - Help center: https://ourresearch.gitbook.io/help.openalex.org/how-it-works/concepts  
  - Tagging code: https://github.com/ourresearch/openalex-concept-tagging  
- Concepts are **deprecated** in favor of **Topics**; OpenAlex still serves concept fields on works but does not actively maintain them.  
  - https://developers.openalex.org/guides/deprecations  
- Because tagging is text-based and applied across the corpus, **modern concept labels attach to older works** whenever the model thinks the abstract matches. That is expected taxonomy behavior, not a year-filter bug in our fetch.
- Independent evaluations note concept assignment can be noisy / inaccurate as index terms (homonyms, hierarchy quirks). Example CAIS work: https://journals.library.ualberta.ca/ojs.cais-acsi.ca/index.php/cais-asci/article/download/1979/1652/2738

**Verdict:** Live G3 river (`concepts.id` + locked primaries) is **honest OpenAlex concept volume**. The bug was **UI interpretation** (reading counts as “field buzzword coined that year”), not a silent year off-by-N in the API call.

---

## Milestone years (cited)

### CRISPR / gene editing

- Term **CRISPR** enters print ~**2002** (Jansen; Mojica correspondence). Bacterial adaptive-immunity experimental demo **2007** (Barrangou et al.). Programmable Cas9 gene-editing milestone **June 2012** (Jinek, Doudna, Charpentier, *Science*).  
  - Broad timeline: https://www.broadinstitute.org/what-broad/areas-focus/project-spotlight/crispr-timeline  
  - Berkeley CRISPR timeline: https://news.berkeley.edu/2019/06/25/crispr-timeline/  
  - Paper: https://doi.org/10.1126/science.1225829  
  - Nobel background: https://www.nobelprize.org/uploads/2020/10/advanced-chemistryprize2020.pdf  

**Dashboard primary:** OpenAlex concept **CRISPR** `C98108389` (not a separate “gene editing only” ID). Pre-2012 bacterial CRISPR papers are historically real for the *concept name*; pre-~2002 tags and a 1974 “CRISPR boom” under our race label are not scientifically defensible for the gene-editing story we imply.

**Floor history:** Originally **2012** (gene-editing milestone). **Audit 2026-07-12** found raw OpenAlex CRISPR concept already had continuous volume before 2012 (2011 global **269**, 2012 **386**) — the n/a→386 cliff was **our hard floor**. **Floor now 1974** (shared scrubber) with retrospective-tag UI disclaimer. Full numbers: [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md).

### Data Science & Big Data

- Modern **data science** action-plan sense: Cleveland **2001**.  
  - Forbes short history (cites Cleveland): https://www.forbes.com/sites/gilpress/2013/05/28/a-very-short-history-of-data-science/  
  - Dataversity brief history: https://www.dataversity.net/articles/brief-history-data-science/  
- **Big Data** etymology: SGI / Mashey mid-1990s; academic Diebold ~2000; Laney “3 Vs” META note **2001**.  
  - NYT Bits etymology: https://archive.nytimes.com/bits.blogs.nytimes.com/2013/02/01/the-origins-of-big-data-an-etymological-detective-story/  
  - Diebold SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2152421  

**Dashboard primary:** concept **Data science** `C2522767166`. Early decades are older stats/CS tagged into that concept.

**Floor history:** Originally **2001** (Cleveland / Big Data popularization). **Audit 2026-07-12** found raw OpenAlex Data science concept already had continuous high volume before 2001 (2000 global **5883**, 2001 **6534**) — the n/a→6500 cliff was **our hard floor**. **Floor now 1974** with retrospective-tag UI disclaimer. See [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md).

### AI / Machine learning vs AI Winter

- UK Lighthill report **1973**; commonly tied to first **AI winter** funding chill ~**1974–1980**.  
  - https://en.wikipedia.org/wiki/Lighthill_report  
  - https://en.wikipedia.org/wiki/AI_winter  
  - Holloway summary: https://www.holloway.com/g/making-things-think/sections/the-first-ai-winter-19741980  
- Nuance: some historians argue the “first winter” narrative is overstated (community metrics still grew).  
  - https://zoo.cs.yale.edu/classes/cs200/lectures/AIACMDec2023.pdf  

**Dashboard primary:** **Machine learning** `C119857082` (not mega-AI `C154945302`).

**Floor history:** Originally **1980** (AI-winter narrative). **Audit 2026-07-12** found raw OpenAlex already had ~3182 global ML works in 1979 and ~3396 in 1980 — the n/a→3000 cliff was **our hard floor**, not the river. **Floor now 1974** (shared scrubber start) with retrospective-tag UI disclaimer. Full numbers: [`G3_AI_1980_JUMP_AUDIT.md`](G3_AI_1980_JUMP_AUDIT.md).

### Quantum Computing

- Shor factoring / discrete-log algorithms FOCS **1994**.  
  - https://en.wikipedia.org/wiki/Shor%27s_algorithm  
  - https://ieeexplore.ieee.org/document/365700  

**Dashboard primary:** **Quantum computer** `C58053490`.

**Floor history:** Originally **1994** (Shor FOCS). **Audit 2026-07-12** found continuous Quantum computer tags well before 1994 (1993 global **62**, 1994 **80**; 1974 already **20**). Hard floor created a fake n/a→80 cliff. **Floor now 1974**. See [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md).

### Infectious Diseases / Renewable Energy / Robotics

- Infectious disease and renewable-energy literatures are historically real in the 1970s; **start 1974**.
- Robotics: originally floored at **1980**; raw series is continuous but tiny pre-1980 (1979 global **14**). Softened to **1974** so we do not show a fake n/a→11 cliff. See [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md).

---

## Scraper audit: `scrape_openalex_data.py`

**Path:** `C:\Users\brata\Downloads\CS661\scrape_openalex_data.py`

| Check | Finding |
|-------|---------|
| What it queries | `filter=primary_topic.subfield.id:{ASJC},publication_year:{Y}` + `group_by=institutions.country_code` |
| IDs | Hardcoded ASJC-like: `1702`, `1311`, `2725`, `1706`, `2105`, `2207`, **`2500`** |
| Years | 1950–2025 |
| Output | Writes `../viz3_data.js` (wrong relative to repo layout if run from repo root) |
| Auth | Polite-pool `mailto` User-Agent (OpenAlex has moved to API keys; polite pool deprecated) |

### Bugs / mismatches vs our locked river

1. **Wrong entity layer.** Canonical G3 uses **OpenAlex concepts** (`concepts.id:C…`) per `topic_id_map.json` / `RIVER_OWNERS.md`. Friend scraper uses **Topics subfield** ASJC-style IDs — a different measurement system.
2. **Quantum = `2500` is Materials Science** (Scopus ASJC), **forbidden**. Live lock is `C58053490`. Documented already in `TOPICS_API_METHOD.md` / `topic_id_map.json`.
3. **Would overwrite the pool** with ASJC subfield rows while UI still claims concept IDs — silent pollution.
4. **Not the river owner.** Canonical fetch: `CS661_Dataset/raw_vault/04_openalex/fetch_topics_full.py` → `topics_full/openalex_topic_country_year.csv` → `dashboard/_river_to_pool_rebuild.py` → `viz3_data.js`.

### Scraper vs honesty problem

| Layer | Status |
|-------|--------|
| Friend scraper | **Wrong / non-canonical** if used as G3 source (especially Quantum `2500`). Do **not** re-pull into the live pool as-is. |
| Canonical concept river | **OK** as OpenAlex concept×country×year counts. |
| Tap / shared 1974 window | **Misleading** without per-topic floors + labeling. |

**Decision:** Fix = **honesty windows + UI labeling** on the concept river. Do **not** adopt the friend scraper as the G3 fetch path. Keep it in-repo only as a warned legacy/demo script pointing at `fetch_topics_full.py`.

---

## Product fix (implemented)

1. **Shared scrubber start 1974** for all live-7 in `_river_to_pool_rebuild.py` (`G3_TOPIC_START_YEARS`). Hard milestone floors (CRISPR 2012, Data Science 2001, Quantum 1994, Robotics 1980, AI 1980) created fake `n/a → spike` cliffs when the raw river was already continuous — see [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md) and [`G3_AI_1980_JUMP_AUDIT.md`](G3_AI_1980_JUMP_AUDIT.md).
2. **UI** (`graphs/g3/g3.js`): honesty subtitle states counts are retrospective OpenAlex concept tags — modern dashboard labels are anachronistic names on continuous tagged volume, not fields “born” at a milestone year.
3. **Credits** state OpenAlex **concept-tagged works** (retrospective taxonomy).
4. Primaries unchanged: ML `C119857082`, Quantum `C58053490`; mega-AI `C154945302` still forbidden.
5. No invented historical milestone charts.

### Floors (current — soft shared window)

| Topic | Start | Anchor |
|-------|------:|--------|
| Infectious Diseases | 1974 | shared scrubber / historically real |
| Renewable Energy | 1974 | shared scrubber / historically real |
| AI & Machine Learning | 1974 | real OpenAlex ML series (was hard-1980) |
| Robotics & Automation | 1974 | was hard-1980; continuous raw (tiny early volume) |
| Quantum Computing | 1974 | was hard-1994; continuous raw (~62 in 1993) |
| Data Science & Big Data | 1974 | was hard-2001; continuous raw (~5883 in 2000) |
| CRISPR & Genomics | 1974 | was hard-2012; continuous raw (~269 in 2011) |

Milestone literature dates (Cas9 2012, Cleveland 2001, Shor 1994, …) remain useful **context** in this doc; they are **not** used as hard pool zeroing walls anymore.

---

## Verify

- At year **1974**, all seven topics are active with real OpenAlex concept volume (CRISPR may be tiny — e.g. global 1 — with disclaimer). No topic shows `n/a` then suddenly thousands at a milestone year.
- Pre-cliff years match river: CRISPR 2011=269, Data Science 2000=5883, Quantum 1993=62, AI 1979=3182.
- Play / scrub still works across `year_min`–2024.
- G1 / G2 / G4 / G5 untouched by this rebuild path when running G3-only.
