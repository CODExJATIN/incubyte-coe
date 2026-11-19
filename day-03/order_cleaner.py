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


def normalise_date(raw_date):
    if "/" in raw_date:
        return datetime.strptime(raw_date, "%d/%m/%Y").date().isoformat()
    return raw_date
