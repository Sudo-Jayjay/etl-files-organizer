from dotenv import load_dotenv
from sqlalchemy import create_engine, text
load_dotenv()

def test_connection(conn_str):
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection successful")
