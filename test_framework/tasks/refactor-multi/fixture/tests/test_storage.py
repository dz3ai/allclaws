"""Storage round-trip + CLI arg tests (existing suite, keep green)."""

import json

import pytest

from invcalc import format_invoice, list_invoices, load_invoice, new_invoice, new_line, save_invoice


def make_invoice(tmp_path, customer="ACME"):
    lines = [
        new_line("Widget", 2, 3.5),
        new_line("Gadget", 1, 10.0, 10.0),
    ]
    inv = new_invoice(customer, lines=lines, tax_rate_pct=10.0)
    path = tmp_path / f"{customer}.json"
    save_invoice(inv, str(path))
    return inv, path


def as_dict(obj):
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "_asdict"):
        return dict(obj._asdict())
    return vars(obj)


class TestStorage:
    def test_round_trip(self, tmp_path):
        inv, path = make_invoice(tmp_path)
        loaded = as_dict(load_invoice(str(path)))
        assert loaded["customer"] == "ACME"
        assert len(loaded["lines"]) == 2
        assert loaded["tax_rate_pct"] == 10.0

    def test_saved_totals_embedded(self, tmp_path):
        _, path = make_invoice(tmp_path)
        raw = json.loads(path.read_text())
        assert raw["totals"]["grand_total"] == 17.6

    def test_load_missing_keys_rejected(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text(json.dumps({"id": "INV-1"}))
        with pytest.raises(ValueError):
            load_invoice(str(bad))

    def test_list_invoices_sorted(self, tmp_path):
        make_invoice(tmp_path, "Beta")
        make_invoice(tmp_path, "Alpha")
        names = list_invoices(str(tmp_path))
        assert names == ["Alpha", "Beta"]

    def test_list_invoices_missing_dir(self, tmp_path):
        assert list_invoices(str(tmp_path / "nope")) == []


class TestFormat:
    def test_format_contains_totals(self, tmp_path):
        inv, _ = make_invoice(tmp_path)
        text = format_invoice(inv)
        assert "ACME" in text
        assert "17.60" in text
        assert "Subtotal" in text
