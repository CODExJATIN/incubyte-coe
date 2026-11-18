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
