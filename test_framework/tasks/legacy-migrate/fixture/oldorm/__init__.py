"""oldorm 0.x — tiny stdlib-only ORM (legacy API, vendored).

This is the LEGACY library of the legacy-migrate fixture. Its 0.x surface:

    Session("memory://").query(Model)      -> Query
    Query.filter(**eq) / .order_by(*fields) / .all() / .first() / .count()
    Model.validate(data)                   -> instance (raises ValidationError)
    model.dict()                           -> dict copy of the fields
    session.save(instance)                 -> upsert, dispatches hooks
    class Meta:                            -> table / pk / ordering / required /
                                                types / hooks config
    hooks signature: def cb(instance, old) — old is the previous persisted
    dict, or None on first save

Application code must migrate to the neworm 2.x API (see MIGRATION.md).
"""

from .model import Model, ValidationError
from .session import Session
from .store import reset_all

__all__ = ["Model", "Session", "ValidationError", "reset_all"]
