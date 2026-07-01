# M1-07 — Marimekko Spend Share

## Intent
Show **global concentration**: a few countries dominate GERD spend while outcome quality splits differently — macro "wealth paradox" at a glance.

## Layout
```
┌─────────────────────────────────────┐
│ Global GERD share vs outcomes  [⛶]  │
├─────────────────────────────────────┤
│ ┌──────┬───┐                          │
│ │ USA  │   │  width = GERD share      │
│ │ wide │ Q1│  height = Q1 share of    │
│ └──────┴ Q4│  that country's pubs     │
│   CHN  EU  ...                       │
└─────────────────────────────────────┘
```

**Fullscreen:** interactive Marimekko with tooltips; click tile → country detail sidebar.

## Visual system
- Width encodes GERD share (honest linear horizontal)
- Height split: Q1 `#3b82f6` / Q4 `#94a3b8` (2 tiers only)
- Background `#0f172a`; borders `#334155`

## Interaction
- Hover tile → country name + exact percentages
- Year slider recomputes shares (pre-computed bins)

## Data bindings
- UNESCO GERD + SCImago Q1/Q4 country totals
- Top 15 countries cover ~85% GERD — remainder grouped "Other"

## Lecture alignment
- **7±2:** One chart, year, footnote
- **Graphical integrity:** "Other" bucket explicit; no 3D

## Risks
- Marimekko area can mislead if readers compare diagonals — footnote required

## Implementation effort
Medium
