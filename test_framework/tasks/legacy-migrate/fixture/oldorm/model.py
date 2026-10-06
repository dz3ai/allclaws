"""oldorm.model — Model base + ValidationError (0.x API)."""


class ValidationError(Exception):
    """Raised by Model.validate when data violates the Meta rules."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class Model:
    """0.x active-record-ish base.

    Subclasses declare a `class Meta:` with any of:
        table     -- storage table name (required for persistence)
        pk        -- primary-key field name (upsert identity)
        ordering  -- default order as a list of field-name strings,
                     "-" prefix means descending
        required  -- iterable of field names that must be present and not None
        types     -- {field: type} map; bool never satisfies int/float/str
        hooks     -- {"before_save": cb, "after_save": cb}; each callback has
                     the 0.x signature `def cb(instance, old)` where `old` is
                     the previous persisted dict or None on first save
    """

    def __init__(self, **fields):
        self._fields = dict(fields)
        for key, value in self._fields.items():
            setattr(self, key, value)

    def __setattr__(self, name, value):
        """Keep declared-field writes in sync with the _fields store, so a
        hydrated instance mutated via attributes saves its new values."""
        object.__setattr__(self, name, value)
        fields = self.__dict__.get("_fields")
        if fields is not None and name in fields:
            fields[name] = value

    @classmethod
    def _meta(cls):
        return getattr(cls, "Meta", None)

    @classmethod
    def _meta_get(cls, name, default=None):
        return getattr(cls._meta(), name, default)

    @classmethod
    def validate(cls, data):
        """Check `data` against Meta.required/Meta.types and build an instance.

        0.x behavior: unknown keys are silently IGNORED; int values are
        coerced to float for float-typed fields.
        """
        errors = []
        clean = dict(data)
        for field in cls._meta_get("required", ()):
            if clean.get(field) is None:
                errors.append(f"{field} is required")
        types = cls._meta_get("types", {}) or {}
        for field, expected in types.items():
            value = clean.get(field)
            if value is None:
                continue
            if expected is float and isinstance(value, int) and not isinstance(value, bool):
                clean[field] = float(value)
            elif isinstance(value, bool) or not isinstance(value, expected):
                errors.append(f"{field} must be {expected.__name__}")
        if errors:
            raise ValidationError(errors)
        return cls(**clean)

    def dict(self):
        """Return a shallow dict copy of the instance fields (0.x API)."""
        return dict(self._fields)

    @classmethod
    def _from_row(cls, row):
        return cls(**row)

    def _pk_field(self):
        pk = self._meta_get("pk")
        if not pk:
            raise ValueError(f"{type(self).__name__} declares no Meta.pk")
        return pk

    def _hooks(self):
        return self._meta_get("hooks", {}) or {}
