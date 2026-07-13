# Light-Mode Theme Research — CS661 Dashboard Experiment

**Scope:** Research findings and concrete token rules for `dashboard-light/` only.  
**Constraint:** No `filter: invert()` / hue-rotate hacks. Parallel semantic tokens.  
**Brand:** Teal–cyan landing chrome + Okabe–Ito categorical chart colors.  
**Date:** 2026-07-12

---

## 1. Why invert fails (dark → light)

Human vision is **not symmetric** across luminance. Mechanically flipping black↔white (or CSS `filter: invert()`) fails because:

1. **Halation / glare** — Pure white on pure black (or the reverse) causes text to appear to bleed; soft off-whites and near-blacks reduce strain ([Muzli / Nathan](https://medium.muz.li/dark-mode-design-why-simply-inverting-colors-is-not-enough-e2584ebb139b)).
2. **Elevation model breaks** — Light UI uses **shadows** (darker under raised surfaces). Dark UI uses **lighter surfaces** for elevation. Invert turns shadows into glows and destroys hierarchy ([ColorArchive](https://colorarchive.org/notes/december-2026-dark-mode-design-decisions/), [Material / UI UX Atlas](https://www.uiuxatlas.com/lessons/design-systems/theming-and-dark-mode-implementation/)).
3. **Accent saturation** — Brand cyans/teals tuned for dark canvases look neon; the same hex on white often fails WCAG or feels washed. Accents must be **re-authored per theme**, not flipped ([Design Systems Collective](https://www.designsystemscollective.com/dark-mode-done-right-building-adaptive-design-systems-5f220f656b9f)).
4. **Images & intentional exceptions** — Modals, photos, and “always-dark” chrome invert incorrectly (Figma Config 2022: invert+hue-rotate is unsustainable).
5. **Semantic meaning** — Warning/success roles need different lightness/chroma on light vs dark; inversion preserves neither contrast nor meaning ([token-layer article](https://www.designsystemscollective.com/dark-mode-is-not-an-inversion-building-it-right-from-the-token-layer-up-f2094136c038)).

**Rule for this experiment:** redefine `--bg`, `--surface`, `--text`, `--accent`, borders, chart paper/grid — never invert the live tree.

---

## 2. Light-mode color systems (surfaces, elevation, borders, WCAG)

### Surfaces & elevation (light polarity)

| Layer | Role | Typical approach |
|-------|------|------------------|
| App canvas | Page floor | Cool off-white / gray-50 — **not** pure `#fff` everywhere |
| Raised surface | Cards, panels | White or +2–4% L with soft shadow |
| Overlay / header | Sticky chrome | Slightly tinted white + hairline border |
| Modal / tooltip | Highest | White + stronger shadow |

GitHub Primer: neutrals are dual scales; backgrounds use early steps, borders mid steps, text late steps; contrast is validated against `bgColor-muted` ([Primer color usage](https://primer.style/foundations/color/overview)).

Material Design 3: themes are full token re-expressions (surface, on-surface, primary, outline) — not overlays ([M3 Color](https://m3.material.io/styles/color/system/overview)).

### Borders

- Prefer **1px hairlines** at low alpha on slate (`rgba(15,23,42,0.08–0.14)`).
- Interactive control borders need ≥ **3:1** vs adjacent fill (WCAG 1.4.11).

### Text contrast (WCAG 2.2 AA baseline)

| Use | Min ratio | Our targets |
|-----|-----------|-------------|
| Body / UI text | 4.5:1 | `--text` `#0f172a` on `--bg` / white ≥ ~16:1 |
| Large text | 3:1 | Titles use `--text` |
| Muted labels | 4.5:1 if used as text | `--text-muted` `#475569` (slate-600) |
| Disabled / dim | may fail AA | `--text-dim` only for non-essential chrome |

APCA (WCAG 3 draft) is a useful **supplement** for polarity-aware checks ([Mantlr color systems](https://mantlr.com/blog/color-systems-that-scale), [Social Animal 2026](https://socialanimal.dev/blog/build-color-system-web-design-2026/)).

---

## 3. Additive vs perceptual color (OKLCH / LCH)

- **sRGB / HSL** are not perceptually uniform: same “L” or “S” looks uneven across hues.
- **OKLCH** keeps lightness comparable across hues → predictable ramps, theme forks, and contrast gates ([BoldVanta OKLCH](https://www.boldvanta.com/design/designing-luminance-cefirst-color-systems-with-oklch-tokens-ramps-and-real-ceworld-pitfalls.html), [Mantlr](https://mantlr.com/blog/color-systems-that-scale)).
- Practical pattern: lock **L** for semantics (`text` L≈0.20–0.25 light mode; surfaces L≈0.96–0.99), then set **C/H** for brand.

**Brand-safe accent remapping (light):**

| Role | Dark (current live) | Light (experiment) | Why |
|------|---------------------|--------------------|-----|
| Accent / links / focus | `#22d3ee` (cyan-400) | `#0e7490` (teal-700) | Darker L for AA on white; keeps teal identity |
| Accent soft / chips | bright cyan glow | `#0891b2` / tinted fills | Readable fills without neon |
| Okabe blue (pair-a) | `#0072B2` | **keep** `#0072B2` | Already designed for light figures |
| Sky (accent3) | `#56B4E9` | `#0284c7` for UI links; keep `#56B4E9` in charts | Sky alone can fail body-text AA on white |
| Success / warning / danger | Okabe greens/oranges | **keep Okabe hexes** | Palette is light-paper native |

---

## 4. How major products handle light themes

| Product | Light-mode pattern | Takeaway for us |
|---------|--------------------|-----------------|
| **GitHub / Primer** | Dual neutral scales; functional tokens (`bgColor-default`, `fgColor-muted`); accent role for links/focus | Semantic tokens + inverted scale direction |
| **Material You (M3)** | Surface / on-surface / primary containers; elevation via tone + shadow | Separate light scheme, not invert |
| **Linear** | Restraint: neutrals + one accent; surface ladder; hairlines ([craft synthesis](https://mantlr.com/blog/stripe-linear-vercel-premium-ui)) | Few accents; hierarchy via surfaces |
| **Vercel** | Near-monochrome + precise accent; off-black/off-white discipline | Cool grays, not cream clichés |
| **Stripe** | Whitespace + restrained indigo; density via typography | Soft neutrals; one action color |
| **Notion** | Warm minimalism, soft elevated surfaces | Warmth optional — we stay **cool** to match teal brand |

Shared craft: **interaction completeness**, typography as hierarchy, color as meaning not decoration ([Mantlr premium UI](https://mantlr.com/blog/stripe-linear-vercel-premium-ui)).

---

## 5. Conversion-oriented hierarchy on light backgrounds

On light canvases, hierarchy is mostly **contrast + weight + whitespace**, not glow:

1. **Squint / blur test** — Headline and primary CTA must remain the most salient elements ([StoreMD hierarchy](https://leakdetector.tech/blog/saas-visual-hierarchy)).
2. **CTA singularity** — One saturated action color (our teal-700) used for primary buttons / key CTAs; secondary = outline ([Spell UI CTAs](https://spell.sh/blog/landing-page-cta-best-practices)).
3. **60 / 30 / 10** — Neutrals dominate; brand ~20–25%; action color ~5–10% ([GFX-Art](https://www.gfx-art.org/visual-hierarchy-principles-for-landing-page-layout-a-designers-breakdown/)).
4. **Cards on light** — Prefer white surfaces + soft shadow + hairline over heavy fills; avoid competing neon borders.

Landing implications for CS661 light copy:

- Soft cool canvas (`#f1f5f9` / `#f8fafc`) with subtle teal radial wash (low chroma).
- Near-black titles (`#0f172a`); muted slate subcopy.
- Gallery cards: white / soft gray, teal accent on hover — not cyan glow stacks.
- Chart panels: light paper, slate axis ticks, hairline grids.

---

## 6. Okabe–Ito on light paper (charts)

Canonical hexes ([ConceptViz](https://conceptviz.app/blog/okabe-ito-palette-hex-codes-complete-reference), [jfly / Wong Nature Methods](https://www.nature.com/articles/nmeth.1618)):

| Name | Hex |
|------|-----|
| Orange | `#E69F00` |
| Sky blue | `#56B4E9` |
| Bluish green | `#009E73` |
| Yellow | `#F0E442` |
| Blue | `#0072B2` |
| Vermillion | `#D55E00` |
| Reddish purple | `#CC79A7` |
| Black / screen grey | `#000000` → prefer `#334155` for series that would collide with axis text |

**Important:** Okabe–Ito was designed for **light / print** figures. On dark dashboards we often lighten/desaturate; for this light experiment we **restore** standard Okabe values for categorical series and remap only **chrome** (paper, grid, labels, tooltips).

Cascivo note: on dark themes, raise L ~0.06–0.1; on light, use base palette unmodified ([cascivo chart palette](https://github.com/cascivo/cascivo/blob/main/docs/specs/chart-palette.md)).

Chart chrome (light):

| Token | Value |
|-------|-------|
| Paper / plot | `#f8fafc` or transparent over `--bg2` |
| Grid | `rgba(15, 23, 42, 0.08)` |
| Axis line | `rgba(15, 23, 42, 0.18)` |
| Tick labels | `#475569` |
| Legend text | `#334155` |
| Tooltip | white / `#fff` + slate text + teal border |

---

## 7. Concrete CSS token rules (`dashboard-light` only)

```css
:root {
  /* Surfaces — cool gray ladder (GitHub/Primer-inspired polarity) */
  --bg: #f1f5f9;                 /* canvas — soft cool gray, not #fff everywhere */
  --bg2: #e8eef5;                /* panel floor, slightly deeper */
  --surface: #ffffff;            /* raised cards */
  --surface-hover: #f8fafc;
  --border: rgba(15, 23, 42, 0.10);
  --border-accent: rgba(14, 116, 144, 0.45); /* teal-700 @ 45% */

  /* Brand accents — darker for light AA */
  --accent: #0e7490;             /* teal-700 — links, CTA, focus */
  --accent-bright: #0891b2;      /* teal-600 — chips / hover fills */
  --accent2: #0072B2;            /* Okabe blue */
  --accent3: #0284c7;            /* sky remapped for UI text */

  /* Okabe–Ito semantic (charts + status) — keep */
  --pair-a: #0072B2;
  --pair-b: #E69F00;
  --success: #009E73;
  --warning: #E69F00;
  --danger: #D55E00;
  --purple: #CC79A7;
  --landing-magenta: #7c3aed;    /* violet-600 — readable on light */

  /* Text — slate, WCAG AA+ */
  --text: #0f172a;               /* slate-900 */
  --text-muted: #475569;         /* slate-600 */
  --text-dim: #94a3b8;           /* slate-400 — decorative only */

  /* Elevation (light = shadow, not lighter fill alone) */
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.10);
  --shadow-lg: 0 16px 40px rgba(15, 23, 42, 0.14);
}
```

### Do / Don’t

| Do | Don’t |
|----|-------|
| Semantic token swap per theme | `filter: invert(1)` on `html`/`body` |
| Darker teal for buttons/links on light | Keep `#22d3ee` for body links on white |
| Soft cool canvas + white cards | Flat pure `#ffffff` with no hierarchy |
| Okabe hexes for series | Recolor categorical series to neon cyan |
| Slate grids on light paper | White 5% grids (invisible on light) |
| Soft multi-stop shadows | Heavy black 0.5 opacity “dark mode” shadows |

---

## 8. Implementation map (this experiment)

| Area | Files under `dashboard-light/` |
|------|--------------------------------|
| Global tokens + landing + panel chrome | `style.css` |
| G1 Plotly paper/grid/labels | `graphs/g1/g1.js`, `graphs/g1/g1.css` |
| G2 D3 axes / cards | `graphs/g2/g2.js`, `graphs/g2/g2.css` |
| G3 Chart.js + CSS vars | `graphs/g3/g3.js`, `graphs/g3/g3.css` |
| G4 dumbbell | `graphs/g4/g4.js` |
| G5 India network | `graphs/g5/g5.css`, `india_network.js` |
| Shared canvas helpers | `app.js` |

**Data files** (`viz*_data.js`, pools, etc.) remain byte-identical to `dashboard/`.

**Serving:** `python -m http.server 8088` with cwd `dashboard-light/`. Live dark dashboard on `:8080` untouched.

---

## 9. Key citations

1. https://medium.muz.li/dark-mode-design-why-simply-inverting-colors-is-not-enough-e2584ebb139b  
2. https://www.designsystemscollective.com/dark-mode-is-not-an-inversion-building-it-right-from-the-token-layer-up-f2094136c038  
3. https://www.designsystemscollective.com/dark-mode-done-right-building-adaptive-design-systems-5f220f656b9f  
4. https://colorarchive.org/notes/december-2026-dark-mode-design-decisions/  
5. https://www.uiuxatlas.com/lessons/design-systems/theming-and-dark-mode-implementation/  
6. https://mantlr.com/blog/color-systems-that-scale  
7. https://socialanimal.dev/blog/build-color-system-web-design-2026/  
8. https://www.boldvanta.com/design/designing-luminance-cefirst-color-systems-with-oklch-tokens-ramps-and-real-ceworld-pitfalls.html  
9. https://primer.style/foundations/color/overview  
10. https://m3.material.io/styles/color/system/overview  
11. https://mantlr.com/blog/stripe-linear-vercel-premium-ui  
12. https://conceptviz.app/blog/okabe-ito-palette-hex-codes-complete-reference  
13. https://github.com/cascivo/cascivo/blob/main/docs/specs/chart-palette.md  
14. https://leakdetector.tech/blog/saas-visual-hierarchy  
15. https://spell.sh/blog/landing-page-cta-best-practices  
16. https://www.nature.com/articles/nmeth.1618 (Wong / Okabe–Ito popularization)

---

*Verification token for pipeline discipline: research → tokens → themed CSS/JS → separate localhost. No invert.*
