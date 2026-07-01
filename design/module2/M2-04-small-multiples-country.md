# M2-04 — Country Small Multiples

## Intent
Drill-down variant: **one mini ridgeline (or density strip) per selected country** showing that country’s Q1 vs Q4 publication mix over time. Answers “Which countries diverged from the global pattern?” — e.g., China elite breakaway vs India Q4 flood.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Country Quality Paths        [⛶]   │
├─────────────────────────────────────┤
│ [USA] [CHN] [IND]  3×1 mini ridges  │
│ each: Q1/Q4 hue, 1996→2024 mini-x   │
├─────────────────────────────────────┤
│ Tap ⛶ to pick countries             │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Search country…]  Compare: up to 6 ▾  Region filter ▾   │
├──────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐                      │
│ │ USA     │ │ CHN     │ │ IND     │   3×2 or 2×3 grid    │
│ │ ridgeline│ │ ridgeline│ │ ridgeline│   small multiples  │
│ └─────────┘ └─────────┘ └─────────┘                      │
│ Each panel: country name, ISO flag optional, Q1/Q4 curves │
│ Shared color legend; independent y-scale per panel (auto)  │
├──────────────────────────────────────────────────────────┤
│ Sync: brush one panel → vertical year line on all        │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago per-country tier %              │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Panel chrome | `#1e293b` border 1px, radius 4px, padding 8px |
| Q1 / Q4 | Same as M2-01 |
| Country title | `#e2e8f0` 12px bold; ISO `#94a3b8` |
| Max panels | 6 compare (7±2 with search = 7 controls) |
| Overview | 3 preset countries: USA, CHN, IND |

## Interaction (Shneiderman)
1. **Overview:** fixed trio; no search
2. **Zoom/filter:** region dropdown filters pick list; multi-select up to 6
3. **Details-on-demand:** click panel → enlarge to half-width hero + stats table
4. **Sync brush:** linked year cursor across panels

## Data bindings
- ETL: per (country, year): Q1%, Q4%, docs → optional 1D density from tier histogram
- JSON schema: `{ countries: [{ iso, name, region, years: [{ year, q1_pct, q4_pct, docs }] }] }`
- Target: `module2_country_quality.json`
- Placeholder: sample 6 countries from `COUNTRIES` in `data.js` with synthetic tier trajectories

## Lecture alignment
- **Small multiples (Tufte L10):** Same scale structure, eye travels across comparisons
- **7±2:** Six panels + search + region filter
- **Overview→detail:** Grid shows 3; fullscreen expands selection

## Risks
- Per-panel scale differences hide magnitude — optional "normalize to global" toggle
- 240 countries overwhelming — search + region filter required

## Implementation effort
Medium–high — grid layout + linked interaction + per-country ETL
