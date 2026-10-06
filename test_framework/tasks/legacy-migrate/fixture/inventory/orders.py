"""inventory.orders — order lifecycle (oldorm 0.x API)."""

import itertools

from oldorm import Session

from . import warehouse
from .models import Order

_order_ids = itertools.count(1)


class UnknownOrder(LookupError):
    pass


class AlreadyFulfilled(LookupError):
    pass


def _session():
    return Session("memory://")


def reset():
    """Restart the oid sequence (test helper, called by inventory.reset)."""
    global _order_ids
    _order_ids = itertools.count(1)


def create_order(sku, qty):
    """Open an order against a known sku. Returns the order dict."""
    warehouse.get_stock(sku)
    if qty <= 0:
        raise ValueError("qty must be positive")
    order = Order.validate(
        {"oid": f"ORD-{next(_order_ids):04d}", "sku": sku, "qty": qty, "status": "open"}
    )
    _session().save(order)
    return order.dict()


def fulfill_order(oid):
    """Ship an open order: decrement stock, mark fulfilled. Idempotent-no."""
    session = _session()
    order = session.query(Order).filter(oid=oid).first()
    if order is None:
        raise UnknownOrder(oid)
    if order.status == "fulfilled":
        raise AlreadyFulfilled(oid)
    warehouse.issue_stock(order.sku, order.qty)
    order.status = "fulfilled"
    session.save(order)
    return order.dict()


def list_orders():
    """All orders, in the default Meta.ordering (oid ascending)."""
    return [order.dict() for order in _session().query(Order).all()]


def order_ledger():
    """All orders, newest first (explicit descending order)."""
    return [order.dict() for order in _session().query(Order).order_by("-oid").all()]
