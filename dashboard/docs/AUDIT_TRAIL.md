# Audit trail — major fixes (2026-07-12 session)

Chronological summary of the consolidation / honesty pass. Pack state: **after G5 edge-vis revert**.

---

## 1. Friend landing / G5 CSS collision

- Friend `style.css` overwrite risked Graph 5 circles/layout.
- Restored G5 behavior while iterating landing chrome.
- Backups kept as `index.html.bak-*-friend-landing*`, `style.css.bak-*-friend-landing*` (local only; often excluded from zips).

## 2. Friend-copy revert then modularization

- Reverted dashboard toward pre-bad-copy graph behavior, then **modularized**:
  - `graphs/g1` … `graphs/g5` each with `gN.js` + `gN.css`
  - Thin `app.js` orchestrator + shared `style.css`
- See [`../GRAPHS_LAYOUT.md`](../GRAPHS_LAYOUT.md).

## 3. Landing chrome (kept)

- Two-column landing shell (hero left, viz-card gallery right) in `index.html` / `style.css`.
- Landing font tweaks to match teammate screenshot **without** changing graph pipelines.

## 4. River clean → pool rebuild

- Locked owners in [`RIVER_OWNERS.md`](RIVER_OWNERS.md).
- Quarantined stub H (`CS661_Dataset/_QUARANTINE/`).
- Rebuilt G1–G4 pools via `dashboard/_river_to_pool_rebuild.py`.
- G1: real SCImago H (USA ~3388); UMAP regen path `_regen_viz1_umap.py`.
- G2: uncapped publisher-country Q1/Q4 ratios.
- G3: OpenAlex concepts; Quantum `C58053490`; AI primary `C119857082`.
- G4: dated premium series (later expanded).

## 5. GERD hierarchy + LOCF display

- Built gated hierarchical GERD river (`_build_gerd_hierarchy.py`).
- Pool LOCF for display gaps (India GERD after last WB year) — [`G2_CARRY_AND_GERD_FFILL.md`](G2_CARRY_AND_GERD_FFILL.md).

## 6. G3 floors / honesty / Lane C / L2 demo

- Removed hard milestone floors that created fake cliffs ([`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md)).
- Audited AI 1979→1980 jump ([`G3_AI_1980_JUMP_AUDIT.md`](G3_AI_1980_JUMP_AUDIT.md)).
- Live L3 seven-topic set + Supervised learning; L2 broader demo on **:8085** ([`G3_L3_FIX_AND_L2_DEMO.md`](G3_L3_FIX_AND_L2_DEMO.md)).
- Lane C fetch tracked in [`G3_LANE_C_FETCH_STATUS.md`](G3_LANE_C_FETCH_STATUS.md).
- Export pack under `dashboard/exports/g3_recheck_20260712/`.

## 7. G4 expand

- Expanded collaboration premium from core 20 → **73** countries (2010–2024).
- Region-balance rules ([`G4_REGION_BALANCE.md`](G4_REGION_BALANCE.md)); status [`G4_EXPAND_STATUS.md`](G4_EXPAND_STATUS.md).
- Runner: `scripts/expand_g4_openalex.py` (needs `.env` OpenAlex key).

## 8. G5 edge-vis revert (latest, pack baseline)

- User: **REVERT G5** — undo hanging-edge / edge-visibility experiment in `india_network.js`.
- Cache-bust returned to non-`g5-edge-vis` token (e.g. `?v=20260712-g5-count-picker`).
- Region-blend cluster fill (`VIZ5_REGION_BLEND`) is a **separate** flag and may remain enabled.

---

## Pointers

- Plain language: [`EXPLAINER_FINDINGS_AND_CHANGES.md`](EXPLAINER_FINDINGS_AND_CHANGES.md)
- Teammate handoff: [`../TEAM_HANDOFF_README.md`](../TEAM_HANDOFF_README.md)
- Fact-check: [`FACTCHECK_CHECKLIST.md`](FACTCHECK_CHECKLIST.md)
