"""inventory.warehouse — stock receive/issue/report (oldorm 0.x API)."""

from oldorm import Session

from .models import Item


class UnknownSku(LookupError):
    pass


class InsufficientStock(LookupError):
    pass


def _session():
    return Session("memory://")


def receive_stock(sku, qty, price=0.0):
    """Add units to a sku, creating it when unknown. Returns the item dict."""
    session = _session()
    found = session.query(Item).filter(sku=sku).first()
    if found is None:
        item = Item.validate({"sku": sku, "qty": qty, "price": price})
        session.save(item)
        return item.dict()
    found.qty += qty
    if price:
        found.price = price
    session.save(found)
    return found.dict()


def issue_stock(sku, qty):
    """Remove units from a sku. Raises UnknownSku / InsufficientStock."""
    session = _session()
    found = session.query(Item).filter(sku=sku).first()
    if found is None:
        raise UnknownSku(sku)
    if found.qty < qty:
        raise InsufficientStock(f"{sku}: have {found.qty}, need {qty}")
    found.qty -= qty
    session.save(found)
    return found.dict()


def get_stock(sku):
    found = _session().query(Item).filter(sku=sku).first()
    if found is None:
        raise UnknownSku(sku)
    return found.dict()


def list_items():
    """All items, in the default Meta.ordering (sku ascending)."""
    return [item.dict() for item in _session().query(Item).all()]


def low_stock(threshold):
    """Items at or below `threshold` units, qty ascending (explicit order)."""
    rows = _session().query(Item).order_by("qty").all()
    return [item.dict() for item in rows if item.qty <= threshold]
