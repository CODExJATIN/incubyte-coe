def load_orders_table(connection, csv_path):
    connection.execute("create table orders as select * from read_csv(?)", [str(csv_path)])
