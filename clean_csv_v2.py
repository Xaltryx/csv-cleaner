import csv
from pathlib import Path
import sys
import pandas as pd


def load_csv(file_name):
    file_path = Path(file_name).resolve()
    if not file_path.exists():
        sys.exit(f"Error: file '{file_name}' not found.")
    with open(file_path, encoding="utf-8-sig") as csv_file:
        csv_reader = pd.read_csv(csv_file)
        return csv_reader

def strip_whitespace(csv_data_frame):
    def strip_col(col):
        if col.dtype == 'object' or col.dtype == 'str':
            return col.str.strip()
        else:
            return col
    return csv_data_frame.apply(strip_col)


def flag_bad_values(df):
    bad_words = ["ERROR", "UNKNOWN", "NULL", "N/A"]
    mask = df.apply(lambda col: col.str.upper().isin(bad_words) if (col.dtype == 'object' or str(col.dtype) == 'str') else False).any(axis=1)
    flagged = df[mask].copy()
    clean = df[~mask].copy()
    flagged["error"] = "contains ERROR/UNKNOWN/NULL/N/A"
    return flagged, clean


def flag_missing_values(flagged,cleaned):
    new_clean = cleaned[~cleaned.isna().any(axis=1)].copy()
    new_flagged = cleaned[cleaned.isna().any(axis=1)].copy()
    error_messages = new_flagged.isna().apply(
        lambda row: f"missing values in: {', '.join(row[row == True].index)}", axis=1
    )
    new_flagged.loc[:, "error"] = error_messages
    new_flagged = pd.concat([flagged, new_flagged], ignore_index=True)
    return new_flagged, new_clean


def remove_duplicates(flagged_rows, clean_rows, column_id):
    if column_id:
        new_clean = clean_rows.drop_duplicates(subset=[column_id], keep="first").copy()
        new_flagged = clean_rows[clean_rows.duplicated(subset=[column_id], keep="first")].copy()
        error_messages = new_flagged.apply(
            lambda row: f"duplicate id: {row[column_id]}", axis=1
        )
        new_flagged.loc[:, "error"] = error_messages
    else:
        new_clean = clean_rows.drop_duplicates(keep="first").copy()
        new_flagged = clean_rows[clean_rows.duplicated(keep="first")].copy()
        if not new_flagged.empty:
            new_flagged["error"] = "duplicate row"

    new_flagged = pd.concat([flagged_rows, new_flagged], ignore_index=True)

    return new_flagged, new_clean


def save_csv(csv_good_data, csv_bad_data, file_name):
    cleaned_filename = file_name.removesuffix(".csv") + "_cleaned_data.csv"
    flagged_filename = file_name.removesuffix(".csv") + "_flagged_data.csv"
    csv_good_data.to_csv(cleaned_filename, index=False, encoding="utf-8-sig")
    csv_bad_data.to_csv(flagged_filename, index=False, encoding="utf-8-sig")
    return f"Saved {flagged_filename}, {cleaned_filename} successfully"

def clean(filename, id_column):
    content = load_csv(filename)
    if content.empty :
        sys.exit("Error: file is empty.")

    if id_column and id_column not in content.columns:
        sys.exit(f"Error: column '{id_column}' not found. Available: {content.columns.tolist()}")  # ✅

    remove_whitespace = strip_whitespace(content)
    bad_values, good_values = flag_bad_values(remove_whitespace)
    bad_values, good_values = flag_missing_values(bad_values, good_values)
    bad_values, good_values = remove_duplicates(bad_values, good_values, id_column)
    return save_csv(good_values, bad_values, filename)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        id_column = sys.argv[2] if len(sys.argv) > 2 else ""
    except IndexError:
        filename = input("Please enter the name of the file: ")
        id_column = input("Enter ID column for duplicate check (or press Enter to use full row): ").strip()

    clean(filename, id_column)
