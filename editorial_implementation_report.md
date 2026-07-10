# Editorial Magazine Layout — Implementation Report

**Branch:** `ui-vision-editorial`  
**Direction:** 3 — Editorial Magazine Layout (with Presentation Mode)  
**Files touched:** `dashboard/index.html`, `dashboard/style.css`, `dashboard/app.js`

---

## Summary

The CS661 dashboard was redesigned from a dark SaaS-style card gallery into a **data-journalism article** with serif typography, reading-flow prose, numbered editorial figures, and a sticky table of contents. All **DOM hooks** used by `app.js` (`#preview-1`…`#preview-5`, `#card-1`…`#card-5`, `onclick="openViz(n)"`, panel IDs) are **unchanged**. A **Present Mode** toggles full-viewport scroll-snapped slides via `body.present-mode`.

---

## HTML Changes (`dashboard/index.html`)

### Typography & assets

- Replaced Outfit / Plus Jakarta Sans with **Lora** (serif) and **Source Sans 3** (UI sans).
- Removed particle hero (`#hero-particles`) and gradient headline chrome.

### Structure

| Before | After |
|--------|-------|
| `<header class="hero-header">` | `<header class="masthead">` — publication nameplate, dek, date, data badges |
| `<main class="gallery-section">` + 2×2 grid | `<main class="editorial-article">` inside `.editorial-shell` |
| Flat `.viz-grid` of cards | Five `<figure class="editorial-figure" id="figure-N">` blocks in reading order |
| No navigation rail | `<nav class="toc-rail">` with anchor links to `#figure-1`…`#figure-5`, `#methods` |

### New UI element

- **Present Mode button:** `<button id="present-mode-btn" class="present-toggle">` fixed top-right.

### Prose & captions

- Added lede (`#lede`), five section intros (Roman numerals I–V), and **Methods** block (`#methods`).
- Each figure has:
  - `.figure-label` — e.g. “Figure 1. High-Dimensional Peer Clustering”
  - `.figure-caption` — provenance line + `<span class="interactive-badge">Interactive</span>`

### Preserved hooks (unchanged)

- `id="card-1"` … `id="card-5"` on `.viz-card`
- `id="preview-1"` … `id="preview-5"` on preview canvases
- `onclick="openViz(n)"` on each card
- `class="viz-card featured"` on card 5
- Loading screen: `#loading-screen`, `#loading-text`
- Fullscreen panel: `#viz-panel`, `#panel-body`, `#panel-controls`, `#panel-num`, `#panel-title`, `#data-credit`, `#prev-btn`, `#next-btn`
- Script load order unchanged

---

## CSS Changes (`dashboard/style.css`)

### Design tokens (`:root`)

- Documented **Okabe-Ito** palette as named variables (`--oi-orange`, `--oi-blue`, `--oi-sky`, `--oi-green`, `--oi-vermillion`, etc.).
- **Paper theme:** `--paper` (#faf9f7), `--paper-ink` (#1a1a1a) for WCAG AA body contrast.
- **Figure wells** retain dark `--bg` / `--text` for chart contrast islands.
- `--font-serif: 'Lora', Georgia, serif`; `--font-ui: 'Source Sans 3', sans-serif`.

### Layout

- **`.editorial-shell`:** CSS Grid — TOC rail + article column (`--article-width: 42rem`).
- **`.editorial-figure`:** Breaks out of text measure (`margin-left` negative offset) up to `--figure-width: 72rem`.
- **`.viz-grid`:** Now `flex-direction: column` (legacy class kept; figures stack in document order).

### Typography

- Masthead title, section headings (`.section-heading`), card titles (`.card-info h3`), panel title — **serif**.
- Controls, captions, TOC, badges, tags — **sans-serif** (`var(--font-ui)`).
- Chart axes unchanged: `.tick text { font-family: var(--font-b); }` (sans).

### Figure styling

- `.viz-card` restyled as dark editorial figure wells on light page.
- `.interactive-badge` — green Okabe-Ito outline for discoverability.
- `.methods-box` — blue left rule for reproducibility sidebar.

### Present Mode (`body.present-mode`)

| Rule | Effect |
|------|--------|
| `scroll-snap-type: y mandatory` on `body` | Vertical slide snapping |
| `min-height: 100vh` on `.masthead`, `.editorial-figure`, `.article-methods` | One screen per slide |
| `scroll-snap-align: start` | Snap to slide tops |
| Hide `.article-lede`, `.article-prose-block` | Figures-only walkthrough |
| Hide `.toc-rail` | Cleaner presenter view |
| Taller `.card-preview` (`min(62vh, 520px)`) | Charts dominate viewport |

### Responsive

- `@media (max-width: 1100px)`: single column; TOC becomes horizontal link list.
- Present toggle repositioned on small screens.

### Removed / deprecated styles

- Hero particles, gradient `.gradient-text`, gallery header, 2×2 grid layout (replaced by editorial flow).

---

## JavaScript Changes (`dashboard/app.js`)

Only **minimal** edits for Present Mode and editorial compatibility:

1. **`spawnParticles()`** — early return if `#hero-particles` is absent (editorial masthead has no particle layer).
2. **`togglePresentMode()`** — toggles `body.present-mode`, updates `#present-mode-btn` `aria-pressed` and label text (“Present” / “Exit Present”).
3. **`DOMContentLoaded`** — wires click on `#present-mode-btn`.
4. **`keydown` listener** — **P** toggles Present Mode (ignored when focus is in input/textarea/select).

No changes to `openViz`, `closeViz`, `renderViz`, preview drawing, or India network logic.

---

## How the Layout Works

```
[Masthead — title, dek, sources]
        ↓
[TOC rail (sticky)] | [Article lede]
                    | [Prose section I]
                    | [Figure 1 — viz-card → openViz(1)]
                    | [Prose section II]
                    | [Figure 2]
                    | …
                    | [Methods]
```

1. User reads top-to-bottom in a **single article column**.
2. Figures are **dark interactive cards** embedded as `<figure>` elements.
3. Clicking a card still calls **`openViz(n)`** → fullscreen `#viz-panel` (unchanged behavior).
4. TOC anchors (`#figure-3`, etc.) use `scroll-margin-top` for fixed Present button clearance.

---

## How to Trigger Present Mode

| Method | Action |
|--------|--------|
| **Button** | Click **Present** (top-right). Click **Exit Present** to leave. |
| **Keyboard** | Press **P** (when not typing in a form control). |

When active, `document.body` has class **`present-mode`**: prose sections hide, each figure (plus masthead and methods) fills **100vh** with **scroll snap** between slides. Fullscreen viz panel (`#viz-panel`) is independent and works the same when a figure is clicked.

---

## Color & Accessibility Notes

- Page body: `#1a1a1a` on `#faf9f7` — meets **WCAG AA** for normal text.
- Accents limited to **Okabe-Ito** hues (orange, blue, sky, green, vermillion); no indigo/purple/cyan gradients.
- Figure interiors remain dark with `--text: #f0ebe3` for chart legibility.

---

## Verification Checklist

- [ ] Load `dashboard/index.html` — article layout, serif masthead, five figures in sequence.
- [ ] Click each card — fullscreen viz opens; Back returns to article.
- [ ] Press **P** — scroll snaps between full-height slides; prose hidden.
- [ ] Preview canvases render on load (`#preview-1`…`#preview-5`).
- [ ] TOC links scroll to correct `#figure-N` anchors.

---

## Git

```bash
git add dashboard/index.html dashboard/style.css dashboard/app.js editorial_implementation_report.md
git commit -m "feat(ui): implement editorial magazine layout with present mode"
```
