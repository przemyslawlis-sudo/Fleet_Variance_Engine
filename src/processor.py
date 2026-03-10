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

    # Transforming from Wide to Long

    df_old_long = df_old.melt(id_vars="Location",var_name="Week_No",value_name="KPI_Old")
    df_new_long = df_new.melt(id_vars="Location",var_name="Week_No",value_name="KPI_New")
    
    # Refactor: explicitly convert the column type 
    df_old_long["Week_No"] = df_old_long["Week_No"].astype(int)
    df_new_long["Week_No"] = df_new_long["Week_No"].astype(int)
        
    # Merging and Calculation
    combined = pd.merge(df_old_long,df_new_long,on=['Location','Week_No'])

    # Green: Math
    combined['Variance'] = combined['KPI_New']-combined['KPI_Old']
    # Refactor: For precision round()
    combined['%Variance'] = round((combined['Variance']/combined['KPI_Old']) * 100,2)

    # Pivoting and Exporting
    pivot_var = combined.pivot_table(index='Location', columns='Week_No', values='Variance', aggfunc='sum', margins=True)
    pivot_pct = combined.pivot_table(index='Location', columns='Week_No', values='%Variance', aggfunc='mean', margins=True)

    pivot_pct = pivot_pct.round(2).fillna(0)

    pivot_var.to_csv("output/variance.csv")
    pivot_pct.to_csv("output/variance_percentage.csv")

    return combined
process_variance()

