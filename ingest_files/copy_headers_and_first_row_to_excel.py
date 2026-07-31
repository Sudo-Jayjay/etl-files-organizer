import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def copy_headers_and_first_row_to_excel(source_table, destination_folder, conn_str):
    engine = create_engine(conn_str)

    df = pd.read_sql(f"SELECT TOP 1 * FROM {source_table}", engine)

    filepath = os.path.join(destination_folder, f"{source_table}_first_row.xlsx")
    df.to_excel(filepath, index=False)

if __name__ == "__main__":
    conn_str = (
    f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    copy_headers_and_first_row_to_excel("Lkp_Plan_Index", r"C:\Users\VERZ0003\OneDrive - Bon Secours Mercy Health\Documents\arrived_files", conn_str)