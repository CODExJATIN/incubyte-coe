def load_orders_table(connection, csv_path):
    connection.execute(
        """
        create table orders as
        select * from read_csv(?, header = true, columns = {
            'order_id': 'VARCHAR',
            'customer': 'VARCHAR',
            'order_date': 'DATE',
            'amount': 'DECIMAL(10,2)'
        })
        """,
        [str(csv_path)],
    )


def order_counts(connection):
    rows, distinct_ids, missing_dates = connection.execute(
        """
        select
            count(*),
            count(distinct order_id),
            count(*) filter (where order_date is null)
        from orders
        """
    ).fetchone()
    return {"rows": rows, "distinct_ids": distinct_ids, "missing_dates": missing_dates}
