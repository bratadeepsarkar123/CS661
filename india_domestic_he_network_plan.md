# India Domestic Higher Education Network — Master Plan

**Project:** CS661 Group 2 — *Global Knowledge & Wealth Paradox*  
**Module:** §4.5 / Visualization 5 of 5 on the single-screen dashboard  
**Owner:** Module 5 implementer  
**Last updated:** 2026-06-23 (execution start: Option 1 API path, dynamic year-end)  
**Purpose:** Persistent handoff document. Any agent can continue from here without re-deriving context.

---

## 0. Dashboard context — two levels (overview grid → fullscreen)

The app has **two modes**, not one crowded screen forever.

### Level A — Overview grid (default, 1920×1080)

All **five** charts visible as **thumbnails**. No scrolling. Click any panel to expand.

| Slot | Module | Approx. footprint | One-glance story |
|------|--------|-------------------|------------------|
| 1 | High-Dimensional Peer Clustering (t-SNE) | ~35% top-left | Countries cluster by behavior, not map |
| 2 | Global Quality Shift (ridgeline) | ~35% top-center | Q1 vs Q4 split over years |
| 3 | Top-10 Research Topics (bar race) | ~30% top-right | Which fields rose/fell |
| 4 | Collaboration Premium (dumbbell) | ~55% bottom-left | Intl co-auth = more citations |
| **5** | **India Domestic HE Network** | **~45% bottom-right** | **Elite hubs vs weak state tier** |

**Module 5 overview pixel budget:** ~860×460 px. Shows **only the headline** (sparse hub map + tier one-liner).

### Level B — Fullscreen (click any panel)

Clicked chart **expands to full viewport**. Other four hidden. **Back** or **Esc** returns to grid.

Inside fullscreen, module 5 still obeys lecture rules — pick **one** pattern per module:

| Pattern | Meaning for India module |
|---------|--------------------------|
| **Overview → details** (Shneiderman) | Full map first → click university → side panel opens with funding + quality tabs |
| **Focus + context** (Munzner Ch. 14) | Selected university **large in center**; rest of network **dimmed but visible** around it |

**Recommended for module 5:** **Focus + context** on the map (click node → fisheye-style highlight + detail card). Tier comparison strip stays visible as context.

### What each level shows (module 5 only)

| | Overview (grid) | Fullscreen (expanded) |
|--|-----------------|----------------------|
| Nodes | ~12 labeled hubs + faint dots | Up to ~80 institutions |
| Edges | Hub-to-hub only | All edges above threshold |
| Side panels | None | Left: Premier tier · Right: State tier (from docx prototype) |
| Funding / quality | 1 line (tier averages) | Full gauges, bars, pie breakdown |
| Tabs | None | **Funding** \| **Publications** per institution on click |

**Performance rule:** Both levels read **pre-computed JSON** (&lt;100 ms). Overview payload ~40 KB; fullscreen payload ~200 KB. No live API in browser.

---

## 1. Cognitive design — compressing four data layers

### 1.1 Problem with the prototype (Image 5)

The docx prototype shows:
- India map + ~20 nodes + thick edges
- **Two** full side columns (pie charts, radial gauges, multiple bar charts, funding tables)

That is **~6 simultaneous chart types** in ~20% of a 1080p screen. Lecture 2 & 10 flag this as harmful:
- Limited working memory / chartjunk (Lecture 2, slide 21)
- Magic number **7±2** for colors and categories (Lecture 10, slide 44)
- Munzner **Ch. 13 — Reduce Items and Attributes**
- Shneiderman: **Overview → zoom/filter → details-on-demand** (Lecture 2, slides 15–18)

### 1.2 Strategy: store everything, show almost nothing

| Layer | Full data (backend / PostgreSQL) | Default on screen | Details-on-demand |
|-------|----------------------------------|-------------------|-------------------|
| **A. Institution registry** | 80–200 institutions with tier, geo, IDs | **12 hub nodes** labeled + ~30 unlabeled dots | Hover: name, tier, 3 metrics |
| **B. Collaboration graph** | All domestic co-auth edges (institution pairs) | **Hub-to-hub edges only** (weight ≥ threshold) | Hover edge: co-paper count |
| **C. Research quality** | pubs, citations, cit/paper, h-index, Q1% | **2 tier aggregates** (Premier vs State) | Click node → mini card |
| **D. Funding** | NIRF/DST/NSTMIS per institution + tier totals | **1 comparative strip** (2 bars or dumbbell) | Optional expand (not default) |

**Principle:** *Filter* eliminates items (hide low-degree nodes). *Aggregate* creates tier-level rows (45,000 colleges → 2 tier summaries in AISHE/NSTMIS narrative).

