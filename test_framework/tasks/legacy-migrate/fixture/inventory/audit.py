"""inventory.audit — oldorm hook callbacks (0.x signature).

The 0.x hook contract is `def cb(instance, old)` where `old` is the
previous persisted dict, or None when the instance is saved for the first
time.
"""

_log: list = []


def before_item_save(instance, old):
    if old is None:
        _log.append(
            {
                "event": "create",
                "kind": "item",
                "key": instance.sku,
                "before": None,
                "after": instance.qty,
            }
        )
    else:
        _log.append(
            {
                "event": "update",
                "kind": "item",
                "key": instance.sku,
                "before": old["qty"],
                "after": instance.qty,
            }
        )


def after_order_save(instance, old):
    _log.append(
        {
            "event": "order",
            "kind": "order",
            "key": instance.oid,
            "before": None if old is None else old["status"],
            "after": instance.status,
        }
    )


def entries():
    """Audit trail so far (list of dicts, oldest first)."""
    return list(_log)


def reset():
    _log.clear()
