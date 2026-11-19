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


DATE_FORMAT_BY_SEPARATOR = {"/": "%d/%m/%Y", " ": "%d %b %Y"}


def normalise_date(raw_date):
    for separator, date_format in DATE_FORMAT_BY_SEPARATOR.items():
        if separator in raw_date:
            return datetime.strptime(raw_date, date_format).date().isoformat()
    return raw_date
