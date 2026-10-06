"""inventory — warehouse stock and order tracking (oldorm 0.x edition).

Public API (behavior contract covered by tests/test_app.py):
    receive_stock / issue_stock / get_stock / list_items / low_stock
    create_order / fulfill_order / list_orders / order_ledger
    stock_valuation / open_order_units
    ValidationError, UnknownSku, InsufficientStock, UnknownOrder,
    AlreadyFulfilled
    audit.entries / audit.reset
    reset   (test helper: wipes stores + audit log + id counter)
"""

import oldorm
from oldorm import ValidationError

from . import audit
from . import orders as _orders
from .models import Item, Order
from .orders import (
    AlreadyFulfilled,
    UnknownOrder,
    create_order,
    fulfill_order,
    list_orders,
    order_ledger,
)
from .reports import open_order_units, stock_valuation
from .warehouse import (
    InsufficientStock,
    UnknownSku,
    get_stock,
    issue_stock,
    list_items,
    low_stock,
    receive_stock,
)

__all__ = [
    "Item",
    "Order",
    "ValidationError",
    "UnknownSku",
    "InsufficientStock",
    "UnknownOrder",
    "AlreadyFulfilled",
    "receive_stock",
    "issue_stock",
    "get_stock",
    "list_items",
    "low_stock",
    "create_order",
    "fulfill_order",
    "list_orders",
    "order_ledger",
    "stock_valuation",
    "open_order_units",
    "audit",
    "reset",
]

def reset():
    """Test helper: wipe stores, audit log, and the order-id counter."""
    oldorm.reset_all()
    audit.reset()
    _orders.reset()
