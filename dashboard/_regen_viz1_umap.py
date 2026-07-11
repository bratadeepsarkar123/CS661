"""
Regenerate G1 UMAP x,y from g1_features_panel.csv into viz1_data.js.

Stability goals (stop left/right "dance" on Play):
  1. Seed each year with the previous year's coordinates (UMAP init).
  2. Align with reflection-aware Procrustes on shared countries.
  3. Bake a light temporal EMA into the pool so year-to-year paths glide.

Layout goals (fill the plot canvas):
  - Coords stay in a compact range; app.js sets axis ranges from data extents.

Backup: viz1_data_BEFORE_POOLFIX.js must exist.
Does NOT touch app.js / HTML / CSS (axis ranges live in app.js separately).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.linalg import orthogonal_procrustes
import umap

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "CS661_Dataset" / "raw_vault" / "READY_FOR_TEAM" / "g1_features_panel.csv"
VIZ1 = ROOT / "dashboard" / "viz1_data.js"
BAK = ROOT / "dashboard" / "viz1_data_BEFORE_POOLFIX.js"
PROOF = ROOT / "CS661_Dataset" / "raw_vault" / "READY_FOR_TEAM" / "_notes" / "_umap_regen_proof.json"

FEATURES = ["GDP_Per_Capita_PPP", "GERD_Percent_GDP", "Total_Docs", "H_Index"]
RANDOM_STATE = 42
N_NEIGHBORS = 15
MIN_DIST = 0.1
TEMPORAL_EMA = 0.18  # baked into pool; lower = stick closer to previous year (less dance)
BLEND_TO_PREV = 0.55  # after Procrustes, mix toward previous coords for shared countries


def load_viz1(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    i, j = text.find("["), text.rfind("]")
    return json.loads(text[i : j + 1])


def write_viz1(path: Path, rows: list[dict]) -> None:
    body = json.dumps(rows, separators=(",", ":"))
    path.write_text("const VIZ1_DATA = " + body + ";\n", encoding="utf-8")


def coalesce_docs(df: pd.DataFrame) -> pd.DataFrame:
    """Prefer Total_Docs; fall back to WB_Pubs then SCImago_Documents only.

    Never use OpenAlex for Total_Docs (incompatible 'works' scale vs journal articles).
    WB / Total_Docs zeros are treated as missing so a WB=0 year does not block
    a positive SCImago document count — fixes microstate ghost gaps.
    """
    out = df.copy()
    for col in ("Total_Docs", "WB_Pubs", "SCImago_Documents"):
        if col not in out.columns:
            out[col] = np.nan
    # Zeros are not observations — only positive counts (or true NaN) participate.
    docs = out["Total_Docs"].mask(out["Total_Docs"] <= 0)
    wb = out["WB_Pubs"].mask(out["WB_Pubs"] <= 0)
    sci = out["SCImago_Documents"].mask(out["SCImago_Documents"] <= 0)
    out["Total_Docs"] = docs.fillna(wb).fillna(sci)
    return out


def impute_gerd(df: pd.DataFrame) -> pd.DataFrame:
    """Country ffill/bfill, then region-year median, then global-year median."""
    out = df.sort_values(["Country_Code", "Year"]).copy()
    out["gerd_imputed"] = out["GERD_Percent_GDP"].isna()
    out["GERD_Percent_GDP"] = out.groupby("Country_Code")["GERD_Percent_GDP"].transform(
        lambda s: s.ffill().bfill()
    )
    region_col = "SCImago_Region" if "SCImago_Region" in out.columns else None
    if region_col:
        med = out.groupby([region_col, "Year"])["GERD_Percent_GDP"].transform("median")
        out["GERD_Percent_GDP"] = out["GERD_Percent_GDP"].fillna(med)
    year_med = out.groupby("Year")["GERD_Percent_GDP"].transform("median")
    out["GERD_Percent_GDP"] = out["GERD_Percent_GDP"].fillna(year_med)
    return out


def validate_h(df: pd.DataFrame) -> None:
    usa = float(df.loc[(df.Country_Code == "USA") & (df.Year == 2022), "H_Index"].iloc[0])
    irl = float(df.loc[(df.Country_Code == "IRL") & (df.Year == 2022), "H_Index"].iloc[0])
    assert irl < usa, f"Ireland H ({irl}) must not exceed USA ({usa})"
    assert 3000 <= usa <= 4000, f"USA H expected ~3388 scale, got {usa}"


def scale_features(g: pd.DataFrame) -> np.ndarray:
    X = g[FEATURES].to_numpy(dtype=float).copy()
    X[:, [0, 2, 3]] = np.log1p(X[:, [0, 2, 3]])
    return StandardScaler().fit_transform(X)


def embed_year(g: pd.DataFrame, init: np.ndarray | None = None) -> np.ndarray:
    Xs = scale_features(g)
    n = len(g)
    n_neighbors = min(N_NEIGHBORS, max(2, n - 1))
    kwargs: dict = dict(
        n_components=2,
        n_neighbors=n_neighbors,
        min_dist=MIN_DIST,
        metric="euclidean",
        random_state=RANDOM_STATE,
    )
    # Seeding from previous year keeps topology continuous across time.
    if init is not None and init.shape == (n, 2) and np.all(np.isfinite(init)):
        kwargs["init"] = init
    reducer = umap.UMAP(**kwargs)
    return reducer.fit_transform(Xs)


def best_procrustes(ref: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Align target → ref. Try orthogonal Procrustes plus explicit axis reflections
    and pick the transform with lowest SSE on the paired points.
    Returns (aligned_full_target_transform_fn applied via R,t on centered target), sse.
    Actually returns R (2x2), t (2,), sse for transforming full cloud:
      aligned = (xy - tgt_mean) @ R + ref_mean   but we need to use common subset means.
    """
    ref_mean = ref.mean(axis=0)
    tgt_mean = target.mean(axis=0)
    ref_c = ref - ref_mean
    tgt_c = target - tgt_mean

    candidates = [np.eye(2), np.diag([1.0, -1.0]), np.diag([-1.0, 1.0]), np.diag([-1.0, -1.0])]
    best = None
    best_sse = float("inf")
    best_R = None
    for flip in candidates:
        flipped = tgt_c @ flip
        R, _ = orthogonal_procrustes(flipped, ref_c)
        aligned = flipped @ R
        sse = float(np.sum((aligned - ref_c) ** 2))
        if sse < best_sse:
            best_sse = sse
            best = aligned
            best_R = flip @ R
    assert best_R is not None and best is not None
    return best_R, tgt_mean, ref_mean, best_sse


