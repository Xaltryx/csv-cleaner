import csv
from pathlib import Path
import sys


try:
    filename = sys.argv[1]
    id_column = sys.argv[2] if len(sys.argv) > 2 else ""
except IndexError:
    filename = input("Please enter the name of the file: ")
    id_column = input("Enter ID column for duplicate check (or press Enter to use full row): ").strip()

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
    for row in list(clean_rows):
        missing_value = []
        flagged = False
        for key,value in list(row.items()):
            if value == "":
                flagged = True
                missing_value.append(key)
        if flagged:
            clean_rows.remove(row)
            row['error'] = f"missing value in column: {missing_value}"
            flagged_rows.append(row)

    return flagged_rows, clean_rows

def remove_duplicates(flagged_rows, clean_rows, id_column):
    seen = set()
    for row in list(clean_rows):
        key = row[id_column] if id_column else tuple(row.values())
        if key in seen:
            clean_rows.remove(row)
            row["error"] = f"duplicate id: {id_column or 'full row'}"
            flagged_rows.append(row)
        else:
            seen.add(key)
    return flagged_rows, clean_rows

def save_csv(csv_good_data, csv_bad_data, filename, fieldnames):
    cleaned_filename = filename.removesuffix(".csv") + "_cleaned_data.csv"
    flagged_file_name = filename.removesuffix(".csv") + "_flagged_data.csv"

    with open(cleaned_filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(csv_good_data)

    with open(flagged_file_name, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames + ['error'], extrasaction='ignore')
        writer.writeheader()
        writer.writerows(csv_bad_data)

    return f"Saved {flagged_file_name}, {cleaned_filename} successfully"

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
print(save_csv(good_values, bad_values, filename, fieldnames))