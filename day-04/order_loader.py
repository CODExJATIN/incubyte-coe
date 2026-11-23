from order_splitter import split_order
from table_loader import load_table

ORDER_TYPES = {"order_id": "VARCHAR", "customer.name": "VARCHAR", "customer.email": "VARCHAR"}
LINE_TYPES = {"order_id": "VARCHAR", "sku": "VARCHAR", "qty": "INTEGER"}


def load_orders(connection, orders):
    order_rows = []
    line_rows = []
    for order in orders:
        order_row, lines = split_order(order)
        order_rows.append(order_row)
        line_rows.extend(lines)
    load_table(connection, "orders", order_rows, ORDER_TYPES)
    load_table(connection, "order_lines", line_rows, LINE_TYPES)


def reconcile(connection):
    orders = connection.execute("select count(*) from orders").fetchone()[0]
    lines = connection.execute("select count(*) from order_lines").fetchone()[0]
    orders_after_join, lines_after_join = connection.execute(
        """
        select count(distinct o.order_id), count(l.order_id)
        from orders o
        left join order_lines l on l.order_id = o.order_id
        """
    ).fetchone()
    return {
        "orders": orders,
        "orders_after_join": orders_after_join,
        "lines": lines,
        "lines_after_join": lines_after_join,
    }
