"""
main.py — Entry point for the ETL files organizer.
"""

import os
import signal
import sys
from dotenv import load_dotenv
from manipulate_files.compare_rows import compare_rows
from ingest_files.traverse_folder import list_files
from ingest_files.create_table_from_first_column import copy_first_column_and_row
from ingest_files.ingest_files import csv_to_sql



load_dotenv()

ZIP_SOURCE_DIR    = os.getenv("ZIP_SOURCE_DIR")
ZIP_DESTINATION_DIR   = os.getenv("ZIP_DESTINATION_DIR")
EXTRACT_DIR       = os.getenv("EXTRACT_DIR")
DESTINATION_DIR   = os.getenv("DESTINATION_DIR")



def handle_interrupt(sig, frame):
    """Handle keyboard interrupt gracefully."""
    print("\n[SKIP] Interrupted by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)




if __name__ == "__main__":
    # run()
    # format_date_column(r"C:\Users\VERZ0003\Downloads\dates.xlsx", ["A", "B", "C"])
    conn_str = (
    f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    print("DONE!")