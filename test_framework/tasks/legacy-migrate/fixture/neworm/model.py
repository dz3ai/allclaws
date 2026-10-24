"""neworm.model — Model base, Snapshot, ValidationError (2.x API)."""


class ValidationError(Exception):
    """Raised by Model.model_validate when data violates the config rules."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


class Snapshot:
    """Immutable view of the previous persisted state, handed to hooks.

    2.x BREAKING change vs 0.x: hooks used to receive a plain dict or None;
    they now receive a Snapshot that is never None — empty on first save.
    `.as_dict()` gives the old dict form.
    """

    def __init__(self, fields=None):
        self._fields = dict(fields) if fields else {}

    def as_dict(self):
        return dict(self._fields)

    @property
    def is_new(self):
        return not self._fields

    def __bool__(self):
        return bool(self._fields)

    def __contains__(self, key):
        return key in self._fields

    def __getitem__(self, key):
        return self._fields[key]

    def __repr__(self):
        return f"Snapshot({self._fields!r})"


class Model:
    """2.x base.

    Subclasses declare `class Config:` (structural: `table`, and the
    `order_by(M)` callable returning asc()/desc() specs — default ordering)
    plus a `model_config` dict (`pk`, `required`, `types`, and `hooks`).
    Hook callbacks use the 2.x signature
    `def cb(instance, previous_state)`.
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
    def _model_config(cls):
        return dict(getattr(cls, "model_config", {}) or {})

    @classmethod
    def model_validate(cls, data):
        """Check `data` against model_config rules and build an instance.

        2.x BREAKING change vs 0.x: unknown keys raise ValidationError
        instead of being silently ignored. int values are still coerced to
        float for float-typed fields.
        """
        errors = []
        clean = dict(data)
        cfg = cls._model_config()
        required = cfg.get("required", ()) or ()
        types = cfg.get("types", {}) or {}
        for field in required:
            if clean.get(field) is None:
                errors.append(f"{field} is required")
        for field, expected in types.items():
            value = clean.get(field)
            if value is None:
                continue
            if expected is float and isinstance(value, int) and not isinstance(value, bool):
                clean[field] = float(value)
            elif isinstance(value, bool) or not isinstance(value, expected):
                errors.append(f"{field} must be {expected.__name__}")
        unknown = sorted(set(clean) - set(types))
        if unknown:
            errors.append("unknown field(s): " + ", ".join(unknown))
        if errors:
            raise ValidationError(errors)
        return cls(**clean)

    def model_dump(self):
        """Return a shallow dict copy of the instance fields (2.x API)."""
        return dict(self._fields)

    @classmethod
    def _from_row(cls, row):
        return cls(**row)

    def _pk_field(self):
        pk = self._model_config().get("pk")
        if not pk:
            raise ValueError(f"{type(self).__name__} declares no model_config pk")
        return pk

    def _hooks(self):
        return self._model_config().get("hooks", {}) or {}

    @classmethod
    def _default_order(cls):
        order_by = getattr(getattr(cls, "Config", None), "order_by", None)
        return list(order_by(cls)) if order_by else []