**State-tier map representation (explicit decision):**

| Aspect | What appears | Source | Why |
|--------|-------------|--------|-----|
| Map nodes (state tier) | Only OpenAlex-resolvable state/deemed universities with `total_works >= 10` (up to 60) | OpenAlex + AISHE | Affiliated colleges have no research signal in OpenAlex |
| Tier aggregate strip | Full ~40k affiliated colleges represented as sector-level averages | AISHE + NSTMIS reports | Preserves the "many but weak" narrative without polluting the graph |
| Graphical integrity footnote | **Mandatory in visualization:** "Map shows ~120 research-active institutions. ~40k affiliated colleges are represented in tier averages only." | — | Prevents lie-by-omission; Tufte integrity |

### 1.3 What we remove from the always-visible UI

| Removed (prototype) | Why | Lecture basis |
|---------------------|-----|---------------|
| Dual side panels with pie + radial + multi-bar | Attribute overload | Reduce items/attributes (Munzner Ch. 13) |
| Per-institution funding tables | Too many numbers | 7±2 |
| All node labels | Clutter | Chartjunk (Lecture 10) |
| Decorative map textures / region callout boxes | Non-data ink | Tufte graphical integrity |
| 3D node sizing | Distorts magnitude | Lie factor (Lecture 10) |

### 1.4 What we keep (one glance story)

**Headline:** *A few blue elite hubs collaborate densely; purple state institutions are many but loosely connected and underfunded.*

**Visible encodings (max 4):**
1. **Position** — geographic (India outline + node lat/lon)
2. **Color** — tier (2 colors only: Premier vs State/Affiliated)
3. **Node area** — total publication volume per institution (√ scale for area ∝ value; uses `total_works` from OpenAlex, NOT domestic-only count)
4. **Edge width** — co-publication count (domestic-only)

**One text annotation on chart:**  
`Premier tier: 18.5 cit/paper · State tier: 4.1 cit/paper` (illustrative until real data loaded)

### 1.5 Interaction model (two levels)

**Grid overview (small panel):**

| Action | Result |
|--------|--------|
| See panel | Hub map + tier one-liner only |
| Hover node | Tiny tooltip (name + 1 metric) |
| **Click panel background** | **→ Fullscreen mode** |
| Year slider (global) | All 5 thumbnails update |

**Fullscreen (after click):**

| Action | Result |
|--------|--------|
| **Overview** | Full India map, ~80 nodes, tier side panels (docx layout) |
| Hover node | Rich tooltip |
| **Click node** | **Focus + context:** node enlarged, partners highlighted, detail card with Funding \| Publications tabs |
| Click tier legend | Filter by premier / state |
| Esc / Back | Return to 5-panel grid |

Depth lives in fullscreen; grid stays cognitively light (Lecture 2 mantra).

---

## 2. Color scheme & visual style

Aligned with the dark-theme prototypes (modules 1–2) for one-screen cohesion.

### 2.1 Module 5 palette

| Role | Hex | Usage |
|------|-----|--------|
| Panel background | `#0f172a` | Matches ridgeline / t-SNE panels |
| Panel border | `#334155` | 1px subtle frame |
| India land (choropleth fill) | `#1e293b` | Low-contrast base map |
| State borders | `#475569` | Thin, no fill pattern |
| **Premier / Elite tier** | `#3b82f6` | Nodes, legend swatch |
| **State & Affiliated tier** | `#a855f7` | Nodes, legend swatch |
| Edge (low weight) | `#64748b` @ 25% opacity | Background ties |
| Edge (high weight) | `#94a3b8` @ 70% opacity | Hub corridors |
| Hover / selection ring | `#f8fafc` | 2px stroke |
| Annotation text | `#94a3b8` | Tier comparison strip |
| Value emphasis | `#f8fafc` | Bold numbers in tooltip |
| Destructive / caution | `#f43f5e` | Only if showing funding gap callout |

**Accessibility:** Two hues + luminance difference; avoid red/green-only encoding. Test with grayscale — tiers must remain separable.

### 2.2 Typography (panel)

| Element | Size | Weight |
|---------|------|--------|
| Panel title | 13px | 600 |
| Node label (hubs only) | 10px | 500 |
| Tooltip | 11px | 400 |
| Tier strip | 11px | 400 / 700 for values |

Font: `system-ui, -apple-system, sans-serif` (same as `animation.html`).

### 2.3 Chartjunk checklist (must pass before merge)

- [ ] No background grid on map
- [ ] No drop shadows on nodes
- [ ] No more than **2** fill colors for data
- [ ] No more than **12** text labels visible at once
- [ ] Legend fits in &lt;40px height
- [ ] Y/X axes only where needed (tier strip only)

