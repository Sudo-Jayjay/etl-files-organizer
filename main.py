"""
main.py — Entry point for the ETL files organizer.
"""

import os
import signal
import sys
from dotenv import load_dotenv
from file_ops import list_files, move_files, unzip_files, delete_zip_files

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
    # conn_str = (
    # f"mssql+pyodbc://{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
    # f"?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    # )
    print(list_files(r"C:\Users\JAYSON\Documents\smm-website\smmpanel_next_js", pattern=r"\.sql"))
    print("DONE!")