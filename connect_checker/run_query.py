import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

TABLE_NAME='audit.file_processing_history'
def run_query(conn_str, query):
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()

if __name__ == "__main__":
    load_dotenv()
    conn_str = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
        f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    rows = run_query(conn_str, f"SELECT * FROM {TABLE_NAME}")
    print(rows[0][1])