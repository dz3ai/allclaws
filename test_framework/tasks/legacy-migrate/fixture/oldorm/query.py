"""oldorm.query — Query builder (0.x API)."""


class Query:
    """Lazy query over one table's rows (row = plain dict).

    Default ordering comes from Meta.ordering (list of field-name strings,
    "-" prefix = descending). `.order_by(*fields)` overrides it with the
    same string form.
    """

    def __init__(self, model, rows):
        self._model = model
        self._rows = [dict(r) for r in rows.values()]
        self._order = list(model._meta_get("ordering", []) or [])

    def filter(self, **eq):
        self._rows = [
            r for r in self._rows if all(r.get(k) == v for k, v in eq.items())
        ]
        return self

    def order_by(self, *fields):
        self._order = list(fields)
        return self

    def all(self):
        rows = self._rows
        for spec in reversed(self._order):
            descending = spec.startswith("-")
            key = spec.lstrip("-")
            rows = sorted(rows, key=lambda r: r[key], reverse=descending)
        return [self._model._from_row(dict(r)) for r in rows]

    def first(self):
        rows = self.all()
        return rows[0] if rows else None

    def count(self):
        return len(self._rows)
