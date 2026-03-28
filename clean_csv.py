import csv
from pathlib import Path
import sys

def load_csv(file_name):
    file_path = Path(file_name).resolve().absolute()
    with open(file_path, encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        return list(csv_reader)

def strip_whitespace(csv_data_list):
    for row in csv_data_list:
        for key,value in row.items():
            row[key] = value.strip()
    return csv_data_list

def flag_bad_values(csv_data_list):
    flagged_rows = []
    clean_rows = []
    for row in csv_data_list:
        flagged = False
        for key, value in row.items():
            if value.upper() in ["ERROR", "UNKNOWN","NULL",]:
                flagged = True
                break

        if flagged:
            flagged_rows.append(row)
        else:
            clean_rows.append(row)

    for row in flagged_rows:
        row["error"] = f"contains ERROR/UNKNOWN/NULL"
    return flagged_rows, clean_rows

def flag_missing_values(flagged_rows, clean_rows):
    new_clean = []
    for row in clean_rows:
        missing = [key for key, value in row.items() if value == ""]
        if missing:
            row['error'] = f"missing value in column: {missing}"
            flagged_rows.append(row)
        else:
            new_clean.append(row)
    return flagged_rows, new_clean

def remove_duplicates(flagged_rows, clean_rows, column_id):
    new_clean = []
    seen = set()
    for row in clean_rows:
        key = row[column_id] if column_id else tuple(row.values())
        if key in seen:
            row["error"] = f"duplicate in column {column_id}"
            flagged_rows.append(row)
        else:
            new_clean.append(row)
            seen.add(key)
    return flagged_rows, new_clean

def save_csv(csv_good_data, csv_bad_data, file_name, field_names):
    cleaned_filename = file_name.removesuffix(".csv") + "_cleaned_data.csv"
    flagged_file_name = file_name.removesuffix(".csv") + "_flagged_data.csv"

    with open(cleaned_filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(csv_good_data)

    with open(flagged_file_name, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=field_names + ['error'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(csv_bad_data)

    return f"Saved {flagged_file_name}, {cleaned_filename} successfully"

def clean(filename, id_column):
    content = load_csv(filename)
    if not content:
        sys.exit("Error: file is empty.")

    fieldnames = list(content[0].keys())
    if id_column and id_column not in fieldnames:
        sys.exit(f"Error: column '{id_column}' not found. Available: {fieldnames}")

    remove_whitespace = strip_whitespace(content)
    bad_values, good_values = flag_bad_values(remove_whitespace)
    bad_values, good_values = flag_missing_values(bad_values, good_values)
    bad_values, good_values = remove_duplicates(bad_values, good_values, id_column)
    return save_csv(good_values, bad_values, filename, fieldnames)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        id_column = sys.argv[2] if len(sys.argv) > 2 else ""
    except IndexError:
        filename = input("Please enter the name of the file: ")
        id_column = input("Enter ID column for duplicate check (or press Enter to use full row): ").strip()

    clean(filename, id_column)
