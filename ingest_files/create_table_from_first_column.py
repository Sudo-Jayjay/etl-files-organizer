import pandas as pd
from sqlalchemy import create_engine, inspect, text
import os
from dotenv import load_dotenv

load_dotenv()

def copy_headers_and_first_row_to_table(source_table, target_table, source_conn_str, target_conn_str):
    source_engine = create_engine(source_conn_str)
    target_engine = create_engine(target_conn_str)
 
    inspector = inspect(source_engine)
    columns = inspector.get_columns(source_table)  # [{'name': ..., 'type': ...}, ...]
 
    df = pd.read_sql(f"SELECT TOP 1 * FROM {source_table}", source_engine)
 
    column_defs = ", ".join(f"[{col['name']}] NVARCHAR(MAX)" for col in columns)
    with target_engine.connect() as conn:
        conn.execute(text(f"CREATE TABLE {target_table} ({column_defs})"))
        conn.commit()
 
    df.to_sql(target_table, target_engine, if_exists="append", index=False)

if __name__ == "__main__":
    source_engine = (
    f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    target_engine = (
    f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE2')}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    copy_headers_and_first_row_to_table("Lkp_Plan_Index", "lkp_plan_index", source_engine, target_engine)