---

## 3. Data sources — full inventory

### 3.1 Sufficiency verdict

| Need | Covered? | Primary source | Gap |
|------|----------|----------------|-----|
| Institution list + tier | ✅ | NIRF + AISHE + UGC | Affiliated colleges sparse in OpenAlex |
| Lat/lon | ✅ | OpenAlex geo + github geo DB | Some fuzzy matches |
| Domestic co-authorship | ✅ | OpenAlex works | Requires ETL; 414k IN works/yr (verified) |
| Publication volume | ✅ | OpenAlex + SCImago | — |
| Citations / cit per paper | ✅ | OpenAlex | — |
| Q1% / h-index | ✅ | SCImago SIR CSV | Year lag (~2019 in CSV URL) |
| Funding (institution) | ⚠️ partial | NIRF PDFs, DST Extramural dir. | Parsing effort |
| Funding (tier narrative) | ✅ | NSTMIS sector tables | Aggregate only |
| Enrollment scale (45k colleges) | ✅ | AISHE final report | Unit-level not public |

**Conclusion:** Sources are **sufficient** if we accept (a) hub network not full 45k graph, (b) funding at tier-level + top-N institutions, (c) one feasibility script to validate edge counts before building UI.

### 3.2 Tier 0 — Must download first

| ID | Source | URL | Format | Key fields | Download method |
|----|--------|-----|--------|------------|----------------|
| DS-01 | NIRF rankings (compiled) | https://dataful.in/datasets/19320/ | CSV | `institute_id`, `institute_name`, `city`, `state`, `ranking_category`, `score`, `rank` | Direct download |
| DS-02 | NIRF patents | https://dataful.in/datasets/20551/ | CSV | `institute_id`, patents published/granted | Direct download |
| DS-03 | SCImago Institutions (India) | https://www.scimagoir.com/rankings.php?ranking=Research&country=IND | CSV via `getdata.php?...&format=csv` | Output, citations, intl collab %, Q1%, h-index | **Caveat:** URL params (`year=`, `country=IND`) may need manual inspection in browser DevTools first; validate CSV opens correctly before scripting |
| DS-04 | OpenAlex institutions (IN) | https://api.openalex.org/institutions?filter=country_code:IN,type:education | JSON API | `id`, `ror`, `display_name`, `geo`, `works_count`, `cited_by_count` | Standard paginated API |
| DS-05 | OpenAlex works (domestic co-auth) | https://api.openalex.org/works?filter=institutions.country_code:IN | JSON API / snapshot | `authorships`, `publication_year` | **`group_by` primary** (§3.6); full pagination fallback (§3.7) |
| DS-06 | AISHE university directory | https://aikosh.indiaai.gov.in/home/datasets/details/all_universities_as_per_aishe_dashboard.html | XLSX | AISHE code, name, state, district, type | **Caveat:** IndiaAI Kosh requires clicking a form button; may need `requests.Session` with cookies OR manual download → place in `data/raw/` |
| DS-07 | ROR registry | https://ror.org | JSON API | Canonical IDs, aliases | Standard API or bulk dump |
| DS-08 | India HE geo (community) | https://github.com/notrueindian/india-higher-ed-db | CSV | `lat`, `long`, `Uni Classification`, `State` | `git clone` or raw GitHub CSV URL |

### 3.3 Tier 1 — Funding & enrichment

| ID | Source | URL | Use |
|----|--------|-----|-----|
| DS-09 | NSTMIS S&T Indicators | https://dst.gov.in/sites/default/files/Updated%20ST%20INDICATORS%20TABLES%202022-23.pdf | Sector R&D ₹ crores |
| DS-10 | DST Extramural R&D Directory | https://dst.gov.in/sites/default/files/EM%20Directory%202019-20.pdf | Project-level → sum by institution |
| DS-11 | DST R&D Institutions Directory 2025 | https://dst.gov.in/sites/default/files/Directory%20of%20RD%20Ins%202025.pdf | Addresses, institution list |
| DS-12 | NIRF official rankings | https://www.nirfindia.org/Rankings/2025/OverallRanking.html | HTML tables / PDF report cards |
| DS-13 | UGC university lists | https://www.ugc.gov.in/universitydetails | Central / State / Deemed counts |
| DS-14 | AISHE final reports | https://aishe.gov.in/aishe-final-report/ | Enrollment, aggregate finance |

### 3.4 Tier 2 — Optional validation

