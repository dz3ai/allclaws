"""Existing public-API tests — these MUST stay green through the refactor."""

import subprocess
import sys

import pytest

from invcalc import (
    apply_early_payment_discount,
    calculate_invoice_total,
    calculate_line_total,
    calculate_tax,
    invoice_summary,
    new_invoice,
    new_line,
)


def make_lines():
    return [
        {"description": "Widget", "quantity": 2, "unit_price": 3.5, "discount_pct": 0.0},
        {"description": "Gadget", "quantity": 1, "unit_price": 10.0, "discount_pct": 10.0},
    ]


def as_dict(obj):
    """Read record fields from dicts OR (post-refactor) model objects."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "_asdict"):
        return dict(obj._asdict())
    return vars(obj)


class TestLineMath:
    def test_simple_line(self):
        assert calculate_line_total(2, 3.5) == 7.0

    def test_line_with_discount(self):
        assert calculate_line_total(1, 10.0, 10.0) == 9.0

    def test_zero_quantity(self):
        assert calculate_line_total(0, 5.0) == 0.0

    def test_rounding_two_decimals(self):
        # 3 * 3.34 = 10.02 exactly; no banker's-rounding ambiguity here
        assert calculate_line_total(3, 3.34) == 10.02

    @pytest.mark.parametrize("q,p", [(-1, 3.0), (2, -3.0)])
    def test_negative_values_rejected(self, q, p):
        with pytest.raises(ValueError):
            calculate_line_total(q, p)

    @pytest.mark.parametrize("d", [-0.1, 100.1])
    def test_discount_bounds(self, d):
        with pytest.raises(ValueError):
            calculate_line_total(1, 1.0, d)


class TestTax:
    def test_simple_tax(self):
        assert calculate_tax(100.0, 8.5) == 8.5

    def test_zero_rate(self):
        assert calculate_tax(100.0, 0.0) == 0.0

    def test_negative_amount_rejected(self):
        with pytest.raises(ValueError):
            calculate_tax(-1.0, 5.0)

    def test_negative_rate_rejected(self):
        with pytest.raises(ValueError):
            calculate_tax(100.0, -5.0)


class TestInvoiceTotals:
    def test_totals_no_tax(self):
        result = calculate_invoice_total(make_lines())
        assert result["subtotal"] == 16.0
        assert result["tax"] == 0.0
        assert result["grand_total"] == 16.0

    def test_totals_with_tax(self):
        result = calculate_invoice_total(make_lines(), tax_rate_pct=10.0)
        assert result["subtotal"] == 16.0
        assert result["tax"] == 1.6
        assert result["grand_total"] == 17.6

    def test_empty_lines(self):
        result = calculate_invoice_total([])
        assert result == {"subtotal": 0.0, "tax": 0.0, "grand_total": 0.0}

    def test_line_discount_validation(self):
        bad = [{"quantity": 1, "unit_price": 1.0, "discount_pct": 150}]
        with pytest.raises(ValueError):
            calculate_invoice_total(bad)

    def test_negative_tax_rate_rejected(self):
        with pytest.raises(ValueError):
            calculate_invoice_total([], tax_rate_pct=-1)


class TestEarlyPay:
    def test_tier1(self):
        assert apply_early_payment_discount(100.0, 10) == 98.0

    def test_tier2(self):
        assert apply_early_payment_discount(100.0, 5) == 99.0

    def test_no_discount(self):
        assert apply_early_payment_discount(100.0, 2) == 100.0

    def test_zero_days(self):
        assert apply_early_payment_discount(100.0, 0) == 100.0

    def test_negative_days_rejected(self):
        with pytest.raises(ValueError):
            apply_early_payment_discount(100.0, -1)


class TestModels:
    def test_new_line_fields(self):
        line = as_dict(new_line("Widget", 2, 3.5))
        assert line["description"] == "Widget"
        assert line["quantity"] == 2
        assert line["unit_price"] == 3.5
        assert line["discount_pct"] == 0.0

    def test_new_invoice_fields(self):
        inv = as_dict(new_invoice("ACME"))
        assert inv["customer"] == "ACME"
        assert inv["lines"] == []
        assert inv["currency"] == "USD"

    def test_summary(self):
        inv = new_invoice("ACME", lines=make_lines(), tax_rate_pct=10.0)
        s = as_dict(invoice_summary(inv))
        assert s["customer"] == "ACME"
        assert s["n_lines"] == 2

    def test_summary_on_plain_dict_still_works(self):
        s = as_dict(invoice_summary({"customer": "X", "lines": []}))
        assert s["customer"] == "X"
        assert s["n_lines"] == 0


class TestCliSmoke:
    def test_total_subcommand(self):
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "invcalc.cli",
                "total",
                "--lines-json",
                '[{"quantity":2,"unit_price":3.5}]',
                "--tax-rate",
                "0",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert proc.returncode == 0, proc.stderr
        assert '"grand_total": 7.0' in proc.stdout
