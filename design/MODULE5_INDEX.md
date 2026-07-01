# Module 5 Design Variants — Selection Index

**Scope:** India Domestic Higher Education Network (Panel 5 only)  
**Status:** Planning only — no implementation until one variant is chosen  
**Constraints:** Lecture 2/10 (overview→detail, 7±2, Tufte integrity), dark theme `#0f172a`, 2 tier colors only, pre-computed JSON

| ID | Name | One-line pitch | Best for |
|----|------|----------------|----------|
| [M5-01](module5/M5-01-hub-corridor-minimal.md) | Hub Corridor Minimal | Sparse hub map + one tier strip | Grader demo in 10 seconds |
| [M5-02](module5/M5-02-split-tier-panels.md) | Split Tier Panels | Docx-style dual columns in fullscreen only | Funding vs quality story |
| [M5-03](module5/M5-03-focus-fisheye.md) | Focus Fisheye | Click node → magnify + dim context (Munzner Ch.14) | Interaction showcase |
| [M5-04](module5/M5-04-corridor-annotations.md) | Corridor Annotations | NCR/Bengaluru/Mumbai/Chennai callout ribbons | Geographic narrative |
| [M5-05](module5/M5-05-funding-dumbbell-strip.md) | Funding Dumbbell Strip | Tier funding gap as bottom dumbbell, map above | Wealth paradox tie-in |
| [M5-06](module5/M5-06-search-first-command.md) | Search-First Command | Large search + minimal map until query | 80-node discoverability |
| [M5-07](module5/M5-07-year-scrub-hero.md) | Year Scrub Hero | Year slider drives edge pulse animation | Temporal change story |
| [M5-08](module5/M5-08-integrity-footnote-first.md) | Integrity Footnote First | Tufte-forward: footnote + 2 metrics only on map | Academic rigor / honesty |

## Recommendation (planner default)

**Primary:** M5-03 (Focus Fisheye) — closest to current `india_network.js` after audit fix; satisfies Shneiderman + Munzner.  
**Runner-up:** M5-01 (Hub Corridor Minimal) for overview grid thumbnail if we need smaller cognitive load on the 5-panel landing page.

## Data layer (shared by all variants)

- 120 institutions, hub-to-hub overview edges, full ≤200 edges
- `funding_status` / `patent_status` for missing NIRF data
- SCImago static 2019 footnote on quality fields

## Out of scope (teammates)

Modules 1–4 design variants live in `design/module1/` … `design/module4/` — separate tracks.
