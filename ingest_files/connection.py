"""
modules/connection.py
─────────────────────
Builds and returns a SQLAlchemy engine for SQL Server.
Supports both Windows Authentication and SQL Server Authentication.
"""

import logging
from sqlalchemy import create_engine, Engine

log = logging.getLogger(__name__)


def get_engine(
    server: str,
    database: str,
    username: str | None = None,
    password: str | None = None,
    driver: str = "ODBC Driver 17 for SQL Server",
) -> Engine:
    """
    Create a SQLAlchemy engine for SQL Server.

    Args:
        server:    Server name or IP (e.g. "localhost", "srv\\SQLEXPRESS").
        database:  Target database name.
        username:  SQL Server login. Pass None for Windows Authentication.
        password:  SQL Server password. Pass None for Windows Authentication.
        driver:    ODBC driver name installed on the machine.

    Returns:
        A connected SQLAlchemy Engine with fast_executemany enabled.
    """
    if username and password:
        # SQL Server Authentication
        conn_str = (
            f"mssql+pyodbc://{username}:{password}@{server}/{database}"
            f"?driver={driver.replace(' ', '+')}"
        )
        auth_mode = "SQL Auth"
    else:
        # Windows Authentication (trusted connection)
        conn_str = (
            f"mssql+pyodbc://{server}/{database}"
            f"?driver={driver.replace(' ', '+')}&trusted_connection=yes"
        )
        auth_mode = "Windows Auth"

    engine = create_engine(conn_str, fast_executemany=True)
    log.info("Engine ready → %s / %s  [%s]", server, database, auth_mode)
    return engine