# Python Tasks

A collection of small, self-contained Python scripts. Each task lives in its own file, and sample outputs are stored in the `outputs/` folder.

```
.
├── task_ascii.py      # Name → ASCII sum → single digit (odd/even)
├── task_logger.py     # Scheduled JSON telemetry logger
├── task_pattern.py    # Star pattern for odd n >= 5
├── task_model.py      # (see Task 4 below)
├── outputs/           # Sample outputs for each task
└── README.md
```

---

## Prerequisites

- **Python 3.8+** (check with `python --version` or `python3 --version`)
- **No third-party packages.** All scripts use only the Python standard library (`argparse`, `json`, `os`, `shutil`, `sys`, `time`, `datetime`).

## Environment Setup

```bash
# 1. Clone or download the repository
git clone <repo-url>
cd <repo-folder>

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. No pip install needed (standard library only)
```

> On some systems use `python3` instead of `python`.

---

## Task 1: `task_ascii.py`, Name to Single Digit

**Description:** Takes a name, converts each letter (uppercased, non-letters ignored) to its ASCII value, sums them, then repeatedly adds the digits until a single digit remains. Finally reports whether that digit is **EVEN** or **ODD**.

**Run:**
```bash
python task_ascii.py
```

**Example:**
```
Enter your name: Sawan
S -> 83
A -> 65
W -> 87
A -> 65
N -> 78
Sum = 378
Digit sum: 3 + 7 + 8 = 18
Digit sum: 1 + 8 = 9

Final single digit for 'Sawan': 9 (ODD)
```

**Notes:** Empty input is rejected. Spaces, digits and symbols are skipped.

---

## Task 2: `task_logger.py`, Scheduled JSON Logger

**Description:** Appends a telemetry entry to a JSON file at a fixed interval (default **600 s / 10 min**). Each entry records the time, date and a counter that increases by **10** per entry.

```json
[
  { "time": "14:30:00", "date": "2026-09-17", "counter": 10 },
  { "time": "14:40:00", "date": "2026-09-17", "counter": 20 }
]
```

**Features:**
- Creates the file if it doesn't exist; starts fresh if it's empty.
- **Resumes** the counter from the last valid entry on restart.
- **Corrupt JSON** is backed up to `<file>.corrupt.<timestamp>.bak` before starting fresh.
- **Atomic writes** (temp file + replace) so a crash never corrupts the log.
- Drift-free scheduling using a monotonic clock.

**Run:**
```bash
# Path as argument, default 10-minute interval
python task_logger.py data.json

# Custom interval (e.g., every 5 seconds, useful for testing)
python task_logger.py data.json --interval 5

# No argument: the script prompts for the path
python task_logger.py

# Help
python task_logger.py --help
```

| Argument     | Required | Default | Description                  |
|--------------|----------|---------|------------------------------|
| `path`       | No       | prompt  | Path to the JSON log file    |
| `--interval` | No       | `600`   | Seconds between entries      |

Stop with **Ctrl+C**; the script prints the final counter and total entries.

---

## Task 3: `task_pattern.py`, Star Pattern

**Description:** Prints an `n`-row star pattern for an **odd integer n >= 5**: a left border of stars, a right-side triangle that grows to `n//2 + 1` stars and shrinks back, and a fully filled middle row. Invalid input is re-prompted.

**Run:**
```bash
python task_pattern.py
```

**Example (n = 5):**
```
Enter n: 5
 *     *
 *     **
 *********
 *     **
 *     *
```
