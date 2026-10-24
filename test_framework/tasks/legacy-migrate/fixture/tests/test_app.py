"""inventory app test suite — behavior contract.

These tests document CURRENT behavior. They are green on the oldorm 0.x
codebase and must stay green (unchanged) after the neworm 2.x migration.
"""

import pytest

from inventory import (
    AlreadyFulfilled,
    InsufficientStock,
    UnknownOrder,
    UnknownSku,
    ValidationError,
    audit,
    create_order,
    fulfill_order,
    get_stock,
    issue_stock,
    list_items,
    list_orders,
    low_stock,
    open_order_units,
    order_ledger,
    receive_stock,
    reset,
    stock_valuation,
)


@pytest.fixture(autouse=True)
def clean_stores():
    reset()
    yield
    reset()


class TestReceiveStock:
    def test_new_sku_creates_item(self):
        assert receive_stock("widget", 5, 2.5) == {
            "sku": "widget",
            "qty": 5,
            "price": 2.5,
        }

    def test_known_sku_accumulates(self):
        receive_stock("widget", 5, 2.0)
        assert receive_stock("widget", 3, 2.0)["qty"] == 8

    def test_reprice_on_receive(self):
        receive_stock("widget", 5, 2.0)
        assert receive_stock("widget", 3, 3.0)["price"] == 3.0

    def test_int_price_coerced_to_float(self):
        assert receive_stock("bolt", 4, 1)["price"] == 1.0

    def test_type_violation_raises(self):
        with pytest.raises(ValidationError):
            receive_stock("widget", "lots")

    def test_missing_qty_raises(self):
        with pytest.raises(ValidationError):
            receive_stock("widget", None)


class TestIssueStock:
    def test_issue_decrements(self):
        receive_stock("widget", 5, 2.0)
        assert issue_stock("widget", 2)["qty"] == 3

    def test_unknown_sku(self):
        with pytest.raises(UnknownSku):
            issue_stock("ghost", 1)

    def test_over_issue_refused(self):
        receive_stock("widget", 2, 1.0)
        with pytest.raises(InsufficientStock):
            issue_stock("widget", 5)

    def test_get_stock(self):
        receive_stock("widget", 5, 2.0)
        assert get_stock("widget")["qty"] == 5
        with pytest.raises(UnknownSku):
            get_stock("ghost")


class TestListings:
    def test_list_items_default_ordering_is_sku(self):
        receive_stock("bolt", 1, 0.5)
        receive_stock("widget", 2, 2.0)
        receive_stock("anchor", 3, 9.0)
        assert [i["sku"] for i in list_items()] == ["anchor", "bolt", "widget"]

    def test_low_stock_orders_by_qty(self):
        receive_stock("a", 10, 1.0)
        receive_stock("b", 2, 1.0)
        receive_stock("c", 5, 1.0)
        receive_stock("d", 3, 1.0)
        assert [i["sku"] for i in low_stock(5)] == ["b", "d", "c"]

    def test_low_stock_empty(self):
        receive_stock("a", 10, 1.0)
        assert low_stock(5) == []


class TestOrders:
    def test_create_against_unknown_sku(self):
        with pytest.raises(UnknownSku):
            create_order("ghost", 1)

    def test_create_rejects_nonpositive_qty(self):
        receive_stock("widget", 5, 1.0)
        with pytest.raises(ValueError):
            create_order("widget", 0)

    def test_create_and_list(self):
        receive_stock("widget", 5, 1.0)
        order = create_order("widget", 2)
        assert order["oid"].startswith("ORD-")
        assert order["status"] == "open"
        assert [o["oid"] for o in list_orders()] == [order["oid"]]

    def test_fulfill_decrements_stock(self):
        receive_stock("widget", 10, 1.0)
        order = create_order("widget", 4)
        fulfilled = fulfill_order(order["oid"])
        assert fulfilled["status"] == "fulfilled"
        assert get_stock("widget")["qty"] == 6

    def test_double_fulfill_refused(self):
        receive_stock("widget", 5, 1.0)
        order = create_order("widget", 2)
        fulfill_order(order["oid"])
        with pytest.raises(AlreadyFulfilled):
            fulfill_order(order["oid"])

    def test_fulfill_unknown_order(self):
        with pytest.raises(UnknownOrder):
            fulfill_order("ORD-9999")

    def test_order_ledger_newest_first(self):
        receive_stock("widget", 10, 1.0)
        first = create_order("widget", 2)
        second = create_order("widget", 3)
        assert [o["oid"] for o in order_ledger()] == [second["oid"], first["oid"]]


class TestAudit:
    def test_create_entry_has_no_previous(self):
        receive_stock("widget", 5, 2.0)
        entries = [e for e in audit.entries() if e["kind"] == "item"]
        assert entries == [
            {
                "event": "create",
                "kind": "item",
                "key": "widget",
                "before": None,
                "after": 5,
            }
        ]

    def test_update_entry_captures_previous_qty(self):
        receive_stock("widget", 5, 2.0)
        receive_stock("widget", 3, 2.0)
        entries = [e for e in audit.entries() if e["kind"] == "item"]
        assert entries[-1] == {
            "event": "update",
            "kind": "item",
            "key": "widget",
            "before": 5,
            "after": 8,
        }

    def test_order_hook_tracks_status(self):
        receive_stock("widget", 5, 1.0)
        order = create_order("widget", 2)
        fulfill_order(order["oid"])
        entries = [e for e in audit.entries() if e["kind"] == "order"]
        assert entries == [
            {
                "event": "order",
                "kind": "order",
                "key": order["oid"],
                "before": None,
                "after": "open",
            },
            {
                "event": "order",
                "kind": "order",
                "key": order["oid"],
                "before": "open",
                "after": "fulfilled",
            },
        ]


class TestReports:
    def test_stock_valuation(self):
        receive_stock("widget", 5, 2.0)
        receive_stock("gadget", 3, 1.5)
        assert stock_valuation() == {"skus": 2, "units": 8, "value": 14.5}

    def test_open_order_units(self):
        receive_stock("widget", 10, 1.0)
        first = create_order("widget", 4)
        create_order("widget", 3)
        fulfill_order(first["oid"])
        assert open_order_units() == 3
