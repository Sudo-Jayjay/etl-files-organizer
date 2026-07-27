import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def test_connection(conn_str):
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection successful")

if __name__ == "__main__":
    load_dotenv()
    conn_str = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
        f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    test_connection(conn_str)