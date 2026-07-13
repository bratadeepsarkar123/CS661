# Fact-check checklist (G1–G5)

**Audience:** teammates verifying the live dashboard  
**Serve:** `python -m http.server 8080 --directory dashboard --bind 127.0.0.1` then **Ctrl+F5**

Anchors below use **USA** and **India**, year **2022** unless noted.

---

## Prep

- [ ] Dashboard loads on http://127.0.0.1:8080
- [ ] `index.html` loads modular `graphs/gN/gN.js` (not a single mega-`app.js` graph body)
- [ ] No real API keys in any file you are about to share

---

## G1 — Peer clusters (`viz1_data.js`)

- [ ] Open Graph 1; USA 2022 **H_Index ≈ 3388** (SCImago stock), **not** ~53 stub scale
- [ ] India 2022 **H_Index ≈ 1001**
- [ ] USA 2022 GERD ≈ **3.49** (`GERD_Source` WB); India 2022 GERD ≈ **0.646** with `LOCF:WB:y2020` (display LOCF — river may lack 2021–22)
- [ ] Bubble size policy: WB scientific articles, else SCImago Documents — **not** OpenAlex country totals ([`../G1_TOTAL_DOCS_POLICY.md`](../G1_TOTAL_DOCS_POLICY.md))
- [ ] Optional: compare `READY_FOR_TEAM/g1_features_panel.csv` + `gerd_pct_gdp_hierarchical.csv`

---

## G2 — Quality shift (`ridgeline_data.js`)

- [ ] UI / report wording says **publisher country**, not author nationality
- [ ] Ratios are **uncapped** in pool (e.g. elite publishers can exceed 5)
- [ ] Sidebar H / GDP / GERD for a country-year **join from G1** (same LOCF GERD story)
- [ ] River: `READY_FOR_TEAM/q1_q4_country_year.csv` + `_notes/G2_PUBLISHER_SCHEMA_NOTE.md`

---

## G3 — Topics (`viz3_data.js`)

Live L3 topics (exactly **7**):

1. Infectious disease  
2. Robotics  
3. Quantum computer (`C58053490`)  
4. CRISPR  
5. Energy storage  
6. Photovoltaics  
7. Supervised learning (`C119857082` family / Machine learning primary — see topic map)

Checks:

- [ ] Quantum is **not** Materials Science ASJC 2500
- [ ] AI/ML primary is **Machine learning** `C119857082`, not mega-AI `C154945302` in the pool
- [ ] Shared honest window ~**1974–2024** (no hard “field birth” zero floors)
- [ ] Infectious 2019→2020 spike treated as **real corpus**, not a pipeline bug
- [ ] Optional L2 demo on `:8085` does **not** change `:8080` G3

Rebuild path: `CS661_Dataset/raw_vault/04_openalex/fetch_topics_full.py` → river CSV → `dashboard/_river_to_pool_rebuild.py`  
**Not:** root `scrape_openalex_data.py` (ASJC / non-canonical).

---

## G4 — Collaboration premium (`viz4_data.js`)

- [ ] Chart family is **dumbbell** (not overnight grouped bars)
- [ ] `VIZ4_META.n_countries === 73` (`n_core20=20`, `n_expanded=53`)
- [ ] Years **2010–2024**
- [ ] Do **not** cite unverified old **111** undated snapshot (`viz4_data_BEFORE_POOLFIX.js`)
- [ ] River: `CS661_Dataset/collaboration_premium.csv` (+ READY_FOR_TEAM expanded copies)

---

## G5 — India network

- [ ] Map loads from `data/india_network/{year}_*.json`
- [ ] NIRF rank / funding / patents follow carry footnotes — no invented years ([`GRAPH5_DATA_PRESENTATION_POLICY`](../../docs/GRAPH5_DATA_PRESENTATION_POLICY.md))
- [ ] Post **edge-vis revert**: no “hanging edge” filter experiment — edges behave as pre-fix
- [ ] Region cluster blend flag may still be on (`VIZ5_REGION_BLEND`); that is separate from edge-vis revert

---

## Cross-cutting

- [ ] Any “publications” claim names the **correct river** (G1 docs ≠ G2 publisher docs ≠ G3 concept works)
- [ ] Report abstract does **not** claim React if you already fixed it — if not, flag it
- [ ] `.env` present locally only when rebuilding OpenAlex; never in zip
