import pandas as pd
import os
import glob
from pathlib import Path

# function to get the two files of budget
def get_latest_budget(dir_data = "data"):
    # glob search data folder for any CSV files
    # os.path.join handles slashes correctly based on os
    # refactor: the file-handling logic by transitioning from the legacy os module to pathlib
    path = Path(dir_data)
    #green fix: sorting files chronologically
    files = sorted([str(f) for f in path.glob("*.csv")])

    # defensive check: ensuring I have two files needed for variance
    if len(files) < 2:
        raise FileNotFoundError(f"Insufficient files in {dir_data}. Need at least 2")
    # ensure code always gives the last two files
    return files[-2:]

# Update process_variance to accept an optional path
def process_variance(dir_path="data"):
    # Pass that path into get_latest_budget
    old_file, new_file = get_latest_budget(dir_path) 
    
    # Load data
    df_old = pd.read_csv(old_file)
    df_new = pd.read_csv(new_file)

    # Green Phase: renaming first column from Week to Location
    df_old = df_old.rename(columns={'Week':'Location'})
    df_new = df_new.rename(columns={'Week':'Location'})
    
    # Save output (Optional: you could also parameterise the output path!)
    df_new.to_csv("output/new.csv", index=False)
    
    return df_new

