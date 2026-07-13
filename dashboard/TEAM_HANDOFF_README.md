# CS661 Dashboard — Team Handoff

**Branch:** `ui-redesign-2026-07`  
**Repo:** https://github.com/bratadeepsarkar123/CS661  
**Live folder:** `dashboard/` (this is the main deliverable)  
**Date:** 2026-07-12  
**Secrets:** Never commit `.env`, API keys, or `ag gemini key] .txt`.

**Landing chrome:** two-column shell (left brand intro · right vertical viz-card list) in `index.html` / `style.css` — layout only; Graph 1–5 pipelines unchanged.

---

## How to run (teammates)

```powershell
cd C:\Users\brata\Downloads\CS661\dashboard
python -m http.server 8080 --bind 127.0.0.1
# open http://127.0.0.1:8080
```

Or clone:

```powershell
git clone https://github.com/bratadeepsarkar123/CS661.git
cd CS661
git checkout ui-redesign-2026-07
cd dashboard
python -m http.server 8080 --bind 127.0.0.1
```

After pulling JS/CSS changes, **hard-refresh** the browser (Ctrl+F5). Script tags use cache-bust query strings like `?v=20260712-landing-split` in `index.html`.

**Not in this pack (optional / separate):**
- `dashboard-g3-dynamic-top7/` — experiment: dynamic Top-7 OpenAlex topics
- `demos/g2-diverging/` — G2 diverging-bar demo only
- Full `CS661_Dataset/` — huge river vault; only needed to **rebuild** pools

---

# Part A — Simple language for teammates

## The one metaphor: River → Pool → Tap

| Layer | What it is | Where it lives |
|-------|------------|----------------|
| **River** | Source-of-truth CSVs / APIs / PDFs | `CS661_Dataset/` (+ `raw_vault/`, `READY_FOR_TEAM/`) |
| **Pool** | Bundled JS the charts drink from | `dashboard/*_data.js`, `dashboard/data/india_network/` |
| **Tap** | UI framing: labels, filters, charts | `dashboard/app.js`, `index.html`, `style.css`, `india_network.js` |

**Rule:** River wins. If the pool disagrees with the river, fix the pool. If the tap tells the wrong story about correct numbers, fix the copy/filters — do not invent numbers in the UI.

---

## Graph-by-graph (what you see)

### Graph 1 — Peer clusters (UMAP bubbles)
Countries as bubbles over time. Neighbors look similar on wealth (GDP), R&D (GERD), publication volume, and quality (H-index).

- **Fixed:** H-index was a tiny wrong scale (USA ~53); now real SCImago stock (~3388). UMAP positions regenerated for most countries.
- **Caveat:** Bubble size uses **World Bank journal articles**, then SCImago Documents — **never OpenAlex** (OA is ~3× larger and caused a fake cliff). 2023→2024 can still step up once when WB ends and SCImago takes over.
- **Tap files:** `app.js` (Plotly / play / compare), `viz1_data.js`

### Graph 2 — Global quality shift (Q1 vs Q4)
Bars / ridgeline of elite vs low-tier journal output by country–year.

- **Meaning (locked):** Counts are by **journal publisher country** (bookstore location), **not** author home country.
- **Fixed:** Pool ratios were capped at 5; now **uncapped** (UK 2022 ratio ≈ 25). Copy says publisher country.
- **Tap files:** `app.js`, `ridgeline_data.js`

### Graph 3 — Research frontiers (topics × country × year)
Topic volume over time (AI/ML, Infectious, Quantum, …).

- **Fixed:** Quantum was wrongly Materials Science (`2500`); now OpenAlex concept `C58053490`. Topic filters use `C…` ids. Tap years **1974–2024** (shared honest window).
- **COVID caveat:** Infectious Diseases **2019→2020** spike is real OpenAlex corpus tagging (India ~40×) — not a pipeline bug. UI shows a COVID-era note. Numbers are **not** dampened. Share-of-topic mode was planned but **not shipped**.
- **Tap files:** `app.js`, `viz3_data.js`

### Graph 4 — Collaboration premium (dumbbell)
Domestic vs international mean citations; length = “premium.”

- **Fixed:** Was 111 undated countries; now **20 countries × 2010–2024** from river (`VIZ4_BY_YEAR`). Chart is classic **dumbbell** (not bars — bars were a mistaken overnight swap; only G2 keeps bars).
- **Tap files:** `app.js`, `viz4_data.js`

### Graph 5 — India HE collaboration network
Map + network of Indian institutes; NIRF rank / funding / patents with honest carry footnotes.

- **Pool:** Already aligned; no rewrite in the consolidation pass.
- **Policy:** Never invent missing NIRF years; grey out / footnote instead. See `docs/GRAPH5_DATA_PRESENTATION_POLICY.md`.
- **Tap files:** `india_network.js`, `india_network_data.js`, `data/india_network/*`

---

# Part B — AI agents (structured)

## Quick file map

