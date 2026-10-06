"""neworm.session — Session facade over the shared store (2.x API)."""

from . import store
from .model import Snapshot
from .query import Select


class Session:
    """2.x session. Stateless facade; all sessions share the in-memory store."""

    def __init__(self, url="memory://"):
        self.url = url

    def select(self, model):
        config = getattr(model, "Config", None)
        return Select(model, store.table(getattr(config, "table", None)))

    def persist(self, instance):
        """Upsert the instance keyed by its model_config pk; dispatch hooks.

        Hook callbacks use the 2.x signature `def cb(instance,
        previous_state)` where previous_state is a Snapshot of the previous
        persisted state (never None; empty on first save).
        """
        model = type(instance)
        pk = instance._pk_field()
        config = getattr(model, "Config", None)
        table = store.table(getattr(config, "table", None))
        key = instance._fields[pk]
        previous = table.get(key)
        state = Snapshot(previous)
        hooks = instance._hooks()
        before = hooks.get("before_save")
        if before:
            before(instance, state)
        table[key] = dict(instance._fields)
        after = hooks.get("after_save")
        if after:
            after(instance, state)
        return instance
