# M4-07 — Barbell Error Bars

## Intent
**Statistical honesty**: dumbbell (dom vs intl mean cites) plus **95% CI whiskers** from bootstrap or standard error using paper counts. Surfaces when premium is significant vs noise from small samples.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Premium + Uncertainty        [⛶]   │
├─────────────────────────────────────┤
│ CHE  ●──|──|──●  CI shown           │
│ IND  ●─|──●   wide CI (small n)     │
├─────────────────────────────────────┤
│ Whiskers on 3 countries only        │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  CI: [95%|90%]  Min n: 50 ▾  Sort: gain ▾       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Dumbbell + horizontal error bars on each dot            │
│  Whiskers `#94a3b8` 1px; cap width 4px                   │
│  Hollow dot if n below min threshold                     │
│  Tooltip: mean, CI low/high, n papers                    │
│  Optional: significance bracket if CIs non-overlap       │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: country | dom_mean | dom_ci | intl_mean | n_*   │
├──────────────────────────────────────────────────────────┤
│ *Synthetic: generate CI from fake n_dom/n_intl in ETL     │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Dumbbell | M4-01 base |
| CI whisker | `#94a3b8` 1px; extends from dot |
| Non-sig premium | Connector dashed when CIs overlap |
| Sig premium | Connector solid `#22c55e` |
| Hollow dot | n < min: stroke only, `#64748b` |
| Overview | 3 countries with visible CI difference |

## Interaction (Shneiderman)
1. **Overview:** 3 rows with whiskers; no CI toggle
2. **Zoom/filter:** CI level; min n threshold hides unstable rows
3. **Details-on-demand:** hover → full CI table
4. **Sort:** by gain only among significant pairs optional filter

## Data bindings
- ETL: store `dom_se`, `intl_se`, `n_dom`, `n_intl` per country×year
- Pre-compute bootstrap CI in Python (Lecture 15 — not in browser)
- JSON schema extend M4-01: `{ domestic_ci: [lo, hi], intl_ci: [lo, hi] }`
- Placeholder: synthetic SE = mean / √n with fake n

## Lecture alignment
- **Statistical integrity (L10):** Uncertainty visible; small n flagged
- **Tufte:** Whiskers minimal ink; no 3D error cones
- **7±2:** Defaults hide CI complexity in overview

## Risks
- Bootstrap expensive — pre-compute offline; cache in JSON
- Users ignore whiskers — tooltip + sig bracket on hover

## Implementation effort
Medium–high — ETL bootstrap + error bar rendering
