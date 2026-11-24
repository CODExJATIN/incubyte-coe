from flatten_json import build_row, flatten

ORDER_COLUMNS = ["order_id", "customer.name", "customer.email"]
LINE_COLUMNS = ["order_id", "sku", "qty"]


def split_order(order):
    header = {key: value for key, value in order.items() if key != "items"}
    order_row = build_row(flatten(header), ORDER_COLUMNS, {})
    line_rows = [
        build_row({"order_id": order["order_id"], **flatten(item)}, LINE_COLUMNS, {})
        for item in order.get("items") or []
        if isinstance(item, dict)
    ]
    return order_row, line_rows
