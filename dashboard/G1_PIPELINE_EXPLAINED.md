# Graph 1 pipeline — where each number comes from

**Metaphor:** river (CSV sources) → pool (`viz1_data.js`) → tap (`app.js` / Plotly HTML)

**Name map (spoken → source):**
- **Credit line** = footer text under each viz (`VIZ_META[n].credit` in `app.js`)
- **OpenAlex** = open scholarly works API / our topic & docs extracts
- **SCImago** (“Cyma”) = SCImago Journal & Country Rank exports
- **Country Rank** = SCImago **countryrank** (H-index stock), not journalrank

---

## What each bubble uses

| Field in pool / tooltip | Meaning | River source | File(s) |
|-------------------------|---------|--------------|---------|
| `GDP_Per_Capita_PPP` | Wealth | World Bank WDI `NY.GDP.PCAP.PP.CD` | `raw_vault/01_world_bank/` → panel |
| `GERD_Percent_GDP` | R&D intensity | World Bank WDI `GB.XPD.RSDV.GD.ZS` (UIS via WDI) | same |
| `Total_Docs` | Publication volume (single channel) | **World Bank** `IP.JRN.ARTC.SC` journal articles whenever present; else **SCImago** Country Rank `Documents`. **Never OpenAlex** (works ≫ articles — see `G1_TOTAL_DOCS_POLICY.md`) | panel `WB_Pubs` / `SCImago_Documents` |
| `H_Index` | Quality stock (flat across years) | SCImago **Country Rank** `H index` | `02_scimago_country/` |
| `x`, `y` | Peer layout | **Computed** UMAP on the four features above | `dashboard/_regen_viz1_umap.py` |
| `Region` | Color group | Geography label carried into pool | in pool |

## Flow (end-to-end)

```
World Bank zips (GDP, GERD, journal articles)
      │
      ├──────────────────┐
      ▼                  ▼
SCImago countryrank   (H-index + Documents fallback for Total_Docs)
      │                  │
      └────────┬─────────┘
               ▼
      g1_features_panel.csv  (READY_FOR_TEAM)
               │
               ▼
      _regen_viz1_umap.py  (impute GERD → coalesce WB→SCImago docs → UMAP → x,y)
               │
               ▼
      dashboard/viz1_data.js   ←── POOL
               │
               ▼  <script src="viz1_data.js">
      app.js renderViz1() → Plotly bubbles  ←── TAP
```

OpenAlex country-year works (`OA_Docs`) may sit on the panel as a **side column** for research, but they do **not** feed `Total_Docs`, bubble size, or UMAP.

**How HTML sees it:** `index.html` loads `viz1_data.js` as `VIZ1_DATA`. Opening viz 01 runs `renderViz1()`, which filters by year slider and plots `x,y` with size ≈ docs and tooltip from the same row. No live World Bank / OpenAlex calls at runtime — only the pool file.

## Why not all old rows got new UMAP coords

UMAP needs **all four** features present (after GERD fill). Many small countries / years lack GERD, docs, or H.

| Policy | What happens | Result |
|--------|--------------|--------|
| **Old (wrong)** | Keep incomplete rows with **pre-fix** `x,y` | Mixed map: some peers on new layout, some still on wrong-H layout |
| **Current** | **Drop** incomplete rows | Every bubble on screen has regenerated coords + correct H |
| **Improved impute** | Country ffill/bfill → region-year median → year median + coalesce docs **WB → SCImago only** (never OA) | More countries become UMAP-ready without mixing article/works scales |

We do **not** invent fake GDP/H just to force 6022 points — that would lie harder than dropping sparse cells.

## What “fix the credit line” means

The HTML footer must name the rivers that actually feed Graph 1:

`World Bank (GDP, GERD, journal articles) · SCImago Country Rank (H-index; Documents fallback) · UMAP`

Do **not** credit OpenAlex for G1 bubble size — OA works are a different, larger corpus (see `G1_TOTAL_DOCS_POLICY.md`).

## Other graphs (same river → pool → tap idea)

| Graph | River | Pool file | What “fix it” means in TAP |
|-------|-------|-----------|------------------------------|
| **G2** | SCImago **journalrank** `Country` = **publisher country** | `ridgeline_data.js` | Say publisher country; credit SJR journalrank; uncapped ratio in pool |
| **G3** | OpenAlex topic concepts (`C…` ids) | `viz3_data.js` | Credit OpenAlex; Quantum = `C58053490` not Materials; CSS `--g-quantum` |
| **G4** | OpenAlex collab cites (shipped sample) | `viz4_data.js` | Say **Top 20 / 2024**, not 111 countries |
| **G5** | NIRF · ROR · SCImago India network | `india_network_data.js` | Already aligned; keep credits honest |