| Role | Path |
|------|------|
| Entry | `dashboard/index.html` |
| TAP logic | `dashboard/app.js` |
| Styles | `dashboard/style.css` |
| G1 pool | `dashboard/viz1_data.js` |
| G2 pool | `dashboard/ridgeline_data.js` |
| G3 pool | `dashboard/viz3_data.js` (`window.CSV_DATA`) |
| G4 pool | `dashboard/viz4_data.js` (`VIZ4_BY_YEAR`, `VIZ4_DATA`) |
| G5 pool | `dashboard/data/india_network/*.json`, `india_network_data.js` |
| G5 TAP | `dashboard/india_network.js` |
| Semantics lock | `dashboard/SEMANTICS_DECISION.md` |
| Pool changelog | `dashboard/PER_GRAPH_POOL_CHANGELOG.md` |
| Teammate TAP checklist | `dashboard/TEAMMATE_CHANGE_REPORT.md` |
| Plain-language story | `dashboard/GRAPH_CHANGES_EXPLAINED_SIMPLY.md` |
| G1 docs policy | `dashboard/G1_TOTAL_DOCS_POLICY.md` |
| G3 root cause | `docs/GRAPH3_DATA_ROOT_CAUSE.md` |
| G2/G4 status | `docs/G2_G4_PIPELINE_STATUS.md` |
| G5 presentation | `docs/GRAPH5_DATA_PRESENTATION_POLICY.md` |

**Cache-bust:** Bump `?v=` on script/link tags in `index.html` whenever pool or TAP JS/CSS changes.

**Do not pack / commit:** `node_modules/`, `*.bak*`, `*_BEFORE_*`, `.env`, API key files, `dashboard/raw_vault/` copies, experiment folders as primary.

---

## Full pipeline per graph

### G1 — Peer clusters

| Layer | Detail |
|-------|--------|
| **River sources** | World Bank WDI (GDP `NY.GDP.PCAP.PP.CD`, GERD `GB.XPD.RSDV.GD.ZS`, articles `IP.JRN.ARTC.SC`); SCImago Country Rank H-index (+ Documents fallback); panel: `g1_features_panel.csv` / `READY_FOR_TEAM/` |
| **Pool build** | Join H into `viz1_data.js`; regenerate UMAP via `dashboard/_regen_viz1_umap.py` (log1p features, per-year UMAP + Procrustes). Helper: `_poolfix_rebuild.py` G1 section |
| **Tap** | `app.js` Plotly animation, EMA smoother, compare/search, region legend; credit: WB + SCImago H + UMAP (**not** OpenAlex for size) |
| **Fixed holes** | Stub H (USA 53→3388); UMAP trained on bad H → regen (~4196/6022 rows); docs channel no longer mixes OA |
| **Caveats** | ~1826 sparse rows may keep old xy; 2024 size may use SCImago when WB missing (`G1_TOTAL_DOCS_POLICY.md`) |
| **Rebuild** | `python dashboard/_regen_viz1_umap.py` then bump `viz1_data.js?v=` |
| **Policy locks** | `Total_Docs` = WB else SCImago Documents; **never** OpenAlex for bubble size / UMAP docs feature |

### G2 — Q1 vs Q4 quality mix

| Layer | Detail |
|-------|--------|
| **River sources** | SCImago journalrank XLS → `q1_q4_country_year.csv` / `country_year_publisher_quartile_docs_1999_2024.csv` (`CS661_Dataset/raw_vault/03_scimago_journal_quartiles/`) |
| **Pool build** | `scripts/rebuild_g2_g4_project_pool.py` or `_poolfix_rebuild.py` → `ridgeline_data.js` (1999–2024, uncapped `ratio`) |
| **Tap** | `app.js` grouped/stacked bars, Quality Guide layout (`margin.top` void), publisher-country metric copy |
| **Fixed holes** | Capped ratios; non-anchor drift; author-country wording |
| **Caveats** | Elite publishers stretch axes (UK ratio ≈ 25). Optional display-only `min(5,ratio)` in TAP only — **never** re-cap the pool |
| **Rebuild** | `python CS661_Dataset/raw_vault/03_scimago_journal_quartiles/aggregate_g2_quartiles.py` then `python scripts/rebuild_g2_g4_project_pool.py` |
| **Policy locks** | **Publisher country** only. No author-affiliation multi-CSV rebuild (`SEMANTICS_DECISION.md`) |

### G3 — Topic frontiers

