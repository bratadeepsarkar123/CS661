# Module 4 Design Variants — Selection Index

**Scope:** Collaboration Premium (Panel 4 — domestic vs intl citation dumbbell)  
**Status:** Planning only — teammates implement  
**Data today:** Synthetic in `dashboard/data.js`

| ID | Name | One-line pitch | Best for |
|----|------|----------------|----------|
| [M4-01](module4/M4-01-classic-dumbbell.md) | Classic Dumbbell | Domestic vs intl citation markers per country | Proposal §4.4 |
| [M4-02](module4/M4-02-lollipop-gain-sorted.md) | Lollipop Gain Sorted | Single dot at citation gain, sorted | Gain-first story |
| [M4-03](module4/M4-03-scatter-dom-intl.md) | Scatter Dom vs Intl | x=domestic cites, y=intl cites | Correlation view |
| [M4-04](module4/M4-04-regional-facet-dumbbell.md) | Regional Facet Dumbbell | Small multiples by continent | 7±2 regions |
| [M4-05](module4/M4-05-top8-overview-strip.md) | Top-8 Overview Strip | Grid shows top 8 gains only | Overview readability |
| [M4-06](module4/M4-06-connected-dot-time.md) | Connected Dot Time | 1996 vs 2024 dumbbell pairs | Temporal premium shift |
| [M4-07](module4/M4-07-barbell-error-bars.md) | Barbell Error Bars | Dumbbell + CI whiskers from sample size | Statistical honesty |
| [M4-08](module4/M4-08-footnote-denominator.md) | Footnote Denominator | Lead with paper-count footnote + chart | Tufte integrity |

## Recommendation

**Primary:** M4-01 (Classic Dumbbell)  
**Runner-up:** M4-05 for small overview cell

## Data layer

- OpenAlex: domestic-only vs intl co-auth works → mean citations per country×year
- Target: `module4_collaboration_premium.json`
