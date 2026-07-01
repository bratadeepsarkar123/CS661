# M3-03 — Dumbbell Decile Gap

## Intent
**Extreme inequality**: dumbbell per metric comparing World Bank income **top decile vs bottom decile** group averages (GERD%, Q1 share, cites/paper).

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Income Decile Gap            [⛶]   │
├─────────────────────────────────────┤
│ GERD%   ●━━━━━━━━━━━━●              │
│ Q1 share ●━━━━━━━●                  │
│ (2 dumbbells, top vs bottom decile) │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Metric ▾  Group: income | region decile        │
├──────────────────────────────────────────────────────────┤
│ 5 dumbbell rows (7±2): GERD%, pubs/cap, Q1%, cites, h   │
│ Left dot = bottom decile avg; right = top decile avg     │
│ Line length = gap; label gap value at center             │
├──────────────────────────────────────────────────────────┤
│ Click row → expand with country exemplars in each decile │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Bottom decile | `#f97316` |
| Top decile | `#3b82f6` |
| Connector | `#64748b` 2px |
| Gap label | `#f8fafc` 11px center

## Interaction
1. Overview: 2 metrics only
2. Fullscreen: metric picker cycles rows
3. Click row → exemplar country list
4. Year slider updates dot positions with transition

## Data bindings
- WB income group classification → assign countries to decile proxies (high/low income aggregates if decile unavailable)
- Aggregate SCImago + UIS metrics per group in ETL
- JSON: `{ year, metrics: [{ id, bottom, top, gap, exemplars: [...] }] }`

## Lecture alignment
- **Comparative encoding (L10):** Dumbbell length = gap magnitude
- **7±2:** Five metrics max in fullscreen
- **Integrity:** Decile = income group proxy if true decile missing — footnote

## Risks
- True decile data sparse — use WB low/lower-middle vs high-income groups with clear label
- Averages hide within-group variance — link to M3-06 violins

## Implementation effort
Medium
