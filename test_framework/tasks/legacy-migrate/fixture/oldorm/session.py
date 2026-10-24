"""oldorm.session — Session facade over the shared store (0.x API)."""

from . import store
from .query import Query


class Session:
    """0.x session. Stateless facade; all sessions share the in-memory store."""

    def __init__(self, url="memory://"):
        self.url = url

    def query(self, model):
        return Query(model, store.table(model._meta_get("table")))

    def save(self, instance):
        """Upsert the instance keyed by its Meta.pk; dispatch hooks.

        Hook callbacks use the 0.x signature `def cb(instance, old)` where
        `old` is a dict copy of the previous persisted state, or None when
        the instance is saved for the first time.
        """
        model = type(instance)
        pk = instance._pk_field()
        table = store.table(model._meta_get("table"))
        key = instance._fields[pk]
        previous = table.get(key)
        old = dict(previous) if previous is not None else None
        hooks = instance._hooks()
        before = hooks.get("before_save")
        if before:
            before(instance, old)
        table[key] = dict(instance._fields)
        after = hooks.get("after_save")
        if after:
            after(instance, old)
        return instance