| ID | Source | URL |
|----|--------|-----|
| DS-15 | Semantic Scholar Graph API | https://api.semanticscholar.org |
| DS-16 | Crossref REST API | https://api.crossref.org |
| DS-17 | Unpaywall | https://unpaywall.org/products/api |
| DS-18 | OpenAlex snapshot (bulk) | https://openalex.org/download/snapshot |

### 3.5 OpenAlex feasibility (verified 2026-06-23)

```
Indian education institutions in OpenAlex:  1,684
Works with IN affiliation (2023 only):    414,638
IIT Kanpur ROR:                             https://ror.org/05pjsgx75
IIT Kanpur OpenAlex ID:                     https://openalex.org/I94234084
```

API etiquette: `User-Agent: CS661-IndiaNetwork/1.0 (mailto:YOUR_IITK_EMAIL)`

### 3.6 API call volume estimate

Rough order-of-magnitude for full pagination (if used):

| Scope | Estimate |
|-------|----------|
| Top 20 institutions | ~5,000–10,000 works/year each × 10 years ≈ 500K–1M works |
| Pages per institution | At `select=` with 200/page → ~2,500–5,000 pages each |
| **120 institutions total** | **~50,000–100,000 paginated requests** |
| At 10 req/s (polite pool) | **1.5–3 hours minimum**; realistically **overnight** with retries and cache resume |

**Mitigation (Phase 1 Step 1.1 — mandatory order):**

1. **Primary path — `group_by`:** co-institution pair counts without downloading every work:
   ```text
   GET /works?filter=institutions.id:{OPENALEX_ID},institutions.country_code:IN
       &group_by=authorships.institutions.id
   ```
   Gives edge weights in **O(N) requests** (≈120 calls) instead of O(N × pages). Apply W3 filter in post-processing on grouped pairs where metadata allows.

2. **Fallback — selective pagination:** if `group_by` undercounts (no `cited_by_count` per pair, or W3 cannot be applied cleanly), fetch full works **only for top 40** institutions by `total_works`; use OpenAlex snapshot or tier aggregates for the remaining 80.

3. **Last resort — full pagination:** paginate minimal work metadata per institution (Option 1 below). Cache each page; expect overnight run.

### 3.7 Ingestion strategy — Option 1 (fallback pagination)

Use when `group_by` path is insufficient. Do **not** use bulk snapshot on tight disk (~40 GB free).

**What we fetch per work (no abstracts, no PDFs):**

```text
GET /works?filter=institutions.id:{OPENALEX_ID},publication_year:{YEAR_MIN}-{YEAR_MAX}
    &select=id,publication_year,cited_by_count,authorships
    &per_page=200
```

Cache each page to `data/cache/openalex/works_{inst_id}_page_{n}.json` (resume-safe).

**Volume:** see §3.6. Disk for cached minimal JSON: typically **a few GB**, well under 40 GB.

**Deferred:** OpenAlex S3 snapshot (Option 3) — only if API budget exhausted and team has more disk/time.

Final `collaboration_edges` built from deduplicated work records + W3 filter in Python (§4.2).

### 3.8 Year range — dynamic end year

| Setting | Value | Notes |
|---------|-------|-------|
| `YEAR_MIN` | `2015` | Aligns with global dashboard slider |
| `YEAR_MAX` | **Auto-detected in Phase 0** | Not hard-coded to 2022 |

**Rule:** Run `scripts/india_network/00_detect_year_range.py` — count IN works per year 2015–current calendar year. Pick the latest year where count is **≥ 90% of the prior year's count** (guards against incomplete indexing). Expect **2023 or 2024**; avoid **2025–2026** for primary demo unless probe shows stability.

**SCImago is separate:** Q1% / h-index stay on static ~2019 snapshot (§4.3b). Year slider changes edges and OpenAlex volume/citations only.

### 3.9 International vs domestic papers (no data loss)

| Paper type | Example | In `total_works` / node size? | In domestic edges? |
|------------|---------|------------------------------|-------------------|
| Pure domestic | IITK + IIT Delhi only | Yes | Yes |
| Mixed intl | IITK + IIT Delhi + MIT | **Yes** (IITK output) | **No** (W3 fails) |
| Solo / foreign only | IITK + MIT only | Yes | No |

**UI on institution click:** show `total_works`, `domestic_collab_works`, and `intl_collab_share` so IIT Kanpur's global collaboration is visible without drawing non-domestic lines on the domestic network map.

---

## 4. Data model (backend)

### 4.1 `institution_master`

