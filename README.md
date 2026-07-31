# etl-files-organizer

Python-based ETL project for automating file ingestion, transformation, data quality validation, and SQL Server integration. Runs locally on Windows and on the self-hosted Azure DevOps agent ("L4 Pipeline") via `azure-pipelines.yml`.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Module Reference](#module-reference)
  - [config](#config)
  - [db](#db)
  - [file_ops](#file_ops)
  - [transform](#transform)
  - [data_quality](#data_quality)
  - [ingest_files](#ingest_files)
  - [email_utils](#email_utils)
- [Running the Pipeline](#running-the-pipeline)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Known Gotchas](#known-gotchas)

---

## Environment Setup

### 1. Prerequisites

- Python (Windows)
- Git Bash
- **ODBC Driver 17 or 18 for SQL Server** — must be installed at the system level. This is a system dependency, not a pip package, and it must be installed separately on every machine and on the pipeline agent.
- Access to SQL Server (Windows trusted authentication)

### 2. Clone the repo

Clone somewhere **outside any OneDrive/SharePoint-synced folder**. Background sync can lock or corrupt `.git` internals — this has happened before on this project. Keep the repo on local disk only, e.g.:

```bash
cd C:\Users\<you>\Documents
git clone https://github.com/Sudo-Jayjay/etl-files-organizer.git
cd etl-files-organizer
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `tkinter` is part of the Python standard library. It cannot be pip-installed and must never appear in `requirements.txt`.

### 4. Configure environment variables

Create a `.env` file in the project root (this file is git-ignored and never committed):

```env
SQL_SERVER=your_sql_server_hostname
SQL_DATABASE=your_primary_database
SQL_DATABASE2=your_secondary_database   # only needed for cross-database utilities
ZIP_SOURCE_DIR=C:\path\to\incoming_zips
ZIP_DESTINATION_DIR=C:\path\to\zip_archive
EXTRACT_DIR=C:\path\to\extracted_files
DESTINATION_DIR=C:\path\to\processed_files
```

`load_dotenv()` reads this file locally. On the pipeline agent, the same variable names are injected instead via the `etl-sql-credentials` Azure DevOps Variable Group — `load_dotenv()` silently does nothing if no `.env` file is present, so the same code runs unmodified in both places. Secret variables must be explicitly mapped under `env:` in the pipeline YAML to be accessible to the running script.

### 5. Verify your SQL Server connection

```bash
python -m db.test_connection
```

This confirms `SQL_SERVER` / `SQL_DATABASE` are correct and that the ODBC driver is installed properly before you run anything else.

---

## Project Structure

```
etl-files-organizer/
├── config/          # centralized environment configuration
├── db/              # SQL Server connection, query execution, connectivity checks
├── file_ops/        # move, list, zip/unzip files on disk
├── transform/        # in-place file content transformations (e.g. date formatting)
├── data_quality/     # row/column/schema comparisons between two files
├── ingest_files/     # CSV → SQL, SQL → Excel/table transfers
├── email_utils/      # pipeline status notifications
├── main.py           # orchestrator / entry point
├── azure-pipelines.yml
└── requirements.txt
```

Each folder is a Python package with an `__init__.py` that re-exports its public functions, so other modules import from the folder directly:

```python
from db import get_engine
from file_ops import move_files, list_files
```

---

## Module Reference

### `config`

Centralized environment configuration. All other modules read settings from here rather than calling `os.getenv()` directly.

```python
from config import settings

settings.SQL_SERVER
settings.ZIP_SOURCE_DIR
```

### `db`

SQL Server connectivity — the single source of truth for the connection string.

| Function | Purpose |
|---|---|
| `get_engine(database=None)` | Returns a SQLAlchemy engine. Defaults to `SQL_DATABASE`; pass a database name to target a different one (e.g. `SQL_DATABASE2`). |
| `test_connection(engine)` | Runs `SELECT 1` to confirm connectivity. Raises/prints on failure. |
| `run_query(conn_str, query)` | Executes an arbitrary SQL string and returns the result rows. |

```python
from db import get_engine, run_query

engine = get_engine()
rows = run_query(str(engine.url), "SELECT * FROM audit.file_processing_history")
```

### `file_ops`

File system operations — moving, discovering, and unpacking files. No SQL or file-content awareness.

| Function | Purpose |
|---|---|
| `move_files(source_folder, destination_folder, pattern="*", use_regex=True)` | Moves files matching a glob or regex pattern. |
| `list_files(folder, pattern=None)` | Returns full paths of files in a folder, optionally filtered by regex. |
| `unzip_files(source_folder, destination_folder)` | Extracts all `.zip` files found in a folder. |
| `delete_zip_files(folder)` | Deletes all `.zip` files in a folder (typically after extraction). |

```python
from file_ops import list_files, move_files

csv_files = list_files(r"C:\incoming", pattern=r"\.csv$")
move_files(r"C:\incoming", r"C:\processed", pattern="*.csv", use_regex=False)
```

### `transform`

In-place edits to file contents, distinct from `file_ops` (which only moves/discovers files without touching their contents).

| Function | Purpose |
|---|---|
| `format_date_column(filepath, columns, sheet=None)` | Applies `mm/dd/yyyy` number formatting to the given Excel columns. |

```python
from transform import format_date_column

format_date_column(r"C:\Downloads\dates.xlsx", ["A", "B", "C"])
```

### `data_quality`

Compares two files (typically an old vs. new version of the same feed) and reports differences. Exploratory/diagnostic — distinct from the `checks.py` + `test_data_quality.py` pytest layer used for automated assertions.

| Function | Purpose |
|---|---|
| `compare_rows(old_filepath, new_filepath)` | Returns the row-count difference between two files. |
| `compare_columns(old_filepath, new_filepath)` | Returns columns present in the new file but not the old. |
| `compare_column_count(file1, file2)` | Returns the column count of each file. |
| `excess_columns(base_filepath, compare_filepath)` | Returns columns in the compare file not present in the base file (case + whitespace insensitive). |
| `check_schema_drift(old_filepath, new_filepath)` | Returns whether column order/names are identical between two files. |

```python
from data_quality import compare_rows, check_schema_drift

diff = compare_rows("old.xlsx", "new.xlsx")
if not check_schema_drift("old.xlsx", "new.xlsx"):
    print("Schema drift detected")
```

### `ingest_files`

Moves data between flat files, Excel, and SQL Server.

| Function | Purpose |
|---|---|
| `csv_to_sql(csv_paths, table_name, conn_str, if_exists="append")` | Loads one or more CSVs into a SQL Server table. Accepts a single path or a list. |
| `copy_headers_and_first_row_to_table(source_table, target_table, source_conn_str, target_conn_str)` | Copies a table's headers and first row into a new table, useful for schema scaffolding across databases. |
| `copy_headers_and_first_row_to_excel(source_table, destination_folder, conn_str)` | Exports a table's headers and first row to an Excel file. |

```python
from db import get_engine
from ingest_files import csv_to_sql

engine = get_engine()
csv_to_sql([r"C:\incoming\feed.csv"], "tmp_staging_table", str(engine.url))
```

### `email_utils`

Pipeline status notifications.

| Function | Purpose |
|---|---|
| `send_email(subject, body, to_addresses, smtp_server, from_address, attachment_path=None)` | Sends an email, optionally with a file attachment. |

```python
from email_utils import send_email

send_email(
    subject="ETL Job Status",
    body="Pipeline completed successfully.",
    to_addresses=["you@example.com"],
    smtp_server=("smtp.office365.com", 587),
    from_address="pipeline@example.com",
)
```

---

## Running the Pipeline

```bash
python main.py
```

`main.py` orchestrates the modules above in sequence: verify SQL Server connectivity → unpack incoming files → discover files to process → run data quality checks → ingest to SQL Server → move processed files → send a status email.

Press `Ctrl+C` at any point to interrupt gracefully — this is handled via a `SIGINT` handler in `main.py`.

---

## Testing

Data quality assertions live in a two-layer pattern:

- `checks.py` — pure assertion logic, no pytest dependency, so checks can be called outside test contexts.
- `test_data_quality.py` — thin pytest wiring around `checks.py`, using a module-scoped `engine` fixture.

Run tests locally:

```bash
pytest --junitxml=test-results.xml
```

---

## CI/CD

CI/CD runs via `azure-pipelines.yml` on the self-hosted **L4 Pipeline** agent pool. The agent operates on local disk only — network/shared drives are copy destinations, never the agent's working directory.

Pipeline steps: install dependencies → run tests → publish JUnit results → run `main.py`. Secrets come from the `etl-sql-credentials` Variable Group and are explicitly mapped under each step's `env:` block.

---

## Known Gotchas

- **OneDrive/SharePoint sync corrupts `.git`.** Keep the repo outside any synced folder.
- **`pyodbc` needs a system-level ODBC driver** (17 or 18) installed separately on every machine and on the pipeline agent — `pip install pyodbc` alone is not enough.
- **Variable Group secrets must be explicitly mapped** under `env:` in pipeline YAML, or the running script won't see them.
- **The L4 agent runs on local disk only** — never point the agent's working directory at a network share.
