from flatten_json import flatten


def test_joins_nested_keys_with_a_dot():
    record = {"id": 1, "customer": {"name": "Asha"}}

    assert flatten(record) == {"id": 1, "customer.name": "Asha"}


def test_joins_keys_from_several_levels_deep():
    record = {"customer": {"address": {"city": "Pune"}}}

    assert flatten(record) == {"customer.address.city": "Pune"}


def test_keeps_a_null_value_instead_of_dropping_the_field():
    record = {"id": 1, "customer": None}

    assert flatten(record) == {"id": 1, "customer": None}