```text
institution_id          PK (internal UUID)
nirf_institute_id       e.g. IR-O-U-0456
openalex_id             e.g. I94234084
ror_id                  e.g. 05pjsgx75
scimago_idp             optional
canonical_name
tier                    premier | state_affiliated
inst_type               IIT | IISc | Central_Univ | State_Univ | NIT | ...
city, state
latitude, longitude
total_works             from OpenAlex institution object (all-time or year-range)
is_hub                  boolean (top 12–15 by network degree)
match_confidence        exact | fuzzy | manual
```

**Institution inclusion rules (tiered threshold):**

| Tier | `total_works` threshold | Cap | Rationale |
|------|----------------------|-----|-----------|
| `premier` | `total_works >= 50` | Top 60 by `total_works` desc | Research-active elite institutions |
| `state_affiliated` | `total_works >= 10` | Top 60 by `total_works` desc | Allows state universities that publish modestly to appear on map |

Both tiers require resolvable `latitude`/`longitude` (OpenAlex geo OR geo CSV fallback). Total master list capped at **120 institutions** (60 premier + 60 state).

> **Why tiered:** A single `>= 50` threshold eliminates nearly all state universities from the map because their OpenAlex affiliation strings are poorly resolved. The lower `>= 10` for state tier preserves the visual story of "many but weak" while still excluding zero-research affiliated colleges.

### 4.2 `collaboration_edges`

```text
inst_a, inst_b          FK → institution_master
year                    int
weight                  co-authored paper count (domestic only)
citation_weight         optional sum of citing counts
```

**Domestic-only filter (W3 — corrected):**

> W3 (corrected): A work is domestic if every element of `authorships[].institutions[]` has `country_code == 'IN'`, AND at least **2 distinct institution IDs** from that list appear in `institution_master`. Works with no institutional affiliation recorded are **excluded** (not assumed domestic).

> **Implementation note:** Use `authorships[i].institutions[j].country_code`, not `authorships[i].countries`. The latter is author-level and may be empty for unaffiliated authors.

Legacy incorrect rule (do not implement): ~~every authorship has `countries == ['IN']`~~.

### 4.3 `institution_metrics` (yearly — time-varying only)

> **Implementation note (2026-07-08):** There is no standalone `07_build_institution_metrics.py`. Yearly `total_works`, `domestic_collab_works`, and citation rollups are computed at export time in `09_export_payloads.py` from `domestic_works.parquet` + `institution_master.csv`. The schema below remains the logical model.

```text
institution_id, year
total_works             all published works by institution (year-filtered; OpenAlex `.works_count` / yearly rollup)
domestic_collab_works   count of works passing W1–W5 filters (from domestic_works.parquet)
cited_by_count          sum of citations on that year's works
citations_per_work      cited_by_count / total_works
funding_inr_cr          from NIRF/DST when available (null in v1)
```

| Column | Definition | Source | Used for |
|--------|------------|--------|----------|
| `total_works` | All published works by institution | OpenAlex institution object `.works_count` field (year-filtered in metrics table) | Node circle area on map |
| `domestic_collab_works` | Works passing all W1–W5 filters | Count from `domestic_works.parquet` | Edge weight narrative only |

> **Critical distinction:** Never add these two figures. `total_works` is a **superset** of `domestic_collab_works`. Node size uses `total_works`; edges use domestic pairs only.

**SCImago fields are NOT in this table** — see §4.3b (`institution_quality_static`). Year-varying metrics keep only OpenAlex volume/citation fields.

### 4.3b `institution_quality_static` (time-invariant SCImago snapshot)

```text
institution_id
scimago_q1_pct          single value (snapshot ~2019)
scimago_h_index         single value
scimago_year            label: "2019" — display as footnote in UI
```

> **Why static:** SCImago's free CSV export provides a single snapshot (approximately 2019 data). There is no year-by-year institution CSV available for free. These fields do NOT change when the year slider moves. In JSON payloads and tooltips, always display as `"Q1%: 67 (2019 data)"` with the `scimago_year` label for graphical integrity.

### 4.4 `tier_aggregates` (for default UI strip)

> **Implementation note (2026-07-08):** There is no standalone `08_compute_tier_aggregates.py`. Tier summaries in JSON payloads (`tier_panels` / `tier_summary`) are computed inline in `09_export_payloads.py`. NIRF funding joins use `08_join_nirf_funding.py` instead.

```text
tier, year
institution_count
total_works, mean_citations_per_work
mean_q1_pct
total_funding_inr_cr
total_enrollment        narrative from AISHE (optional)
```

### 4.5 API payloads (two levels)

**Overview (grid thumbnail):** `GET /api/india/network?year=2022&detail=overview` → **&lt; 40 KB**

