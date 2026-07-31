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