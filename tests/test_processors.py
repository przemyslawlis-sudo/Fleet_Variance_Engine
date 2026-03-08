import pytest
import os
# Import processor.py and get_latest_budget function.
from src.processor import get_latest_budget

# Test 1. 
def test_get_latest_budget_fails_with_one_file(tmp_path):
    # Setup: Create a directory with only ONE file
    d = tmp_path / "data"
    d.mkdir()
    (d / "budget_v1_20260101.csv").write_text("content")
    
    # This should RAISE a FileNotFoundError because we can't do variance with 1 file
    with pytest.raises(FileNotFoundError):
        get_latest_budget(str(d))
