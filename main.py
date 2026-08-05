"""
main.py — Entry point for the ETL files organizer.
"""

import signal
import sys
from dotenv import load_dotenv
from ingest_files import sql_file_to_excel, ingest_files, sql_file_to_csv, create_table_from_first_column
from db import get_conn_str
from file_ops import excel_to_csv

load_dotenv()

def handle_interrupt(sig, frame):
    """Handle keyboard interrupt gracefully."""
    print("\n[SKIP] Interrupted by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

def run():
    source = get_conn_str('Mgd_Care_Reporting')
    target =  get_conn_str()
    separator = ['|', '\t']
    sql_file_path = r"C:\etl-files-organizer\sql_scripts\sql_holder.sql"
    output_folder = r"C:\Users\VERZ0003\OneDrive - Bon Secours Mercy Health\Documents\arrived_files"
    csv_path = r"\\mdcofs900011\corpshared$\NetMgt\Managed Care Analytics\Reporting\Data Imports for SQL\DataFeed\landing_ingestion"
    source_table = ''
    target_table = ''
    create_table_from_first_column(source_table, target_table, source, target)
    sql_file_to_excel(source, sql_file_path, output_folder)
    excel_to_csv(output_folder, csv_path, separator[0])


if __name__ == "__main__":
    run()
    print("DONE!")