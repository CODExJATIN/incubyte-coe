from pathlib import Path

import duckdb
import pytest

from order_loader import load_orders, load_orders_file, reconcile


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


SAMPLE_ORDERS_JSON = Path(__file__).parent / "orders.json"


def test_loads_the_nested_sample_file_without_losing_orders_or_lines(db):
    load_orders_file(db, SAMPLE_ORDERS_JSON)

    assert reconcile(db) == {
        "orders": 5,
        "orders_after_join": 5,
        "lines": 4,
        "lines_after_join": 4,
    }


def test_loads_empty_tables_when_there_are_no_orders(db):
    load_orders(db, [])

    assert reconcile(db) == {"orders": 0, "orders_after_join": 0, "lines": 0, "lines_after_join": 0}


def test_skips_an_order_with_no_order_id(db):
    orders = [
        {"order_id": "1001", "items": [{"sku": "A1", "qty": 2}]},
        {"customer": {"name": "Ghost"}, "items": [{"sku": "Z9", "qty": 1}]},
    ]

    load_orders(db, orders)

    assert reconcile(db) == {"orders": 1, "orders_after_join": 1, "lines": 1, "lines_after_join": 1}


def test_keeps_only_the_first_order_when_an_order_id_repeats(db):
    orders = [
        {"order_id": "1001", "items": [{"sku": "A1", "qty": 2}]},
        {"order_id": "1001", "items": [{"sku": "A9", "qty": 5}]},
    ]

    load_orders(db, orders)

    assert reconcile(db) == {"orders": 1, "orders_after_join": 1, "lines": 1, "lines_after_join": 1}
    assert db.execute("select sku from order_lines").fetchall() == [("A1",)]
