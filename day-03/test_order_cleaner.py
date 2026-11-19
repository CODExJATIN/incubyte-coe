import pytest

from order_cleaner import clean_orders, normalise_date, read_orders, remove_duplicates, write_orders


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
        pytest.param("2025-02-30", id="impossible-day"),
        pytest.param("", id="empty"),
        pytest.param("   ", id="only-spaces"),
        pytest.param("next Tuesday", id="words-with-spaces"),
        pytest.param("2025/01/12", id="year-first-slashes"),
    ],
)
def test_rejects_an_unreadable_date(raw_date):
    with pytest.raises(ValueError):
        normalise_date(raw_date)


def test_passes_a_clean_order_through_unchanged():
    order = an_order()

    assert clean_orders([order]) == [order]


def test_normalises_the_order_date_of_every_order():
    cleaned = clean_orders([an_order(order_date="12/01/2025")])

    assert cleaned[0]["order_date"] == "2025-01-12"


def test_drops_an_order_whose_date_cannot_be_read():
    good = an_order(order_id="1001")
    unreadable = an_order(order_id="1006", order_date="next Tuesday")

    assert clean_orders([good, unreadable]) == [good]


@pytest.mark.parametrize(
    "blank_id",
    [
        pytest.param("", id="empty"),
        pytest.param("   ", id="only-spaces"),
    ],
)
def test_drops_an_order_with_a_blank_id(blank_id):
    good = an_order(order_id="1001")
    no_id = an_order(order_id=blank_id)

    assert clean_orders([good, no_id]) == [good]


def test_trims_spaces_from_every_field():
    padded = an_order(order_id=" 1004 ", customer="  Kiran ", amount=" 75 ")

    assert clean_orders([padded]) == [an_order(order_id="1004", customer="Kiran", amount="75")]


def test_removes_duplicate_ids_after_trimming():
    first = an_order(order_id="1001", amount="250.00")
    padded_repeat = an_order(order_id=" 1001 ", amount="999.00")

    assert clean_orders([first, padded_repeat]) == [first]


def test_keeps_an_order_with_an_empty_customer():
    no_customer = an_order(customer="")

    assert clean_orders([no_customer]) == [no_customer]


def test_does_not_modify_the_input_orders():
    padded = an_order(order_id=" 1004 ", order_date="12/01/2025")

    clean_orders([padded])

    assert padded == an_order(order_id=" 1004 ", order_date="12/01/2025")


@pytest.fixture
def small_csv(tmp_path):
    path = tmp_path / "orders.csv"
    path.write_text(
        "order_id,customer,order_date,amount\n"
        "1001,Asha,2025-01-12,250.00\n"
        " 1004 ,Kiran,2025-02-30,75\n"
    )
    return path


def test_reads_every_row_of_a_csv_as_a_dict_of_strings(small_csv):
    assert read_orders(small_csv) == [
        an_order(),
        an_order(order_id=" 1004 ", customer="Kiran", order_date="2025-02-30", amount="75"),
    ]


def test_writes_orders_as_a_csv_with_a_header(tmp_path):
    path = tmp_path / "clean.csv"

    write_orders([an_order()], path)

    assert path.read_text() == (
        "order_id,customer,order_date,amount\n"
        "1001,Asha,2025-01-12,250.00\n"
    )
