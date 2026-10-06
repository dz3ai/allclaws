"""oldorm.store — shared in-memory table storage (0.x)."""

_TABLES: dict = {}


def table(name):
    """Return (creating if needed) the dict row-store for a table name."""
    return _TABLES.setdefault(name, {})


def reset_all():
    """Drop every table. Test/driver helper — not part of the 0.x ORM API."""
    _TABLES.clear()
