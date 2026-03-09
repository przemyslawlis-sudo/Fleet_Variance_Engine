import pytest
import os
# Import processor.py and get_latest_budget function.
from src.processor import get_latest_budget

# Test 1.
# Code must crash if one file is at present. 
def test_get_latest_budget_fails_with_one_file(tmp_path):
    # Setup: Create a directory with only ONE file
    d = tmp_path / "data"
    d.mkdir()
    (d / "budget_v1_20260101.csv").write_text("content")
    
    # This should RAISE a FileNotFoundError because we can't do variance with 1 file
    with pytest.raises(FileNotFoundError):
        get_latest_budget(str(d))

# Test 2.
# Code must fail if two files are not retured in old, new seqence.
def test_get_latest_budget_sorted_files (tmp_path):
    # Setup: Create a directory with two CSV files
    d = tmp_path / "data"
    d.mkdir()
    # V2 was created first to test if the code correctly sort them.
    (d / "budget_v2_20260201.csv").write_text("new_data")
    (d / "budget_v1_20260101.csv").write_text("old_data")

    # Action
    result = get_latest_budget(str(d))
    # Assertions I insist that index 0 is v1
    # If glob returns them in the order they were created (v2, then v1), 
    # this will FAIL unless you have .sorted() in your code.

    assert len(result) == 2
    assert result[0].endswith("budget_v1_20260101.csv")
    assert result[1].endswith("budget_v2_20260201.csv")