from order_splitter import split_order


def test_splits_an_order_into_an_order_row_and_line_rows_linked_by_order_id():
    order = {
        "order_id": "1001",
        "customer": {"name": "Asha"},
        "items": [{"sku": "A1", "qty": 2}],
    }

    order_row, line_rows = split_order(order)

    assert order_row == {"order_id": "1001", "customer.name": "Asha"}
    assert line_rows == [{"order_id": "1001", "sku": "A1", "qty": 2}]
