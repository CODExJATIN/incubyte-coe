from order_splitter import split_order


def test_splits_an_order_into_an_order_row_and_line_rows_linked_by_order_id():
    order = {
        "order_id": "1001",
        "customer": {"name": "Asha", "email": "asha@example.com"},
        "items": [{"sku": "A1", "qty": 2}],
    }

    order_row, line_rows = split_order(order)

    assert order_row == {
        "order_id": "1001",
        "customer.name": "Asha",
        "customer.email": "asha@example.com",
    }
    assert line_rows == [{"order_id": "1001", "sku": "A1", "qty": 2}]


def test_fills_a_missing_order_field_with_null():
    order = {
        "order_id": "1002",
        "customer": {"name": "Ravi"},
        "items": [{"sku": "B7", "qty": 1}],
    }

    order_row, _ = split_order(order)

    assert order_row == {"order_id": "1002", "customer.name": "Ravi", "customer.email": None}


def test_ignores_an_unexpected_new_order_field():
    order = {
        "order_id": "1003",
        "customer": {"name": "Meera", "email": "meera@example.com"},
        "coupon": "DIWALI",
        "items": [{"sku": "C3", "qty": 1}],
    }

    order_row, _ = split_order(order)

    assert order_row == {
        "order_id": "1003",
        "customer.name": "Meera",
        "customer.email": "meera@example.com",
    }
