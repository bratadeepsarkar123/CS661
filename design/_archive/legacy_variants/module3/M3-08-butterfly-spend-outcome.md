# M3-08 — Butterfly Spend/Outcome

## Intent
**Butterfly chart**: each country row with spend metric bars extending left and outcome metric extending right — mirror comparison of wealth input vs knowledge output.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Spend ↔ Outcome Mirror       [⛶]   │
├─────────────────────────────────────┤
│      │USA│                         │
│ ████ │   │ ██████  GERD | Q1 pubs  │
│      │IND│                         │
│  ██  │   │ ████                    │
│ 6 countries, center axis            │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Left: GERD% ▾  Right: Q1 count ▾  Sort ▾       │
├──────────────────────────────────────────────────────────┤
│ ~25 country rows; independent scales left/right          │
│ Center labels ISO3; bar length linear per side           │
│ Click row → highlight + normalized z-score sidebar       │
├──────────────────────────────────────────────────────────┤
│ Footnote: sides not directly comparable scale — read labels│
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Spend bars | `#f97316` extend left |
| Outcome bars | `#38bdf8` extend right |
| Center axis | `#475569` |
| Row hover | `#1e293b` band

## Interaction
1. Overview: 6 countries by combined magnitude
2. Fullscreen: sort by left, right, or asymmetry index
3. Click row focus; others fade
4. Metric dropdowns change bar data columns

## Data bindings
- UIS GERD + SCImago Q1 counts merged
- JSON: `{ year, rows: [{ iso, spend, outcome, asymmetry }] }`
- Asymmetry = z(outcome) - z(spend) pre-computed

## Lecture alignment
- **Comparative small multiples (L10):** Row = entity
- **Integrity:** Independent scales labeled — no implied equal units
- **7±2:** Overview 6 rows

## Risks
- Users compare bar lengths across sides incorrectly — footnote prominent
- Asymmetry index needs explanation

## Implementation effort
Low–medium
