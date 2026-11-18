def clean_record(raw: dict) -> dict:
    if not raw.get("id"):
        raise ValueError("id is required")
    return {key: value.strip() for key, value in raw.items()}
