import pytest

from record_cleaner import clean_record


def a_record(**overrides):
    record = {"id": "42", "name": "Asha", "city": "Pune", "signup_date": "2025-01-12"}
    record.update(overrides)
    return record


def test_does_not_modify_the_input_record():
    raw = a_record(name="  Asha  ")

    clean_record(raw)

    assert raw["name"] == "  Asha  "


def test_trims_whitespace_from_every_text_field():
    raw = a_record(id="  42 ", name="  Asha  ", city="\tPune\n")

    cleaned = clean_record(raw)

    assert cleaned["id"] == "42"
    assert cleaned["name"] == "Asha"
    assert cleaned["city"] == "Pune"


def test_rejects_a_record_with_no_id_key():
    raw = a_record()
    del raw["id"]

    with pytest.raises(ValueError, match="id"):
        clean_record(raw)


@pytest.mark.parametrize("bad_id", ["", "   ", None])
def test_rejects_a_blank_id(bad_id):
    with pytest.raises(ValueError, match="id"):
        clean_record(a_record(id=bad_id))
