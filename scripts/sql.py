"""Tiny DuckDB runner.

  uv run scripts/sql.py                 # interactive prompt (end statements with ;)
  uv run scripts/sql.py sql/01_basics.sql  # run every statement in a file
  uv run scripts/sql.py -c "SELECT 42"  # run one query

Uses a persistent database at data/craft.duckdb so tables you CREATE survive.
"""
import argparse
import os
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "craft.duckdb"


def run(con: duckdb.DuckDBPyConnection, sql: str) -> None:
    for stmt in (s.strip() for s in sql.split(";")):
        if not stmt or all(l.strip().startswith("--") or not l.strip() for l in stmt.splitlines()):
            continue
        try:
            rel = con.sql(stmt)
            if rel is not None:
                rel.show()
        except duckdb.Error as e:
            print(f"Error: {e}", file=sys.stderr)


def repl(con: duckdb.DuckDBPyConnection) -> None:
    print("DuckDB", duckdb.__version__, "| end with ';' | Ctrl-D to quit")
    buf = []
    while True:
        try:
            line = input("... " if buf else "sql> ")
        except EOFError:
            print()
            return
        buf.append(line)
        if line.rstrip().endswith(";"):
            run(con, "\n".join(buf))
            buf = []


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", nargs="?", help="SQL file to run")
    p.add_argument("-c", "--command", help="SQL string to run")
    p.add_argument("--memory", action="store_true", help="use an in-memory database")
    args = p.parse_args()

    con = duckdb.connect(":memory:" if args.memory else str(DB_PATH))
    # Resolve relative paths like 'data/orders.csv' from the project root.
    os.chdir(ROOT)

    if args.command:
        run(con, args.command)
    elif args.file:
        run(con, Path(args.file).read_text())
    else:
        repl(con)


if __name__ == "__main__":
    main()
