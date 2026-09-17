#!/usr/bin/env python3
"""
task_logger.py - Scheduled Telemetry JSON Logger

Appends a telemetry entry {time, date, counter} to a JSON array file every
10 minutes. Resumes from the last entry if the file exists; otherwise creates
it and starts fresh. Runs until stopped with Ctrl+C.

Usage:
    python task_logger.py telemetry.json
    python task_logger.py                     # prompts for path
    python task_logger.py telemetry.json --interval 5   # quick test (seconds)
"""

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime

INTERVAL_SECONDS = 600  # 10 minutes
COUNTER_STEP = 10


def load_entries(path):
    """Return existing entries list, or [] if the file is missing/empty."""
    if not os.path.exists(path):
        print(f"[init] '{path}' not found -> creating new file.")
        save_entries(path, [])
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            print(f"[init] '{path}' is empty -> starting fresh.")
            return []
        data = json.loads(content)
        if not isinstance(data, list):
            raise ValueError("top-level JSON must be an array")
        return data
    except (json.JSONDecodeError, ValueError) as e:
        backup = f"{path}.corrupt.{datetime.now():%Y%m%d%H%M%S}.bak"
        shutil.copy2(path, backup)
        print(f"[warn] Invalid JSON ({e}). Backed up to '{backup}', starting fresh.")
        return []


def save_entries(path, entries):
    """Atomic write: write to temp file, then replace, so a crash never corrupts data."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def last_counter(entries):
    """Get counter from the last valid entry, else 0."""
    for entry in reversed(entries):
        if isinstance(entry, dict) and isinstance(entry.get("counter"), int):
            return entry["counter"]
    return 0


def log_entry(path, entries, counter):
    now = datetime.now()
    entry = {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "counter": counter,
    }
    entries.append(entry)
    save_entries(path, entries)
    print(f"[log] {entry['date']} {entry['time']}  counter={counter}")


def parse_args():
    parser = argparse.ArgumentParser(description="Scheduled telemetry JSON logger")
    parser.add_argument("path", nargs="?", help="Path to JSON file")
    parser.add_argument(
        "--interval", type=float, default=INTERVAL_SECONDS,
        help=f"Seconds between entries (default {INTERVAL_SECONDS})",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    path = args.path or input("Enter path to JSON file: ").strip()
    if not path:
        sys.exit("[error] No path provided.")

    entries = load_entries(path)
    counter = last_counter(entries)
    if entries:
        print(f"[init] Resuming from {len(entries)} entries, last counter={counter}")

    print(f"[run] Logging every {args.interval:g}s to '{path}'. Press Ctrl+C to stop.")

    # Schedule against a monotonic clock so intervals don't drift over time.
    next_run = time.monotonic()
    try:
        while True:
            counter += COUNTER_STEP
            log_entry(path, entries, counter)
            next_run += args.interval
            time.sleep(max(0.0, next_run - time.monotonic()))
    except KeyboardInterrupt:
        print(f"\n[stop] Stopped by user. Final counter={counter}, total entries={len(entries)}")


if __name__ == "__main__":
    main()