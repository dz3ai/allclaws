"""inventory.reports — aggregate views over the stores (oldorm 0.x API)."""

from oldorm import Session

from .models import Item, Order


def stock_valuation():
    """Units and value across all skus."""
    rows = [item.dict() for item in Session("memory://").query(Item).all()]
    return {
        "skus": len(rows),
        "units": sum(r["qty"] for r in rows),
        "value": round(sum(r["qty"] * r["price"] for r in rows), 2),
    }


def open_order_units():
    """Total ordered units across orders that are still open."""
    return sum(
        order.qty
        for order in Session("memory://").query(Order).all()
        if order.status == "open"
    )
