import duckdb
import pytest

from order_checks import load_orders_table, order_counts


@pytest.fixture
def orders_db(clean_sample_csv):
    connection = duckdb.connect()
    load_orders_table(connection, clean_sample_csv)
    yield connection
    connection.close()


def test_loads_every_row_of_the_clean_file_into_an_orders_table(orders_db):
    assert orders_db.execute("select count(*) from orders").fetchone()[0] == 4


def test_loads_orders_with_explicit_column_types(orders_db):
    column_types = dict(orders_db.execute("select column_name, column_type from (describe orders)").fetchall())

    assert column_types == {
        "order_id": "VARCHAR",
        "customer": "VARCHAR",
        "order_date": "DATE",
        "amount": "DECIMAL(10,2)",
    }


def test_counts_rows_distinct_ids_and_missing_dates(orders_db):
    assert order_counts(orders_db) == {"rows": 4, "distinct_ids": 4, "missing_dates": 0}
