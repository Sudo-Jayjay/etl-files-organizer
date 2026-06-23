"""
modules/reader.py
─────────────────
Handles CSV file discovery and reading into pandas DataFrames.
Keeps all file I/O and path logic in one place.
"""

import glob
import logging
from pathlib import Path

import pandas as pd

log = logging.getLogger(__name__)


def find_csv_files(source: str) -> list[Path]:
    """
    Discover CSV files from a folder path or a glob pattern.

    Args:
        source: A directory path (loads all *.csv inside)
                OR a glob pattern (e.g. "data/sales_*.csv").

    Returns:
        Sorted list of resolved Path objects.

    Raises:
        FileNotFoundError: If no files are matched.
    """
    p = Path(source)
    if p.is_dir():
        files = sorted(p.glob("*.csv"))
    else:
        files = [Path(f) for f in sorted(glob.glob(source, recursive=True))]

    if not files:
        raise FileNotFoundError(f"No CSV files found for source: {source!r}")

    log.info("Discovered %d CSV file(s):", len(files))
    for f in files:
        log.info("  • %s", f)

    return files


def read_csv(
    file_path: str | Path,
    dtype_map: dict | None = None,
    parse_dates: list[str] | None = None,
    usecols: list[str] | None = None,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Read a single CSV file into a DataFrame and sanitise column names.

    Column names are lowercased and spaces replaced with underscores so
    they map cleanly to SQL Server column names.

    Args:
        file_path:   Path to the CSV file.
        dtype_map:   Optional {column: dtype} overrides for read_csv.
        parse_dates: Column names to parse as datetime.
        usecols:     Subset of columns to load (None = all).
        encoding:    File encoding (try "latin-1" if utf-8 raises errors).

    Returns:
        Clean DataFrame ready for upload.
    """
    path = Path(file_path)
    log.info("Reading %s ...", path.name)

    df = pd.read_csv(
        path,
        dtype=dtype_map,
        parse_dates=parse_dates,
        usecols=usecols,
        encoding=encoding,
    )

    # Sanitise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    log.info("  → %d rows, %d columns", len(df), df.shape[1])
    return df


def validate_dataframe(df: pd.DataFrame, file_name: str) -> None:
    """
    Run basic checks on a DataFrame before uploading.

    Raises:
        ValueError: If the DataFrame is empty or has no columns.
    """
    if df.empty:
        raise ValueError(f"{file_name}: DataFrame is empty — nothing to upload.")
    if df.shape[1] == 0:
        raise ValueError(f"{file_name}: DataFrame has no columns.")

    # Warn about fully-null columns
    null_cols = [c for c in df.columns if df[c].isna().all()]
    if null_cols:
        log.warning("%s: fully-null columns detected: %s", file_name, null_cols)