"""Apply light-mode token remaps to dashboard-light only. No invert."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch_style_css() -> None:
    path = ROOT / "style.css"
    text = path.read_text(encoding="utf-8")

    start = text.index(":root {")
    end = text.index("}", start) + 1
    new_root = """:root {
  /* Light-mode experiment — see docs/LIGHT_MODE_RESEARCH.md (no invert) */
  --bg: #f1f5f9;
  --bg2: #e8eef5;
  --surface: #ffffff;
  --surface-hover: #f8fafc;
  --border: rgba(15, 23, 42, 0.10);
  /* Teal remapped darker for WCAG on light; Okabe–Ito chart poles unchanged */
  --border-accent: rgba(14, 116, 144, 0.45);
  --accent: #0e7490;
  --accent-bright: #0891b2;
  --accent2: #0072B2;
  --accent3: #0284c7;
  --pair-a: #0072B2;
  --pair-b: #E69F00;
  --success: #009E73;
  --warning: #E69F00;
  --danger: #D55E00;
  --purple: #CC79A7;
  --landing-magenta: #7c3aed;
  --text: #0f172a;
  --text-muted: #475569;
  --text-dim: #94a3b8;
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
  --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.10);
  --shadow-lg: 0 16px 40px rgba(15, 23, 42, 0.14);
  --font-h: 'Outfit', sans-serif;
  --font-b: 'Plus Jakarta Sans', sans-serif;
  --radius: 14px;
  --radius-sm: 8px;
  --ease: cubic-bezier(0.4, 0, 0.2, 1);
}"""
    text = text[:start] + new_root + text[end:]

    replacements = [
        (
            "::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 3px; }",
            "::-webkit-scrollbar-thumb { background: rgba(15,23,42,0.18); border-radius: 3px; }",
        ),
        (
            """  background:
    radial-gradient(ellipse 55% 45% at 12% 18%, rgba(34,211,238,0.08) 0%, transparent 65%),
    radial-gradient(ellipse 40% 35% at 88% 70%, rgba(192,132,252,0.06) 0%, transparent 60%),
    var(--bg);""",
            """  background:
    radial-gradient(ellipse 55% 45% at 12% 18%, rgba(14,116,144,0.08) 0%, transparent 65%),
    radial-gradient(ellipse 40% 35% at 88% 70%, rgba(124,58,237,0.05) 0%, transparent 60%),
    var(--bg);""",
        ),
        (
            """  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(255,255,255,0.1);""",
            """  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(15,23,42,0.10);""",
        ),
        (
            "  50% { box-shadow: 0 0 14px var(--accent), 0 0 22px rgba(34,211,238,0.45); }",
            "  50% { box-shadow: 0 0 10px var(--accent), 0 0 16px rgba(14,116,144,0.28); }",
        ),
        ("  color: #fff;\n}\n\n.gradient-text {", "  color: var(--text);\n}\n\n.gradient-text {"),
        (
            "  background: linear-gradient(105deg, #22d3ee 0%, #67e8f9 28%, #a78bfa 68%, #e879f9 100%);",
            "  background: linear-gradient(105deg, #0e7490 0%, #0891b2 28%, #7c3aed 68%, #a855f7 100%);",
        ),
        (
            "  border-bottom: 1px dotted rgba(148, 163, 184, 0.45);",
            "  border-bottom: 1px dotted rgba(71, 85, 105, 0.45);",
        ),
        (
            """  background: rgba(30, 58, 95, 0.55);
  border: 1px solid rgba(148, 163, 184, 0.22);
  color: #e2e8f0;""",
            """  background: rgba(14, 116, 144, 0.08);
  border: 1px solid rgba(14, 116, 144, 0.22);
  color: #0f172a;""",
        ),
        ("  color: #fff;\n}\n\n.gallery-header p {", "  color: var(--text);\n}\n\n.gallery-header p {"),
        (
            """  background: rgba(17, 24, 39, 0.72);
  border: 1px solid rgba(255,255,255,0.07);""",
            """  background: var(--surface);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);""",
        ),
        (
            """  background: rgba(22, 32, 48, 0.92);
  box-shadow: 0 10px 28px rgba(0,0,0,0.35), 0 0 0 1px rgba(34,211,238,0.12);""",
            """  background: var(--surface-hover);
  box-shadow: var(--shadow-md), 0 0 0 1px rgba(14,116,144,0.18);""",
        ),
        (
            """  background: rgba(0,0,0,0.35);
  border-right: 1px solid rgba(255,255,255,0.05);""",
            """  background: #e2e8f0;
  border-right: 1px solid rgba(15,23,42,0.08);""",
        ),
        (
            "  background: linear-gradient(135deg, rgba(34,211,238,0.45), rgba(168,85,247,0.4));",
            "  background: linear-gradient(135deg, rgba(14,116,144,0.88), rgba(124,58,237,0.82));",
        ),
        ("  color: #fff;\n  line-height: 1.2;", "  color: var(--text);\n  line-height: 1.2;"),
        (
            """  background: rgba(255,255,255,0.045);
  border: 1px solid rgba(255,255,255,0.08);""",
            """  background: #f1f5f9;
  border: 1px solid rgba(15,23,42,0.08);""",
        ),
        ("  background: rgba(8,12,20,0.92);", "  background: rgba(241,245,249,0.92);"),
        ("  border: 3px solid rgba(34,211,238,0.2);", "  border: 3px solid rgba(14,116,144,0.2);"),
        ("  background: rgba(0,0,0,0.4);", "  background: rgba(255,255,255,0.82);"),
        (
            "/* Ensure select options are readable in dark mode across all browsers */\nselect option {\n  background-color: #0e1420 !important;\n  color: #f0ebe3 !important;\n}",
            "/* Ensure select options are readable in light mode across all browsers */\nselect option {\n  background-color: #ffffff !important;\n  color: #0f172a !important;\n}",
        ),
        (
            '  background-image: url("data:image/svg+xml;utf8,<svg fill=\'%23cbd5e1\' height=\'24\' viewBox=\'0 0 24 24\' width=\'24\' xmlns=\'http://www.w3.org/2000/svg\'><path d=\'M7 10l5 5 5-5z\'/></svg>");',
            '  background-image: url("data:image/svg+xml;utf8,<svg fill=\'%23475569\' height=\'24\' viewBox=\'0 0 24 24\' width=\'24\' xmlns=\'http://www.w3.org/2000/svg\'><path d=\'M7 10l5 5 5-5z\'/></svg>");',
        ),
        ("  background: rgba(255,255,255,0.1);", "  background: rgba(15,23,42,0.10);"),
        ("  background: rgba(0,0,0,0.3);", "  background: rgba(255,255,255,0.72);"),
        (
            """  background: rgba(10, 15, 28, 0.97);
  border: 1px solid var(--border-accent);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12px;
  line-height: 1.55;
  color: var(--text);
  pointer-events: none;
  box-shadow: 0 8px 30px rgba(0,0,0,0.5);""",
            """  background: rgba(255, 255, 255, 0.98);
  border: 1px solid var(--border-accent);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12px;
  line-height: 1.55;
  color: var(--text);
  pointer-events: none;
  box-shadow: var(--shadow-lg);""",
        ),
        (
            ".d3-tooltip strong { display: block; font-size: 13px; margin-bottom: 4px; color: #e8d4b8; }",
            ".d3-tooltip strong { display: block; font-size: 13px; margin-bottom: 4px; color: #0e7490; }",
        ),
        (
            ".tick line, .domain { stroke: rgba(255,255,255,0.08); }",
            ".tick line, .domain { stroke: rgba(15,23,42,0.10); }",
        ),
        (
            "#preview-1 { background: linear-gradient(135deg, #0e1420 0%, rgba(34,211,238,0.12) 100%); }",
            "#preview-1 { background: linear-gradient(135deg, #e2e8f0 0%, rgba(14,116,144,0.18) 100%); }",
        ),
        (
            "#preview-2 { background: linear-gradient(135deg, #0e1420 0%, rgba(232,121,249,0.10) 100%); }",
            "#preview-2 { background: linear-gradient(135deg, #e2e8f0 0%, rgba(124,58,237,0.14) 100%); }",
        ),
        (
            "#preview-3 { background: linear-gradient(135deg, #0e1420 0%, rgba(86,180,233,0.10) 100%); }",
            "#preview-3 { background: linear-gradient(135deg, #e2e8f0 0%, rgba(2,132,199,0.14) 100%); }",
        ),
        (
            "#preview-4 { background: linear-gradient(135deg, #0e1420 0%, rgba(0,158,115,0.10) 100%); }",
            "#preview-4 { background: linear-gradient(135deg, #e2e8f0 0%, rgba(0,158,115,0.14) 100%); }",
        ),
        (
            "#preview-5 { background: linear-gradient(135deg, #0e1420 0%, rgba(167,139,250,0.12) 100%); }",
            "#preview-5 { background: linear-gradient(135deg, #e2e8f0 0%, rgba(124,58,237,0.16) 100%); }",
        ),
        (
            "    border-bottom: 1px solid rgba(255,255,255,0.05);",
            "    border-bottom: 1px solid rgba(15,23,42,0.08);",
        ),
    ]

    for old, new in replacements:
        if old not in text:
            print(f"WARN style.css miss: {old[:60]!r}...")
        else:
            text = text.replace(old, new, 1)

    path.write_text(text, encoding="utf-8")
    print("patched style.css")


