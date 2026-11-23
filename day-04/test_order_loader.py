import duckdb
import pytest

from order_loader import load_orders, reconcile


@pytest.fixture
def db():
    connection = duckdb.connect()
    yield connection
    connection.close()


def some_orders():
    return [
        {
            "order_id": "1001",
            "customer": {"name": "Asha", "email": "asha@example.com"},
            "items": [{"sku": "A1", "qty": 2}, {"sku": "A2", "qty": 1}],
        },
        {
            "order_id": "1002",
            "customer": {"name": "Ravi"},
            "items": [{"sku": "B7", "qty": 1}],
        },
        {
            "order_id": "1005",
            "customer": {"name": "Zoya", "email": "zoya@example.com"},
            "items": [],
        },
    ]


def test_loads_one_row_per_order_and_one_row_per_line(db):
    load_orders(db, some_orders())

    assert db.execute("select count(*) from orders").fetchone()[0] == 3
    assert db.execute("select count(*) from order_lines").fetchone()[0] == 3


def test_joining_lines_back_to_orders_loses_no_order_and_no_line(db):
    load_orders(db, some_orders())

    assert reconcile(db) == {
        "orders": 3,
        "orders_after_join": 3,
        "lines": 3,
        "lines_after_join": 3,
    }
