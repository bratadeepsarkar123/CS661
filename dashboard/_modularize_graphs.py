# -*- coding: utf-8 -*-
"""One-shot structural cut: app.js/style.css -> graphs/gN/ + G3 UI removals."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAPHS = ROOT / "graphs"


def slice_lines(lines: list[str], start: int, end: int) -> str:
    """1-indexed inclusive start, exclusive end (end line number = first line NOT included)."""
    return "\n".join(lines[start - 1 : end - 1]) + "\n"


def main() -> None:
    app_path = ROOT / "app.js"
    css_path = ROOT / "style.css"
    html_path = ROOT / "index.html"

    # Backups (once)
    bak_app = ROOT / "app.js.bak-pre-modular"
    bak_css = ROOT / "style.css.bak-pre-modular"
    if not bak_app.exists():
        shutil.copy2(app_path, bak_app)
    if not bak_css.exists():
        shutil.copy2(css_path, bak_css)

    app_lines = app_path.read_text(encoding="utf-8").splitlines()
    css_lines = css_path.read_text(encoding="utf-8").splitlines()
    n_app = len(app_lines)

    # --- Line map (1-indexed, verified against markers) ---
    # Shared shell: APP through renderViz dispatcher (excludes VIZ1 globals at top)
    # VIZ1: globals 1-129 + body 581-1664
    # VIZ2: 1665-2734
    # VIZ3: 2735-4253
    # VIZ4: 4255-4541
    # VIZ5: 4543-4678 (through selectIndiaNode)
    # Shared tail: toggleAnimation onward

    # Find exact boundaries by scanning
    def find_line(substr: str, after: int = 1) -> int:
        for i in range(after - 1, n_app):
            if substr in app_lines[i]:
                return i + 1
        raise SystemExit(f"marker not found: {substr!r} after {after}")

    g1_globals_end = find_line("// CS661 Group 10")  # exclusive start of shared
    shared_head_start = g1_globals_end
    viz1_body_start = find_line("// VIZ 1: High-Dimensional")
    viz2_start = find_line("// VIZ 2: Global Quality")
    viz3_start = find_line("function renderViz3")
    # prefer section banner if present
    try:
        viz3_banner = find_line("// VIZ 3")
        if viz3_banner < viz3_start:
            viz3_start = viz3_banner
    except SystemExit:
        pass
    viz4_start = find_line("function renderViz4")
    viz5_start = find_line("// VIZ 5: India")
    toggle_start = find_line("function toggleAnimation")
    # selectIndiaNode is before toggleAnimation; include it in g5
    select_india = find_line("function selectIndiaNode")

    print("Boundaries:")
    print(f"  g1 globals: 1 .. {g1_globals_end - 1}")
    print(f"  shared head: {shared_head_start} .. {viz1_body_start - 1}")
    print(f"  g1 body: {viz1_body_start} .. {viz2_start - 1}")
    print(f"  g2: {viz2_start} .. {viz3_start - 1}")
    print(f"  g3: {viz3_start} .. {viz4_start - 1}")
    print(f"  g4: {viz4_start} .. {viz5_start - 1}")
    print(f"  g5: {viz5_start} .. {toggle_start - 1}")
    print(f"  shared tail: {toggle_start} .. {n_app}")
    print(f"  selectIndiaNode @ {select_india}")

    for d in ("g1", "g2", "g3", "g4", "g5"):
        (GRAPHS / d).mkdir(parents=True, exist_ok=True)

    # ========== G1 JS ==========
    # Strip shared OKABE palette (lives in app.js; graphs load after orchestrator)
    g1_globals = slice_lines(app_lines, 1, g1_globals_end)
    g1_globals = re.sub(
        r"// Okabe-Ito[\s\S]*?const OKABE = OKABE_ITO;\s*",
        "// OKABE_ITO / OKABE provided by app.js (shared)\n",
        g1_globals,
        count=1,
    )
    g1_js = (
        "// graphs/g1/g1.js — Graph 1 (UMAP peer clustering)\n"
        + g1_globals
        + "\n"
        + slice_lines(app_lines, viz1_body_start, viz2_start)
    )
    (GRAPHS / "g1" / "g1.js").write_text(g1_js, encoding="utf-8")

    # ========== G2 JS (+ extract CSS) ==========
    g2_raw = slice_lines(app_lines, viz2_start, viz3_start)
    g2_css_match = re.search(
        r"const styleBlock = document\.createElement\(\"style\"\);\s*"
        r"styleBlock\.textContent = `([\s\S]*?)`;\s*"
        r"container\.appendChild\(styleBlock\);",
        g2_raw,
    )
    if not g2_css_match:
        raise SystemExit("G2 styleBlock not found")
    g2_css = (
        "/* graphs/g2/g2.css — Graph 2 only */\n"
        + g2_css_match.group(1).strip()
        + "\n"
    )
    # Scope #panel-body overflow under viz2 container via a safer rule already in block
    (GRAPHS / "g2" / "g2.css").write_text(g2_css, encoding="utf-8")
    g2_js = (
        "// graphs/g2/g2.js — Graph 2 (Global Quality Shift)\n"
        + g2_raw[: g2_css_match.start()]
        + "// Styles: graphs/g2/g2.css (loaded from index.html)\n"
        + g2_raw[g2_css_match.end() :]
    )
    (GRAPHS / "g2" / "g2.js").write_text(g2_js, encoding="utf-8")

    # ========== G3 JS (+ extract CSS, UI removals) ==========
    g3_raw = slice_lines(app_lines, viz3_start, viz4_start)

    # Extract inline <style>...</style>
    style_m = re.search(r"<style>([\s\S]*?)</style>", g3_raw)
    if not style_m:
        raise SystemExit("G3 inline <style> not found")
    g3_css_body = style_m.group(1)
    # Drop header chrome CSS (removed with header element)
    g3_css_body = re.sub(
        r"/\*\s*Header\s*\*/[\s\S]*?(?=/\*\s*Dashboard Grid|/Dashboard Grid|\.dashboard-grid)",
        "/* Header chrome removed (Job B) */\n\n        ",
        g3_css_body,
        count=1,
    )
    # Also remove leftover header rules if banner comment pattern differed
    for rule in (
        r"\s*header\s*\{[\s\S]*?\}\s*",
        r"\s*\.header-title h1\s*\{[\s\S]*?\}\s*",
        r"\s*\.header-title p\s*\{[\s\S]*?\}\s*",
        r"\s*\.group-badge\s*\{[\s\S]*?\}\s*",
    ):
        g3_css_body = re.sub(rule, "\n", g3_css_body)

    g3_css = "/* graphs/g3/g3.css — Graph 3 only */\n" + g3_css_body.strip() + "\n"
    # Prefix top-level selectors that could leak: scope under .viz3-container where needed.
    # Keep as-is; original was already injected under .viz3-container parent with nested CSS vars.
    (GRAPHS / "g3" / "g3.css").write_text(g3_css, encoding="utf-8")

    g3_js = g3_raw.replace(style_m.group(0), "<!-- styles: graphs/g3/g3.css -->", 1)

    # Remove repeating site header flex
    g3_js = re.sub(
        r"\s*<header>\s*"
        r"<div class=\"header-title\">\s*"
        r"<h1>The Global Knowledge & Wealth Paradox</h1>\s*"
        r"<p>CS661 Visual Analytics &bull; Group 10 Dashboard</p>\s*"
        r"</div>\s*"
        r"<div class=\"group-badge\">Project Module 4\.3: Research topics evolution</div>\s*"
        r"</header>\s*",
        "\n",
        g3_js,
        count=1,
    )

    # Remove OpenAlex period note paragraph
    g3_js = re.sub(
        r"\s*<p style=\"margin: 0\.75rem 1rem 1rem; font-size: 0\.78rem; line-height: 1\.45; color: #94a3b8;\">\s*"
        r"OpenAlex concept counts[\s\S]*?</p>\s*",
        "\n",
        g3_js,
        count=1,
    )

    # Remove COVID infectious note strip
    g3_js = re.sub(
        r"\s*<div id=\"covidInfectiousNote\"[\s\S]*?</div>\s*",
        "\n",
        g3_js,
        count=1,
    )

    # Remove JS for covid note
    g3_js = re.sub(
        r"\s*const covidInfectiousNote = container\.querySelector\('#covidInfectiousNote'\);\s*",
        "\n",
        g3_js,
        count=1,
    )
    g3_js = re.sub(
        r"\s*const COVID_NOTE_HTML = `[\s\S]*?`;\s*"
        r"\s*function updateCovidInfectiousNote\(\) \{[\s\S]*?\}\s*",
        "\n",
        g3_js,
        count=1,
    )
    g3_js = re.sub(
        r"\s*updateCovidInfectiousNote\(\);\s*",
        "\n",
        g3_js,
    )
    # Remove insight-card COVID callout
    g3_js = re.sub(
        r"\s*\$\{topic === 'Infectious Diseases' \? `[\s\S]*?` : ''\}\s*",
        "\n",
        g3_js,
        count=1,
    )

    g3_js = "// graphs/g3/g3.js — Graph 3 (Research topics)\n" + g3_js
    (GRAPHS / "g3" / "g3.js").write_text(g3_js, encoding="utf-8")

    # ========== G4 JS ==========
    g4_js = (
        "// graphs/g4/g4.js — Graph 4 (Collaboration Premium)\n"
        + slice_lines(app_lines, viz4_start, viz5_start)
    )
    (GRAPHS / "g4" / "g4.js").write_text(g4_js, encoding="utf-8")
    (GRAPHS / "g4" / "g4.css").write_text(
        "/* graphs/g4/g4.css — Graph 4 only (dumbbell uses shared panel chrome + inline SVG styles) */\n"
        ".viz4-empty {\n  color: var(--text-muted, #94a3b8);\n  padding: 2rem;\n}\n",
        encoding="utf-8",
    )

    # ========== G5 JS + CSS from style.css ==========
    g5_js = (
        "// graphs/g5/g5.js — Graph 5 shell (India network via INDIA / india_network.js)\n"
        + slice_lines(app_lines, viz5_start, toggle_start)
    )
    (GRAPHS / "g5" / "g5.js").write_text(g5_js, encoding="utf-8")

    # ========== Shared app.js ==========
    shared = (
        "// app.js — shared orchestrator / landing / routing (thin)\n"
        "// Graph renderers live in graphs/gN/gN.js\n\n"
        "// Okabe-Ito shared palette (used by G2/G4 controls chrome)\n"
        "const OKABE_ITO = {\n"
        "  blue: '#0072B2',\n"
        "  orange: '#E69F00',\n"
        "  sky: '#56B4E9',\n"
        "  vermillion: '#D55E00',\n"
        "  purple: '#CC79A7',\n"
        "  green: '#009E73',\n"
        "  yellow: '#F0E442',\n"
        "  black: '#000000',\n"
        "  muted: '#94a3b8',\n"
        "  grey: '#999999'\n"
        "};\n"
        "const OKABE = OKABE_ITO;\n\n"
        + slice_lines(app_lines, shared_head_start, viz1_body_start)
        + "\n"
        + slice_lines(app_lines, toggle_start, n_app + 1)
    )
    # Remove OKABE_ITO duplicate if it was in shared head — shared head starts at CS661 banner
    # which is AFTER OKABE — good. But VIZ_META / previews don't need viz1 palette.
    app_path.write_text(shared, encoding="utf-8")

    # ========== CSS split ==========
    # Find CSS sections
    def find_css(substr: str, after: int = 1) -> int:
        for i in range(after - 1, len(css_lines)):
            if substr in css_lines[i]:
                return i + 1
        raise SystemExit(f"CSS marker not found: {substr!r}")

    india_legacy_start = find_css("India map + sidebar")
    # Keep split-layout with g1 (marked Special: viz 1)
    split_start = find_css("Special: viz 1")
    module5_start = find_css("Module 5")
    viz1_css_start = find_css("VIZ 1 LAYOUT")

    # Media query blocks that mention india — keep india rules in g5
    # Shared CSS = lines 1..(split_start-1) plus landing media queries without india-only overrides
    # Simpler approach: shared = 1..(split_start-1); g1 = split + viz1 layout; g5 = india legacy + module5 + india media bits

    # Between india_legacy and module5 there are panel-footer, tooltip, ticks, previews, media queries.
    # Structure:
    # 689-704 split (g1)
    # 706-808 india-layout (g5)
    # 810-891 panel footer / tooltip / ticks / legend / previews (shared)
    # 900+ media — mix

    g1_css_parts: list[str] = []
    g5_css_parts: list[str] = []
    shared_css_parts: list[str] = []

    # Lines 1 .. split_start-1 = shared (through panel-body)
    shared_css_parts.append(slice_lines(css_lines, 1, split_start))

    # split-layout -> g1
    # india-layout starts at india_legacy_start
    g1_css_parts.append(slice_lines(css_lines, split_start, india_legacy_start))

    # india-layout block until "Panel footer"
    panel_footer = find_css("Panel footer")
    g5_css_parts.append(slice_lines(css_lines, india_legacy_start, panel_footer))

    # panel footer through end of preview canvases / before first media that is landing-only
    # Keep shared from panel footer until Module 5, but strip india-only media rules into g5

    mid = slice_lines(css_lines, panel_footer, module5_start)
    # Pull india-related media rules out
    india_media = []

    def split_media(block: str) -> tuple[str, str]:
        """Return (shared_block, india_only_rules_joined)."""
        india_bits = []
        shared_bits = []
        # crude: remove lines containing .india- or india-layout from shared media
        for line in block.splitlines(keepends=True):
            if "india-" in line or "india-layout" in line or "india-map" in line:
                india_bits.append(line)
            else:
                shared_bits.append(line)
        return "".join(shared_bits), "".join(india_bits)

    mid_shared, mid_india = split_media(mid)
    shared_css_parts.append(mid_shared)
    if mid_india.strip():
        g5_css_parts.append("/* india rules lifted from shared media */\n" + mid_india)

    # Module 5 through before VIZ 1 = g5
    g5_css_parts.append(slice_lines(css_lines, module5_start, viz1_css_start))

    # VIZ 1 to EOF = g1
    g1_css_parts.append(slice_lines(css_lines, viz1_css_start, len(css_lines) + 1))

    shared_css = (
        "/* style.css — SHARED only: landing, chrome, page-wide colors */\n"
        + "".join(shared_css_parts)
    )
    css_path.write_text(shared_css, encoding="utf-8")
    (GRAPHS / "g1" / "g1.css").write_text(
        "/* graphs/g1/g1.css — Graph 1 only */\n" + "".join(g1_css_parts),
        encoding="utf-8",
    )
    (GRAPHS / "g5" / "g5.css").write_text(
        "/* graphs/g5/g5.css — Graph 5 (India network) only */\n" + "".join(g5_css_parts),
        encoding="utf-8",
    )

    # ========== index.html wiring ==========
    html = html_path.read_text(encoding="utf-8")
    # Replace stylesheet block
    html = re.sub(
        r'<link rel="stylesheet" href="style\.css[^"]*">\s*'
        r'<link rel="stylesheet" href="https://unpkg.com/leaflet@1\.9\.4/dist/leaflet\.css"[^>]*>',
        """<link rel="stylesheet" href="style.css?v=20260712-modular">
  <link rel="stylesheet" href="graphs/g1/g1.css?v=20260712-modular">
  <link rel="stylesheet" href="graphs/g2/g2.css?v=20260712-modular">
  <link rel="stylesheet" href="graphs/g3/g3.css?v=20260712-modular">
  <link rel="stylesheet" href="graphs/g4/g4.css?v=20260712-modular">
  <link rel="stylesheet" href="graphs/g5/g5.css?v=20260712-modular">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">""",
        html,
        count=1,
    )
    # Replace app.js script with graph scripts then thin app.js
    html = re.sub(
        r'<script src="india_network\.js[^"]*"></script>\s*'
        r'<script src="viz4_data\.js[^"]*"></script>\s*'
        r'<script src="app\.js[^"]*"></script>',
        """<script src="india_network.js?v=20260712-g5-count-picker"></script>
  <script src="viz4_data.js?v=20260712g24b"></script>
  <script src="app.js?v=20260712-modular"></script>
  <script src="graphs/g1/g1.js?v=20260712-modular"></script>
  <script src="graphs/g2/g2.js?v=20260712-modular"></script>
  <script src="graphs/g3/g3.js?v=20260712-modular"></script>
  <script src="graphs/g4/g4.js?v=20260712-modular"></script>
  <script src="graphs/g5/g5.js?v=20260712-modular"></script>""",
        html,
        count=1,
    )
    html_path.write_text(html, encoding="utf-8")

    # ========== GRAPHS_LAYOUT.md ==========
    (ROOT / "GRAPHS_LAYOUT.md").write_text(
        """# Dashboard graph layout

Per-graph folders so editing one visualization does not require touching another.

```
dashboard/
  index.html          # shell + landing + script/link order
  style.css           # SHARED: landing, panel chrome, page-wide colors
  app.js              # SHARED: routing, controls chrome, helpers
  graphs/
    g1/  g1.css  g1.js   # UMAP peer clustering
    g2/  g2.css  g2.js   # Global quality shift
    g3/  g3.css  g3.js   # Research topics
    g4/  g4.css  g4.js   # Collaboration premium
    g5/  g5.css  g5.js   # India network shell
  india_network.js    # G5 Leaflet engine (kept at root; safe)
  *_data.js / data/   # pools — do not merge
```

## Load order

1. Shared CSS (`style.css`) then `graphs/gN/gN.css`
2. Vendor (D3, Leaflet, Plotly, Chart.js)
3. Data pools (`viz*_data.js`, `india_network_data.js`, …)
4. `india_network.js` (G5 engine)
5. Thin `app.js` orchestrator (shared palette + routing)
6. `graphs/gN/gN.js`

## Editing rule

Change graph N only under `graphs/gN/`. Do not put graph-only CSS/JS back into `style.css` / `app.js`.
""",
        encoding="utf-8",
    )

    # Sanity checks
    g3_check = (GRAPHS / "g3" / "g3.js").read_text(encoding="utf-8")
    assert "The Global Knowledge & Wealth Paradox" not in g3_check, "G3 header title still present"
    assert "covidInfectiousNote" not in g3_check, "covid note still present"
    assert "OpenAlex concept counts for 1974" not in g3_check, "OpenAlex period note still present"
    assert "updateCovidInfectiousNote" not in g3_check
    assert "function renderViz3" in g3_check
    assert "function renderViz1" in (GRAPHS / "g1" / "g1.js").read_text(encoding="utf-8")
    assert "function renderViz" in app_path.read_text(encoding="utf-8")
    print("OK — modularization + G3 cleanup written")


if __name__ == "__main__":
    main()
