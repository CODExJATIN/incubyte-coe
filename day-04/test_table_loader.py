import duckdb
import pytest

from table_loader import load_table


@pytest.fixture
def db():
    connection = duckdb.connect()
    yield connection
    connection.close()


def test_loads_every_row_into_a_table(db):
    rows = [
        {"id": 1, "customer.email": "asha@example.com"},
        {"id": 2, "customer.email": None},
    ]

    load_table(db, "customers", rows, {"id": "INTEGER", "customer.email": "VARCHAR"})

    assert db.execute("select count(*) from customers").fetchone()[0] == 2
