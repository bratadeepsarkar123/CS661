# CS661 Dashboard — Design Planning Master Index

**Project:** The Global Knowledge & Wealth Paradox (Group 10)  
**Phase:** Design planning only — no implementation until variants are chosen per module  
**Last updated:** 2026-07-01

## Module ownership

| Module | Panel | Owner | Data status | Design folder |
|--------|-------|-------|-------------|---------------|
| 1 | Global HE spend vs outcomes | Teammate | Synthetic (`data.js`) | [module1/](module1/) |
| 2 | Knowledge production | Teammate | Synthetic | [module2/](module2/) |
| 3 | Wealth / inequality | Teammate | Synthetic | [module3/](module3/) |
| 4 | International mobility | Teammate | Synthetic | [module4/](module4/) |
| 5 | India domestic HE network | **You** | Real ETL (120 inst, 11/11 verification) | [module5/](module5/) |

## Variant indices (8 each)

- [MODULE1_INDEX.md](MODULE1_INDEX.md) — expenditure vs outcomes
- [MODULE2_INDEX.md](MODULE2_INDEX.md) — knowledge production
- [MODULE3_INDEX.md](MODULE3_INDEX.md) — wealth paradox
- [MODULE4_INDEX.md](MODULE4_INDEX.md) — student mobility
- [MODULE5_INDEX.md](MODULE5_INDEX.md) — India network (**concrete first**)

## Shared design constraints (Lecture 2/10)

1. **Overview → detail** — grid thumbnail vs fullscreen docx-style layout
2. **7±2** — max categories/colors per view
3. **Tufte** — no chartjunk; missing data ≠ zero; footnotes for aggregates
4. **Dark theme** — `#0f172a` background, light text
5. **Module 5 colors** — Premier `#3b82f6`, State `#a855f7` (2 tiers only)

## Recommended selection workflow

1. Review Module 5 variants; pick primary (planner default: **M5-03** + optional **M5-08** header)
2. Align teammates on Modules 1–4 indices before they implement ETL
3. Unify fullscreen chrome (⛶ button, panel width, footnote style) across panels

## Implementation status

| Area | Status |
|------|--------|
| Module 5 pipeline | Complete (verification **14/14**) |
| Module 5 UI | Working (`dashboard/india_network.js`) |
| Design specs M5 | 8/8 complete |
| Design specs M1–M4 | 8/8 each — canonical specs in `module{N}/`; legacy duplicates in `_archive/legacy_variants/` |
| Authority audit | PASS — see `design/AUTHORITY_AUDIT_M5.md` |

## Authority review

See `data/processed/verification_report.md` and post-audit `india_network.js` focus+context fixes before coding any chosen design.
