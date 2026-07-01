# M4-07 — Heatmap Origin×Host

## Intent
**Bilateral matrix**: rows = origin countries, columns = host countries, cell color = mobile student count — full table view for precise comparison.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Origin × Host Matrix         [⛶]   │
├─────────────────────────────────────┤
│       USA GBR AUS                   │
│ CHN   ██  ░  ░                      │
│ IND   ░   █  ░                      │
│ IND   ░   ░  ░                      │
│ 6×6 subset                          │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Top origins: 15 ▾  Top hosts: 15 ▾  Log color  │
├──────────────────────────────────────────────────────────┤
│ Scrollable matrix with sticky headers                    │
│ Hover cell → tooltip count + % of origin total           │
│ Click row → highlight row; click col → highlight column  │
├──────────────────────────────────────────────────────────┤
│ Reorder: sort by row sum or col sum                      │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Scale | `#0f172a` → `#38bdf8` sequential |
| Highlight cross | `#334155` band |
| Cell size | 16×16px min |
| Missing | `#1e293b`

## Interaction
1. Overview: 6×6 top flows
2. Fullscreen: expand; row/col focus
3. Log toggle for skew
4. Double-click cell → pin origin→host pair in sidebar

## Data bindings
- Bilateral UIS/OECD matrix sparse → dense subset in ETL
- JSON: `{ year, origins: [...], hosts: [...], values: [[n|null]] }`

## Lecture alignment
- **Matrix linked views (L10):** Row/col brushing
- **Tufte:** Cell value in tooltip; legend breaks labeled
- **Overview limits:** 6×6 = 36 cells manageable

## Risks
- Sparse matrix — many empty cells grey
- Not visually dramatic — pair with M4-06 for demo

## Implementation effort
Low–medium