```json
{
  "year": 2022,
  "nodes": [ /* ~45: 12 labeled hubs + faint satellites */ ],
  "edges": [ /* hub-hub only */ ],
  "tier_summary": [ /* 2 rows, 2 metrics each */ ],
  "annotations": ["NCR Hub", "Bengaluru Hub", "Mumbai-IITB Corridor"]
}
```

**Fullscreen (expanded):** `GET /api/india/network?year=2022&detail=full` → **&lt; 200 KB**

```json
{
  "year": 2022,
  "quality_year": 2019,
  "quality_note": "Q1% and h-index from SCImago 2019 snapshot; do not vary with year slider",
  "nodes": [ /* up to ~80 institutions with full metrics */ ],
  "edges": [ /* all edges with weight >= 2 (max 200) */ ],
  "tier_panels": {
    "premier": { "cit_per_paper", "q1_pct", "funding_cr", "total_works", ... },
    "state_affiliated": { ... }
  },
  "institution_detail": { /* keyed by id; includes total_works, domestic_collab_works, citations_per_work, scimago_q1_pct, scimago_h_index */ }
}
```

Full DB holds 120 institutions (60 premier + 60 state) and all edges; browser loads overview on grid mount, full payload only on expand.

---

## 5. Entity resolution

**Institution cap (cross-ref §4.1):** master list = top **60 premier** (`total_works >= 50`) + top **60 state_affiliated** (`total_works >= 10`), sorted by `total_works` desc, max **120** total.

**Order of matching:**
1. Manual override CSV: `data/manual_institution_overrides.csv` (23 IITs, IISc, major NITs) — highest priority
2. `ror_id` exact (OpenAlex ↔ ROR)
3. `nirf_institute_id` from NIRF CSV
4. Fuzzy name + city + state (`rapidfuzz`, threshold ≥ 90)

### Hub selection — build order (mandatory sequence)

Hub selection depends on the full edge graph and must follow this strict order:

```text
Step 1: Build ALL edges at minimum threshold (weight >= 2, all-years rollup)
        → collaboration_edges_full.csv

Step 2: Compute degree_centrality on this full graph
        → Rank all 120 institutions

Step 3: Mark is_hub=True for:
        - Top 12 by degree
        - Force-include at least 1 per corridor: NCR, Bengaluru, Mumbai, Chennai (by city match)
        → hub_flags.csv (joined back to institution_master)

Step 4: Export scripts apply is_hub as a DISPLAY FILTER only
        - Overview: show only hub-hub edges (E2)
        - Full: show all edges above threshold (no hub restriction)
```

> **No circular dependency:** Hubs are computed once after full edge build. They are never used as a fetch filter — only as a display filter during JSON export. If edges change (e.g., year range widened), re-run from Step 1.

---

## 6. Execution plan

### Phase 0 — Feasibility gate (1–2 days) ⬅ START HERE

| Step | Task | Done when |
|------|------|-----------|
| 0.0 | Run `00_detect_year_range.py` → set `YEAR_MAX` in `config.py` | `data/processed/year_range.json` |
| 0.1 | Download DS-01, DS-03, DS-06, DS-08 | Files in `data/raw/` |
| 0.2 | Script `02_fetch_openalex_institutions.py` | `data/processed/openalex_institutions.parquet` |
| 0.3 | Script `03_build_institution_master.py` | `institution_master.csv` ≥ 80 rows matched |
| 0.4 | Script `04_feasibility_domestic_edges.py` (top 30 inst; group_by OK here only) | Report: edge count, domestic % |
| 0.5 | **Gate:** if &lt; 500 domestic edges among top 30 → widen year range or lower threshold | `feasibility_report.md` |

### Phase 1 — Full ETL (3–5 days)

| Step | Task | Output |
|------|------|--------|
| 1.1 | **Primary:** `group_by=authorships.institutions.id` per master institution (§3.6). **Fallback:** paginate minimal metadata for top 40 only (§3.7). **Last resort:** full pagination all 120 | Pair counts and/or `data/cache/openalex/` |
| 1.1b | **Deduplicate works on `work_id`** — same paper fetched via multiple institutions must count once only | `data/processed/domestic_works.parquet` (unique on `work_id`) |
| 1.2 | Build `collaboration_edges_full.csv` (all pairs, weight >= 2, all years) | domestic pairs |
| 1.2b | Compute hub flags from full edge graph (see §5 build order) | `hub_flags.csv` |
| 1.3 | Join SCImago → `institution_quality_static` table | `07_join_scimago_quality.py` → `institution_quality_static.csv` |
| 1.4 | Join NIRF funding + patents | `08_join_nirf_funding.py`, `08b_join_nirf_patents.py` |
| 1.5 | Export two JSON payloads per year (overview + full); **yearly metrics and tier summaries computed inline** in export (no separate metrics script) | `09_export_payloads.py`, `09b_export_year_slices.py` → `public/india_network/{year}_overview.json`, `{year}_full.json` |

