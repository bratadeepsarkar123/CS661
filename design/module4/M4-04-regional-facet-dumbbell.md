# M4-04 — Regional Facet Dumbbell

## Intent
**Small multiples by continent**: dumbbell charts faceted into 7 region panels (from `data.js` REGIONS), each showing countries in that region. Surfaces regional collaboration patterns — e.g., Europe tight clusters vs South Asia wider spread.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Premium by Region            [⛶]   │
├─────────────────────────────────────┤
│ EU: ●──● ●──●   APAC: ●──● ●──●     │
│ 2 mini dumbbell strips              │
├─────────────────────────────────────┤
│ NA + EU facets in overview          │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Sort within facet: gain|name                   │
├──────────────────────────────────────────────────────────┤
│ ┌─ North America ─┐ ┌─ Europe ────────┐                  │
│ │ USA ●────●      │ │ GBR ●────●      │  3×3 or 2×4     │
│ │ CAN ●────●      │ │ DEU ●────●      │  facet grid     │
│ └─────────────────┘ └─────────────────┘                  │
│ Shared x-scale across facets (citation axis)               │
│ Region title bar in region color                           │
├──────────────────────────────────────────────────────────┤
│ Click country → highlight across dashboard if linked     │
├──────────────────────────────────────────────────────────┤
│ *Synthetic COLLAB_DATA + REGIONS join                    │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Facet chrome | `#1e293b` border; title bar region hue 0.3 fill |
| Dumbbell | Same as M4-01; scaled to facet width |
| Shared x-scale | 0 to p95 intl cites across all countries |
| Overview | 2 facets × 2 countries each |

## Interaction (Shneiderman)
1. **Overview:** NA + EU mini-facets only
2. **Zoom/filter:** year slider updates all facets
3. **Details-on-demand:** click dumbbell → sidebar
4. **Shared scale toggle:** free vs shared x per facet

## Data bindings
- Join M4-01 countries with `REGIONS` via region field
- Group by region in client or pre-group in JSON: `{ regions: [{ name, countries }] }`
- Placeholder: map 17 `COLLAB_DATA` rows to regions manually

## Lecture alignment
- **7±2:** Seven region facets = category limit at panel level
- **Small multiples (Tufte):** Shared scale enables cross-region compare
- **Geographic consistency:** Region colors match Module 1 scatter

## Risks
- Sparse facets (Oceania n=1) — merge with neighbor or show strip
- Facet height uneven — scroll within facet if >8 countries

## Implementation effort
Medium — facet grid + shared scales; same ETL as M4-01
