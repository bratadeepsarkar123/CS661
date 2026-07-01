# M4-05 — Dumbbell Mobility Balance

## Intent
Per-country **dumbbell**: left = outbound mobile students, right = inbound — line length shows net brain gain vs drain (recommended Module 4 default).

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Mobility Balance             [⛶]   │
├─────────────────────────────────────┤
│ IND ●━━━━━━━━━━━━● inbound small    │
│ CHN ●━━━━━━━━●                      │
│ USA ●●━━━━━━━━━━━━ inbound large    │
│ top 6 by |net|                       │
├─────────────────────────────────────┤
│ ● outbound  ● inbound               │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Sort: net ▾ | outbound | inbound | name        │
├──────────────────────────────────────────────────────────┤
│ ~35 dumbbells; net gain countries line extends right     │
│ Hover → exact counts + ratio                             │
│ Click → sidebar 10-year sparkline both endpoints         │
├──────────────────────────────────────────────────────────┤
│ OpenAlex co-auth proxy toggle OFF by default (footnote)  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Outbound dot | `#f97316` |
| Inbound dot | `#22c55e` |
| Connector | `#64748b`; net direction arrow subtle |
| Missing | hollow grey if one side missing

## Interaction
1. Overview: 6 countries extreme net
2. Fullscreen: sort/filter; click sparkline
3. Region filter
4. Focus+context on click

## Data bindings
- UIS outbound + inbound by country-year
- JSON: `{ year, countries: [{ iso, out, in, net }] }`
- Optional proxy from OpenAlex intl coauth **disabled** unless UIS gap

## Lecture alignment
- **Graphical integrity (L10):** Label gain explicitly on connector
- **Comparative viz:** Dumbbell length = imbalance
- **7±2:** Overview 6 rows

## Risks
- Small countries asymmetric noise — min enrollment threshold
- Do not conflate with Module 4 collaboration premium (citations)

## Implementation effort
Low–medium
