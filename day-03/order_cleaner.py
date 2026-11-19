from datetime import datetime


def remove_duplicates(orders):
    seen_ids = set()
    unique_orders = []
    for order in orders:
        order_id = order["order_id"].strip()
        if order_id not in seen_ids:
            seen_ids.add(order_id)
            unique_orders.append(order)
    return unique_orders


DATE_FORMAT_BY_SEPARATOR = {"-": "%Y-%m-%d", "/": "%d/%m/%Y", " ": "%d %b %Y"}


def normalise_date(raw_date):
    trimmed_date = raw_date.strip()
    for separator, date_format in DATE_FORMAT_BY_SEPARATOR.items():
        if separator in trimmed_date:
            return datetime.strptime(trimmed_date, date_format).date().isoformat()
    raise ValueError(f"unreadable date: {raw_date!r}")


def clean_orders(orders):
    cleaned_orders = []
    for order in orders:
        order = {field: value.strip() for field, value in order.items()}
        if not order["order_id"].strip():
            continue
        try:
            order_date = normalise_date(order["order_date"])
        except ValueError:
            continue
        cleaned_orders.append({**order, "order_date": order_date})
    return cleaned_orders
