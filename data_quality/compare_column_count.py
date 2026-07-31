import pandas as pd

def compare_column_count(file1, file2):
    count1 = len(pd.read_excel(file1, nrows=0).columns)
    count2 = len(pd.read_excel(file2, nrows=0).columns)
    return [count1, count2]

if __name__ == "__main__":
    diff = compare_column_count(r"C:\Users\VERZ0003\Downloads\DE5500 - Visit Billing Data (03-6-2026).xlsx", r"C:\Users\VERZ0003\Downloads\DE5500 - Visit Billing Data (02-13-2026).xlsx")
    print("Column count difference:", diff)