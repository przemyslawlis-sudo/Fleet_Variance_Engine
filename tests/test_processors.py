import pytest
import os
# Import processor.py and get_latest_budget function.
from src.processor import get_latest_budget
# Import process_variance function
from src.processor import process_variance

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
    # this will FAIL.

    assert len(result) == 2
    assert result[0].endswith("budget_v1_20260101.csv")
    assert result[1].endswith("budget_v2_20260201.csv")


from src.processor import process_variance

def test_process_variance_column_integrity(tmp_path):
    # 1. Arrange: Create the temp folder and files
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    
    csv_content = "Week,1,2\nAltens,100,110\nArnold,200,210"
    (data_dir / "budget_v1.csv").write_text(csv_content)
    (data_dir / "budget_v2.csv").write_text(csv_content)

    # 2. Act: Pass the temp directory path into your function
    df_result = process_variance(str(data_dir))

    # 3. Assert: Check the results
    assert df_result.columns[0] == "Location"
    assert df_result.iloc[0, 0] == "Altens"

def test_process_variance_first_row_and_column_integrity(tmp_path):
    # Setup
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    csv_content = "Week,1\nAltens,100"
    (data_dir / "budget_v1.csv").write_text(csv_content)
    (data_dir / "budget_v2.csv").write_text(csv_content)
    # Action
    df_result = process_variance(str(data_dir))
    # Assert
    assert df_result.iloc[0,0] == "Altens"
    assert str(df_result.iloc[0,1]) == "1"


def test_variance_calculation_accuracy(tmp_path):
    # Setup
    data_dir = tmp_path / "calc_test"
    data_dir.mkdir()
    
    # 100 (Old) and 120 (New)
    csv_old = "Week,1\nAltens,100"
    csv_new = "Week,1\nAltens,120"
    
    (data_dir / "budget_v1.csv").write_text(csv_old)
    (data_dir / "budget_v2.csv").write_text(csv_new)

    # Action
    df_result = process_variance(str(data_dir))

    # Assert
    # Check absolute variance: 120 - 100 = 20
    assert df_result.loc[0,'Variance'] == 20
    
    # Check percentage variance: (20 / 100) * 100 = 20.0
    assert df_result.loc[0,'%Variance'] == 20.0

def test_pivot_export_integrity(tmp_path):
    # Setup data in a mock folder
    data_dir = tmp_path / "export_test"
    data_dir.mkdir()
    (data_dir / "budget_v1.csv").write_text("Week,1\nAltens,100")
    (data_dir / "budget_v2.csv").write_text("Week,1\nAltens,120")

    # Action
    process_variance(str(data_dir))

    # Assert: 
    assert os.path.exists("output/variance.csv")
