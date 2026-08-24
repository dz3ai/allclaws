"""invcalc.storage — JSON persistence for invoice records."""

import json
import os

from .core import calculate_invoice_total
from .models import REQUIRED_INVOICE_KEYS


def save_invoice(invoice, path):
    """Persist an invoice record to `path` as indented JSON."""
    payload = dict(invoice)
    payload["totals"] = calculate_invoice_total(
        invoice.get("lines", []), invoice.get("tax_rate_pct", 0.0)
    )
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)


def load_invoice(path):
    """Load an invoice record from JSON, validating required keys."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: invoice file must contain a JSON object")
    missing = [k for k in REQUIRED_INVOICE_KEYS if k not in data]
    if missing:
        raise ValueError(f"{path}: missing keys: {', '.join(missing)}")
    return data


def list_invoices(directory):
    """Invoice ids (filenames) found in a directory, sorted."""
    if not os.path.isdir(directory):
        return []
    names = sorted(
        fn[:-5]
        for fn in os.listdir(directory)
        if fn.endswith(".json") and not fn.startswith(".")
    )
    return names
