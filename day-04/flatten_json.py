def flatten(record, prefix=""):
    flat = {}
    for key, value in record.items():
        full_key = f"{prefix}{key}"
        if value == {}:
            flat[full_key] = None
        elif isinstance(value, dict):
            flat.update(flatten(value, prefix=f"{full_key}."))
        else:
            flat[full_key] = value
    return flat


def flatten_all(records, columns, defaults=None):
    defaults = defaults or {}
    rows = []
    for record in records:
        flat = flatten(record)
        row = {}
        for column in columns:
            value = flat.get(column)
            row[column] = defaults.get(column) if value is None else value
        rows.append(row)
    return rows
