import os

def get_conn_str(database=None):
    """Return a SQLAlchemy engine connected to the given database, or SQL_DATABASE by default."""
    db_name = database or os.getenv('SQL_DATABASE')
    conn_str = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{db_name}"
        f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    return conn_str