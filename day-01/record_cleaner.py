def clean_record(raw: dict) -> dict:
    if "id" not in raw:
        raise ValueError("id is required")
    return {key: value.strip() for key, value in raw.items()}
