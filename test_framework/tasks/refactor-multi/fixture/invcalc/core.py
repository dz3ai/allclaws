"""invcalc.core — invoice calculation engine (monolith, pre-refactor).

Everything calculation-related lives here in 1.0: line math, tax, discounts,
formatting. See issue.md for the refactor brief.
"""

from .models import invoice_summary

EARLY_PAY_TIER1_DAYS = 10
EARLY_PAY_TIER1_RATE = 2.0
EARLY_PAY_TIER2_DAYS = 3
EARLY_PAY_TIER2_RATE = 1.0


def calculate_line_total(quantity, unit_price, discount_pct=0.0):
    """Net total for one line: quantity * unit_price minus discount_pct."""
    if quantity < 0:
        raise ValueError("quantity must be >= 0")
    if unit_price < 0:
        raise ValueError("unit_price must be >= 0")
    if not 0 <= discount_pct <= 100:
        raise ValueError("discount_pct must be within 0-100")
    gross = quantity * unit_price
    discount = round(gross * discount_pct / 100, 2)
    return round(gross - discount, 2)


def calculate_tax(amount, tax_rate_pct):
    """Sales tax for an amount at tax_rate_pct percent."""
    if amount < 0:
        raise ValueError("amount must be >= 0")
    if tax_rate_pct < 0:
        raise ValueError("tax_rate_pct must be >= 0")
    return round(amount * tax_rate_pct / 100, 2)


def calculate_invoice_total(lines, tax_rate_pct=0.0):
    """Totals for a list of line records (dicts with quantity/unit_price).

    Returns {"subtotal", "tax", "grand_total"} — all rounded to 2 dp.
    """
    if tax_rate_pct < 0:
        raise ValueError("tax_rate_pct must be >= 0")
    subtotal = 0.0
    tax_total = 0.0
    for line in lines:
        qty = line["quantity"]
        price = line["unit_price"]
        disc = line.get("discount_pct", 0.0)
        if qty < 0:
            raise ValueError("quantity must be >= 0")
        if price < 0:
            raise ValueError("unit_price must be >= 0")
        if not 0 <= disc <= 100:
            raise ValueError("discount_pct must be within 0-100")
        gross = qty * price
        discount = round(gross * disc / 100, 2)
        line_net = round(gross - discount, 2)
        subtotal = round(subtotal + line_net, 2)
        tax_total = round(tax_total + round(line_net * tax_rate_pct / 100, 2), 2)
    grand = round(subtotal + tax_total, 2)
    return {"subtotal": subtotal, "tax": tax_total, "grand_total": grand}


def apply_early_payment_discount(amount, days_early):
    """Early payment discount on an amount.

    2% when paid 10+ days early, 1% for 3-9 days early, else no discount.
    """
    if amount < 0:
        raise ValueError("amount must be >= 0")
    if days_early < 0:
        raise ValueError("days_early must be >= 0")
    if days_early >= EARLY_PAY_TIER1_DAYS:
        rate = EARLY_PAY_TIER1_RATE
    elif days_early >= EARLY_PAY_TIER2_DAYS:
        rate = EARLY_PAY_TIER2_RATE
    else:
        rate = 0.0
    discount = round(amount * rate / 100, 2)
    return round(amount - discount, 2)


def format_invoice(invoice):
    """Render an invoice record as a human-readable multi-line string."""
    totals = calculate_invoice_total(invoice.get("lines", []), invoice.get("tax_rate_pct", 0.0))
    currency = invoice.get("currency", "USD")
    lines = [
        f"Invoice {invoice.get('id', '?')} — {invoice.get('customer', '?')} [{currency}]",
        "-" * 48,
    ]
    for line in invoice.get("lines", []):
        qty = line["quantity"]
        price = line["unit_price"]
        disc = line.get("discount_pct", 0.0)
        net = calculate_line_total(qty, price, disc)
        lines.append(f"  {line.get('description', 'item'):<24} x{qty:<6g} @{price:<10g} = {net:.2f}")
    lines += [
        "-" * 48,
        f"  Subtotal:   {totals['subtotal']:.2f} {currency}",
        f"  Tax:        {totals['tax']:.2f} {currency}",
        f"  TOTAL:      {totals['grand_total']:.2f} {currency}",
        f"  Status:     {invoice.get('status', 'draft')}",
    ]
    return "\n".join(lines)


def summarize(invoice):
    """Compact summary (thin wrapper kept for internal use)."""
    return invoice_summary(invoice)
