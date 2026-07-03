import pandas as pd
from sqlalchemy import create_engine

def csv_to_sql(csv_paths, table_name, conn_str, if_exists="append"):
    if isinstance(csv_paths, str):
        csv_paths = [csv_paths]

    engine = create_engine(conn_str)
    for path in csv_paths:
        df = pd.read_csv(path)
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        if_exists = "append"  # only replace/fail on first file, append the rest