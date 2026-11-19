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
