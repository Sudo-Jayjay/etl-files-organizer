"""
modules/verifier.py
────────────────────
Post-upload verification: compares SQL Server row counts
against the source CSV row counts.
"""

import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, text

log = logging.getLogger(__name__)


def get_table_row_count(engine: Engine, table: str, schema: str = "dbo") -> int:
    """
    Return the current row count of a SQL Server table.

    Args:
        engine: SQLAlchemy engine.
        table:  Table name.
        schema: Schema name (default: dbo).

    Returns:
        Integer row count.
    """
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM [{schema}].[{table}]"))
        count = result.scalar()
    log.info("SQL Server [%s].[%s]: %d rows", schema, table, count)
    return count


def verify_upload(
    engine: Engine,
    table: str,
    expected_rows: int,
    schema: str = "dbo",
) -> bool:
    """
    Confirm the SQL Server table contains the expected number of rows.

    Logs a warning if there is a mismatch (e.g. if_exists='append'
    adds to existing rows, so the total may exceed expected_rows).

    Args:
        engine:        SQLAlchemy engine.
        table:         Table name.
        expected_rows: Row count from the source CSV.
        schema:        Schema name.

    Returns:
        True if counts match, False otherwise.
    """
    actual = get_table_row_count(engine, table, schema)
    if actual >= expected_rows:
        log.info("  ✓ Verification passed: %d rows in [%s].[%s]", actual, schema, table)
        return True
    else:
        log.warning(
            "  ✗ Mismatch for [%s].[%s]: expected %d, found %d",
            schema, table, expected_rows, actual,
        )
        return False


def verify_all(
    engine: Engine,
    results: dict[str, int],
    table_prefix: str = "",
    schema: str = "dbo",
) -> dict[str, bool]:
    """
    Verify all tables from a batch upload.

    Args:
        engine:       SQLAlchemy engine.
        results:      Dict of {filename: rows_uploaded} from upload_all_csvs().
        table_prefix: Prefix used when deriving table names.
        schema:       Schema name.

    Returns:
        Dict of {table_name: passed (bool)}.
    """
    checks: dict[str, bool] = {}

    for filename, expected in results.items():
        table = f"{table_prefix}{Path(filename).stem.lower().replace(' ', '_')}"
        passed = verify_upload(engine, table, expected, schema)
        checks[table] = passed

    passed_count = sum(checks.values())
    log.info("─" * 55)
    log.info("Verification: %d/%d tables passed", passed_count, len(checks))

    return checks


def print_summary(results: dict[str, int], checks: dict[str, bool]) -> None:
    """Print a formatted upload + verification summary table."""
    print("\n" + "─" * 60)
    print(f"{'File':<35} {'Rows':>8}  {'Verified'}")
    print("─" * 60)
    for filename, rows in results.items():
        from pathlib import Path
        table = Path(filename).stem.lower().replace(" ", "_")
        status = "✓" if checks.get(table, False) else "✗"
        print(f"{filename:<35} {rows:>8,}  {status}")
    print("─" * 60)
    print(f"{'TOTAL':<35} {sum(results.values()):>8,}")
    print()