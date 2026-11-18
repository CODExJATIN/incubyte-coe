def clean_record(raw: dict) -> dict:
    return {key: value.strip() for key, value in raw.items()}