| Layer | Detail |
|-------|--------|
| **River sources** | OpenAlex concepts → `openalex_topic_country_year.csv` + `topic_id_map.json` (`raw_vault/04_openalex/topics_full/`). Fetch: `fetch_topics_full.py` (reads `OPENALEX_API_KEY` from **repo-root `.env`** — never commit) |
| **Pool build** | Honest rebuild → `viz3_data.js` years **1974–2024**, primary concept IDs only. AI primary = Machine learning `C119857082` (mega AI demoted). Script: `topics_full/_rebuild_viz3_honest.py` |
| **Tap** | `app.js` `topicSubfields` map to `C…` ids; year window from data; COVID Infectious note `#covidInfectiousNote` |
| **Fixed holes** | Quantum `2500` (Materials) → `C58053490`; ASJC-like ids; misleading pre-1974 / mega-concept AI at 1950 |
| **Caveats** | COVID Infectious 2019→2020 real spike (IN ~41×; matches live API). Cross-topic absolute bars still imperfect (ML L1 vs Infectious L3). Share mode **not shipped**. Experiment Top-7 lives in `dashboard-g3-dynamic-top7/` only |
| **Rebuild** | Prefer sleep + key: `python fetch_topics_full.py --years … --sleep 0.35` then `_rebuild_viz3_honest.py`. Verify: `_g3_verify_honest.py` |
| **Policy locks** | Do not dampen COVID spike; do not invent pre-1974 shared bars; Quantum ≠ ASJC 2500 |

### G4 — Collaboration premium

| Layer | Detail |
|-------|--------|
| **River sources** | `collaboration_premium.csv` (20 countries × years; OpenAlex domestic vs intl mean cites) |
| **Pool build** | `scripts/rebuild_g2_g4_project_pool.py` → `viz4_data.js` with `VIZ4_BY_YEAR` / `VIZ4_META` (2010–2024) |
| **Tap** | `app.js` **dumbbell** (domestic ↔ international), year scrub, region drill, Esc clear |
| **Fixed holes** | 111 undated countries; overnight bar chart mistake reverted to dumbbell |
| **Caveats** | Extending beyond 20 countries needs documented OpenAlex regen (`G4_RECOVERY_PLAN.md`) — do not invent |
| **Rebuild** | `python scripts/rebuild_g2_g4_project_pool.py` (from premium CSV) |
| **Policy locks** | Honest 20-country panel; domestic/intl mean cites (not FWCI unless proven) |

### G5 — India network

| Layer | Detail |
|-------|--------|
| **River sources** | OpenAlex collab edges; NIRF PDFs/HTML for rank / funding / patents; `india_outline.geojson` |
| **Pool build** | Pipeline under `scripts/india_network/` → `dashboard/data/india_network/{year}_*.json` + manifest; `india_network_data.js` payload |
| **Tap** | `india_network.js` + footnotes for mapped seasons / static SCImago 2019 / funding carry |
| **Fixed holes** | NIRF ID overrides / match rate; funding static-snapshot footnote; verification checklist |
| **Caveats** | Rank/funding/patents years **do not** equal collaboration slider 1:1 — show mapped year + footnote (`GRAPH5_DATA_PRESENTATION_POLICY.md`) |
| **Rebuild** | Run india_network pipeline scripts; `10_verification_checklist.py` must PASS before demo |
| **Policy locks** | Never fabricate NIRF metrics; grey out beats wrong numbers; third-party scrapers are reference-only |

---

## Intentional non-goals / caveats (do not “fix” wrongly)

| Item | Status |
|------|--------|
| G3 Infectious COVID spike | Real OpenAlex; annotate only; do not dampen |
| G3 Share mode (country % of topic) | Planned, **not shipped** |
| G3 dynamic Top-7 topics | Separate experiment folder — not main pack |
| G2 diverging demo | `demos/g2-diverging/` — optional |
| G2 author-country rebuild | **Locked out** — publisher country forever unless product decision changes |
| G1 OpenAlex bubble size | **Forbidden** |
| `.env` / OpenAlex key | Local only — **never commit or zip** |

---

## Related docs (read order for agents)

1. This file (`TEAM_HANDOFF_README.md`)
2. `SEMANTICS_DECISION.md` — product locks
3. `PER_GRAPH_POOL_CHANGELOG.md` — what changed in pools
4. `TEAMMATE_CHANGE_REPORT.md` — TAP checklist
5. `GRAPH_CHANGES_EXPLAINED_SIMPLY.md` — viva / human story
6. Per-graph deep dives: `G1_TOTAL_DOCS_POLICY.md`, `docs/GRAPH3_DATA_ROOT_CAUSE.md`, `docs/G2_G4_PIPELINE_STATUS.md`, `docs/GRAPH5_DATA_PRESENTATION_POLICY.md`

---

## Send-to-teammates blurb (copy/paste)

> Main CS661 dashboard is on branch **`ui-redesign-2026-07`**: clone https://github.com/bratadeepsarkar123/CS661.git , checkout that branch, `cd dashboard`, run `python -m http.server 8080 --bind 127.0.0.1`, open http://127.0.0.1:8080 . Read `dashboard/TEAM_HANDOFF_README.md` for Graph 1–5 (river→pool→tap), COVID Infectious note, and rebuild rules. Ignore `dashboard-g3-dynamic-top7/` and `demos/` unless you specifically want those experiments. Do not commit `.env`.
