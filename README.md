# 🧹 CSV Cleaner CLI

> Automatically clean messy CSV files — strip whitespace, flag bad values, catch missing fields, and remove duplicates — all in one command.

---

## Overview

Given any raw CSV file, **CSV Cleaner** produces two output files:

| Output File | Contents |
|---|---|
| `yourfile_cleaned_data.csv` | Rows that passed all checks |
| `yourfile_flagged_data.csv` | Rows that failed, with an `error` column explaining why |

No config files. No setup. Just point it at a CSV and go.

---

## Features

- ✂️ **Whitespace stripping** — Trims leading/trailing spaces from every cell
- 🚩 **Bad value detection** — Flags rows containing `ERROR`, `UNKNOWN`, `NULL`, or `N/A`
- ❓ **Missing value detection** — Flags rows with empty fields and names the affected columns
- 🔁 **Duplicate detection** — Flags duplicate rows by a specified ID column, or by full row if no ID is given
- 📁 **Two clean outputs** — Always produces a cleaned file and a flagged file, side by side

---

## Requirements

- Python 3.9+
- `clean_csv.py` — stdlib only, no dependencies
- `clean_csv_v2.py` — requires `pandas` (`pip install pandas`)

---

## Installation

```bash
git clone https://github.com/Xaltryx/csv-cleaner.git
cd csv-cleaner

# Only needed for the pandas variant
pip install pandas
```

---

## Usage

```bash
python clean_csv.py <filename> [id_column]
```

| Argument | Required | Description |
|---|---|---|
| `filename` | ✅ Yes | Path to the CSV file to clean |
| `id_column` | ❌ Optional | Column name to use for duplicate detection. Omit to compare full rows. |

### Examples

**Basic clean (full-row duplicate detection):**
```bash
python clean_csv.py customers.csv
```

**With ID column for smart duplicate detection:**
```bash
python clean_csv.py customers.csv customer_id
```

**Interactive mode (no arguments):**
```bash
python clean_csv.py
# > Please enter the name of the file: customers.csv
# > Enter ID column for duplicate check (or press Enter to use full row): customer_id
```

---

## Example Walkthrough

**Input: `customers.csv`**
```
customer_id,name,email,status
001,Alice,alice@example.com,active
002,Bob,,active
003,Carol,carol@example.com,NULL
001,Alice,alice@example.com,active
004,Dave,dave@example.com,active
```

**Output: `customers_cleaned_data.csv`**
```
customer_id,name,email,status
001,Alice,alice@example.com,active
004,Dave,dave@example.com,active
```

**Output: `customers_flagged_data.csv`**
```
customer_id,name,email,status,error
002,Bob,,active,"missing value in column: ['email']"
003,Carol,carol@example.com,NULL,contains ERROR/UNKNOWN/NULL
001,Alice,alice@example.com,active,duplicate id: 001
```

---

## How It Works

The cleaner runs each row through a pipeline of checks, in order:

```
Load CSV → Strip Whitespace → Flag Bad Values → Flag Missing Values → Remove Duplicates → Save Outputs
```

1. **Load** — Reads the file with UTF-8 BOM support for Excel compatibility
2. **Strip whitespace** — Applies `.str.strip()` across all string columns
3. **Flag bad values** — Case-insensitive match against `ERROR`, `UNKNOWN`, `NULL`, `N/A`
4. **Flag missing values** — Detects empty cells and records which columns are affected
5. **Remove duplicates** — Tracks seen keys; routes second occurrences to the flagged file with a reason
6. **Save** — Writes `_cleaned_data.csv` and `_flagged_data.csv` with UTF-8 BOM encoding

---

## Error Handling

| Situation | Behavior |
|---|---|
| File not found | Exits with a clear message |
| File is empty | Exits with a clear message |
| ID column doesn't exist in file | Exits and lists available columns |
| Row has bad value AND is a duplicate | Flagged for bad value first (pipeline order) |

---

## Project Structure

```
csv-cleaner/
├── clean_csv.py          # Main cleaner (stdlib only, no dependencies)
├── clean_csv_v2.py       # Pandas-based variant
├── test_clean_csv.py     # Unit tests for clean_csv.py
├── test_clean_csv_v2.py  # Unit tests for clean_csv_v2.py
└── README.md
```

---

## Running Tests

```bash
pip install pytest
pytest test_clean_csv.py -v
```

For the pandas variant:
```bash
pip install pytest pandas
pytest test_clean_csv_v2.py -v
```

> **Note:** `test_load_csv` in `test_clean_csv_v2.py` expects a `customers.csv` file in the working directory.

---

## Author

Built by [Xaltryx](https://github.com/Xaltryx) — Python automation tools for real business workflows.