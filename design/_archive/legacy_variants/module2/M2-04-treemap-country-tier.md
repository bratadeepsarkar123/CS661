# M2-04 — Treemap Country×Tier

## Intent
Nested **treemap**: outer area = country share of global publications; inner split = Q1/Q2/Q3/Q4 tier colors — hierarchical view of who produces what quality.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Production Treemap           [⛶]   │
├─────────────────────────────────────┤
│ ┌──────USA─────┬─CHN─┬─IND─┐         │
│ │Q1│Q2│Q3│Q4   │     │     │         │
│ └──────────────┴─────┴─────┘         │
│ Labels: USA, CHN, IND only           │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Color: Q tier ▾ | Region group                 │
├──────────────────────────────────────────────────────────┤
│ Treemap ~20 countries + Other tile                       │
│ Hover tile → breadcrumb Country > Tier                   │
│ Click country → zoom tile (focus+context)                │
│ Zoom out: breadcrumb back                                │
├──────────────────────────────────────────────────────────┤
│ Sidebar on zoom: tier counts + % of country total        │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Q1 | `#3b82f6` |
| Q2 | `#6366f1` |
| Q3 | `#64748b` |
| Q4 | `#475569` |
| Padding | 2px `#0f172a` gutters |

## Interaction
1. Overview: top 6 countries by area, no zoom
2. Fullscreen: click-to-zoom with smooth transition
3. Year slider morphs tile areas
4. Double-click root to reset zoom

## Data bindings
- SCImago country-year Q1–Q4 publication counts
- JSON hierarchical: `{ name, children: [{ name, children: [{ tier, value }] }] }`
- Pre-build tree per year in ETL

## Lecture alignment
- **7±2:** Four tier colors — at limit; no fifth encoding
- **Area integrity (Tufte):** Rect area = count; no padding inflation
- **Overview→detail:** Overview flat one level

## Risks
- Small Q1 slivers invisible — minimum tile label threshold
- Not a map — avoids Module 5 collision

## Implementation effort
Medium
