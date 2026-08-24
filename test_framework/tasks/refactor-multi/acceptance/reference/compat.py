"""invcalc.compat — helpers shared across modules (dict/model duck-typing)."""


def record_get(record, key, default=None):
    """Read a field from a plain dict OR a model object with attributes."""
    if isinstance(record, dict):
        return record.get(key, default)
    return getattr(record, key, default)


def record_as_dict(record):
    """Normalize a record (dict or to_dict()-capable model) to a dict."""
    if isinstance(record, dict):
        return dict(record)
    if hasattr(record, "to_dict"):
        return record.to_dict()
    if hasattr(record, "_asdict"):
        return dict(record._asdict())
    return dict(vars(record))
