# AGENTS.md

## Cursor Cloud specific instructions

This repo is a single **static, vanilla-JS visual-analytics dashboard** (`dashboard/`) plus an
**optional Python ETL pipeline** (`scripts/india_network/`). There is **no backend, no database,
no Node/npm, and no build step**. See `README.md` for the canonical run/setup commands.

### Services

| Service | Required? | How to run | Notes |
|---------|-----------|------------|-------|
| Dashboard static server | Yes (to view/test) | `cd dashboard && python3 -m http.server 8766` then open `http://localhost:8766` | Must be served over HTTP, not `file://` — Module 5 uses `fetch()` for JSON/GeoJSON which browsers block over the file protocol. |
| Module 5 ETL | Optional | See `README.md` "Module 5 ETL" | Only needed to regenerate India network data; pre-computed JSON is already committed under `dashboard/data/india_network/`. |

### Non-obvious caveats

- **Internet/CDN is required at runtime.** `dashboard/index.html` loads D3 v7, TopoJSON, Leaflet,
  and Google Fonts from CDNs. A vendored `dashboard/d3.v7.min.js` exists but is **not** wired into
  `index.html`, so charts/map need network access to render. Cloud VMs have this by default.
- **Modules 1–4 use hardcoded synthetic data** in `dashboard/data.js`. Only **Module 5** (India
  network) is backed by real data loaded from `dashboard/data/india_network/*.json`.
- **No lint or automated test suite exists** (no linters, no test framework, no `package.json`).
  "Testing" is manual: serve the dashboard and interact with the visualizations in a browser.
- **README/pipeline commands are PowerShell-oriented** (`copy`, `Copy-Item`, `.ps1` runner). On this
  Linux VM substitute `cp -r` for the copy steps if you ever run the optional ETL.
- `README.md` mentions `pdfplumber` for the ETL PDF-scraping scripts, but it is **not** listed in
  `requirements-india-network.txt`. Install it separately only if running those specific scripts.
- The optional ETL fetch stage needs `OPENALEX_API_KEY` in a `.env` file (copy from `.env.example`).
  Not needed to view/test the dashboard.
