import sys
from pathlib import Path

import duckdb

SQL_DIR = Path(__file__).resolve().parent / "sql"


def statements(sql: str) -> list[str]:
    return [stmt.strip() for stmt in sql.split(";") if stmt.strip()]


def run_sql_file(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    print(f"\n=== {path.name} ===")
    for stmt in statements(path.read_text()):
        result = con.sql(stmt)
        if result is not None:
            result.show()


def python_examples(con: duckdb.DuckDBPyConnection) -> None:
    print("\n=== Python ↔ DuckDB ===")

    rows = con.sql("SELECT city, sum(revenue) FROM sales GROUP BY city ORDER BY 2 DESC").fetchall()
    best_city, best_total = rows[0]
    print(f"Best city: {best_city} ({best_total})")

    df = con.sql("SELECT * FROM sales").df()
    print(f"DataFrame shape: {df.shape}")

    duckdb.sql("SELECT city, max(revenue) AS best_month FROM df GROUP BY city ORDER BY city").show()

    city = "Pune"
    total = con.execute("SELECT sum(revenue) FROM sales WHERE city = ?", [city]).fetchall()[0][0]
    print(f"{city} total via parameter: {total}")


def main() -> None:
    wanted = sys.argv[1:]
    files = sorted(SQL_DIR.glob("*.sql"))
    if wanted:
        files = [f for f in files if f.stem in wanted]
        if not files:
            sys.exit(f"No SQL file named {wanted}. Choose from: {[f.stem for f in SQL_DIR.glob('*.sql')]}")

    con = duckdb.connect()
    for path in files:
        run_sql_file(con, path)

    if not wanted:
        python_examples(con)


if __name__ == "__main__":
    main()
