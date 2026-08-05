import pandas as pd

def excel_to_csv(excel_path, csv_path, delimiter=None):
    separator = delimiter or ','
    df = pd.read_excel(excel_path)
    df.to_csv(csv_path, sep=separator, index=False)
    