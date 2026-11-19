from order_cleaner import remove_duplicates


def test_keeps_the_first_order_when_an_id_repeats():
    orders = [
        {"order_id": "1001", "amount": "250.00"},
        {"order_id": "1001", "amount": "999.00"},
    ]

    assert remove_duplicates(orders) == [{"order_id": "1001", "amount": "250.00"}]


def test_keeps_every_order_when_ids_are_different():
    orders = [
        {"order_id": "1001", "amount": "250.00"},
        {"order_id": "1002", "amount": "99.50"},
    ]

    assert remove_duplicates(orders) == orders


def test_removes_a_duplicate_that_is_not_next_to_the_original():
    orders = [
        {"order_id": "1001", "amount": "250.00"},
        {"order_id": "1002", "amount": "99.50"},
        {"order_id": "1001", "amount": "999.00"},
    ]

    assert remove_duplicates(orders) == [
        {"order_id": "1001", "amount": "250.00"},
        {"order_id": "1002", "amount": "99.50"},
    ]


def test_treats_ids_that_differ_only_by_spaces_as_duplicates():
    orders = [
        {"order_id": "1001", "amount": "250.00"},
        {"order_id": " 1001 ", "amount": "999.00"},
    ]

    assert remove_duplicates(orders) == [{"order_id": "1001", "amount": "250.00"}]
