def remove_duplicates(orders):
    seen_ids = set()
    unique_orders = []
    for order in orders:
        if order["order_id"] not in seen_ids:
            seen_ids.add(order["order_id"])
            unique_orders.append(order)
    return unique_orders
