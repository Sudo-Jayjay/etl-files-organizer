"""
initiate_zip_files/zip_utils.py — Orchestrates unzip and move into a single operation.
"""
from .imports import *
from .unzip_files import unzip_all
from .move_files import move_files

def unzip_and_move(
    zip_source_dir: str,
    final_destination_dir: str,
    temp_extract_dir: str = None, # type: ignore
    overwrite: bool = False,
    cleanup: bool = True,
) -> list[Path]:
    """Extracts all ZIPs from zip_source_dir, moves contents to final_destination_dir, then deletes extracted files. O(n)"""
    temp_dir = temp_extract_dir or os.path.join(zip_source_dir, "_temp_extract")

    print(f"\n[zip_utils] Step 1/2 - Extracting ZIPs from '{zip_source_dir}'...")
    unzip_all(source_dir=zip_source_dir, extract_dir=temp_dir, cleanup=cleanup) # type: ignore

    print(f"\n[zip_utils] Step 2/2 - Moving files to '{final_destination_dir}'...")
    moved = move_files(
        source_dir=temp_dir,
        destination_dir=final_destination_dir,
        overwrite=overwrite,
        cleanup=cleanup,
    )

    print(f"\n[zip_utils] [DONE] {len(moved)} item(s) moved to '{final_destination_dir}'.")
    return moved