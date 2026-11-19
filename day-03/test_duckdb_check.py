import duckdb

from order_checks import load_orders_table


def test_loads_every_row_of_the_clean_file_into_an_orders_table(clean_sample_csv):
    connection = duckdb.connect()

    load_orders_table(connection, clean_sample_csv)

    assert connection.execute("select count(*) from orders").fetchone()[0] == 4


def test_loads_orders_with_explicit_column_types(clean_sample_csv):
    connection = duckdb.connect()

    load_orders_table(connection, clean_sample_csv)

    column_types = dict(connection.execute("select column_name, column_type from (describe orders)").fetchall())
    assert column_types == {
        "order_id": "VARCHAR",
        "customer": "VARCHAR",
        "order_date": "DATE",
        "amount": "DECIMAL(10,2)",
    }
