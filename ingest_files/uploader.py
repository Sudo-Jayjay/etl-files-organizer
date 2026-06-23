"""
modules/uploader.py
────────────────────
Handles writing DataFrames to SQL Server — both single-file
and batch (multi-file) uploads.
"""

import logging
import time
from pathlib import Path

from sqlalchemy import Engine

from modules.reader import find_csv_files, read_csv, validate_dataframe

log = logging.getLogger(__name__)


def upload_dataframe(
    df,
    engine: Engine,
    table_name: str,
    schema: str = "dbo",
    if_exists: str = "append",
    chunksize: int = 10_000,
) -> int:
    """
    Write a DataFrame to a SQL Server table.

    Args:
        df:          DataFrame to upload.
        engine:      SQLAlchemy engine.
        table_name:  Target table name.
        schema:      SQL Server schema (default: dbo).
        if_exists:   'append' | 'replace' | 'fail'.
        chunksize:   Rows per INSERT batch.

    Returns:
        Number of rows written.
    """
    row_count = len(df)
    log.info(
        "Uploading %d rows → [%s].[%s]  (if_exists=%r)",
        row_count, schema, table_name, if_exists,
    )

    start = time.perf_counter()
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists=if_exists,
        index=False,
        chunksize=chunksize,
        method="multi",   # batched INSERTs (works with fast_executemany=True)
    )
    elapsed = time.perf_counter() - start

    log.info("  ✓ Done in %.1fs → [%s].[%s]", elapsed, schema, table_name)
    return row_count


def upload_csv_file(
    file_path: str | Path,
    engine: Engine,
    table_name: str | None = None,
    schema: str = "dbo",
    if_exists: str = "append",
    chunksize: int = 10_000,
    dtype_map: dict | None = None,
    parse_dates: list[str] | None = None,
    usecols: list[str] | None = None,
    table_prefix: str = "",
) -> int:
    """
    Read a single CSV file and upload it to SQL Server.

    Args:
        file_path:   Path to the CSV file.
        engine:      SQLAlchemy engine.
        table_name:  Target table name (defaults to filename stem).
        schema:      SQL Server schema.
        if_exists:   'append' | 'replace' | 'fail'.
        chunksize:   Rows per INSERT batch.
        dtype_map:   Column dtype overrides for read_csv.
        parse_dates: Columns to parse as datetime.
        usecols:     Subset of columns to load.
        table_prefix: Prefix prepended to the auto-derived table name.

    Returns:
        Number of rows uploaded.
    """
    path = Path(file_path)
    table = table_name or f"{table_prefix}{path.stem.lower().replace(' ', '_')}"

    df = read_csv(path, dtype_map=dtype_map, parse_dates=parse_dates, usecols=usecols)
    validate_dataframe(df, path.name)

    return upload_dataframe(df, engine, table_name=table, schema=schema,
                            if_exists=if_exists, chunksize=chunksize)


def upload_all_csvs(
    source: str,
    engine: Engine,
    schema: str = "dbo",
    if_exists: str = "append",
    chunksize: int = 10_000,
    table_prefix: str = "",
    table_name_map: dict[str, str] | None = None,
    dtype_map: dict | None = None,
    parse_dates: list[str] | None = None,
    usecols: list[str] | None = None,
) -> dict[str, int]:
    """
    Discover and upload every CSV matched by `source`.

    Args:
        source:         Folder path or glob pattern.
        engine:         SQLAlchemy engine.
        schema:         Target schema.
        if_exists:      'append' | 'replace' | 'fail'.
        chunksize:      Rows per INSERT batch.
        table_prefix:   Prefix added to auto-derived table names.
        table_name_map: Dict mapping filename → explicit table name.
        dtype_map:      Column dtype overrides applied to every file.
        parse_dates:    Date columns applied to every file.
        usecols:        Column subset applied to every file.

    Returns:
        Dict mapping each filename to the number of rows uploaded.
        Files that failed are excluded from results and logged as errors.
    """
    files = find_csv_files(source)

    results: dict[str, int] = {}
    errors:  dict[str, str] = {}

    for csv_path in files:
        override   = (table_name_map or {}).get(csv_path.name)
        table_name = override or f"{table_prefix}{csv_path.stem.lower().replace(' ', '_')}"

        try:
            rows = upload_csv_file(
                file_path=csv_path,
                engine=engine,
                table_name=table_name,
                schema=schema,
                if_exists=if_exists,
                chunksize=chunksize,
                dtype_map=dtype_map,
                parse_dates=parse_dates,
                usecols=usecols,
            )
            results[csv_path.name] = rows

        except Exception as exc:
            log.error("FAILED  %s → %s", csv_path.name, exc)
            errors[csv_path.name] = str(exc)

    # Summary
    total = sum(results.values())
    log.info("─" * 55)
    log.info("Batch complete: %d uploaded, %d failed | %d total rows",
             len(results), len(errors), total)

    return results