from flatten_json import flatten


def split_order(order):
    header = {key: value for key, value in order.items() if key != "items"}
    order_row = flatten(header)
    line_rows = [{"order_id": order["order_id"], **flatten(item)} for item in order["items"]]
    return order_row, line_rows
