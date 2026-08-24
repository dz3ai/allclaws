"""invcalc — invoice calculation service (stdlib-only)."""

from .core import (
    apply_early_payment_discount,
    calculate_invoice_total,
    calculate_line_total,
    calculate_tax,
    format_invoice,
)
from .models import invoice_summary, new_invoice, new_line
from .storage import list_invoices, load_invoice, save_invoice

__version__ = "1.0.0"

__all__ = [
    "apply_early_payment_discount",
    "calculate_invoice_total",
    "calculate_line_total",
    "calculate_tax",
    "format_invoice",
    "invoice_summary",
    "list_invoices",
    "load_invoice",
    "new_invoice",
    "new_line",
    "save_invoice",
    "__version__",
]
