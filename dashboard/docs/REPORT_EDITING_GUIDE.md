# Report editing guide (LaTeX ↔ live dashboard)

**Primary LaTeX:** `CS661 Project/CS661_Project_Report_Group10_Final.tex`  
**Working copy:** `CS661 Project/CS661_Project_Report_Group10_WORKING.tex` (see also `REPORT_TEX_PATH.md`)  
**Dashboard copy (optional):** `dashboard/CS661_Project_Report_Group10_WORKING.tex`

Edit against **live truth** in `dashboard/` + `CS661_Dataset/raw_vault/READY_FOR_TEAM/`, not against outdated proposal text.

---

## Stack truth (fix these first)

| Claim | Live truth |
|-------|------------|
| Frontend | **Vanilla** HTML/CSS/JS + D3 + Plotly + Leaflet + Chart.js |
| **Not** | React / Vite / Next.js runtime |
| Serve | `python -m http.server 8080 --directory dashboard` |
| G3 demo | Separate `:8085` under `demos/g3-l2-broader/` |

### Still-stale abstract / intro claims (must fix in Final.tex)

The **abstract** and **Bespoke Visualization** objective still say **“bespoke React and D3.js”** / **React.js**. That is **false** for the shipped app.

Also over-claims in Domain Research that treat **UNESCO BDDS** and **OECD MSTI** as equal live acquisition pillars for Graph 1 — see honesty docs below. WB WDI (+ SCImago / OpenAlex where noted) is what the FE mostly drinks.

---

## What is already audited (safe to cite if you match the docs)

| Topic | Read before writing |
|-------|---------------------|
| Domain Research / data acquisition | [`../REPORT_SECTION2_FACTCHECK.md`](../REPORT_SECTION2_FACTCHECK.md) |
| River owners + forbidden sources | [`RIVER_OWNERS.md`](RIVER_OWNERS.md) |
| Publications naming (G1≠G2≠G3) | [`GAPS_AND_PUBLICATIONS_FACTCHECK.md`](GAPS_AND_PUBLICATIONS_FACTCHECK.md) |
| G2 = publisher country | [`../SEMANTICS_DECISION.md`](../SEMANTICS_DECISION.md) |
| GERD hierarchy + LOCF display | [`RIVER_GERD_HIERARCHY.md`](RIVER_GERD_HIERARCHY.md), [`G2_CARRY_AND_GERD_FFILL.md`](G2_CARRY_AND_GERD_FFILL.md) |
| G3 concepts / floors / L2 demo | [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md), [`G3_L3_FIX_AND_L2_DEMO.md`](G3_L3_FIX_AND_L2_DEMO.md) |
| G4 N countries | [`G4_EXPAND_STATUS.md`](G4_EXPAND_STATUS.md) — live **73**, not unverified 111 |
| G5 NIRF presentation | `docs/GRAPH5_DATA_PRESENTATION_POLICY.md` (repo `docs/`) |
| Plain-language change story | [`EXPLAINER_FINDINGS_AND_CHANGES.md`](EXPLAINER_FINDINGS_AND_CHANGES.md) |

---

## Module ↔ live encoding (report language)

| Module | Report should say | Avoid |
|--------|-------------------|--------|
| G1 | UMAP peer clusters; Plotly; H from SCImago Country Rank; bubble size WB articles then SCImago Documents | “OpenAlex drives bubble size”; H≈53 scale |
| G2 | Publisher-country Q1/Q4; uncapped ratio; ridgeline/bars | Author-nationality Q1/Q4 |
| G3 | OpenAlex **concepts**; 7 live L3 topics; shared ~1974 window | ASJC 2500 Quantum; mega-AI as primary; React race |
| G4 | Dumbbell; domestic vs intl mean cites; 73 countries × 2010–2024 | 111 undated countries; FWCI unless proven; grouped bars as the live chart |
| G5 | Leaflet India network; NIRF carry footnotes; honest missing years | Invented NIRF years; claiming edge-vis “fix” that was reverted |

---

## Editing workflow

1. Run dashboard on `:8080` and spot-check the claim in the UI.
2. Confirm river CSV in `READY_FOR_TEAM/` (or vault) matches the pool.
3. Update Final.tex (and WORKING if that is your edit surface).
4. Re-run [`FACTCHECK_CHECKLIST.md`](FACTCHECK_CHECKLIST.md) on any number you cite.
5. Do not paste API keys or `.env` contents into the report.

---

## Domain Research honesty pointers

- Prefer: “UIS GERD series **via World Bank WDI**” over “we downloaded UNESCO BDDS bulk.”
- OECD MSTI exists in the vault and feeds **gated GERD hole-fill** — not a full equal third pillar for every G1 field.
- Sector GERD CSV is thin and **unused** by the FE.
- Cite [`../REPORT_SECTION2_FACTCHECK.md`](../REPORT_SECTION2_FACTCHECK.md) when rewriting §Domain Research.
