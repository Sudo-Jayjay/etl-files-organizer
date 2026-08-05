from sqlalchemy import create_engine, text

def run_query(conn_str, query):
    engine = create_engine(conn_str)
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()
