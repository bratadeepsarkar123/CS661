# Module 2 Design Variants — Selection Index

**Scope:** Global Quality Shift (Panel 2 — ridgeline / Q1 vs Q4)  
**Status:** Planning only — teammates implement  
**Data today:** Synthetic placeholder in `dashboard/data.js`  
**ETL reference:** `global_quality_shift_agent_handoff.md`

| ID | Name | One-line pitch | Best for |
|----|------|----------------|----------|
| [M2-01](module2/M2-01-classic-ridgeline.md) | Classic Ridgeline | Stacked KDE curves per year, Q1 vs Q4 hue | Proposal §4.2 faithful |
| [M2-02](module2/M2-02-bimodal-split-annotations.md) | Bimodal Split Annotations | Three era labels: Parity, Breakaway, Q4 Flood | Docx wireframe story |
| [M2-03](module2/M2-03-streamgraph-quality.md) | Streamgraph Quality | Stacked area % Q1/Q2/Q3/Q4 over time | Single-canvas trend |
| [M2-04](module2/M2-04-small-multiples-country.md) | Country Small Multiples | One ridgeline per selected country | Country drill-down |
| [M2-05](module2/M2-05-dumbbell-year-pairs.md) | Dumbbell Year Pairs | 1996 vs 2024 Q1/Q4 share dumbbells | Before/after clarity |
| [M2-06](module2/M2-06-heatmap-tier-year.md) | Heatmap Tier×Year | Rows=quality tier, cols=years, color=share | Compact overview |
| [M2-07](module2/M2-07-violin-facet-region.md) | Violin Facet Region | Regional violins of journal tier mix | Geographic quality lens |
| [M2-08](module2/M2-08-integrity-sparse-overview.md) | Integrity Sparse Overview | Overview = 3 annotated milestones only | Tufte / grader honesty |

## Recommendation

**Primary:** M2-02 (Bimodal Split) — matches team docx narrative.  
**Runner-up:** M2-01 for technical purity.

## Data layer

- SCImago SJR: Q1–Q4 publication counts per country×year
- Pre-computed KDE bins per year in Python (Lecture 15 — no raw papers in browser)
- Target: `module2_ridgeline.json`
