# M1-06 — Dot Matrix Linked

## Intent
Ultra-compact overview for the grid cell: countries as rows, normalized indicators as columns — instant heatmap of who leads on spend vs outcomes without a scatter.

## Layout
```
┌─────────────────────────────────────┐
│ Macro indicator matrix       [⛶]   │
├─────────────────────────────────────┤
│      G  P  C  H  R  (columns)       │
│ USA  ● ● ● ● ●                      │
│ CHN  ● ● ● ○ ●                      │
│ IND  ○ ○ ○ ○ ○                      │
│ ... (top 25 countries by pubs)      │
├─────────────────────────────────────┤
│ ● = top tertile  ○ = bottom         │
└─────────────────────────────────────┘
```

**Fullscreen:** full ~180-country matrix + column brush + linked mini t-SNE inset.

## Visual system
- Cell fill: `#3b82f6` (high) → `#1e293b` (mid) → `#334155` (low)
- Row highlight on hover: `#475569` band
- Max 5 columns (GERD, pubs, cites, h-index, researchers) — 7±2

## Interaction
- Click row → highlight same country in global year-linked panels (if brush-and-link wired)
- Column header click → sort rows by that indicator

## Data bindings
- Pre-compute tertile thresholds per year in ETL
- `module1_matrix.json` — sparse alternative to full scatter payload

## Lecture alignment
- Overview-first (Munzner small multiples)
- Tufte: no pseudo-3D; discrete tertiles avoid false precision

## Risks
- Loses geographic intuition — pair with t-SNE inset in fullscreen

## Implementation effort
Low–medium
