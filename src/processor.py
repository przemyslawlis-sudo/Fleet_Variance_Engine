import pandas as pd
import os
import glob

# function to get the two files of budget
def get_latest_budget(dir_data = "data"):
    # glob search data folder for any CSV files
    # os.path.join handles slashes correctly based on os
    files = glob.glob(os.path.join(dir_data,"*.csv"))

    # defensive check: ensuring I have two files needed for variance
    if len(files) < 2:
        raise FileNotFoundError(f"Insuficent files in {dir_data}. Need at least 2")
    return files[-2:]

