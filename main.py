"""
main.py — Entry point for the ETL files organizer.
"""

import os
import signal
import sys
from dotenv import load_dotenv
from manipulate_files.unzip_files import unzip_all
from manipulate_files.move_files import move_files
from manipulate_files.unzip_utils import unzip_and_move
from ingest_files.count_rows import count_lines
from docs_utils.modify_header import replace_right_header
from docx import Document
from manipulate_files.format_date_column import format_date_column

load_dotenv()

ZIP_SOURCE_DIR    = os.getenv("ZIP_SOURCE_DIR")
ZIP_DESTINATION_DIR   = os.getenv("ZIP_DESTINATION_DIR")
EXTRACT_DIR       = os.getenv("EXTRACT_DIR")
DESTINATION_DIR   = os.getenv("DESTINATION_DIR")


# def run():
#     # Option 3: Move only (after unzipping separately)
#     move_files(
#     source_dir=EXTRACT_DIR, # type: ignore
#     destination_dir=DESTINATION_DIR, # type: ignore
#     overwrite=True,
#     )
#     # Option 1: Unzip + move in one call
#     unzip_and_move(
#         zip_source_dir=ZIP_SOURCE_DIR, # type: ignore
#         final_destination_dir=ZIP_DESTINATION_DIR, # type: ignore
#         overwrite=True,
#         cleanup=True,
#     )

    # # Option 2: Unzip only
    # unzip_all(
    #     source_dir=ZIP_SOURCE_DIR,
    #     extract_dir=EXTRACT_DIR,
    # )


def handle_interrupt(sig, frame):
    """Handle keyboard interrupt gracefully."""
    print("\n[SKIP] Interrupted by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)




if __name__ == "__main__":
    # run()
    format_date_column(r"C:\Users\VERZ0003\Downloads\dates.xlsx", ["A", "B", "C"])
    print("DONE!")