def build_init(codes: list[str], prev_codes: list[str], prev_xy: np.ndarray, rng: np.random.RandomState) -> np.ndarray:
    prev_map = {c: prev_xy[i] for i, c in enumerate(prev_codes)}
    centroid = prev_xy.mean(axis=0)
    init = np.zeros((len(codes), 2), dtype=float)
    for i, code in enumerate(codes):
        if code in prev_map:
            init[i] = prev_map[code]
        else:
            init[i] = centroid + rng.normal(0, 0.15, size=2)
    return init


def temporal_ema_smooth(xy_map: dict[tuple[str, int], tuple[float, float]], alpha: float) -> None:
    """In-place EMA along each country's year path (reduces residual dance)."""
    by_code: dict[str, list[tuple[int, tuple[float, float]]]] = {}
    for (code, year), xy in xy_map.items():
        by_code.setdefault(code, []).append((year, xy))
    for code, pts in by_code.items():
        pts.sort(key=lambda t: t[0])
        mx, my = pts[0][1]
        xy_map[(code, pts[0][0])] = (mx, my)
        for year, (x, y) in pts[1:]:
            mx = alpha * x + (1 - alpha) * mx
            my = alpha * y + (1 - alpha) * my
            xy_map[(code, year)] = (mx, my)


def count_x_flips(xy_map: dict[tuple[str, int], tuple[float, float]], code: str) -> int:
    yrs = sorted(y for (c, y) in xy_map if c == code)
    flips = 0
    for i in range(1, len(yrs) - 1):
        x0 = xy_map[(code, yrs[i - 1])][0]
        x1 = xy_map[(code, yrs[i])][0]
        x2 = xy_map[(code, yrs[i + 1])][0]
        if (x1 - x0) * (x2 - x1) < 0:
            flips += 1
    return flips


