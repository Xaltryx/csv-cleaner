# test_clean_csv_v2.py
from clean_csv import strip_whitespace
from clean_csv import flag_bad_values

def test_strip_whitespace():
    dirty = [{"name": "  Youssef  ", "age": " 15"}]
    result = strip_whitespace(dirty)
    assert result[0]["name"] == "Youssef"
    assert result[0]["age"] == "15"

def test_flag_bad_value():
    dirty = [
        {"name": "Youssef", "age": "null"},
        {"name": "ERROR", "age": "25"},
        {"name": "Youssef", "age": "UNKNOWN"},
    ]
    flagged, cleaned = flag_bad_values(dirty)
    assert len(cleaned) == 0
    assert len(flagged) == 3  # all 3 are bad