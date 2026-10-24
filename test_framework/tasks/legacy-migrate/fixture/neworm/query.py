"""neworm.query — Select builder + ordering specs (2.x API)."""

from typing import NamedTuple


class OrderSpec(NamedTuple):
    field: str
    descending: bool


def asc(field):
    """Ascending order spec (replaces the 0.x "field" string)."""
    return OrderSpec(field, False)


def desc(field):
    """Descending order spec (replaces the 0.x "-field" string)."""
    return OrderSpec(field, True)


class Select:
    """Lazy query over one table's rows (row = plain dict).

    Default ordering comes from Config.order_by(M) — a callable returning a
    list of asc()/desc() specs. `.order_by(*specs)` overrides it.
    """

    def __init__(self, model, rows):
        self._model = model
        self._rows = [dict(r) for r in rows.values()]
        self._order = list(model._default_order())

    def where(self, **eq):
        self._rows = [
            r for r in self._rows if all(r.get(k) == v for k, v in eq.items())
        ]
        return self

    def order_by(self, *specs):
        for spec in specs:
            if not isinstance(spec, OrderSpec):
                raise TypeError(
                    "order_by takes asc()/desc() specs, got "
                    f"{spec!r} — the 0.x string form is gone in 2.x"
                )
        self._order = list(specs)
        return self

    def all(self):
        rows = self._rows
        for spec in reversed(self._order):
            rows = sorted(rows, key=lambda r: r[spec.field], reverse=spec.descending)
        return [self._model._from_row(dict(r)) for r in rows]

    def first(self):
        rows = self.all()
        return rows[0] if rows else None

    def count(self):
        return len(self._rows)
