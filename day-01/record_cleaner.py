def clean_record(raw: dict) -> dict:
    cleaned = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in raw.items()
    }
    if not cleaned.get("id"):
        raise ValueError("id is required")
    return cleaned
