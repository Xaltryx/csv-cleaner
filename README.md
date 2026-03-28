# CSV Cleaner CLI

A command-line tool that automatically cleans messy CSV files — flagging bad values, missing fields, and duplicates, then splitting the data into a clean file and a flagged file with error reasons.

---

## What It Does

Given a raw CSV file, it produces two output files:

- `yourfile_cleaned_data.csv` — rows that passed all checks
- `yourfile_flagged_data.csv` — rows that failed, with an `error` column explaining why

**Checks performed:**
- Strips leading/trailing whitespace from all values
- Flags rows containing `ERROR`, `UNKNOWN`, or `NULL`
- Flags rows with missing (empty) values, naming the affected columns
- Flags duplicate rows by a specified ID column — or by full row if no ID column is given

---

## Usage

```bash
python clean_csv.py <filename> [id_column]
```

**With arguments:**
```bash
python clean_csv.py customers.csv customer_id
```

**Interactive mode** (no arguments):
```bash
python clean_csv.py
# Please enter the name of the file: customers.csv
# Enter ID column for duplicate check (or press Enter to use full row): customer_id
```

The `id_column` argument is optional. If omitted or left blank, duplicate detection compares the entire row.

---

## Example

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

## Requirements

- Python 3.9+
- No external dependencies — standard library only

---

## Error Handling

| Situation | Behavior |
|---|---|
| File is empty | Exits with a clear message |
| ID column doesn't exist | Exits and lists available columns |
| File not found | Python raises a clean `FileNotFoundError` |

---

## Author

Built by [Xaltryx](https://github.com/Xaltryx) — Python automation tools for real business workflows.
