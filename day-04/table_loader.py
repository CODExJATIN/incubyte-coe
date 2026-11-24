def load_table(connection, table_name, rows, column_types):
    columns = list(column_types)
    column_definitions = ", ".join(f'"{column}" {column_types[column]}' for column in columns)
    connection.execute(f'create table "{table_name}" ({column_definitions})')
    if not rows:
        return
    placeholders = ", ".join("?" for _ in columns)
    connection.executemany(
        f'insert into "{table_name}" values ({placeholders})',
        [[row[column] for column in columns] for row in rows],
    )