def main() -> None:
    t0 = time.time()
    if not BAK.exists():
        raise SystemExit(f"Refusing to run: missing backup {BAK}")

    panel = coalesce_docs(pd.read_csv(PANEL))
    panel = impute_gerd(panel)
    validate_h(panel)

    ready = panel.dropna(subset=FEATURES).copy()
    ready = ready[ready["Total_Docs"] > 0].copy()
    ready["Year"] = ready["Year"].astype(int)
    ready = ready[ready["Country_Code"].str.len() == 3].copy()

    bak_rows = load_viz1(BAK)
    region_by_code = {}
    name_by_code = {}
    for r in bak_rows:
        region_by_code[r["Country_Code"]] = r.get("Region") or region_by_code.get(r["Country_Code"])
        if r.get("Country_Name"):
            name_by_code[r["Country_Code"]] = r["Country_Name"]

    xy_map: dict[tuple[str, int], tuple[float, float]] = {}
    prev_codes: list[str] | None = None
    prev_xy: np.ndarray | None = None
    years_done = []
    rng = np.random.RandomState(RANDOM_STATE)

    for year, g in ready.groupby("Year", sort=True):
        g = g.sort_values("Country_Code").reset_index(drop=True)
        if len(g) < 4:
            print(f"year {year}: skip (only {len(g)} countries)")
            continue
        codes = g["Country_Code"].tolist()

        init = None
        if prev_xy is not None and prev_codes is not None:
            init = build_init(codes, prev_codes, prev_xy, rng)

        xy = embed_year(g, init=init)

        if prev_xy is not None and prev_codes is not None:
            common = [c for c in codes if c in set(prev_codes)]
            if len(common) >= 3:
                idx_new = [codes.index(c) for c in common]
                idx_old = [prev_codes.index(c) for c in common]
                R, tgt_mean, ref_mean, sse = best_procrustes(prev_xy[idx_old], xy[idx_new])
                xy = (xy - tgt_mean) @ R + ref_mean
                # Anchor shared countries toward last year's spot so Play doesn't L/R-dance
                prev_map = {c: prev_xy[i] for i, c in enumerate(prev_codes)}
                for i, code in enumerate(codes):
                    if code in prev_map:
                        xy[i] = (1.0 - BLEND_TO_PREV) * xy[i] + BLEND_TO_PREV * prev_map[code]
                print(f"year {year}: aligned {len(common)} countries sse={sse:.2f} blend={BLEND_TO_PREV}")
            else:
                print(f"year {year}: embedded {len(g)} countries (no align)")
        else:
            print(f"year {year}: embedded {len(g)} countries (seed year)")

        for i in range(len(g)):
            code = g.iloc[i]["Country_Code"]
            yr = int(g.iloc[i]["Year"])
            xy_map[(code, yr)] = (float(xy[i, 0]), float(xy[i, 1]))

        prev_codes = codes
        prev_xy = xy
        years_done.append(int(year))
        print(f"year {year}: done ({len(g)} countries)")

    flips_before = {c: count_x_flips(xy_map, c) for c in ("USA", "CHN", "IND", "GBR", "DEU", "JPN")}
    temporal_ema_smooth(xy_map, TEMPORAL_EMA)
    flips_after = {c: count_x_flips(xy_map, c) for c in ("USA", "CHN", "IND", "GBR", "DEU", "JPN")}

    new_viz_rows = []
    for _, r in ready.iterrows():
        key = (r["Country_Code"], int(r["Year"]))
        if key not in xy_map:
            continue
        x, y = xy_map[key]
        code = r["Country_Code"]
        name = r.get("Country_Name") or name_by_code.get(code) or code
        if not isinstance(name, str) or not str(name).strip() or str(name).lower() == "nan":
            name = name_by_code.get(code) or code
        region = region_by_code.get(code) or r.get("SCImago_Region") or "Other"
        if not isinstance(region, str) or not str(region).strip() or str(region).lower() == "nan":
            region = "Other"
        new_viz_rows.append(
            {
                "Country_Code": code,
                "Country_Name": name,
                "Year": int(r["Year"]),
                "Region": region,
                "Total_Docs": float(r["Total_Docs"]),
                "H_Index": float(r["H_Index"]),
                "GERD_Percent_GDP": float(r["GERD_Percent_GDP"]),
                "GDP_Per_Capita_PPP": float(r["GDP_Per_Capita_PPP"]),
                "x": x,
                "y": y,
            }
        )

    updated = len(new_viz_rows)
    print(f"pool rows written: {updated} (incomplete rows dropped)")
    print("USA x-flips before/after EMA:", flips_before["USA"], flips_after["USA"])

    majors = ["USA", "CHN", "IND", "GBR", "DEU", "JPN"]
    for y in (2015, 2020, 2022, 2024):
        for c in majors:
            assert (c, y) in xy_map, f"missing embed for {c} {y}"

    write_viz1(VIZ1, new_viz_rows)

    after = load_viz1(VIZ1)
    before = load_viz1(BAK)

    def find(rows, code, year):
        for r in rows:
            if r["Country_Code"] == code and int(r["Year"]) == year:
                return r
        raise KeyError((code, year))

    a, b = find(after, "USA", 2022), find(before, "USA", 2022)
    assert float(a["H_Index"]) == 3388.0
    xs = [r["x"] for r in after]
    ys = [r["y"] for r in after]

    proof = {
        "status": "OK",
        "elapsed_sec": round(time.time() - t0, 1),
        "panel": str(PANEL),
        "random_state": RANDOM_STATE,
        "n_neighbors": N_NEIGHBORS,
        "min_dist": MIN_DIST,
        "init": "previous_year_coords",
        "procrustes": "reflection_aware",
        "temporal_ema": TEMPORAL_EMA,
        "blend_to_prev": BLEND_TO_PREV,
        "gerd_policy": "ffill+bfill Country_Code → region-year median → year median; docs coalesce WB→SCImago only (never OA; WB/Total_Docs zeros treated as NA)",
        "years_embedded": years_done,
        "xy_updated": updated,
        "xy_kept_old": 0,
        "USA_2022_H": float(a["H_Index"]),
        "USA_2022_xy_before_backup": [b["x"], b["y"]],
        "USA_2022_xy_after": [a["x"], a["y"]],
        "coord_extent": {"x": [min(xs), max(xs)], "y": [min(ys), max(ys)]},
        "x_flips_before_ema": flips_before,
        "x_flips_after_ema": flips_after,
        "backup": BAK.name,
        "viz1_bytes": VIZ1.stat().st_size,
    }
    PROOF.parent.mkdir(parents=True, exist_ok=True)
    PROOF.write_text(json.dumps(proof, indent=2), encoding="utf-8")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
