#!/usr/bin/env python3
"""Overnight agent monitor — 5 min cycles, recovery actions, morning summary."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "data" / "logs"
MONITOR_LOG = LOG_DIR / "agent_monitor.log"
SUPERVISOR_LOG = LOG_DIR / "supervisor.log"
STATUS_PATH = LOG_DIR / "supervisor_status.json"
SUMMARY_PATH = LOG_DIR / "morning_agent_summary.txt"
SCRIPTS = ROOT / "scripts" / "india_network"
CACHE = ROOT / "data" / "cache" / "openalex"

MANUAL_STEPS: dict[str, tuple[list[str], int]] = {
    "03a": ([str(SCRIPTS / "03a_enrich_institution_master.py")], 600),
    "07": ([str(SCRIPTS / "07_join_scimago_quality.py")], 600),
    "05b": ([str(SCRIPTS / "05b_assemble_works_from_cache.py"), "--pilot-top", "30", "--memory", "low"], 7200),
    "06": ([str(SCRIPTS / "06_build_domestic_edges.py")], 1200),
    "04": ([str(SCRIPTS / "04_feasibility_domestic_edges.py")], 300),
    "09": ([str(SCRIPTS / "09_export_payloads.py"), "--year", "0"], 600),
}

manual_attempted: set[str] = set()
last_cache_count = -1
last_cache_change = time.time()


def amlog(msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with MONITOR_LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def read_status() -> dict | None:
    if not STATUS_PATH.is_file():
        return None
    try:
        return json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def cache_file_count() -> int:
    if not CACHE.is_dir():
        return 0
    return sum(1 for _ in CACHE.glob("works_*.json"))


def process_running(pattern: str) -> bool:
    ps = (
        "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
        f"Where-Object {{ $_.CommandLine -match '{pattern}' }} | "
        "Select-Object -First 1 -ExpandProperty ProcessId"
    )
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=45,
        )
        return bool(out.stdout.strip())
    except Exception:
        return False


def start_supervisor() -> None:
    amlog("ACTION: Restart overnight_supervisor.py (memory=low)")
    subprocess.Popen(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Start-Process python -ArgumentList "
            f"'scripts/india_network/overnight_supervisor.py --hours 4 --pipeline-sec 1800 --memory low' "
            f"-WorkingDirectory '{ROOT}' -WindowStyle Hidden",
        ],
        cwd=ROOT,
    )


def start_fetch() -> None:
    amlog("ACTION: Restart 05_fetch_openalex_works.py --pilot-top 30")
    subprocess.Popen(
        [sys.executable, str(SCRIPTS / "05_fetch_openalex_works.py"), "--pilot-top", "30"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def pilot_progress() -> tuple[int, int, str]:
    try:
        out = subprocess.run(
            [sys.executable, str(SCRIPTS / "openalex_progress.py"), "--pilot-top", "30"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=180,
        )
        text = out.stdout or ""
        m = re.search(r"Complete:\s*(\d+)/(\d+)", text)
        if m:
            return int(m.group(1)), int(m.group(2)), text
    except Exception as exc:
        amlog(f"Progress check failed: {exc}")
    return 0, 30, ""


def api_wait_ok(stall_min: float, fetch_running: bool) -> bool:
    return stall_min >= 25 and not fetch_running


def manual_step_if_needed() -> None:
    if not SUPERVISOR_LOG.is_file():
        return
    tail = SUPERVISOR_LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-200:]
    failed = [m.group(1) for line in tail for m in [re.search(r"STEP (\S+) FAILED", line)] if m]
    from collections import Counter

    for step, count in Counter(failed).items():
        if count < 3 or step in manual_attempted or step not in MANUAL_STEPS:
            continue
        manual_attempted.add(step)
        cmd, timeout = MANUAL_STEPS[step]
        amlog(f"ACTION: Manual retry STEP {step} (timeout {timeout}s)")
        out_f = LOG_DIR / f"manual_{step}_out.txt"
        err_f = LOG_DIR / f"manual_{step}_err.txt"
        try:
            proc = subprocess.run(
                [sys.executable, *cmd],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            out_f.write_text(proc.stdout or "", encoding="utf-8")
            err_f.write_text(proc.stderr or "", encoding="utf-8")
            amlog(f"Manual STEP {step} exit={proc.returncode}")
        except subprocess.TimeoutExpired:
            amlog(f"Manual STEP {step} TIMEOUT after {timeout}s")
        except Exception as exc:
            amlog(f"Manual STEP {step} ERROR: {exc}")


def write_morning_summary(start_time: datetime) -> None:
    done, total, progress_out = pilot_progress()
    count = cache_file_count()
    feas_path = ROOT / "data" / "processed" / "feasibility_report.md"
    feas = "missing"
    if feas_path.is_file():
        feas = " | ".join(feas_path.read_text(encoding="utf-8", errors="replace").splitlines()[:20])
    dash_ts: list[str] = []
    for d in (ROOT / "dashboard" / "data" / "india_network", ROOT / "public" / "india_network"):
        if d.is_dir():
            for f in sorted(d.iterdir()):
                if f.is_file():
                    ts = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    dash_ts.append(f"{f.name}: {ts}")
    st = read_status()
    state = st.get("state", "unknown") if st else "unknown"
    manual = (
        "Manual retries: " + ", ".join(sorted(manual_attempted))
        if manual_attempted
        else "None required by monitor."
    )
    body = f"""Morning agent summary — generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Monitor ran from {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Supervisor state: {state}

Institutions complete: {done} / {total}
OpenAlex cache works_*.json files: {count}

Feasibility (feasibility_report.md): {feas}

Dashboard / public JSON timestamps:
{chr(10).join(dash_ts) if dash_ts else '(none)'}

Progress snapshot:
{progress_out}

Manual steps / notes:
{manual}
"""
    SUMMARY_PATH.write_text(body, encoding="utf-8")
    amlog(f"Wrote morning summary -> {SUMMARY_PATH}")


def main() -> None:
    global last_cache_count, last_cache_change
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=float, default=8.0)
    parser.add_argument("--cycle-sec", type=int, default=300)
    args = parser.parse_args()

    deadline = time.time() + args.hours * 3600
    start_time = datetime.now()
    last_cache_count = cache_file_count()
    last_cache_change = time.time()

    amlog(f"=== Agent monitor started (max {args.hours}h, cycle {args.cycle_sec}s) baseline_cache={last_cache_count} ===")

    while time.time() < deadline:
        cycle_start = time.time()
        sup_tail = ""
        if SUPERVISOR_LOG.is_file():
            sup_tail = " | ".join(SUPERVISOR_LOG.read_text(encoding="utf-8", errors="replace").splitlines()[-5:])
        st = read_status()
        st_line = f"state={st.get('state')} updated={st.get('updated_at')}" if st else "no status json"
        amlog(f"CHECK supervisor: {st_line} | tail: {sup_tail or 'empty'}")

        if not process_running("overnight_supervisor"):
            start_supervisor()
            time.sleep(15)

        done, total, _ = pilot_progress()
        count = cache_file_count()
        if count != last_cache_count:
            last_cache_count = count
            last_cache_change = time.time()
        stall_min = (time.time() - last_cache_change) / 60.0
        fetch_run = process_running("05_fetch_openalex_works")
        amlog(
            f"PROGRESS done={done}/{total} cache={count} stall={stall_min:.1f}min fetch_running={fetch_run}"
        )

        if done < 30 and not fetch_run:
            if api_wait_ok(stall_min, fetch_run):
                amlog(f"INFO: Cache stall {stall_min:.1f}min, fetch not running — API limit wait OK")
            else:
                start_fetch()

        manual_step_if_needed()

        if st and st.get("state") == "complete":
            amlog("STOP: supervisor state=complete")
            break
        if done >= 30:
            amlog("STOP: institutions_done=30")
            break

        elapsed = time.time() - cycle_start
        sleep_sec = max(10, args.cycle_sec - int(elapsed))
        time.sleep(sleep_sec)

    amlog("=== Agent monitor finishing (deadline or stop condition) ===")
    write_morning_summary(start_time)


if __name__ == "__main__":
    main()
