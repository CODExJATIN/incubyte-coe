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


def test_ignores_an_unexpected_new_line_field():
    order = {
        "order_id": "1004",
        "customer": {"name": "Kabir", "email": "kabir@example.com"},
        "items": [{"sku": "D9", "qty": 3, "gift_wrap": True}],
    }

    _, line_rows = split_order(order)

    assert line_rows == [{"order_id": "1004", "sku": "D9", "qty": 3}]


def test_keeps_an_order_with_an_empty_items_array_and_gives_it_no_lines():
    order = {
        "order_id": "1005",
        "customer": {"name": "Zoya", "email": "zoya@example.com"},
        "items": [],
    }

    order_row, line_rows = split_order(order)

    assert order_row == {
        "order_id": "1005",
        "customer.name": "Zoya",
        "customer.email": "zoya@example.com",
    }
    assert line_rows == []


def test_keeps_an_order_with_no_items_field_and_gives_it_no_lines():
    order = {"order_id": "1006", "customer": {"name": "Kabir", "email": "kabir@example.com"}}

    order_row, line_rows = split_order(order)

    assert order_row["order_id"] == "1006"
    assert line_rows == []


def test_keeps_an_order_whose_items_are_null_and_gives_it_no_lines():
    order = {"order_id": "1007", "customer": {"name": "Ira", "email": "ira@example.com"}, "items": None}

    order_row, line_rows = split_order(order)

    assert order_row["order_id"] == "1007"
    assert line_rows == []


def test_skips_a_line_that_is_not_an_object_and_keeps_the_rest():
    order = {"order_id": "1008", "items": [None, "junk", {"sku": "E5", "qty": 1}]}

    _, line_rows = split_order(order)

    assert line_rows == [{"order_id": "1008", "sku": "E5", "qty": 1}]
