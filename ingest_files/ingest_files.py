import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def csv_to_sql(csv_paths, table_name, conn_str, if_exists="append"):
    if isinstance(csv_paths, str):
        csv_paths = [csv_paths]

    engine = create_engine(conn_str)
    for path in csv_paths:
        df = pd.read_csv(path)
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        if_exists = "append"  # only replace/fail on first file, append the rest

if __name__ == "__main__":
    conn_str = (
        f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
        f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    csv_to_sql([r"\\mdcofs900011\corpshared$\NetMgt\Managed Care Analytics\Reporting\SQL Scripts\Physician Monthly Data Import Process\prod_01__PHYSICIAN_CONSOL_BSMH\LkpTables\PlanIndexes\weekly_new_plans\01_mapped_weekly_plans\tmp_weekly_plan_index_for_mapping.csv"], "tmp_weekly_plan_index_for_mapping_072826", conn_str)