> **Deduplication (Step 1.1b) is mandatory:** When fetching works per institution, the same `work_id` will appear in multiple institution batches (e.g., a paper co-authored by IIT Kanpur and IIT Delhi is fetched twice). Before building edges, run `df.drop_duplicates(subset='work_id')`. Without this, edge weights (co-publication counts) will be inflated by the number of co-authoring institutions fetched.

### Phase 2 — Visualization (3–5 days)

| Step | Task | Output |
|------|------|--------|
| 2.1 | India outline GeoJSON (simplified) | `india_states_topo.json` |
| 2.2 | D3 component: `IndiaNetworkPanel.jsx` | map + nodes + edges |
| 2.3 | Tooltip + click highlight | ego-network |
| 2.4 | Tier comparison strip (2 metrics) | bottom of panel |
| 2.5 | Wire to global year filter | sync with other 4 modules |
| 2.6 | Pass chartjunk checklist (§2.3) | review |

### Phase 3 — Integration & demo (2 days)

| Step | Task |
|------|------|
| 3.1 | Flask route or static JSON serve |
| 3.2 | Fit panel in 1080p grid layout |
| 3.3 | Prepare 3 demo questions (see §7) |
| 3.4 | Screenshot + report paragraph |
| 3.5 | **Run verification checklist (mandatory before demo)** |

**Verification checklist:**

- [ ] `institution_master.csv` has >= 80 rows, >= 90% with valid lat/lon
- [ ] `collaboration_edges_full.csv` has >= 200 edges (all years, weight >= 2)
- [ ] `2022_overview.json` is < 40 KB; `2022_full.json` is < 200 KB
- [ ] **Positive test:** find a known IIT Kanpur + IIT Delhi domestic paper → confirm it **is present** in `domestic_works.parquet` and increments edge `weight` correctly in `collaboration_edges_full.csv`
- [ ] **Negative test:** pick a known joint IIT Kanpur + foreign-affiliation paper (e.g., with MIT or Stanford co-author) → confirm it is **absent** from `domestic_works.parquet`
- [ ] No edge exists where either endpoint is a non-IN institution
- [ ] Year slider: 2015 and 2022 produce different edge weights (temporal change visible)
- [ ] SCImago fields show `(2019 data)` footnote in tooltip — do not vary with year slider

### Suggested repo layout

```text
CS661/
├── india_domestic_he_network_plan.md    ← this file
├── requirements-india-network.txt
├── data/
│   ├── raw/                             # downloaded CSV/XLSX
│   ├── cache/openalex/                  # paginated API responses
│   ├── processed/                       # master tables
│   └── manual_institution_overrides.csv
├── scripts/india_network/
│   ├── config.py
│   ├── 00_detect_year_range.py
│   ├── 01_download_sources.py
│   ├── 02_fetch_openalex_institutions.py
│   ├── 03_build_institution_master.py
│   ├── 04_feasibility_domestic_edges.py
│   ├── 05_fetch_openalex_works.py
│   ├── 06_build_domestic_edges.py
│   ├── 07_join_scimago_quality.py          # was planned as 07_build_institution_metrics.py (deprecated name)
│   ├── 08_join_nirf_funding.py             # was planned as 08_compute_tier_aggregates.py (deprecated name)
│   ├── 08b_join_nirf_patents.py
│   ├── 09_export_payloads.py               # institution_metrics + tier_aggregates computed here at export time
│   ├── 09b_export_year_slices.py
│   └── 10_verification_checklist.py
├── public/india_network/
│   └── {year}_overview.json / {year}_full.json
└── hierarchy-app/
    └── src/components/IndiaNetworkPanel.jsx
```

---

## 7. Demo questions (examiner-ready)

The panel must answer these in **&lt; 10 seconds** each without scrolling:

1. **Where are India's domestic research hubs?** → visible dense blue clusters (NCR, Bengaluru, Mumbai)
2. **Is output quality equal across tiers?** → tier strip: cit/paper premier vs state
3. **Does funding follow the same pattern?** → funding dumbbell / bar in tier strip
4. **Who does IIT Kanpur collaborate with domestically?** → click node → ego highlight
5. **How does 2015 compare to 2022?** → global year slider → edge thickness changes

---

## 8. Risks

