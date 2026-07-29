import pandas as pd
from sqlalchemy import create_engine, inspect, text

def copy_first_column_and_row(source_table, target_table, conn_str):
    engine = create_engine(conn_str)

    inspector = inspect(engine)
    first_column = inspector.get_columns(source_table)[0]  # {'name': ..., 'type': ..., ...}
    column_name = first_column["name"]
    column_type = first_column["type"]

    df = pd.read_sql(f"SELECT TOP 1 [{column_name}] FROM {source_table}", engine)

    with engine.connect() as conn:
        conn.execute(text(f"CREATE TABLE {target_table} ([{column_name}] {column_type})"))
        conn.commit()

    df.to_sql(target_table, engine, if_exists="append", index=False)

# Use Case:
# if __name__ == "__main__":
#     conn_str = "mssql+pyodbc://your_user:your_password@your_server/your_db?driver=ODBC+Driver+17+for+SQL+Server"
#     copy_first_column_and_row("your_table", "your_new_table", conn_str)