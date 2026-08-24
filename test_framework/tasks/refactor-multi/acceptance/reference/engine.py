"""invcalc.engine — pure calculation logic (extracted from core per issue.md).

All percentage math routes through percentage_of() — the single helper.
"""

from .compat import record_get

TIER1_DAYS = 10
TIER1_RATE = 2.0
TIER2_DAYS = 3
TIER2_RATE = 1.0


def percentage_of(amount, pct):
    """THE single percentage helper: pct% of amount, 2 decimal places."""
    return round(amount * pct / 100, 2)


def validate_non_negative(name, value):
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def validate_discount_pct(pct):
    if not 0 <= pct <= 100:
        raise ValueError("discount_pct must be within 0-100")


def calculate_line_total(quantity, unit_price, discount_pct=0.0):
    """Net total for one line: quantity * unit_price minus discount_pct."""
    validate_non_negative("quantity", quantity)
    validate_non_negative("unit_price", unit_price)
    validate_discount_pct(discount_pct)
    gross = quantity * unit_price
    return round(gross - percentage_of(gross, discount_pct), 2)


def calculate_tax(amount, tax_rate_pct):
    """Sales tax for an amount at tax_rate_pct percent."""
    validate_non_negative("amount", amount)
    validate_non_negative("tax_rate_pct", tax_rate_pct)
    return percentage_of(amount, tax_rate_pct)


def calculate_invoice_total(lines, tax_rate_pct=0.0):
    """Totals for line records (dicts or Line models) -> subtotal/tax/grand_total."""
    validate_non_negative("tax_rate_pct", tax_rate_pct)
    subtotal = 0.0
    tax_total = 0.0
    for line in lines:
        qty = record_get(line, "quantity")
        price = record_get(line, "unit_price")
        disc = record_get(line, "discount_pct", 0.0)
        validate_non_negative("quantity", qty)
        validate_non_negative("unit_price", price)
        validate_discount_pct(disc)
        gross = qty * price
        line_net = round(gross - percentage_of(gross, disc), 2)
        subtotal = round(subtotal + line_net, 2)
        tax_total = round(tax_total + percentage_of(line_net, tax_rate_pct), 2)
    return {
        "subtotal": subtotal,
        "tax": tax_total,
        "grand_total": round(subtotal + tax_total, 2),
    }


def early_payment_rate(days_early):
    """Applicable early-payment discount rate in percent."""
    if days_early >= TIER1_DAYS:
        return TIER1_RATE
    if days_early >= TIER2_DAYS:
        return TIER2_RATE
    return 0.0


def apply_early_payment_discount(amount, days_early):
    """Early payment discount: 2% at 10+ days early, 1% at 3-9, else 0."""
    validate_non_negative("amount", amount)
    validate_non_negative("days_early", days_early)
    rate = early_payment_rate(days_early)
    return round(amount - percentage_of(amount, rate), 2)
