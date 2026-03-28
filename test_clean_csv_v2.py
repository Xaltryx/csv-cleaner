# test_clean_csv_v2.py
import pandas as pd
from clean_csv_v2 import strip_whitespace
from clean_csv_v2 import flag_bad_values
from clean_csv_v2 import load_csv

def test_strip_whitespace():
    dirty = pd.DataFrame([{"name": "  Youssef  ", "age": 15}])
    cleaned = strip_whitespace(dirty)
    assert cleaned["name"][0] == "Youssef"
    assert cleaned["age"][0] == 15

def test_flag_bad_value():
    dirty = pd.DataFrame([
        {"name": "Youssef", "age": "null"},
        {"name": "ERROR", "age": "25"},
        {"name": "Youssef", "age": "UNKNOWN"},
    ])
    flagged, cleaned = flag_bad_values(dirty)
    assert len(cleaned) == 0
    assert len(flagged) == 3  # all 3 are bad

def test_load_csv():
    data = load_csv('customers.csv')
    assert len(data) != 0
    assert type(data) == pd.DataFrame