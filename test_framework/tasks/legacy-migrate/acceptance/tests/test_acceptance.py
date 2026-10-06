"""HIDDEN acceptance suite for legacy-migrate (mounted at scoring time only).

Two layers:
  (a) behavior — the inventory app still works identically after the
      migration (mirror/extension of the fixture's tests/test_app.py)
  (b) scanner — AST walk over EVERY module under inventory/ proving the
      oldorm 0.x deprecated surface is fully gone, robust to whatever file
      names the agent uses:
        * any `oldorm` import
        * any `.query(` call
        * any `.validate(` call on models (0.x validation entry point)
        * any `.dict(` call (0.x serialization)
        * any `.save(` call (0.x persistence)
        * any `class Meta` (0.x config block)
        * old callback arity/shape: any function with a positional
          parameter named `old` in non-first position (the 0.x
          `def cb(instance, old)` hook signature)

Runs with cwd = the agent's worktree root.
"""

import ast
from pathlib import Path

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
    low_stock,
    open_order_units,
    order_ledger,
    receive_stock,
    reset,
    stock_valuation,
)

INVENTORY = Path("inventory")


# ---- layer (b) scanner helpers ---------------------------------------------

def _collect_violations(matcher):
    """AST-walk every module under inventory/ (any file name); return
    human-readable violations for nodes where `matcher(node)` returns a
    non-None string."""
    if not INVENTORY.is_dir():
        return ["inventory/ package not found — the app must stay at inventory/"]
    violations = []
    for path in sorted(INVENTORY.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as e:
            violations.append(f"{path}: does not parse ({e})")
            continue
        for node in ast.walk(tree):
            hit = matcher(node)
            if hit:
                violations.append(f"{path}:{getattr(node, 'lineno', 0)}: {hit}")
    return violations


def _oldorm_import(node):
    if isinstance(node, ast.Import):
        for alias in node.names:
            if alias.name == "oldorm" or alias.name.startswith("oldorm."):
                return f"import of deprecated library ({alias.name})"
    if isinstance(node, ast.ImportFrom) and node.module:
        if node.module == "oldorm" or node.module.startswith("oldorm."):
            return f"from-import of deprecated library (oldorm.{node.module[len('oldorm.'):]}))"
    return None


def _call_attr(attr, label):
    def matcher(node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == attr
        ):
            return f"deprecated 0.x call .{attr}() ({label})"
        return None

    return matcher


def _meta_class(node):
    if isinstance(node, ast.ClassDef) and node.name == "Meta":
        return "class Meta — 0.x config block; use class Config + model_config"
    return None


def _old_callback_signature(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        positional = node.args.posonlyargs + node.args.args
        for index, arg in enumerate(positional):
            if index >= 1 and arg.arg == "old":
                return (
                    "old-callback signature (positional param 'old' at position "
                    f"{index}) — use def cb(instance, previous_state)"
                )
    return None


# ---- layer (b) scanner tests ------------------------------------------------

def test_no_oldorm_imports():
    assert _collect_violations(_oldorm_import) == []


def test_no_query_calls():
    assert _collect_violations(_call_attr("query", "use session.select")) == []


def test_no_validate_calls():
    assert _collect_violations(_call_attr("validate", "use Model.model_validate")) == []


def test_no_dict_calls():
    assert _collect_violations(_call_attr("dict", "use model.model_dump")) == []


def test_no_save_calls():
    assert _collect_violations(_call_attr("save", "use session.persist")) == []


def test_no_meta_class():
    assert _collect_violations(_meta_class) == []


def test_no_old_callback_signature():
    assert _collect_violations(_old_callback_signature) == []


# ---- layer (a) behavior (must be identical to the pristine app) -------------

@pytest.fixture(autouse=True)
def _clean_stores():
    reset()
    yield
    reset()


class TestBehaviorStock:
    def test_receive_create_accumulate_reprice(self):
        assert receive_stock("widget", 5, 2.5) == {"sku": "widget", "qty": 5, "price": 2.5}
        assert receive_stock("widget", 3, 3.0) == {"sku": "widget", "qty": 8, "price": 3.0}

    def test_issue_and_guards(self):
        receive_stock("widget", 5, 2.0)
        assert issue_stock("widget", 2)["qty"] == 3
        with pytest.raises(UnknownSku):
            issue_stock("ghost", 1)
        with pytest.raises(InsufficientStock):
            issue_stock("widget", 99)
        with pytest.raises(UnknownSku):
            get_stock("ghost")

    def test_validation_errors_unchanged(self):
        with pytest.raises(ValidationError):
            receive_stock("widget", "lots")
        with pytest.raises(ValidationError):
            receive_stock("widget", None)

    def test_listings_and_ordering(self):
        receive_stock("bolt", 1, 0.5)
        receive_stock("widget", 2, 2.0)
        receive_stock("anchor", 3, 9.0)
        assert [i["sku"] for i in list_items()] == ["anchor", "bolt", "widget"]
        assert [i["sku"] for i in low_stock(2)] == ["bolt", "widget"]


class TestBehaviorOrders:
    def test_order_lifecycle(self):
        receive_stock("widget", 10, 1.0)
        order = create_order("widget", 4)
        assert order["oid"].startswith("ORD-") and order["status"] == "open"
        assert fulfill_order(order["oid"])["status"] == "fulfilled"
        assert get_stock("widget")["qty"] == 6
        with pytest.raises(AlreadyFulfilled):
            fulfill_order(order["oid"])
        with pytest.raises(UnknownOrder):
            fulfill_order("ORD-9999")
        with pytest.raises(UnknownSku):
            create_order("ghost", 1)

    def test_ledger_newest_first(self):
        receive_stock("widget", 10, 1.0)
        first = create_order("widget", 2)
        second = create_order("widget", 3)
        assert [o["oid"] for o in order_ledger()] == [second["oid"], first["oid"]]


class TestBehaviorAuditAndReports:
    def test_audit_trail_semantics(self):
        receive_stock("widget", 5, 2.0)
        receive_stock("widget", 3, 2.0)
        receive_stock("widget", 1, 2.0)
        entries = [e for e in audit.entries() if e["kind"] == "item"]
        assert entries[0]["before"] is None and entries[0]["after"] == 5
        assert entries[1]["before"] == 5 and entries[1]["after"] == 8
        assert entries[2]["before"] == 8 and entries[2]["after"] == 9

    def test_order_audit_trail(self):
        receive_stock("widget", 5, 1.0)
        order = create_order("widget", 2)
        fulfill_order(order["oid"])
        trail = [e["after"] for e in audit.entries() if e["kind"] == "order"]
        assert trail == ["open", "fulfilled"]

    def test_reports(self):
        receive_stock("widget", 5, 2.0)
        receive_stock("gadget", 3, 1.5)
        assert stock_valuation() == {"skus": 2, "units": 8, "value": 14.5}
        first = create_order("widget", 4)
        create_order("widget", 3)
        fulfill_order(first["oid"])
        assert open_order_units() == 3
