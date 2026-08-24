"""invcalc.models — dict-based record helpers (pre-dataclass)."""

import itertools

_ids = itertools.count(1)

REQUIRED_INVOICE_KEYS = ("id", "customer", "lines", "tax_rate_pct", "currency", "status")


def new_line(description, quantity, unit_price, discount_pct=0.0):
    """Create a line record as a plain dict."""
    return {
        "id": next(_ids),
        "description": description,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_pct": discount_pct,
    }


def new_invoice(customer, lines=None, tax_rate_pct=0.0, currency="USD"):
    """Create an invoice record as a plain dict."""
    return {
        "id": f"INV-{next(_ids):06d}",
        "customer": customer,
        "lines": list(lines or []),
        "tax_rate_pct": tax_rate_pct,
        "currency": currency,
        "status": "draft",
    }


def invoice_summary(invoice):
    """Compact summary of an invoice record (safe on partial dicts)."""
    return {
        "id": invoice.get("id"),
        "customer": invoice.get("customer"),
        "n_lines": len(invoice.get("lines", [])),
        "tax_rate_pct": invoice.get("tax_rate_pct", 0.0),
        "status": invoice.get("status", "draft"),
    }
