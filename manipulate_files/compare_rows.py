import pandas as pd

def compare_rows(old_filepath, new_filepath):
    old_count = len(pd.read_excel(old_filepath))
    new_count = len(pd.read_excel(new_filepath))
    return old_count - new_count
