import os
import re
import pandas as pd
from sqlalchemy import create_engine, text

STATEMENT_KEYWORDS = r"DROP|SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|TRUNCATE|WITH|MERGE|EXEC"

def sql_file_to_csv(conn_str, sql_filepath, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    engine = create_engine(conn_str)
    with open(sql_filepath) as f:
        raw = f.read()
        raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)  # strip /* block comments */
        raw = re.sub(r"(?m)--.*$", "", raw)  # strip -- line comments
        split_pattern = rf"(?mi)^(?=\s{{0,3}}(?:{STATEMENT_KEYWORDS})\b)"
        statements = [q.strip() for q in re.split(split_pattern, raw) if q.strip()]

    with engine.connect() as conn:
        csv_count = 0
        for i, stmt in enumerate(statements, start=1):
            is_select_into = bool(re.match(r"(?is)^select\b(?:(?!\bfrom\b).)*\binto\b", stmt))
            is_query = stmt.lower().startswith("select") and not is_select_into
            print(f"[{i}] {'SELECT' if is_query else 'EXEC'}: {stmt[:60]!r}")
            if is_query:
                df = pd.read_sql(text(stmt), conn)
                csv_count += 1
                df.to_csv(f"{output_folder}/output_{csv_count}.csv", index=False)
            else:
                conn.execute(text(stmt))
        conn.commit()
        print(f"Total statements: {len(statements)}, CSVs created: {csv_count}")