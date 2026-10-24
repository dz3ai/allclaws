"""inventory.models — Item and Order models (oldorm 0.x Meta config)."""

from oldorm import Model

from . import audit


class Item(Model):
    class Meta:
        table = "items"
        pk = "sku"
        ordering = ["sku"]
        required = ("sku", "qty")
        types = {"sku": str, "qty": int, "price": float}
        hooks = {"before_save": audit.before_item_save}


class Order(Model):
    class Meta:
        table = "orders"
        pk = "oid"
        ordering = ["oid"]
        required = ("oid", "sku", "qty", "status")
        types = {"oid": str, "sku": str, "qty": int, "status": str}
        hooks = {"after_save": audit.after_order_save}
