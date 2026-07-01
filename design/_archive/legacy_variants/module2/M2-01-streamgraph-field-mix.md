# M2-01 — Streamgraph Field Mix

## Intent
Show how **global publication volume** shifts across major fields (AI/ML, biomedicine, energy, etc.) as a single flowing stream — the “what the world publishes” story.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Publication Field Mix        [⛶]   │
├─────────────────────────────────────┤
│ ~~~~~~~~~~~~~~~~~~~~~~~~~ stream    │
│ 3 bands labeled: AI · Health · Eng  │
│ x: time (1996–2024 compressed)      │
├─────────────────────────────────────┤
│ Total pubs ↑ 2.4× since 1996        │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play  [Year ●]  Fields: top 7 ▾  Stack: expand|silhouette│
├──────────────────────────────────────────────────────────┤
│ Streamgraph center-baseline, ~7 OpenAlex concept groups    │
│ Hover band → isolate field + % share tooltip               │
│ Click field → legend lock; other bands 25% opacity         │
├──────────────────────────────────────────────────────────┤
│ Sidebar: field rank table for selected year                │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Fields | 7 colors max (7±2): indigo, cyan, amber, rose, emerald, violet, slate |
| Baseline | wiggle or zero — prefer **silhouette** for honest area |
| Stroke | `#0f172a` 0.5px between layers |
| Overview | 3 callout labels only |

## Interaction
1. Play animates stack morph year-by-year
2. Hover isolates layer (focus+context)
3. Toggle expand vs silhouette (fullscreen)
4. Optional region filter reweights stream (subset re-aggregate from JSON)

## Data bindings
- OpenAlex: aggregate works by concept group × year (top 7 + Other)
- JSON: `{ years: [...], fields: [{ id, name, values: [counts] }] }`
- ETL mirrors OpenAlex topic pipeline in proposal §2

## Lecture alignment
- **Chartjunk (L10):** No decorative gradients on overview
- **Area integrity (Tufte):** Silhouette default; warn if using expand
- **7±2:** Max 7 field bands

## Risks
- Concept taxonomy changes — freeze 2024 mapping retroactively
- Streamgraphs hard to compare — sidebar table mandatory

## Implementation effort
Medium
