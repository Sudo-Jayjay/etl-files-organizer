import pandas as pd

def compare_columns(old_filepath, new_filepath):
    old_cols = set(pd.read_excel(old_filepath, nrows=0).columns)
    new_cols = set(pd.read_excel(new_filepath, nrows=0).columns)
    return new_cols - old_cols
