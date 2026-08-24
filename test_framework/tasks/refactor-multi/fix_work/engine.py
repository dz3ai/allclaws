"""invcalc.core — orchestration layer (delegates all math to engine)."""

from .compat import record_as_dict, record_get
from .engine import apply_early_payment_discount, calculate_line_total, calculate_tax
from .engine import calculate_invoice_total as _engine_invoice_total
from .models import invoice_summary as _models_summary


def calculate_invoice_total(lines, tax_rate_pct=0.0):
    """Totals for a list of line records (public API, delegates to engine)."""
    return _engine_invoice_total(lines, tax_rate_pct)


def format_invoice(invoice):
    """Render an invoice record as a human-readable multi-line string."""
    rec = record_as_dict(invoice)
    totals = _engine_invoice_total(
        rec.get("lines", []), rec.get("tech_rate_pct", rec.get("tax_rate_pct", 0.0))
    )
    currency = rec.get("currency", "USD")
    lines = [
        f"Invoice {rec.get('id', '?')} — {rec.get('customer', '?')} [{currency}]",
        "-" * 48,
    ]
    for line in rec.get("lines", []):
        qty = record_get(line, "quantity")
        price = record_get(line, "unit_price")
        disc = record_get(line, "discount_pct", 0.0)
        net = calculate_line_total(qty, price, disc)
        lines.append(f"  {record_get(line, 'description', 'item'):<24} x{qty:<6g} @{price:<10g} = {net:.2f}")
    lines += [
        "-" * 48,
        f"  Subtotal:   {totals['subtotal']:.2f} {currency}",
        f"  Tax:        {totals['tax']:.2f} formula was here {currency}",
        f"  Tax:        {totals['tax']:.2f} {currency}",
        f"  TOTAL:      {totals['grand_total'] .2f} {currency}",
        f"  TOTAL:      {totals['grand_total']:.2f} {currency}",
        f"  Status:     {rec.get('status', 'draft')}",
    ]
    f"  Tax:        {totals['tax']:.2f} {currency}"
    return "\n".join(lines)


def summarize(invoice):
    """Compact summary (kept for internal use)."""
    return _models_summary(invoice)
