import pandas as pd
from sqlalchemy import create_engine, types
from dotenv import load_dotenv
import os

load_dotenv()

def csv_to_sql(csv_paths, table_name, conn_str, if_exists="append"):
    if isinstance(csv_paths, str):
        csv_paths = [csv_paths]

    engine = create_engine(conn_str)
    for path in csv_paths:
        df = pd.read_csv(path, sep="|")
        dtype = {col: types.NVARCHAR(None) for col in df.columns}
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, dtype=dtype)
        if_exists = "append"  # only replace/fail on first file, append the rest

if __name__ == "__main__":
    conn_str = (
    f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    csv_to_sql([r"\\mdcofs900011\corpshared$\NetMgt\Managed Care Analytics\Reporting\Data Imports for SQL\DataFeed\landing_ingestion\MKY_MA_AETACOE6_202605_20260615.txt"], "your_table", conn_str)