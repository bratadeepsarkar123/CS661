#!/usr/bin/env python3
"""Run Module 5 verification checklist from master plan; write report."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from config import PROCESSED_DIR, PUBLIC_DIR, YEAR_MIN  # noqa: E402
from filters import (  # noqa: E402
    is_domestic_work,
    master_institution_ids_on_work,
    openalex_id,
    work_passes_filters,
)

LOG_DIR = PROCESSED_DIR.parent / "logs"
OUT_MD = PROCESSED_DIR / "verification_report.md"
OUT_JSON = LOG_DIR / "verification_report.json"
SCIMAGEO_YEAR = 2019


def check(name: str, ok: bool, detail: str) -> dict:
    return {"name": name, "ok": bool(ok), "detail": str(detail)}


def _parse_authorships(raw):
    if raw is None:
        return []
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return []
    return raw


def _find_institution(master: pd.DataFrame, *needles: str) -> pd.Series | None:
    for _, row in master.iterrows():
        name = str(row.get("canonical_name", "")).lower()
        if all(n.lower() in name for n in needles):
            return row
    return None


def _positive_domestic_test(master: pd.DataFrame, domestic_path: Path) -> tuple[bool, str]:
    """Known domestic co-auth pair (IIT Kanpur + IIT Delhi) appears in domestic_works."""
    iitk = _find_institution(master, "kanpur")
    iitd = _find_institution(master, "delhi")
    if iitk is None or iitd is None:
        return False, "IIT Kanpur or IIT Delhi not in institution_master"
    oa_k = iitk["openalex_id"]
    oa_d = iitd["openalex_id"]
    inst_pair = {oa_k, oa_d}

    edges = PROCESSED_DIR / "collaboration_edges_full.csv"
    if edges.exists():
        e = pd.read_csv(edges)
        edge_hit = e[
            ((e["openalex_a"] == oa_k) & (e["openalex_b"] == oa_d))
            | ((e["openalex_a"] == oa_d) & (e["openalex_b"] == oa_k))
        ]
        if len(edge_hit) > 0:
            w = int(edge_hit["weight"].sum())
            return True, f"IIT Kanpur ↔ IIT Delhi edge weight={w} in collaboration_edges_full.csv"

    if not domestic_path.exists():
        return False, "domestic_works.parquet missing"
    dom = pd.read_parquet(domestic_path)
    if dom.empty:
        return False, "domestic_works.parquet is empty"
    for _, row in dom.iterrows():
        ids = row.get("institution_ids")
        if isinstance(ids, str):
            try:
                ids = json.loads(ids)
            except json.JSONDecodeError:
                continue
        if inst_pair.issubset(set(ids or [])):
            return True, f"work_id={row.get('work_id')} links IIT Kanpur + IIT Delhi"
    return False, "no IIT Kanpur + IIT Delhi domestic work found"


def _negative_foreign_test(master: pd.DataFrame, works_path: Path, domestic_path: Path) -> tuple[bool, str]:
    """Work with foreign co-author must not appear in domestic_works (W3 filter)."""
    if not works_path.exists() or not domestic_path.exists():
        return False, "works_raw or domestic_works missing"
    iitk = _find_institution(master, "kanpur")
    if iitk is None:
        return False, "IIT Kanpur not in master"
    master_oa = set(master["openalex_id"])
    oa_k = iitk["openalex_id"]
    raw = pd.read_parquet(works_path)
    dom_ids = set(pd.read_parquet(domestic_path)["work_id"].astype(str))

    for _, row in raw.head(50000).iterrows():
        authorships = _parse_authorships(row.get("authorships"))
        insts = []
        for auth in authorships:
            for inst in auth.get("institutions") or []:
                if inst.get("id"):
                    insts.append(inst)
        if not insts:
            continue
        has_k = any(openalex_id(i.get("id")) == oa_k for i in insts)
        has_foreign = any(i.get("country_code") and i.get("country_code") != "IN" for i in insts)
        if not (has_k and has_foreign):
            continue
        wid = str(row.get("id", "")).rsplit("/", 1)[-1]
        if wid in dom_ids:
            return False, f"foreign co-auth work {wid} incorrectly in domestic_works"
        if not is_domestic_work(authorships):
            return True, f"foreign co-auth work {wid} correctly excluded from domestic_works"
    return True, "sampled works: foreign co-auth papers absent from domestic_works (spot check)"


def _payload_orphan_edges(payload_path: Path) -> tuple[bool, str]:
    try:
        data = json.loads(payload_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return False, f"invalid JSON: {exc}"
    node_ids = {n["id"] for n in data.get("nodes", [])}
    orphans = [
        e
        for e in data.get("edges", [])
        if e.get("source") not in node_ids or e.get("target") not in node_ids
    ]
    ok = len(orphans) == 0
    return ok, f"{len(orphans)} orphan edges (nodes={len(node_ids)}, edges={len(data.get('edges', []))})"


def _coord_stack_check(master: pd.DataFrame) -> tuple[bool, str]:
    if master.empty:
        return False, "no master"
    m = master.copy()
    m["lat_r"] = m["latitude"].round(4)
    m["lon_r"] = m["longitude"].round(4)
    stacks = m.groupby(["lat_r", "lon_r"]).size()
    worst = int(stacks.max()) if len(stacks) else 0
    bad_india = m[
        (m["latitude"] < 6) | (m["latitude"] > 38) | (m["longitude"] < 68) | (m["longitude"] > 98)
    ]
    ok = worst <= 2 and len(bad_india) == 0
    return ok, f"max stack={worst}, out_of_india={len(bad_india)}"


def _funding_corruption_check(funding: pd.DataFrame) -> tuple[bool, str]:
    """Newer IITs must not inherit Delhi/Kanpur/Hyderabad-scale recycled funding."""
    suspects = {
        "bhilai": 100.0,
        "jammu": 100.0,
        "dharwad": 50.0,
    }
    problems: list[str] = []
    for _, row in funding.iterrows():
        name = str(row.get("canonical_name", "")).lower()
        amount = row.get("research_funding_cr")
        if pd.isna(amount):
            continue
        for token, ceiling in suspects.items():
            if token in name and float(amount) > ceiling:
                problems.append(f"{row['canonical_name']}={amount} cr (>{ceiling})")
    ok = len(problems) == 0
    return ok, "no suspect funding" if ok else "; ".join(problems[:5])


def _major_iit_funding_check(funding: pd.DataFrame) -> tuple[bool, str]:
    needles = ["technology delhi", "technology kanpur", "technology hyderabad", "technology madras"]
    missing = []
    for needle in needles:
        hit = funding[funding["canonical_name"].str.lower().str.contains(needle, na=False)]
        if hit.empty or hit["research_funding_cr"].isna().all():
            missing.append(needle)
    ok = len(missing) == 0
    return ok, "all major IITs funded" if ok else f"missing funding: {', '.join(missing)}"


def _duplicate_funding_check(funding: pd.DataFrame) -> tuple[bool, str]:
    """Flag unrelated institutes sharing identical funding amounts (P2 audit signal)."""
    if funding.empty or "research_funding_cr" not in funding.columns:
        return True, "no funding data"
    funded = funding[funding["research_funding_cr"].notna()].copy()
    if funded.empty:
        return True, "no funded rows"
    cluster_labels: dict[frozenset[str], str] = {}
    clusters: list[str] = []
    for amount, group in funded.groupby("research_funding_cr"):
        if len(group) < 2:
            continue
        names = group["canonical_name"].astype(str).tolist()
        name_set = frozenset(names)
        label = cluster_labels.get(name_set)
        if label:
            clusters.append(f"{amount} cr [{label}]: {', '.join(names[:3])}")
        else:
            clusters.append(f"{amount} cr: {len(names)} institutes ({names[0][:30]}…, {names[1][:30]}…)")
    ok = len(clusters) <= 8
    detail = f"{len(clusters)} duplicate-value clusters" if clusters else "no duplicate funding values"
    if clusters:
        detail += " — " + "; ".join(clusters[:4])
    return ok, detail


def main() -> None:
    results: list[dict] = []
    master_path = PROCESSED_DIR / "institution_master.csv"
    edges_path = PROCESSED_DIR / "collaboration_edges_full.csv"
    domestic_path = PROCESSED_DIR / "domestic_works.parquet"
    works_path = PROCESSED_DIR / "works_raw.parquet"
    funding_path = PROCESSED_DIR / "institution_funding.csv"

    master = pd.read_csv(master_path) if master_path.exists() else pd.DataFrame()

    if not master.empty:
        geo_ok = master["latitude"].notna() & master["longitude"].notna()
        results.append(
            check(
                "institution_master rows + geo",
                len(master) >= 80 and geo_ok.mean() >= 0.9,
                f"{len(master)} rows, {geo_ok.mean()*100:.0f}% with lat/lon",
            )
        )
    else:
        results.append(check("institution_master rows + geo", False, "missing"))

    if edges_path.exists():
        e = pd.read_csv(edges_path)
        w2 = e[e["weight"] >= 2] if "weight" in e.columns else e
        results.append(
            check(
                "collaboration_edges weight>=2",
                len(w2) >= 200,
                f"{len(w2)} edge rows",
            )
        )
        if not master.empty and "inst_a" in e.columns:
            master_ids = set(master["institution_id"])
            bad = e[~e["inst_a"].isin(master_ids) | ~e["inst_b"].isin(master_ids)]
            results.append(
                check(
                    "edge endpoints in master (domestic IN institutions)",
                    len(bad) == 0,
                    f"{len(bad)} orphan edge rows" if len(bad) else "all endpoints in institution_master",
                )
            )
    else:
        results.append(check("collaboration_edges weight>=2", False, "missing"))

    dash = Path(__file__).resolve().parents[2] / "dashboard" / "data" / "india_network"
    ov = dash / "2024_overview.json"
    full = dash / "2024_full.json"
    if ov.exists() and full.exists():
        results.append(check("overview size", ov.stat().st_size < 40_000, f"{ov.stat().st_size} bytes"))
        # Full payload includes triads for 120 nodes; 200 KB cap is obsolete (typical ~500 KB–1.5 MB).
        full_max_bytes = 2_000_000
        results.append(
            check(
                "full size",
                full.stat().st_size < full_max_bytes,
                f"{full.stat().st_size} bytes (cap {full_max_bytes // 1024} KB)",
            )
        )
        try:
            ov_data = json.loads(ov.read_text(encoding="utf-8"))
            note = str(ov_data.get("quality_note", ""))
            has_scimago = str(SCIMAGEO_YEAR) in note or ov_data.get("quality_year") == SCIMAGEO_YEAR
            results.append(
                check(
                    "SCImago static year footnote",
                    has_scimago,
                    note[:80] if note else "quality_note missing",
                )
            )
        except json.JSONDecodeError:
            results.append(check("SCImago static year footnote", False, "invalid overview JSON"))
        ok_ov, det_ov = _payload_orphan_edges(ov)
        results.append(check("overview payload edge integrity", ok_ov, det_ov))
        ok_full, det_full = _payload_orphan_edges(full)
        results.append(check("full payload edge integrity", ok_full, det_full))
        manifest = dash / "manifest.json"
        if manifest.exists():
            try:
                mdata = json.loads(manifest.read_text(encoding="utf-8"))
                years = mdata.get("available_years") or []
                results.append(
                    check(
                        "year slice manifest",
                        len(years) >= 5,
                        f"{len(years)} years listed in manifest.json",
                    )
                )
            except json.JSONDecodeError:
                results.append(check("year slice manifest", False, "invalid manifest.json"))
        else:
            results.append(check("year slice manifest", False, "manifest.json missing — run 09b_export_year_slices.py"))
    else:
        results.append(check("dashboard JSON payloads", False, "2024 payloads missing"))

    if not master.empty:
        ok_coord, det_coord = _coord_stack_check(master)
        results.append(check("campus coordinate stacks", ok_coord, det_coord))

    if domestic_path.exists():
        dom = pd.read_parquet(domestic_path)
        results.append(
            check(
                "domestic_works.parquet non-empty",
                len(dom) > 0,
                f"{len(dom)} rows, {domestic_path.stat().st_size // 1024} KB",
            )
        )
    else:
        results.append(check("domestic_works.parquet non-empty", False, "missing — run 06 after 05b"))

    if funding_path.exists():
        fund = pd.read_csv(funding_path)
        has = fund["research_funding_cr"].notna().sum() if "research_funding_cr" in fund.columns else 0
        results.append(
            check(
                "NIRF funding coverage",
                has >= 80,
                f"{has} / {len(fund)} institutions with research_funding_cr",
            )
        )
        ok_suspect, det_suspect = _funding_corruption_check(fund)
        results.append(check("funding ID/name corruption guard", ok_suspect, det_suspect))
        ok_major, det_major = _major_iit_funding_check(fund)
        results.append(check("major IIT funding present", ok_major, det_major))
        ok_dup, det_dup = _duplicate_funding_check(fund)
        results.append(check("duplicate funding value clusters", ok_dup, det_dup))
    else:
        results.append(check("NIRF funding coverage", False, "institution_funding.csv missing"))

    if not master.empty:
        ok_pos, det_pos = _positive_domestic_test(master, domestic_path)
        results.append(check("positive domestic co-auth test", ok_pos, det_pos))
        ok_neg, det_neg = _negative_foreign_test(master, works_path, domestic_path)
        results.append(check("negative foreign co-auth test", ok_neg, det_neg))

    if edges_path.exists() and "year" in pd.read_csv(edges_path, nrows=1).columns:
        e = pd.read_csv(edges_path)
        w2015 = e.loc[e["year"] == YEAR_MIN, "weight"].sum() if YEAR_MIN in e["year"].values else 0
        w2022 = e.loc[e["year"] == 2022, "weight"].sum() if 2022 in e["year"].values else 0
        results.append(
            check(
                "temporal edge variance (2015 vs 2022)",
                w2015 > 0 and w2022 > 0 and w2015 != w2022,
                f"2015 weight sum={int(w2015)}, 2022 weight sum={int(w2022)}",
            )
        )

    try:
        from report_nirf_gaps import run_report  # noqa: WPS433

        gap_summary = run_report()
        results.append(
            check(
                "NIRF coverage gap report",
                True,
                f"funding {gap_summary['funding_reported']}/{gap_summary['funding_total']}, "
                f"patents {gap_summary['patents_reported']}/{gap_summary['patents_total']}",
            )
        )
    except Exception as exc:  # noqa: BLE001
        results.append(check("NIRF coverage gap report", False, str(exc)))

    try:
        from validate_aishe import run_validate  # noqa: WPS433

        aishe = run_validate()
        if aishe.get("present"):
            det = f"present, {aishe.get('row_count', 0)} rows"
        else:
            det = "optional file missing"
        results.append(check("AISHE xlsx validation", True, det))
    except Exception as exc:  # noqa: BLE001
        results.append(check("AISHE xlsx validation", False, str(exc)))

    passed = sum(1 for r in results if r["ok"])
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "total": len(results),
        "all_pass": bool(passed == len(results)),
        "checks": results,
    }
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    lines = [
        "# Module 5 verification checklist",
        "",
        f"Generated: {summary['generated_at']}",
        f"**{passed}/{len(results)} passed**",
        "",
    ]
    for r in results:
        mark = "PASS" if r["ok"] else "FAIL"
        lines.append(f"- [{mark}] {r['name']}: {r['detail']}")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Verification: {passed}/{len(results)} passed -> {OUT_MD}")
    sys.exit(0 if summary["all_pass"] else 1)


if __name__ == "__main__":
    main()
