from flatten_json import flatten


def test_joins_nested_keys_with_a_dot():
    record = {"id": 1, "customer": {"name": "Asha"}}

    assert flatten(record) == {"id": 1, "customer.name": "Asha"}
