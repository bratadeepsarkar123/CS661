# CS661 — The Global Knowledge & Wealth Paradox

**Group 10 · IIT Kanpur · CS661 Big Data Visual Analytics**

Interactive five-panel visual analytics dashboard exploring how national wealth, R&D investment, and institutional density translate into scientific output — with a deep-dive on India's domestic higher-education collaboration network.

## Quick start (dashboard)

```powershell
cd dashboard
python -m http.server 8766
```

Open **http://localhost:8766** → click any panel for fullscreen interaction.

Module 5 (India network) loads pre-computed JSON from `dashboard/data/india_network/`.

## Module 5 ETL (India Domestic HE Network)

Pipeline lives in `scripts/india_network/`. Requires Python 3.10+, pandas, pyarrow, requests, pdfplumber.

### Setup

```powershell
pip install -r requirements-india-network.txt
copy .env.example .env
# Edit .env: set OPENALEX_API_KEY=... (from openalex.org/settings/api)
```

### Run full export chain (after cache is complete)

```powershell
python scripts/india_network/08b_join_nirf_patents.py
python scripts/india_network/09b_export_year_slices.py
Copy-Item public\india_network\* dashboard\data\india_network\ -Recurse -Force
python scripts/india_network/10_verification_checklist.py
```

Verification report: `data/processed/verification_report.md` (target: all checks pass).

### Key outputs

| File | Description |
|------|-------------|
| `data/processed/institution_master.csv` | 120 institutions (60 premier + 60 state) |
| `data/processed/collaboration_edges_full.csv` | Domestic co-auth edges |
| `data/processed/institution_funding.csv` | NIRF funding (116/120 from official PDFs) |
| `data/processed/institution_patents.csv` | NIRF patents (42/120 after duplicate-resolved join) |
| `dashboard/data/india_network/*.json` | Year slices 2015–2024 for the UI |

## Architecture

| Layer | Stack |
|-------|-------|
| Dashboard UI | Vanilla JS + D3.js v7 + Leaflet (`dashboard/`) |
| Module 5 ETL | Python batch scripts → CSV/Parquet → JSON |
| Modules 1–4 | **Placeholder synthetic data** in `dashboard/data.js` — real ETL pipelines not yet implemented |

> **Team note:** Modules 1–4 (t-SNE clustering, ridgeline, bar-chart race, dumbbell plot) currently use hardcoded demo arrays in `dashboard/data.js`. Only Module 5 uses real OpenAlex + NIRF data. See `lecture-driven-dashboard-plan.md` for the intended five-panel layout and lecture design contract.

The submitted proposal mentions React+Vite; the working dashboard uses vanilla JS for faster iteration. Document this deviation in the final report (see `india_domestic_he_network_plan.md` §12).

## Planning documents

| Document | Purpose |
|----------|---------|
| `CS661_PROJECT.md` | Official proposal |
| `lecture-driven-dashboard-plan.md` | Five-panel layout + lecture principles |
| `india_domestic_he_network_plan.md` | Module 5 master plan (ETL + viz spec) |
| `data/processed/nirf_coverage_gaps.md` | Institutions missing NIRF funding/patents |

## Data sources (Module 5)

- **OpenAlex** — works, institutions, domestic co-authorship (2015–2024)
- **NIRF official PDFs** — funding + patents (free, nirfindia.org CDN)
- **SCImago Institutions** — static quality snapshot (~2019)
- **AISHE / geo CSV** — institution locations

Four institutions are not in NIRF 2024 rankings (no official PDF exists). Patent counts use Innovation-category PDFs only; institutes without those PDFs show `patent_status: unavailable` in the UI.

## Course requirements checklist

- [x] Custom D3.js visualizations (no Tableau/PowerBI)
- [x] Five interactive visualization modules
- [x] Module 5 real data pipeline with verification
- [ ] Modules 1–4 real data pipelines (synthetic placeholders today)
- [x] README with run instructions
- [ ] GitHub repository (initialize locally; push to remote when ready)

## Team

See `CS661_PROJECT.md` §7 for role assignments.
