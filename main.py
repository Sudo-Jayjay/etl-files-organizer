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
# def count_lines(filepath: str) -> int:
#     """Count lines using memory-mapped file access."""
#     with open(filepath, "rb") as f:
#         mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#         count = mm.read().count(b"\n")
#         mm.close()
#     return count
    
# def count_lines(filepath: str) -> int:
#     """Count the number of lines in a text file efficiently."""
#     with open(filepath, "rb") as f:
#         return sum(1 for _ in f)   

def handle_interrupt(sig, frame):
    """Handle keyboard interrupt gracefully."""
    print("\n[SKIP] Interrupted by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

# def count_lines(filepath: str) -> int:
#     """Count lines by reading fixed-size chunks to minimize I/O calls."""
#     count = 0
#     with open(filepath, "rb") as f:
#         while chunk := f.read(1024 * 1024):  # read 1MB at a time
#             count += chunk.count(b"\n")
#     return count

# def count_lines(filepath: str) -> int:
#     """Count lines using memory-mapped file access."""
#     with open(filepath, "rb") as f:
#         mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#         count = mm.read().count(b"\n")
#         mm.close()
#     return count


if __name__ == "__main__":
    # run()
    file_path = r"S:\NetMgt\Managed Care Analytics\Revenue Applications\DataFeed\Membership\Anthem\Anthem_MA\KYMHPMA_Clinical_Attribution_05092026.txt"
    file_sample = r"KYMHPMA_Clinical_Attribution_05092026.txt"
    line_count = count_lines(file_path)
    print(f"[OK] Total lines: {line_count + 1}")
    print("DONE!")