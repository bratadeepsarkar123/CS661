#!/usr/bin/env python3
"""Resilient overnight supervisor — never stops on a single step failure.

Runs up to 8 hours:
  - Keeps OpenAlex fetch (05) alive
  - Runs pipeline steps individually (failures logged, loop continues)
  - Backs off on API limits, retries fetch after cooldown

Logs: data/logs/supervisor.log
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "data" / "logs"
LOG_PATH = LOG_DIR / "supervisor.log"
STATUS_PATH = LOG_DIR / "supervisor_status.json"
PIPELINE_STATE = LOG_DIR / "pipeline_state.json"
SCRIPTS = ROOT / "scripts" / "india_network"
WORKS_RAW = ROOT / "data" / "processed" / "works_raw.parquet"


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def write_status(**fields) -> None:
    payload = {"updated_at": datetime.now(timezone.utc).isoformat(), **fields}
    STATUS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_step(name: str, cmd: list[str], timeout: int | None = None, extra_env: dict | None = None) -> bool:
    log(f"STEP {name} ...")
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        if proc.stdout.strip():
            for line in proc.stdout.strip().splitlines()[-8:]:
                log(f"  {line}")
        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "unknown error").strip().splitlines()
            log(f"STEP {name} FAILED (exit {proc.returncode}): {err[-1] if err else '?'}")
            return False
        log(f"STEP {name} OK")
        return True
    except subprocess.TimeoutExpired:
        log(f"STEP {name} TIMEOUT after {timeout}s — continuing")
        return False
    except Exception as exc:
        log(f"STEP {name} ERROR: {exc}")
        return False


def fetch_is_running() -> bool:
    try:
        out = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
                "Where-Object { $_.CommandLine -match '05_fetch_openalex_works' } | "
                "Select-Object -First 1 -ExpandProperty ProcessId",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
            timeout=30,
        )
        return bool(out.stdout.strip())
    except Exception:
        return False


def stop_fetch() -> None:
    try:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
                "Where-Object { $_.CommandLine -match '05_fetch_openalex_works' } | "
                "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }",
            ],
            cwd=ROOT,
            timeout=30,
        )
        log("Stopped fetch process (free disk/RAM for assemble)")
    except Exception as exc:
        log(f"stop_fetch warning: {exc}")


def start_fetch(full_master: bool = False) -> None:
    cmd = [sys.executable, str(SCRIPTS / "05_fetch_openalex_works.py")]
    if not full_master:
        cmd.extend(["--pilot-top", "30"])
    log(f"Starting OpenAlex fetch (05) scope={'full-master' if full_master else 'pilot-30'}...")
    subprocess.Popen(
        cmd,
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def pilot_progress(full_master: bool = False) -> tuple[int, int]:
    try:
        cmd = [sys.executable, str(SCRIPTS / "openalex_progress.py")]
        if full_master:
            cmd.append("--full-master")
        else:
            cmd.extend(["--pilot-top", "30"])
        out = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        m = re.search(r"Complete:\s*(\d+)/(\d+)", out.stdout)
        if m:
            return int(m.group(1)), int(m.group(2))
    except Exception as exc:
        log(f"Progress check failed: {exc}")
    return 0, 120 if full_master else 30


def cache_file_count() -> int:
    cache = ROOT / "data" / "cache" / "openalex"
    if not cache.is_dir():
        return 0
    return sum(1 for _ in cache.glob("works_*.json"))


def run_pipeline_pass(
    memory: str = "low", heavy: bool = True, full_master: bool = False
) -> dict[str, bool]:
    py = sys.executable
    mem_env = {"INDIA_ETL_MEMORY": memory}
    results: dict[str, bool] = {}
    steps: list[tuple[str, list[str], int]] = [
        ("03a", [py, str(SCRIPTS / "03a_enrich_institution_master.py")], 300),
        ("07", [py, str(SCRIPTS / "07_join_scimago_quality.py")], 300),
    ]
    assemble_args = ["--memory", memory]
    if not full_master:
        assemble_args.extend(["--pilot-top", "30"])
    if heavy:
        steps.extend(
            [
                (
                    "05b",
                    [py, str(SCRIPTS / "05b_assemble_works_from_cache.py"), *assemble_args],
                    7200 if memory == "high" else 5400,
                ),
                ("06", [py, str(SCRIPTS / "06_build_domestic_edges.py")], 900),
            ]
        )
    else:
        log("SKIP 05b/06 (lightweight pass — laptop-friendly; cache unchanged)")

    steps.extend(
        [
            ("04", [py, str(SCRIPTS / "04_feasibility_domestic_edges.py")], 120),
        ]
    )
    funding_csv = ROOT / "data" / "raw" / "nirf_research_projects.csv"
    if funding_csv.exists():
        steps.extend(
            [
                ("01d", [py, str(SCRIPTS / "01d_prepare_nirf_funding.py")], 300),
                ("08", [py, str(SCRIPTS / "08_join_nirf_funding.py")], 300),
            ]
        )
    steps.append(("09", [py, str(SCRIPTS / "09_export_payloads.py"), "--year", "0"], 300))
    steps.append(("09b", [py, str(SCRIPTS / "09b_export_year_slices.py")], 600))
    if heavy:
        steps.append(("10_verify", [py, str(SCRIPTS / "10_verification_checklist.py")], 120))
    for name, cmd, timeout in steps:
        results[name] = run_step(name, cmd, timeout=timeout, extra_env=mem_env)

    # Copy to dashboard — never fatal
    try:
        src = ROOT / "public" / "india_network"
        dst = ROOT / "dashboard" / "data" / "india_network"
        dst.mkdir(parents=True, exist_ok=True)
        for f in src.glob("*"):
            if f.is_file():
                (dst / f.name).write_bytes(f.read_bytes())
        log("STEP copy dashboard OK")
        results["copy"] = True
    except Exception as exc:
        log(f"STEP copy dashboard FAILED: {exc}")
        results["copy"] = False

    return results


def should_run_heavy(
    memory: str, cache_count: int, marathon: bool = False, cap_resources: bool = False
) -> bool:
    """Incremental assemble. Disabled when cap_resources (user at desk)."""
    if cap_resources:
        return False

    if memory == "high" or marathon:
        state: dict = {}
        if PIPELINE_STATE.exists():
            try:
                state = json.loads(PIPELINE_STATE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        last_cache = int(state.get("cache_at_last_heavy", 0))
        if last_cache == 0:
            return False
        delta = cache_count - last_cache
        threshold = 600 if marathon else 400
        if delta >= threshold:
            log(f"Heavy pipeline: cache grew +{delta} (threshold {threshold})")
            return True
        return False

    state: dict = {}
    if PIPELINE_STATE.exists():
        try:
            state = json.loads(PIPELINE_STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    last_cache = int(state.get("cache_at_last_heavy", 0))
    if last_cache == 0:
        log(
            "SKIP 05b/06 — laptop mode (no assemble baseline yet; "
            "run start_overnight.ps1 when idle)"
        )
        return False

    delta = cache_count - last_cache
    if delta >= 400:
        log(f"Heavy pipeline (low mode): cache grew +{delta} since last assemble")
        return True

    if not WORKS_RAW.exists():
        log("SKIP 05b/06 — works_raw.parquet missing; defer assemble to overnight")
    return False


def save_pipeline_state(cache_count: int, heavy: bool) -> None:
    prev = 0
    if PIPELINE_STATE.exists():
        try:
            prev = int(json.loads(PIPELINE_STATE.read_text(encoding="utf-8")).get("cache_at_last_heavy", 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    new_cache = cache_count if heavy else max(prev, cache_count)
    PIPELINE_STATE.write_text(
        json.dumps(
            {
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "cache_at_last_heavy": new_cache,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=float, default=8.0)
    parser.add_argument("--watch-sec", type=int, default=300)
    parser.add_argument("--pipeline-sec", type=int, default=1800)
    parser.add_argument("--stall-min", type=float, default=20.0)
    parser.add_argument(
        "--memory",
        choices=("low", "high"),
        default=os.environ.get("INDIA_ETL_MEMORY", "low"),
        help="low=RAM-safe (recommended on 12GB); high=only if ETL_RAM_CAP_MB>=8192",
    )
    parser.add_argument(
        "--full-master",
        action="store_true",
        help="Fetch/assemble all 120 master institutions (not pilot-30 only)",
    )
    parser.add_argument(
        "--marathon",
        action="store_true",
        help="Run until deadline: no early exit; chain fetch->assemble->filter->export->verify",
    )
    parser.add_argument(
        "--cap-resources",
        action="store_true",
        help="User at desk: fetch only, no incremental 05b/06; slower API pacing",
    )
    args = parser.parse_args()
    full_master = args.full_master
    marathon = args.marathon
    cap_resources = args.cap_resources or os.environ.get("RESOURCE_CAP", "").lower() in {
        "active",
        "1",
        "true",
        "yes",
    }

    deadline = time.time() + args.hours * 3600
    last_pipeline = 0.0
    last_cache = -1
    stall_since: float | None = None
    api_cooldown_until = 0.0
    nirf_scrape_done = False
    fetch_complete_at: float | None = None
    final_pipeline_runs = 0

    log(
        f"=== Supervisor started ({args.hours}h max, memory={args.memory}, "
        f"full_master={full_master}, marathon={marathon}, cap_resources={cap_resources}) ==="
    )
    write_status(
        state="running",
        hours=args.hours,
        memory_mode=args.memory,
        full_master=full_master,
        marathon=marathon,
        cap_resources=cap_resources,
    )

    run_step(
        "validate_cache",
        [sys.executable, str(SCRIPTS / "validate_openalex_cache.py"), *(["--full-master"] if full_master else ["--pilot-top", "30"])],
        timeout=600,
    )

    if not fetch_is_running():
        start_fetch(full_master=full_master)
    else:
        log("Fetch already running")

    if full_master and not nirf_scrape_done:
        funding_csv = ROOT / "data" / "raw" / "nirf_research_projects.csv"
        if funding_csv.exists():
            log("SKIP 01e — nirf_research_projects.csv already present")
            nirf_scrape_done = True
        else:
            ok = run_step(
                "01e_nirf_funding",
                [sys.executable, str(SCRIPTS / "01e_scrape_nirf_funding_from_pdfs.py")],
                timeout=7200,
            )
            nirf_scrape_done = ok

    count = cache_file_count()
    heavy = should_run_heavy(args.memory, count, marathon=marathon, cap_resources=cap_resources)
    log(f"Initial pipeline pass (heavy={heavy})...")
    run_pipeline_pass(args.memory, heavy=heavy, full_master=full_master)
    save_pipeline_state(count, heavy)
    last_pipeline = time.time()
    last_cache = count

    def run_final_chain() -> None:
        nonlocal final_pipeline_runs
        log("=== FINAL CHAIN: assemble + filter + export + verify + checkpoint ===")
        stop_fetch()
        time.sleep(3)
        run_pipeline_pass(args.memory, heavy=True, full_master=full_master)
        save_pipeline_state(cache_file_count(), True)
        run_step(
            "validate_final",
            [
                sys.executable,
                str(SCRIPTS / "validate_openalex_cache.py"),
                *(["--full-master"] if full_master else ["--pilot-top", "30"]),
            ],
            timeout=600,
        )
        run_step(
            "checkpoint",
            [
                "powershell",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(SCRIPTS / "checkpoint_data.ps1"),
                "-Label",
                f"marathon_pass_{final_pipeline_runs}",
            ],
            timeout=600,
        )
        final_pipeline_runs += 1

    while time.time() < deadline:
        done, total = pilot_progress(full_master=full_master)
        count = cache_file_count()

        if count == last_cache:
            if stall_since is None:
                stall_since = time.time()
        else:
            stall_since = None
            last_cache = count

        stall_min = ((time.time() - stall_since) / 60.0) if stall_since else 0.0
        log(f"Progress {done}/{total} | cache={count} files | stall={stall_min:.0f}min")

        write_status(
            institutions_done=done,
            institutions_total=total,
            cache_files=count,
            stall_minutes=round(stall_min, 1),
            fetch_running=fetch_is_running(),
            marathon=marathon,
            fetch_complete=fetch_complete_at is not None,
            cap_resources=cap_resources,
            final_runs=final_pipeline_runs,
        )

        if done >= total and fetch_complete_at is None:
            fetch_complete_at = time.time()
            log(f"FETCH COMPLETE {done}/{total} — starting final ETL chain")
            if fetch_is_running():
                log("Waiting for fetch process to exit naturally...")
            run_final_chain()

        if fetch_complete_at is not None and marathon:
            # Keep working until deadline: re-export + verify on schedule
            now = time.time()
            if now - last_pipeline >= args.pipeline_sec:
                log("Marathon post-fetch pass (re-export + verify)")
                run_pipeline_pass(args.memory, heavy=False, full_master=full_master)
                run_step(
                    "10_verify",
                    [sys.executable, str(SCRIPTS / "10_verification_checklist.py")],
                    timeout=180,
                )
                last_pipeline = now
            run_step("watch", [sys.executable, str(SCRIPTS / "watch_openalex_fetch.py")], timeout=60)
            time.sleep(args.watch_sec)
            continue

        if done >= total and not marathon:
            run_final_chain()
            log("=== COMPLETE (non-marathon exit) ===")
            write_status(state="complete", institutions_done=done, institutions_total=total)
            return

        now = time.time()
        if not fetch_is_running() and now >= api_cooldown_until:
            if stall_since and stall_min >= args.stall_min:
                log(f"Stall {stall_min:.0f}min — API limit likely. Cooldown 45min...")
                api_cooldown_until = now + 45 * 60
                stall_since = None
            else:
                start_fetch(full_master=full_master)

        if now - last_pipeline >= args.pipeline_sec:
            heavy = should_run_heavy(
                args.memory, count, marathon=marathon, cap_resources=cap_resources
            )
            log(f"Scheduled pipeline pass (heavy={heavy})")
            run_pipeline_pass(args.memory, heavy=heavy, full_master=full_master)
            save_pipeline_state(count, heavy)
            last_pipeline = now

        # Lightweight watch log
        run_step("watch", [sys.executable, str(SCRIPTS / "watch_openalex_fetch.py")], timeout=60)

        time.sleep(args.watch_sec)

    log("=== Deadline reached — final chain if not yet run ===")
    if fetch_complete_at is None:
        done, total = pilot_progress(full_master=full_master)
        if done >= total:
            run_final_chain()
    else:
        run_final_chain()
    run_step("morning_report", ["powershell", "-File", str(SCRIPTS / "morning_report.ps1")], timeout=300)
    write_status(state="deadline", cache_files=last_cache, final_runs=final_pipeline_runs)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Supervisor interrupted")
        write_status(state="interrupted")
    except Exception as exc:
        log(f"Supervisor crash: {exc}")
        write_status(state="crashed", error=str(exc))
        raise
