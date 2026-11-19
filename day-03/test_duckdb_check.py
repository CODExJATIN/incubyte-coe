import duckdb

from order_checks import load_orders_table


def test_loads_every_row_of_the_clean_file_into_an_orders_table(clean_sample_csv):
    connection = duckdb.connect()

    load_orders_table(connection, clean_sample_csv)

    assert connection.execute("select count(*) from orders").fetchone()[0] == 4
