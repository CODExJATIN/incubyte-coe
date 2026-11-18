# incubyte-coe

Day-by-day Python and SQL practice. Runs entirely on your machine: Python 3.14, uv, Git and DuckDB 2.0.

## Setup

```bash
uv sync          # creates .venv and installs duckdb, pandas, pytest, ipython
```

The DuckDB console (`duckdb`, v2.0.0) is installed separately at `~/.local/bin/duckdb`.
Keep it on the same version as the Python package.

## Layout

```
incubyte-coe/
├── day-01/                      Python, test-first with pytest
│   ├── record_cleaner.py        clean_record(): trim fields, normalise a date, reject a missing id
│   └── test_record_cleaner.py   the tests (written first)
├── day-02/                      SQL with DuckDB
│   ├── sql/
│   │   ├── joins.sql            inner / left / full / anti / semi joins
│   │   ├── window_functions.sql ranking, running totals, lag, moving averages, QUALIFY
│   │   └── set_operators.sql    UNION, UNION ALL, INTERSECT, EXCEPT, UNION BY NAME
│   └── duckdb_practice.py       runs the SQL files from Python + Python/pandas examples
└── README.md
```

Every SQL file creates its own small tables, so each one runs on its own with no extra data files.

## Day 01: record cleaner (TDD)

```bash
uv run pytest day-01 -v              # red → make it green
uv run pytest day-01 -k trim -v      # one behaviour at a time: trim, id, date
```

## Day 02: SQL

```bash
duckdb -c ".read day-02/sql/joins.sql"        # in the console
duckdb                                        # interactive; then: .read day-02/sql/joins.sql
uv run day-02/duckdb_practice.py              # the same files, run from Python
uv run day-02/duckdb_practice.py joins        # just one file
```

Console tips: `.tables`, `.schema`, `.mode line`, `.timer on`, `.help`, `.quit`.