def multi_replace(path: Path, pairs: list[tuple[str, str]], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    n = 0
    for old, new in pairs:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
        else:
            # allow optional misses for sparse files
            pass
    path.write_text(text, encoding="utf-8")
    print(f"patched {label}: {n} replacements")


# Shared dark→light chrome swaps for JS/CSS under graphs + app
CHROME_PAIRS = [
    ("rgba(255,255,255,0.05)", "rgba(15,23,42,0.06)"),
    ("rgba(255, 255, 255, 0.05)", "rgba(15, 23, 42, 0.06)"),
    ("rgba(255,255,255,0.06)", "rgba(15,23,42,0.08)"),
    ("rgba(255, 255, 255, 0.06)", "rgba(15, 23, 42, 0.08)"),
    ("rgba(255,255,255,0.08)", "rgba(15,23,42,0.10)"),
    ("rgba(255, 255, 255, 0.08)", "rgba(15, 23, 42, 0.10)"),
    ("rgba(255,255,255,0.1)", "rgba(15,23,42,0.12)"),
    ("rgba(255,255,255,0.10)", "rgba(15,23,42,0.12)"),
    ("rgba(255, 255, 255, 0.1)", "rgba(15, 23, 42, 0.12)"),
    ("rgba(255, 255, 255, 0.10)", "rgba(15, 23, 42, 0.12)"),
    ("rgba(255,255,255,0.12)", "rgba(15,23,42,0.12)"),
    ("rgba(255, 255, 255, 0.12)", "rgba(15, 23, 42, 0.12)"),
    ("rgba(255,255,255,0.15)", "rgba(15,23,42,0.14)"),
    ("rgba(255, 255, 255, 0.15)", "rgba(15, 23, 42, 0.14)"),
    ("rgba(255,255,255,0.2)", "rgba(15,23,42,0.16)"),
    ("rgba(255,255,255,0.20)", "rgba(15,23,42,0.16)"),
    ("rgba(255, 255, 255, 0.2)", "rgba(15, 23, 42, 0.16)"),
    ("rgba(255,255,255,0.35)", "rgba(15,23,42,0.28)"),
    ("rgba(255,255,255,0.55)", "rgba(15,23,42,0.35)"),
    ("rgba(255, 255, 255, 0.55)", "rgba(15, 23, 42, 0.35)"),
    ("rgba(255,255,255,0.65)", "rgba(15,23,42,0.55)"),
    ("rgba(255,255,255,0.7)", "rgba(15,23,42,0.55)"),
    ("rgba(255,255,255,0.02)", "rgba(15,23,42,0.04)"),
    ("rgba(255,255,255,0.04)", "rgba(15,23,42,0.06)"),
    ("rgba(255,255,255,0.035)", "rgba(15,23,42,0.04)"),
    ("rgba(15, 23, 42, 0.6)", "rgba(255, 255, 255, 0.95)"),
    ("rgba(15, 23, 42, 0.92)", "rgba(255, 255, 255, 0.96)"),
    ("background: #0f172a", "background: #ffffff"),
    ("background:#0f172a", "background:#ffffff"),
    ("background: #0b0f19", "background: #f1f5f9"),
    ("--bg-color: #0b0f19", "--bg-color: #f1f5f9"),
    ("color: #0b0f19", "color: #0f172a"),
    ("background-color: #0e1420", "background-color: #ffffff"),
    ("background: #1e293b", "background: #ffffff"),
    ("color: #0f172a;", "color: #0f172a;"),  # no-op keep
    # Plotly / Chart.js axis (if still present)
    ("gridcolor: 'rgba(255,255,255,0.05)'", "gridcolor: 'rgba(15,23,42,0.08)'"),
    ("linecolor: 'rgba(255,255,255,0.2)'", "linecolor: 'rgba(15,23,42,0.18)'"),
    # Text / stroke that was white-on-dark → near-black-on-light
    ("color:#fff;", "color:#0f172a;"),
    ("color: #fff;", "color: #0f172a;"),
    ("color: #fff\"", "color: #0f172a\""),
    ("color:#fff\"", "color:#0f172a\""),
    ("color: #fff,", "color: #0f172a,"),
    ("color:#fff,", "color:#0f172a,"),
    ("color: #fff ", "color: #0f172a "),
    ("font-weight: 800; color: #fff;", "font-weight: 800; color: #0f172a;"),
    ("font-weight:700; color:#fff;", "font-weight:700; color:#0f172a;"),
    ('color="#fff"', 'color="#0f172a"'),
    ('.attr("stroke", "#ffffff")', '.attr("stroke", "#0f172a")'),
    ("color: #cbd5e1", "color: #334155"),
    ("color:#cbd5e1", "color:#334155"),
    # Dark panel backgrounds (explicit property forms only)
    ("background: #0f172a;", "background: #ffffff;"),
    ("background:#0f172a;", "background:#ffffff;"),
    ("background: #0f172a ", "background: #ffffff "),
    ("background: #0b0f19;", "background: #f1f5f9;"),
    ("background: #1e293b;", "background: #ffffff;"),
]


def patch_g1() -> None:
    js = ROOT / "graphs" / "g1" / "g1.js"
    text = js.read_text(encoding="utf-8")
    text = text.replace(
        "paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',",
        "paper_bgcolor: '#f8fafc', plot_bgcolor: '#f8fafc',",
    )
    text = text.replace("gridcolor: 'rgba(255,255,255,0.05)'", "gridcolor: 'rgba(15,23,42,0.08)'")
    text = text.replace("linecolor: 'rgba(255,255,255,0.2)'", "linecolor: 'rgba(15,23,42,0.18)'")
    # Bubble label colors for light paper
    text = text.replace(
        "if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? '#56B4E9' : 'rgba(255,255,255,0.05)';\n"
        "      if (!isSearchActive) return d._positionCarried ? 'rgba(255,255,255,0.35)' : 'rgba(255,255,255,0.7)';\n"
        "      return matchesSearch(d.Country_Name) ? '#ffffff' : 'rgba(255,255,255,0.05)';",
        "if (isCompareActive) return viz1ComparedCountries.includes(d.Country_Code) ? '#0072B2' : 'rgba(15,23,42,0.08)';\n"
        "      if (!isSearchActive) return d._positionCarried ? 'rgba(15,23,42,0.35)' : 'rgba(15,23,42,0.72)';\n"
        "      return matchesSearch(d.Country_Name) ? '#0f172a' : 'rgba(15,23,42,0.08)';",
    )
    text = text.replace(
        'background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;',
        'background: rgba(14,116,144,0.12); padding: 2px 6px; border-radius: 4px; color:#0e7490;',
    )
    js.write_text(text, encoding="utf-8")
    print("patched g1.js")

    css = ROOT / "graphs" / "g1" / "g1.css"
    multi_replace(
        css,
        [
            ("background: #0f172a; /* Fallback for dark theme */", "background: #f8fafc; /* Fallback for light theme */"),
            ("border-right: 1px solid rgba(255,255,255,0.1);", "border-right: 1px solid rgba(15,23,42,0.10);"),
            ("color: #94a3b8;", "color: #475569;"),
            ("color: #cbd5e1;", "color: #334155;"),
            ("border: 1px solid rgba(255,255,255,0.1);", "border: 1px solid rgba(15,23,42,0.10);"),
            ("background: rgba(255,255,255,0.03);", "background: rgba(15,23,42,0.03);"),
            ("border: 1px solid rgba(255,255,255,0.08);", "border: 1px solid rgba(15,23,42,0.10);"),
            ("color: #fff;", "color: #0f172a;"),
            ("border: 1.5px solid rgba(255, 255, 255, 0.55);", "border: 1.5px solid rgba(15, 23, 42, 0.25);"),
            ("background: #1e293b;", "background: #ffffff;"),
            ("background: rgba(255,255,255,0.1);", "background: rgba(14,116,144,0.12);"),
            ("border: 1px solid rgba(255,255,255,0.2);", "border: 1px solid rgba(14,116,144,0.25);"),
            ("color: #0f172a;", "color: #0f172a;"),  # keep dark text on light chrome
            ("--accent, #22d3ee", "--accent, #0e7490"),
        ],
        "g1.css",
    )


def patch_generic_files() -> None:
    files = [
        ROOT / "graphs" / "g2" / "g2.js",
        ROOT / "graphs" / "g2" / "g2.css",
        ROOT / "graphs" / "g3" / "g3.js",
        ROOT / "graphs" / "g3" / "g3.css",
        ROOT / "graphs" / "g4" / "g4.js",
        ROOT / "graphs" / "g5" / "g5.css",
        ROOT / "graphs" / "g5" / "g5.js",
        ROOT / "india_network.js",
        ROOT / "app.js",
    ]
    for f in files:
        if not f.exists():
            print("missing", f)
            continue
        multi_replace(f, CHROME_PAIRS, f.relative_to(ROOT).as_posix())


def patch_g3_specific() -> None:
    css = ROOT / "graphs" / "g3" / "g3.css"
    text = css.read_text(encoding="utf-8")
    text = text.replace("--card-border: rgba(255, 255, 255, 0.07);", "--card-border: rgba(15, 23, 42, 0.10);")
    text = text.replace("--text-muted: #94a3b8;", "--text-muted: #475569;")
    text = text.replace("background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);", "background: linear-gradient(135deg, #0f172a 0%, #64748b 100%);")
    text = text.replace("box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);", "box-shadow: 0 0 16px rgba(14, 116, 144, 0.25);")
    text = text.replace("background: rgba(0,0,0,0.15);", "background: rgba(241,245,249,0.9);")
    css.write_text(text, encoding="utf-8")
    print("patched g3.css specifics")

    js = ROOT / "graphs" / "g3" / "g3.js"
    t = js.read_text(encoding="utf-8")
    t = t.replace("borderColor: 'rgba(255, 255, 255, 0.1)'", "borderColor: 'rgba(15, 23, 42, 0.12)'")
    t = t.replace("color: 'rgba(255, 255, 255, 0.05)'", "color: 'rgba(15, 23, 42, 0.08)'")
    t = t.replace("color: '#94a3b8'", "color: '#475569'")
    js.write_text(t, encoding="utf-8")
    print("patched g3.js chart colors")


def patch_g5_sidebar() -> None:
    css = ROOT / "graphs" / "g5" / "g5.css"
    t = css.read_text(encoding="utf-8")
    t = t.replace("background: rgba(0,0,0,0.15);", "background: rgba(241,245,249,0.95);")
    # tier-central sky may need darker text on light — keep Okabe with darker border already OK
    t = t.replace("color: #56B4E9;", "color: #0284c7;")
    css.write_text(t, encoding="utf-8")
    print("patched g5.css sidebar")


def patch_g2_gradients() -> None:
    js = ROOT / "graphs" / "g2" / "g2.js"
    t = js.read_text(encoding="utf-8")
    t = t.replace(
        "background: linear-gradient(135deg, #fff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;",
        "background: linear-gradient(135deg, #0f172a 0%, #475569 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;",
    )
    t = t.replace("box-shadow: 0 4px 20px rgba(0,0,0,0.25);", "box-shadow: 0 4px 20px rgba(15,23,42,0.08);")
    t = t.replace("box-shadow: 0 4px 15px rgba(0,0,0,0.35);", "box-shadow: 0 4px 15px rgba(15,23,42,0.10);")
    t = t.replace('.attr("fill", "#94a3b8")', '.attr("fill", "#475569")')
    t = t.replace('return item ? getContinentColor(item.metrics.continent) : "#94a3b8";', 'return item ? getContinentColor(item.metrics.continent) : "#475569";')
    js.write_text(t, encoding="utf-8")
    print("patched g2.js headings/shadows")


def patch_app_canvas() -> None:
    app = ROOT / "app.js"
    t = app.read_text(encoding="utf-8")
    t = t.replace('ctx.strokeStyle = "rgba(255,255,255,0.15)";', 'ctx.strokeStyle = "rgba(15,23,42,0.15)";')
    t = t.replace('ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";', 'ctx.strokeStyle = "rgba(15, 23, 42, 0.08)";')
    t = t.replace('ctx.strokeStyle = "rgba(255, 255, 255, 0.15)";', 'ctx.strokeStyle = "rgba(15, 23, 42, 0.15)";')
    app.write_text(t, encoding="utf-8")
    print("patched app.js canvas strokes")


def main() -> None:
    patch_style_css()
    patch_g1()
    patch_generic_files()
    patch_g3_specific()
    patch_g5_sidebar()
    patch_g2_gradients()
    patch_app_canvas()
    print("DONE light theme apply")


if __name__ == "__main__":
    main()
