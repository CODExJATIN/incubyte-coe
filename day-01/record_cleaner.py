from datetime import datetime

DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d %b %Y")


def clean_record(raw: dict) -> dict:
    cleaned = {key: _strip(value) for key, value in raw.items()}
    if not cleaned.get("id"):
        raise ValueError("id is required")
    cleaned["signup_date"] = _to_iso_date(cleaned.get("signup_date"))
    return cleaned


def _strip(value):
    return value.strip() if isinstance(value, str) else value


def _to_iso_date(text: str) -> str:
    if text is None:
        raise ValueError("signup_date is required")
    if not isinstance(text, str):
        raise ValueError(f"signup_date {text!r} is not text")
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(text, date_format).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"signup_date {text!r} is not a recognised date")
