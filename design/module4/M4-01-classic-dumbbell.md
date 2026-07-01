# M4-01 — Classic Dumbbell (Recommended)

## Intent
Proposal §4.4 faithful: **horizontal dumbbell chart** per country comparing **mean citations — domestic-only papers vs international co-authorship papers**. Connector length = collaboration premium (intl − domestic). Answers "Who gains most from cross-border collaboration?"

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Collaboration Premium        [⛶]   │
├─────────────────────────────────────┤
│ USA   ●────────●  dom→intl          │
│ GBR   ●───────●                     │
│ IND   ●─────●   gain +6.7           │
│ ● domestic  ● international         │
├─────────────────────────────────────┤
│ Sorted by citation gain             │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year 1996 ────●──── 2024]  Sort: gain|domestic|name     │
│ Region ▾  Min papers: 100 ▾                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Horizontal dumbbells, ~17–60 countries                │
│  Left dot = domestic mean cites; right = intl mean cites │
│  Connector `#64748b` 2px; length encodes premium         │
│  Color dot by region (REGIONS palette, ≤7)               │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: country | dom | intl | gain | n_dom | n_intl    │
├──────────────────────────────────────────────────────────┤
│ *Synthetic COLLAB_DATA in dashboard/data.js              │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Domestic dot | `#6366f1` r=6px |
| International dot | `#22d3ee` r=6px |
| Connector | `#64748b` 2px; gain>0 only (no negative in demo) |
| Labels | `#cbd5e1` 11px; country name left margin 100px |
| Overview | Top 6 by gain from `COLLAB_DATA` |

## Interaction (Shneiderman)
1. **Overview:** static 2024 (or latest); top 6 rows
2. **Zoom/filter:** year slider; region filter; min paper threshold
3. **Details-on-demand:** click row → sidebar + highlight
4. **Sort:** gain vs domestic vs alphabetical

## Data bindings
- ETL: OpenAlex works → split domestic-only vs has foreign institution → mean citations per country×year
- JSON schema: `{ years: [{ year, countries: [{ iso, name, region, domestic_cites, intl_cites, n_dom, n_intl, gain }] }] }`
- Target: `module4_collaboration_premium.json`
- Placeholder: `DATA.getCollabData()` + `COLLAB_DATA` in `data.js`

## Lecture alignment
- **Graphical integrity (L10):** Common x-axis (citations); dots not area-encoded
- **7±2:** Region colors ≤7; one year, one sort, one filter
- **Overview→detail (L2):** Grid shows premium pattern; full country set in fullscreen

## Risks
- Mean cites skewed by outliers — footnote; optional median toggle in ETL
- Small n countries unstable — min papers filter + hollow dots

## Implementation effort
Low–medium — standard dumbbell; OpenAlex split is ETL heavy lift
