# M4-03 — Scatter Dom vs Intl

## Intent
**Correlation view**: scatter with x = domestic mean citations, y = international mean citations, one point per country. Diagonal = parity; points above line = intl premium. Reveals whether high domestic performers also lead internationally.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Dom vs Intl Citations        [⛶]   │
├─────────────────────────────────────┤
│      ● USA                          │
│    ●   ● diagonal parity            │
│  ● IND                              │
│ x: dom cites  y: intl cites         │
├─────────────────────────────────────┤
│ 6 labeled outliers only             │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Region ▾  Size: papers|uniform ▾  [Search]   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Scatter ~60 countries; bubble area ∝ √(n papers)        │
│  Diagonal y=x dashed `#64748b`; band above = premium zone │
│  Region color fill; selected white ring                  │
│  Optional OLS fit intl ~ domestic (pre-computed)         │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: country | dom | intl | gain | distance to line  │
├──────────────────────────────────────────────────────────┤
│ *Synthetic COLLAB_DATA; module4_collaboration_premium  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Points | Region palette; r=4–12px by √papers |
| Parity line | `#64748b` dashed; label "parity" |
| Premium zone | Above diagonal: `#22c55e` 0.05 fill optional |
| Axes | `#94a3b8`; equal aspect ratio optional toggle |
| Overview | No labels except 3 callouts |

## Interaction (Shneiderman)
1. **Overview:** 6 labeled points max
2. **Zoom/filter:** year; region; search country
3. **Details-on-demand:** click point → sidebar + highlight
4. **Focus:** dim non-selected to 30% opacity

## Data bindings
- M4-01 schema; add `n_total` for bubble size
- Placeholder: `COLLAB_DATA` with uniform size in overview

## Lecture alignment
- **Graphical integrity (L10):** √ area for volume; parity line explicit
- **7±2:** Region colors ≤7; one year, one region filter
- **Module 1 echo:** Same scatter grammar as M1-01 for dashboard cohesion

## Risks
- USA/CHN dominate scale — log axes toggle + footnote
- Correlation ≠ causation — footnote collaboration mix

## Implementation effort
Low–medium — standard D3 scatter; shares ETL with M4-01
