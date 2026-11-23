from flatten_json import build_row, flatten

ORDER_COLUMNS = ["order_id", "customer.name", "customer.email"]


def split_order(order):
    header = {key: value for key, value in order.items() if key != "items"}
    order_row = build_row(flatten(header), ORDER_COLUMNS, {})
    line_rows = [{"order_id": order["order_id"], **flatten(item)} for item in order["items"]]
    return order_row, line_rows
