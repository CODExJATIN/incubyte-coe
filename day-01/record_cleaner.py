from datetime import datetime


def clean_record(raw: dict) -> dict:
    cleaned = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in raw.items()
    }
    if not cleaned.get("id"):
        raise ValueError("id is required")
    if "/" in cleaned["signup_date"]:
        cleaned["signup_date"] = (
            datetime.strptime(cleaned["signup_date"], "%d/%m/%Y").date().isoformat()
        )
    return cleaned
