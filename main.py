"""
main.py — Entry point for the ETL files organizer.
"""

import os
import signal
import sys
from dotenv import load_dotenv
from ingest_files import sql_file_to_excel
from db import get_conn_str

load_dotenv()

def handle_interrupt(sig, frame):
    """Handle keyboard interrupt gracefully."""
    print("\n[SKIP] Interrupted by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)




if __name__ == "__main__":
    sql_file_to_excel(get_conn_str('Mgd_Care_Reporting'), r"C:\etl-files-organizer\sql_scripts\weekly_plan_index.sql", r"C:\Users\VERZ0003\OneDrive - Bon Secours Mercy Health\Documents\arrived_files")
    print("DONE!")