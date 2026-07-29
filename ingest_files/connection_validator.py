import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

def is_connection_valid(conn_str):
    try:
        engine = create_engine(conn_str)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print("Connection failed:", e)
        return False

if __name__ == "__main__":
    load_dotenv()
    conn_str = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
        f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    print("Connection valid:", is_connection_valid(conn_str))