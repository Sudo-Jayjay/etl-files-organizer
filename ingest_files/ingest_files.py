import pandas as pd
from sqlalchemy import create_engine, types

def csv_to_sql(csv_paths, table_name, conn_str, if_exists="append"):
    if isinstance(csv_paths, str):
        csv_paths = [csv_paths]

    engine = create_engine(conn_str)
    for path in csv_paths:
        df = pd.read_csv(path)
        dtype = {col: types.NVARCHAR(255) for col in df.columns}
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, dtype=dtype)
        if_exists = "append"  # only replace/fail on first file, append the rest

if __name__ == "__main__":
    conn_str = "mssql+pyodbc://your_user:your_password@your_server/your_db?driver=ODBC+Driver+17+for+SQL+Server"
    csv_to_sql(["file1.csv", "file2.csv"], "your_table", conn_str)