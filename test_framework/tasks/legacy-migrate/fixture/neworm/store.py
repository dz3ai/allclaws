"""neworm.store — shared in-memory table storage (2.x)."""

_TABLES: dict = {}


def table(name):
    """Return (creating if needed) the dict row-store for a table name."""
    return _TABLES.setdefault(name, {})


def reset_all():
    """Drop every table. Test/driver helper — not part of the 2.x ORM API."""
    _TABLES.clear()
