"""
config/settings.py
──────────────────
Central configuration for the CSV → SQL Server pipeline.
Edit the values here; nothing else needs to change.
"""

# ── SQL Server connection ─────────────────────────────────────────────────────
SERVER   = "YOUR_SERVER_NAME"     # e.g. "localhost" or "myserver\\SQLEXPRESS"
DATABASE = "YOUR_DATABASE"
USERNAME = "YOUR_USER"            # set to None to use Windows Authentication
PASSWORD = "YOUR_PASSWORD"        # set to None to use Windows Authentication
DRIVER   = "ODBC Driver 17 for SQL Server"

# ── Upload behaviour ──────────────────────────────────────────────────────────
SCHEMA       = "dbo"
IF_EXISTS    = "append"           # "append" | "replace" | "fail"
CHUNKSIZE    = 10_000             # rows per INSERT batch
TABLE_PREFIX = "raw_"             # auto-named tables become raw_orders, etc.

# ── Source files ──────────────────────────────────────────────────────────────
SOURCE = "data/"                  # folder path  OR  glob e.g. "data/sales_*.csv"

# ── Optional per-file overrides ───────────────────────────────────────────────
# Map a CSV filename to a custom table name.
TABLE_NAME_MAP: dict[str, str] = {
    # "orders_2024.csv": "orders",
    # "customers.csv":   "dim_customers",
}

# ── Optional column settings applied to every file ───────────────────────────
PARSE_DATES: list[str] = []       # e.g. ["order_date", "ship_date"]
USECOLS:     list[str] | None = None  # None = load all columns
DTYPE_MAP:   dict | None = None   # e.g. {"order_id": str, "amount": float}