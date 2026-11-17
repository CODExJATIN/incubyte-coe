# data-craft

Lightweight local playground for practising SQL and Python with DuckDB.
No servers, no Docker — just Python 3.14, uv, Git and DuckDB 2.0.

## Setup (fresh clone)

```bash
uv sync          # creates .venv and installs duckdb, pandas, pytest, ipython
uv run pytest    # smoke tests
```

## Layout

| Path | Purpose |
|------|---------|
| `data/` | CSV / Parquet files to query (`*.duckdb` files are git-ignored) |
| `sql/` | Practice SQL scripts |
| `scripts/sql.py` | Small DuckDB runner / REPL |
| `tests/` | pytest checks for your Python + SQL |

## Practising SQL

```bash
uv run scripts/sql.py                       # interactive prompt, end with ;
uv run scripts/sql.py sql/01_basics.sql     # run a file
uv run scripts/sql.py -c "SELECT * FROM 'data/orders.csv'"
uv run scripts/sql.py --memory ...          # throwaway in-memory DB
```

By default it uses `data/craft.duckdb`, so tables you `CREATE` persist.
DuckDB reads CSV/Parquet/JSON files directly: `SELECT * FROM 'data/x.csv'`.

## Practising Python

```bash
uv run ipython
```

```python
import duckdb
df = duckdb.sql("SELECT * FROM 'data/orders.csv'").df()   # -> pandas
duckdb.sql("SELECT status, sum(amount) FROM df GROUP BY 1").show()  # query a DataFrame
```

Note: DuckDB 2.0 relations have no `fetchone()`; use `.fetchall()` or `.df()`.

Add packages with `uv add <pkg>` (e.g. `uv add polars matplotlib jupyterlab`).
