#!/usr/bin/env python3
"""Bundle dashboard/data/india_network/*.json into india_network_data.js."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "dashboard" / "data" / "india_network"
OUT = ROOT / "dashboard" / "india_network_data.js"
GEO_CANDIDATES = [
    ROOT / "public" / "india_network" / "india_outline.geojson",
    SRC / "india_outline.geojson",
]


def main() -> None:
    lines = ["const INDIA_NETWORK_DATA = {};"]
    for path in sorted(SRC.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        lines.append(f"INDIA_NETWORK_DATA[{json.dumps(path.name)}] = {json.dumps(data, ensure_ascii=False)};")

    for geo in GEO_CANDIDATES:
        if geo.exists():
            data = json.loads(geo.read_text(encoding="utf-8"))
            lines.append(
                f"INDIA_NETWORK_DATA[{json.dumps('india_outline.geojson')}] = {json.dumps(data, ensure_ascii=False)};"
            )
            break

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
