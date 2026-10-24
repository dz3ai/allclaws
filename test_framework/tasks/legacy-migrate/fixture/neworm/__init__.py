"""neworm 2.x — successor of oldorm (vendored, BREAKING API changes).

2.x surface (migrated from oldorm 0.x — see MIGRATION.md):

    session.select(Model) / .where(**eq) / .order_by(asc("f"), desc("g"))
    Model.model_validate(data)   (raises on UNKNOWN keys too)
    model.model_dump()
    session.persist(instance)
    class Config: (table + order_by callable)  +  model_config = {...} dict
    hook signature: def cb(instance, previous_state) — previous_state is a
    Snapshot, never None (empty on first save); .as_dict() gives the dict
"""

from .model import Model, Snapshot, ValidationError
from .query import asc, desc
from .session import Session
from .store import reset_all

__all__ = [
    "Model",
    "Session",
    "ValidationError",
    "Snapshot",
    "asc",
    "desc",
    "reset_all",
]
