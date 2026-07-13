"""Round-2 light chrome fixes for dashboard-light."""
from pathlib import Path

ROOT = Path(r"C:\Users\brata\Downloads\CS661\dashboard-light")


def rep(path: Path, pairs: list[tuple[str, str]]) -> None:
    t = path.read_text(encoding="utf-8")
    n = 0
    for a, b in pairs:
        c = t.count(a)
        if c:
            t = t.replace(a, b)
            n += c
            print(f"  {c}x {a[:55]}")
        else:
            print(f"  miss {a[:55]}")
    path.write_text(t, encoding="utf-8")
    print(f"{path.name}: {n} total\n")


def main() -> None:
    print("g4.js")
    rep(
        ROOT / "graphs" / "g4" / "g4.js",
        [
            ("background:rgba(15,23,42,0.8)", "background:rgba(255,255,255,0.95)"),
            ("background:rgba(15,23,42,0.5)", "background:rgba(248,250,252,0.98)"),
            ("color:#94a3b8", "color:#475569"),
            ("color:#e2e8f0", "color:#334155"),
            ('attr("fill", "#94a3b8")', 'attr("fill", "#475569")'),
            ('attr("fill", "#cbd5e1")', 'attr("fill", "#334155")'),
            ("rgba(255,255,255,0.25)", "rgba(15,23,42,0.12)"),
            ("rgba(255,255,255,0.6)", "rgba(15,23,42,0.35)"),
        ],
    )

    print("g1.js plotly")
    rep(
        ROOT / "graphs" / "g1" / "g1.js",
        [
            ("font: { family: 'Plus Jakarta Sans, sans-serif', color: '#f8fafc' }",
             "font: { family: 'Plus Jakarta Sans, sans-serif', color: '#0f172a' }"),
            ("hoverlabel: { bgcolor: 'rgba(15, 23, 42, 0.95)', font: { family: 'Plus Jakarta Sans, sans-serif', size: 13, color: '#f8fafc' }, bordercolor: '#56B4E9' }",
             "hoverlabel: { bgcolor: 'rgba(255, 255, 255, 0.98)', font: { family: 'Plus Jakarta Sans, sans-serif', size: 13, color: '#0f172a' }, bordercolor: '#0e7490' }"),
            ("legend: { font: { color: '#e2e8f0', size: 12 }",
             "legend: { font: { color: '#334155', size: 12 }"),
        ],
    )

    print("g1.css")
    rep(
        ROOT / "graphs" / "g1" / "g1.css",
        [
            ("color: #e2e8f0;", "color: #475569;"),
            (
                """  background: rgba(15, 23, 42, 0.92);
  border: 1px solid rgba(86, 180, 233, 0.45);
  border-radius: 8px;
  color: #f8fafc;""",
                """  background: rgba(255, 255, 255, 0.97);
  border: 1px solid rgba(14, 116, 144, 0.35);
  border-radius: 8px;
  color: #0f172a;""",
            ),
            ("box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);", "box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);"),
            ("box-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);", "box-shadow: 0 1px 3px rgba(15, 23, 42, 0.18);"),
        ],
    )

    print("g3.css leftovers")
    rep(
        ROOT / "graphs" / "g3" / "g3.css",
        [
            ("color: rgba(255, 255, 255, 0.035);", "color: rgba(15, 23, 42, 0.04);"),
            ("background: rgba(255, 255, 255, 0.02);", "background: rgba(15, 23, 42, 0.03);"),
        ],
    )

    print("g5")
    rep(
        ROOT / "graphs" / "g5" / "g5.js",
        [('.attr("fill", "rgba(255,255,255,0.03)")', '.attr("fill", "rgba(15,23,42,0.03)")')],
    )
    rep(
        ROOT / "graphs" / "g5" / "g5.css",
        [
            ("border: 1px solid rgba(255, 255, 255, 0.35);", "border: 1px solid rgba(15, 23, 42, 0.14);"),
            ("border: 1px solid rgba(255, 255, 255, 0.4);", "border: 1px solid rgba(15, 23, 42, 0.12);"),
            ("border: 1px solid rgba(255, 255, 255, 0.14);", "border: 1px solid rgba(15, 23, 42, 0.12);"),
        ],
    )

    print("app.js")
    rep(
        ROOT / "app.js",
        [
            ('"#22d3ee"', '"#0e7490"'),
            ("['#f59e0b','#0e7490','#a78bfa','#e879f9']", "['#E69F00','#0e7490','#7c3aed','#CC79A7']"),
            ("['#0e7490','#56B4E9','#a78bfa','#e879f9']", "['#0e7490','#0072B2','#7c3aed','#CC79A7']"),
            ('["#f59e0b","#0e7490","#a78bfa","#e879f9"]', '["#E69F00","#0e7490","#7c3aed","#CC79A7"]'),
            ('["#0e7490","#56B4E9","#a78bfa","#e879f9"]', '["#0e7490","#0072B2","#7c3aed","#CC79A7"]'),
        ],
    )

    # Fix g2 muted labels still #94a3b8
    print("g2 muted")
    rep(
        ROOT / "graphs" / "g2" / "g2.js",
        [("color: #94a3b8", "color: #475569"), ("color:#94a3b8", "color:#475569")],
    )

    print("DONE round2")


if __name__ == "__main__":
    main()
