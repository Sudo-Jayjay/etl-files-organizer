import pandas as pd

def check_schema_drift(old_filepath, new_filepath):
    old_cols = list(pd.read_excel(old_filepath, nrows=0).columns)
    new_cols = list(pd.read_excel(new_filepath, nrows=0).columns)
    return old_cols == new_cols

if __name__ == "__main__":
    excess = check_schema_drift(r"C:\Users\VERZ0003\Downloads\DE5500 - Visit Billing Data (02-13-2026).xlsx", r"C:\Users\VERZ0003\Downloads\DE5500 - Visit Billing Data (02-13-2026).xlsx")
    print("Excess columns:", excess)