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


@pytest.mark.parametrize(
    "raw_date",
    [
        pytest.param("2025-01-12", id="iso"),
        pytest.param("12/01/2025", id="day-first-slashes"),
        pytest.param("12 Jan 2025", id="month-name"),
        pytest.param("  12/01/2025 ", id="surrounding-spaces"),
    ],
)
def test_normalises_a_readable_date_to_iso(raw_date):
    assert normalise_date(raw_date) == "2025-01-12"


@pytest.mark.parametrize(
    "raw_date",
    [
        pytest.param("tomorrow", id="single-word"),
        pytest.param('2025-02-30', id='impossible-day'),
        pytest.param('', id='empty'),
    ],
)
def test_rejects_an_unreadable_date(raw_date):
    with pytest.raises(ValueError):
        normalise_date(raw_date)
