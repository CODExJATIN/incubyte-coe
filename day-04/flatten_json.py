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
