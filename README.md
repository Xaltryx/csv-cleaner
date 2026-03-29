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

## What's New in v2

- ✅ **`N/A` added** to bad value detection (both variants now flag `ERROR`, `UNKNOWN`, `NULL`, `N/A`)
- ✅ **Pandas variant** (`clean_csv_v2.py`) — full feature parity, vectorized for large files
- ✅ **Precise duplicate error messages** — error now includes the duplicate value, not just the column name
- ✅ **Precise missing-value errors** — names the exact affected columns per row
- ✅ **Full pytest coverage** — 5 tests for the pandas variant, 2 for stdlib

---

## Features

| Feature | `clean_csv.py` (stdlib) | `clean_csv_v2.py` (pandas) |
|---|:---:|:---:|
| Whitespace stripping | ✅ | ✅ |
| Bad value detection (`ERROR`, `UNKNOWN`, `NULL`, `N/A`) | ✅ | ✅ |
| Missing value detection (column-level reporting) | ✅ | ✅ |
| Duplicate detection (by ID column or full row) | ✅ | ✅ |
| Two clean output files | ✅ | ✅ |
| Vectorized performance | ❌ | ✅ |
| Handles large files efficiently | ⚠️ | ✅ |

---

## Requirements

- Python 3.9+
- `clean_csv.py` — stdlib only, zero dependencies
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

**Pandas variant — same interface:**
```bash
python clean_csv_v2.py customers.csv customer_id
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
004,Dave,dave@example.com,N/A
```

**Output: `customers_cleaned_data.csv`**
```
customer_id,name,email,status
001,Alice,alice@example.com,active
```

**Output: `customers_flagged_data.csv`**
```
customer_id,name,email,status,error
002,Bob,,active,"missing value in column: ['email']"
003,Carol,carol@example.com,NULL,contains ERROR/UNKNOWN/NULL/N/A
001,Alice,alice@example.com,active,duplicate id: 001
004,Dave,dave@example.com,N/A,contains ERROR/UNKNOWN/NULL/N/A
```

---

## How It Works

Each row passes through a sequential pipeline:

```
Load CSV → Strip Whitespace → Flag Bad Values → Flag Missing Values → Remove Duplicates → Save Outputs
```

| Step | What it does |
|---|---|
| **Load** | Reads the file with UTF-8 BOM support for Excel compatibility |
| **Strip whitespace** | Trims all leading/trailing spaces from every string cell |
| **Flag bad values** | Case-insensitive match against `ERROR`, `UNKNOWN`, `NULL`, `N/A` |
| **Flag missing values** | Detects empty cells; records the exact affected column names |
| **Remove duplicates** | Routes second occurrences to flagged file with the duplicate value in the error reason |
| **Save** | Writes `_cleaned_data.csv` and `_flagged_data.csv` with UTF-8 BOM encoding |

> **Pipeline note:** A row exits at its first failure. A bad-value row is never also checked for duplicates. Error reasons are always unambiguous.

---

## Error Handling

| Situation | Behavior |
|---|---|
| File not found | Exits with a clear message |
| File is empty | Exits with a clear message |
| ID column doesn't exist | Exits and lists available columns |
| Row has bad value AND missing field | Flagged at bad-value step (pipeline order) |

---

## Project Structure

```
csv-cleaner/
├── clean_csv.py          # Stdlib-only cleaner — zero dependencies
├── clean_csv_v2.py       # Pandas-powered variant — vectorized, handles large files
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

**Test coverage — `test_clean_csv_v2.py`:**

| Test | What it verifies |
|---|---|
| `test_strip_whitespace` | String cells stripped; numeric columns untouched |
| `test_flag_bad_value` | All 3 bad rows caught; clean list is empty |
| `test_load_csv` | File loads as a non-empty DataFrame *(requires `customers.csv`)* |
| `test_flag_missing_values` | 2 NaN rows flagged; 1 clean row passes |
| `test_remove_duplicates` | Full-row and ID-column dedup both verified across 4 scenarios |

> **Note:** `test_load_csv` expects a `customers.csv` file in the working directory.

---

## Choosing a Variant

| Use case | Recommended |
|---|---|
| Simple scripts, no extra dependencies | `clean_csv.py` |
| Large files (10k+ rows) | `clean_csv_v2.py` |
| Integrating into a pandas pipeline | `clean_csv_v2.py` |
| Lightweight / auditing environments | `clean_csv.py` |

Both variants produce **identical output files** and accept the **same CLI arguments**.

---

## Author

Built by [Xaltryx](https://github.com/Xaltryx) — Python automation tools for real business workflows.
