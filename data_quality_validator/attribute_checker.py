import pandas as pd

def check_schema_drift(old_filepath, new_filepath):
    old_cols = list(pd.read_excel(old_filepath, nrows=0).columns)
    new_cols = list(pd.read_excel(new_filepath, nrows=0).columns)
    return old_cols == new_cols
