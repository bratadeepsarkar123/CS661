# Module 1 Design Variants — Selection Index

**Scope:** High-Dimensional Peer Clustering / Macro Spend vs Outcomes (Panel 1 — t-SNE story + alternatives)  
**Status:** Planning only — no implementation until one variant is chosen  
**Constraints:** Lecture 2/10 (overview→detail, 7±2, Tufte integrity), dark theme `#0f172a`, pre-computed JSON  
**Data today:** `dashboard/data.js` uses synthetic placeholder arrays — real ETL not yet wired

| ID | Name | One-line pitch | Best for |
|----|------|----------------|----------|
| [M1-01](module1/M1-01-scatter-efficiency-frontier.md) | Scatter Efficiency Frontier | R&D spend vs citation yield with regression frontier | “Who converts money into impact?” |
| [M1-02](module1/M1-02-slopegraph-spend-outcome.md) | Slopegraph Spend→Outcome | 1996→2024 paired slopes for spend and output | Long-run convergence story |
| [M1-03](module1/M1-03-small-multiples-lollipop.md) | Small Multiples Lollipop | Faceted lollipops: bar=GERD%, dot=citations/paper | Country-by-country comparison |
| [M1-04](module1/M1-04-parallel-coordinates-he.md) | Parallel Coordinates HE | Brushable 5-axis profile (GERD, researchers, pubs, cites, h-index) | High-dimensional peer groups |
| [M1-05](module1/M1-05-bump-chart-roi-rank.md) | Bump Chart ROI Rank | Animated rank of efficiency metric 1996–2024 | Temporal leaderboard drama |
| [M1-06](module1/M1-06-dot-matrix-linked.md) | Dot Matrix Linked | Rows=countries, columns=indicators, linked highlight | Compact overview grid cell |
| [M1-07](module1/M1-07-marimekko-spend-share.md) | Marimekko Spend Share | Width=global GERD share, height=outcome tier split | Macro concentration narrative |
| [M1-08](module1/M1-08-diverging-bar-residual.md) | Diverging Bar Residual | Spend minus model-expected output (signed residual) | Outlier / over- & under-performers |

## Recommendation (planner default)

**Primary:** M1-01 (Scatter Efficiency Frontier) — clearest single insight for the wealth→knowledge paradox; maps directly to proposal §4.1 macro story.  
**Runner-up:** M1-08 (Diverging Bar Residual) for overview thumbnail if grid cell must stay text-readable at small size.

## Data layer (shared by all variants)

- **UNESCO UIS:** GERD as % GDP (`EXPGDP.TOT`), researchers per million, HE expenditure (`stats.uis.unesco.org`, BDDS/API)
- **World Bank Open Data:** GDP (current US$), PPP, R&D % GDP, scientific articles (`data.worldbank.org`)
- **OECD MSTI:** Sector-split R&D for OECD members (`stats.oecd.org`)
- **SCImago SJR:** Country publications, citations, h-index (1996–2024, Kaggle/API)
- **Target payload:** `public/data/module1_expenditure_outcomes.json` — one row per country×year, ~180 countries × 29 years, client-side aggregates only

## Out of scope (teammates)

- Module 5 India geo network patterns — do not reuse as Panel 1  
- Live API calls in browser — batch ETL only (mirror `scripts/india_network/`)