| Risk | Mitigation |
|------|------------|
| Panel too crowded on 1080p | Strict hub-only default; details on hover |
| OpenAlex rate limits | Primary `group_by` (§3.6); selective pagination top 40; full pagination overnight; cache resume |
| Name mismatch | ROR + manual overrides (23 IITs pre-mapped) |
| Funding gaps for state colleges | Tier aggregate from NSTMIS; footnote in tooltip |
| SCImago year stale | Treat as static snapshot; label `(2019 data)` in tooltip for integrity |
| Lie factor on node size | Use √radius scaling |
| State tier visually underrepresented on map | Explicit footnote in visualization; tier strip sourced from AISHE aggregate, not map nodes |
| Duplicate work_ids inflating edge weights | Mandatory dedup step 1.1b on `work_id` before edge aggregation |
| Proposal says treemap/sunburst; build is network | Add justification paragraph to final report (see §12) |

---

## 9. Agent handoff instructions

When continuing this work:

1. Read this file first.
2. Check `data/raw/` — if empty, run **Phase 0**.
3. Check `feasibility_report.md` — do not build UI until gate passes.
4. Match color scheme §2.1 exactly for dashboard cohesion.
5. Do **not** expand scope to 45k nodes; aggregate state tier.
6. Pre-compute all payloads; browser only renders JSON.
7. Cross-reference course rules: `markdown_files/markdown_files/Lecture2_*.md` (mantra), `Lecture10_*.md` (integrity, 7±2, chartjunk).
8. Update **§10 Status log** below on every session.

---

## 10. Status log

| Date | Agent | Action | Next |
|------|-------|--------|------|
| 2026-06-23 | Cursor | Created master plan; OpenAlex feasibility verified | Phase 0 downloads + `build_institution_master.py` |
| 2026-06-23 | Cursor | Added two-level UI: 5-panel grid → click fullscreen; focus+context in expand | Implement `detail=overview\|full` API split |
| 2026-06-23 | Cursor | Applied 11-issue critique fix patch | Begin code with corrected thresholds and filter definitions |
| 2026-06-23 | Cursor | **Phase 0 progress:** institutions snapshot complete (50/50 parts, 177MB); `openalex_institutions.parquet` = 1,603 IN education rows; `institution_master.csv` = 142 rows (82 premier, 60 state); `year_range.json` YEAR_MAX=2024 (API blocked); manual overrides RORs fixed; feasibility report written (edges pending) | Run `05_fetch_openalex_works.py --pilot-top 30` after API budget resets |
| 2026-06-23 | Cursor | Cap fix: `institution_master.csv` = **120** (60+60); IIT Madras/Palakkad override IDs; `--pilot-top N` on script 05 | `05 --pilot-top 30` when OpenAlex budget resets |
| 2026-07-01 | Cursor | **Pipeline complete:** 120/120 OpenAlex cache; 13k+ edges; NIRF funding 116/120; patents 42/120 after duplicate-resolved join; verification 11/11; dashboard JSON + UI | UI polish; Modules 1–4 real ETL (team) |

---

## 11. Related project files

| File | Relevance |
|------|-----------|
| `databases.md` | Global dataset inventory |
| `project_knowledge_base.md` | Project-wide context |
| `hierarchy-app/src/App.jsx` | React+D3 POC (tree, not map — reuse patterns only) |
| `animation.html` | D3 interaction patterns (hover, filter) |
| `CS661 project notes.docx` | Image 5 prototype reference |
| `markdown_files/.../CS661_PROJECT.md` | Official §4.6 India module spec |

---

## 12. Proposal vs implementation alignment

The submitted `CS661_PROJECT.md` §4.6 specifies:

> "Hierarchical Treemaps or Zoomable Sunburst Diagrams"

The actual implementation is a **geospatial node-link network**. These are fundamentally different visual forms.

**Why the change is justified (include this paragraph in the final report):**

After data exploration, the core analytical structure of India's domestic research collaboration is **relational** — it consists of edges (co-authorship links) between institutions spread across geography. A treemap or sunburst encodes hierarchical containment (parent → child), which does not naturally represent pairwise collaboration intensity, geographic clustering of hubs, or the hub-vs-periphery topology that answers our key demo questions. A node-link network layout on a geographic base map (Lecture 9: network visualization objectives; Lecture 2: geographic encoding for spatial data) directly encodes:
- **Position** → where institutions are
- **Edges** → who collaborates with whom
- **Node size** → research volume
- **Color** → tier membership

This makes the network form the analytically correct choice for co-authorship data. The hierarchy (tier → institution) is still encoded in the **tier side panels** and **color channel**, preserving the original proposal's intent to show "variance between elite central campuses and broader state infrastructures."

**Action required:** No code change. Add this justification as one paragraph in the final project report under Module 5 description.

---

*ICM_RULES_CHECK=five-layer-glass-box-sequential-review*
