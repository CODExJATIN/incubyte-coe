import csv
import sys
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


ORDER_FIELDS = ["order_id", "customer", "order_date", "amount"]
DATE_FORMAT_BY_SEPARATOR = {"-": "%Y-%m-%d", "/": "%d/%m/%Y", " ": "%d %b %Y"}


def normalise_date(raw_date):
    trimmed_date = raw_date.strip()
    for separator, date_format in DATE_FORMAT_BY_SEPARATOR.items():
        if separator in trimmed_date:
            return datetime.strptime(trimmed_date, date_format).date().isoformat()
    raise ValueError(f"unreadable date: {raw_date!r}")


def trim_fields(order):
    return {field: value.strip() for field, value in order.items()}


def clean_order(order):
    trimmed_order = trim_fields(order)
    if not trimmed_order["order_id"]:
        raise ValueError("blank order_id")
    return {**trimmed_order, "order_date": normalise_date(trimmed_order["order_date"])}


def clean_orders(orders):
    cleaned_orders = []
    for order in orders:
        try:
            cleaned_orders.append(clean_order(order))
        except ValueError:
            continue
    return remove_duplicates(cleaned_orders)


def read_orders(path):
    with open(path, newline="") as file:
        return list(csv.DictReader(file))


def write_orders(orders, path):
    with open(path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=ORDER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(orders)


def clean_file(input_path, output_path):
    write_orders(clean_orders(read_orders(input_path)), output_path)


if __name__ == "__main__":
    clean_file(sys.argv[1], sys.argv[2])
