from flatten_json import flatten, flatten_all


def test_joins_nested_keys_with_a_dot():
    record = {"id": 1, "customer": {"name": "Asha"}}

    assert flatten(record) == {"id": 1, "customer.name": "Asha"}


def test_joins_keys_from_several_levels_deep():
    record = {"customer": {"address": {"city": "Pune"}}}

    assert flatten(record) == {"customer.address.city": "Pune"}


def test_keeps_a_null_value_instead_of_dropping_the_field():
    record = {"id": 1, "customer": None}

    assert flatten(record) == {"id": 1, "customer": None}


def test_turns_an_empty_nested_object_into_null():
    record = {"id": 1, "address": {}}

    assert flatten(record) == {"id": 1, "address": None}


def test_fills_a_column_missing_from_a_record_with_null():
    records = [
        {"id": 1, "customer": {"email": "asha@example.com"}},
        {"id": 2},
    ]

    assert flatten_all(records, columns=["id", "customer.email"]) == [
        {"id": 1, "customer.email": "asha@example.com"},
        {"id": 2, "customer.email": None},
    ]


def test_fills_a_missing_column_with_its_default_when_one_is_given():
    records = [{"id": 1}]

    assert flatten_all(
        records, columns=["id", "country", "email"], defaults={"country": "IN"}
    ) == [{"id": 1, "country": "IN", "email": None}]


def test_fills_a_null_value_with_its_default_when_one_is_given():
    records = [{"id": 1, "country": None}]

    assert flatten_all(records, columns=["id", "country"], defaults={"country": "IN"}) == [
        {"id": 1, "country": "IN"}
    ]
