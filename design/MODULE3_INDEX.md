# Module 3 Design Variants — Selection Index

**Scope:** Top-10 Research Topics (Panel 3 — bar chart race)  
**Status:** Planning only — teammates implement  
**Data today:** Synthetic `TOPICS` in `dashboard/data.js`

| ID | Name | One-line pitch | Best for |
|----|------|----------------|----------|
| [M3-01](module3/M3-01-horizontal-bar-race.md) | Horizontal Bar Race | Classic rank animation over years | Proposal §4.3 default |
| [M3-02](module3/M3-02-bump-rank-trails.md) | Bump Rank Trails | Lines track rank 1–10 over years | Rank volatility story |
| [M3-03](module3/M3-03-stream-topic-share.md) | Stream Topic Share | Topic stacks as % of top-10 volume | Composition view |
| [M3-04](module3/M3-04-sparkline-grid.md) | Sparkline Grid | 10 mini sparklines, no motion | Accessibility |
| [M3-05](module3/M3-05-snapshot-diff.md) | Snapshot Diff | 2010 vs 2024 side-by-side bars | Static overview cell |
| [M3-06](module3/M3-06-field-color-legend.md) | Field Color Legend | Bars colored by OpenAlex field (≤7 hues) | Category encoding |
| [M3-07](module3/M3-07-scrubber-hero.md) | Scrubber Hero | Large year scrubber drives bar positions | Temporal control |
| [M3-08](module3/M3-08-footnote-openalex-lag.md) | Footnote OpenAlex Lag | Metadata caveats + minimal race | Academic integrity |

## Recommendation

**Primary:** M3-01 (Bar Race)  
**Runner-up:** M3-04 for reduced motion

## Data layer

- OpenAlex concepts aggregated by year
- Top-10 per year pre-computed in Python → `module3_topics.json`
