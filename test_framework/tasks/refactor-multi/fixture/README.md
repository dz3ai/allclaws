# invcalc — invoice calculation service

A small, dependency-free (stdlib-only) invoice calculation service used for
refactoring exercises. Version 1.0 ships as a monolith on purpose.

## Public API contract (MUST NOT change in any refactor)

All names below are exported from the `invcalc` package:

| Function | Signature | Behavior |
|---|---|---|
| `calculate_line_total` | `(quantity: float, unit_price: float, discount_pct: float = 0.0) -> float` | Net total for one line, 2 decimal places |
| `calculate_tax` | `(amount: float, tax_rate_pct: float) -> float` | Sales tax, 2 dp |
| `calculate_invoice_total` | `(lines: list, tax_rate_pct: float = 0.0) -> dict` | `{"subtotal", "tax", "grand_total"}` for a list of line records |
| `apply_early_payment_discount` | `(amount: float, days_early: int) -> float` | 2% if paid 10+ days early, 1% if 3-9 days, else 0% |
| `format_invoice` | `(invoice: dict) -> str` | Multi-line human-readable rendering |
| `new_line` | `(description: str, quantity: float, unit_price: float, discount_pct: float = 0.0) -> line record` | Fresh line record |
| `new_invoice` | `(customer: str, lines: list = None, tax_rate_pct: float = 0.0, currency: str = "USD") -> invoice record` | Fresh invoice record |
| `invoice_summary` | `(invoice: dict) -> dict` | Compact summary dict |
| `save_invoice` | `(invoice, path: str) -> None` | Persist invoice as JSON |
| `load_invoice` | `(path: str) -> dict` | Load invoice from JSON (validates keys) |
| `list_invoices` | `(directory: str) -> list` | Sorted invoice ids found in a directory |

Validation rules (must be preserved): quantities/prices/amounts are
non-negative; `discount_pct` is within 0-100; tax rates are non-negative.
Violations raise `ValueError`.

## CLI

```
python -m invcalc.cli total  --lines-json '[{"quantity":2,"unit_price":3.5}]' --tax-rate 8.5
python -m invcalc.cli save   --customer ACME --lines-json '[...]' --out invoice.json
python -m invcalc.cli show   invoice.json
```

`total` prints the result of `calculate_invoice_total` as JSON.

## Development

```
/usr/bin/python3 -m pytest tests/ -q
```

No third-party dependencies — see requirements.txt.
