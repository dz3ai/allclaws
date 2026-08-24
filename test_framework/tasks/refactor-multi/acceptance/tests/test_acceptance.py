"""HIDDEN acceptance suite for refactor-multi (mounted at scoring time only).

Checks the four structural requirements from issue.md plus behavioral parity.
Runs with cwd = the agent's worktree root; the package under test is
imported from the worktree.
"""

import inspect
import re
import sys
from pathlib import Path

import pytest

PKG_DIR = Path.cwd() / "invcalc"

sys.path.insert(0, str(Path.cwd()))


# --------------------------------------------------------------------------
# Requirement 4: public API unchanged (names + parameter lists + defaults)
# --------------------------------------------------------------------------

API_SIGNATURES = {
    "calculate_line_total": ["quantity", "unit_price", "discount_pct"],
    "calculate_tax": ["amount", "tax_rate_pct"],
    "calculate_invoice_total": ["lines", "tax_rate_pct"],
    "apply_early_payment_discount": ["amount", "days_early"],
    "format_invoice": ["invoice"],
    "new_line": ["description", "quantity", "unit_price", "discount_pct"],
    "new_invoice": ["customer", "lines", "tax_rate_pct", "currency"],
    "invoice_summary": ["invoice"],
    "save_invoice": ["invoice", "path"],
    "load_invoice": ["path"],
    "list_invoices": ["directory"],
}

API_DEFAULTS = {
    ("calculate_line_total", "discount_pct"): 0.0,
    ("calculate_invoice_total", "tax_rate_pct"): 0.0,
    ("new_line", "discount_pct"): 0.0,
    ("new_invoice", "lines"): None,
    ("new_invoice", "tax_rate_pct"): 0.0,
    ("new_invoice", "currency"): "USD",
}


def _api():
    import invcalc

    return invcalc


class TestPublicAPI:
    @pytest.mark.parametrize("name,params", sorted(API_SIGNATURES.items()))
    def test_function_exists_and_params_match(self, name, params):
        fn = getattr(_api(), name, None)
        assert callable(fn), f"invcalc.{name} missing or not callable"
        sig = inspect.signature(fn)
        got = list(sig.parameters)
        assert got == params, f"{name}: parameters {got} != expected {params}"

    @pytest.mark.parametrize("item,default", sorted(API_DEFAULTS.items()))
    def test_defaults_preserved(self, item, default):
        name, param = item
        sig = inspect.signature(getattr(_api(), name))
        got = sig.parameters[param].default
        assert got == default, f"{name}({param}=...): default {got!r} != {default!r}"


# --------------------------------------------------------------------------
# Requirement 1: extracted engine module used by core
# --------------------------------------------------------------------------

class TestEngineExtracted:
    def test_engine_module_exists(self):
        assert (PKG_DIR / "engine.py").is_file(), "invcalc/engine.py does not exist"

    def test_core_imports_engine(self):
        core = (PKG_DIR / "core.py").read_text(encoding="utf-8")
        assert re.search(r"from\s+\.engine\s+import|from\s+invcalc\.engine\s+import|import\s+\.engine|\bengine\b", core), (
            "core.py shows no reference to the engine module"
        )

    def test_engine_importable_and_has_math(self):
        from invcalc import engine

        assert hasattr(engine, "calculate_tax") or hasattr(engine, "line_tax") or any(
            hasattr(engine, n) for n in ("calculate_tax", "calculate_line_total", "percentage_of")
        ), "engine module exposes no calculation functions"


# --------------------------------------------------------------------------
# Requirement 2: single percentage helper (no duplicated formula)
# --------------------------------------------------------------------------

PCT_PATTERN = re.compile(r"round\(\s*\w[\w\s+\-*/().]*?/\s*100\s*,\s*2\s*\)")


class TestSinglePercentageHelper:
    def test_percentage_formula_appears_at_most_once(self):
        hits = []
        for py in PKG_DIR.glob("*.py"):
            src = py.read_text(encoding="utf-8")
            # strip comments to avoid counting documentation examples
            code = "\n".join(
                line for line in src.splitlines() if not line.strip().startswith("#")
            )
            n = len(PCT_PATTERN.findall(code))
            if n:
                hits.append((py.name, n))
        total = sum(n for _, n in hits)
        assert total <= 1, (
            f"percentage formula duplicated: {total} occurrences across {hits} "
            "(issue.md allows at most 1 — route all percentage math through one helper)"
        )


# --------------------------------------------------------------------------
# Requirement 3: typed models with dict compatibility
# --------------------------------------------------------------------------

class TestTypedModels:
    def test_dataclass_or_namedtuple_used(self):
        src = (PKG_DIR / "models.py").read_text(encoding="utf-8")
        assert re.search(r"@dataclass|class\s+\w+\(\s*NamedTuple\s*\)|NamedTuple", src), (
            "models.py shows no dataclass/NamedTuple definition"
        )

    def test_line_and_invoice_have_to_dict(self):
        from invcalc import new_invoice, new_line

        for obj in (new_line("x", 1, 2.0), new_invoice("c")):
            method = getattr(obj, "to_dict", None)
            assert callable(method), f"{type(obj).__name__} lacks to_dict()"

    def test_to_dict_round_trip_fields(self):
        from invcalc import new_line

        d = new_line("Widget", 2, 3.5).to_dict()
        assert d["description"] == "Widget"
        assert d["quantity"] == 2
        assert d["unit_price"] == 3.5

    def test_functions_still_accept_plain_dicts(self):
        from invcalc import calculate_invoice_total, format_invoice, invoice_summary

        lines = [{"quantity": 2, "unit_price": 3.5, "discount_pct": 0.0}]
        assert calculate_invoice_total(lines, tax_rate_pct=10.0)["grand_total"] == 7.7
        assert "c" in format_invoice(
            {"id": "i", "customer": "c", "lines": lines, "tax_rate_pct": 0.0, "currency": "USD", "status": "draft"}
        )
        assert invoice_summary({"customer": "c", "lines": []}) is not None


# --------------------------------------------------------------------------
# Behavioral parity spot checks (same math as the visible suite)
# --------------------------------------------------------------------------

class TestBehavior:
    def test_totals_with_tax(self):
        from invcalc import calculate_invoice_total

        lines = [
            {"quantity": 2, "unit_price": 3.5, "discount_pct": 0.0},
            {"quantity": 1, "unit_price": 10.0, "discount_pct": 10.0},
        ]
        r = calculate_invoice_total(lines, tax_rate_pct=10.0)
        assert (r["subtotal"], r["tax"], r["grand_total"]) == (16.0, 1.6, 17.6)

    def test_early_pay_tiers(self):
        from invcalc import apply_early_payment_discount

        assert apply_early_payment_discount(100.0, 10) == 98.0
        assert apply_early_payment_discount(100.0, 5) == 99.0
        assert apply_early_payment_discount(100.0, 2) == 100.0

    def test_validation_intact(self):
        from invcalc import calculate_line_total

        with pytest.raises(ValueError):
            calculate_line_total(1, 1.0, 150)
