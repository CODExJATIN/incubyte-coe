from datetime import datetime


def clean_record(raw: dict) -> dict:
    cleaned = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in raw.items()
    }
    if not cleaned.get("id"):
        raise ValueError("id is required")
    for date_format in ("%d/%m/%Y", "%d %b %Y"):
        try:
            cleaned["signup_date"] = (
                datetime.strptime(cleaned["signup_date"], date_format).date().isoformat()
            )
            break
        except ValueError:
            pass
    return cleaned
