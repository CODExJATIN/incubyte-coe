import pytest

from order_cleaner import normalise_date, remove_duplicates


def an_order(**overrides):
    return {
        "order_id": "1001",
        "customer": "Asha",
        "order_date": "2025-01-12",
        "amount": "250.00",
        **overrides,
    }


def test_keeps_the_first_order_when_an_id_repeats():
    first = an_order(amount="250.00")
    repeat = an_order(amount="999.00")

    assert remove_duplicates([first, repeat]) == [first]


@pytest.mark.parametrize(
    "ids, kept_ids",
    [
        pytest.param(["1001", "1001"], ["1001"], id="repeat"),
        pytest.param(["1001", "1002"], ["1001", "1002"], id="all-different"),
        pytest.param(["1001", "1002", "1001"], ["1001", "1002"], id="not-adjacent"),
        pytest.param(["1001", " 1001 "], ["1001"], id="differ-only-by-spaces"),
    ],
)
def test_removes_duplicate_ids(ids, kept_ids):
    orders = [an_order(order_id=order_id) for order_id in ids]

    kept = remove_duplicates(orders)

    assert [order["order_id"] for order in kept] == kept_ids


def test_leaves_an_iso_date_unchanged():
    assert normalise_date("2025-01-12") == "2025-01-12"


def test_converts_a_day_first_slash_date_to_iso():
    assert normalise_date("12/01/2025") == "2025-01-12"


def test_converts_a_month_name_date_to_iso():
    assert normalise_date("12 Jan 2025") == "2025-01-12"
