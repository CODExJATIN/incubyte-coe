from pathlib import Path

import duckdb

DATA = Path(__file__).resolve().parent.parent / "data"


def test_delivered_revenue_by_city():
    rows = duckdb.sql(f"""
        SELECT c.city, sum(o.amount) AS revenue
        FROM '{DATA / "orders.csv"}' o
        JOIN '{DATA / "customers.csv"}' c USING (customer_id)
        WHERE o.status = 'delivered'
        GROUP BY c.city
    """).fetchall()
    assert dict(rows)["Pune"] == 1650.50


def test_duckdb_to_pandas_roundtrip():
    df = duckdb.sql(f"SELECT * FROM '{DATA / "customers.csv"}'").df()
    assert len(df) == 5
    assert duckdb.sql("SELECT count(*) FROM df").fetchall()[0][0] == 5
