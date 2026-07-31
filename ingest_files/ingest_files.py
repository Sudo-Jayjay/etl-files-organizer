import pandas as pd
from sqlalchemy import create_engine, types
from dotenv import load_dotenv
import os

load_dotenv()

def ingest_files(csv_paths, table_name, conn_str, if_exists="append"):
    if isinstance(csv_paths, str):
        csv_paths = [csv_paths]

    engine = create_engine(conn_str)
    for path in csv_paths:
        df = pd.read_csv(path, sep=",")
        dtype = {col: types.NVARCHAR(None) for col in df.columns}
        df.to_sql(table_name, engine, if_exists=if_exists, index=False, dtype=dtype)
        if_exists = "append"  # only replace/fail on first file, append the rest