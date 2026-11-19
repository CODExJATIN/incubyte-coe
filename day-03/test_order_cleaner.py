from order_cleaner import remove_duplicates


def test_keeps_the_first_order_when_an_id_repeats():
    orders = [
        {"order_id": "1001", "amount": "250.00"},
        {"order_id": "1001", "amount": "999.00"},
    ]

    assert remove_duplicates(orders) == [{"order_id": "1001", "amount": "250.00"}]
