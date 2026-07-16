import pandas as pd

def excess_columns(base_filepath, compare_filepath):
    base_cols = set(pd.read_excel(base_filepath, nrows=0).columns.str.strip().str.lower())
    compare_df_cols = pd.read_excel(compare_filepath, nrows=0).columns
    return [col for col in compare_df_cols if col.strip().lower() not in base_cols]

if __name__ == "__main__":
    excess = excess_columns(r"C:\Users\VERZ0003\Downloads\DE5500 - Visit Billing Data (02-13-2026).xlsx", r"C:\Users\VERZ0003\Downloads\DE5500 - Visit Billing Data (06-30-2026).xlsx")
    print("Excess columns:", excess)