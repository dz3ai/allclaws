"""invcalc.cli — argparse front-end (total / save / show)."""

import argparse
import json
import sys

from .core import calculate_invoice_total
from .models import new_invoice, new_line
from .storage import load_invoice


def _parse_lines(lines_json):
    try:
        raw = json.loads(lines_json)
    except json.JSONDecodeError as e:
        raise SystemExit(f"error: --lines-json is not valid JSON: {e}")
    if not isinstance(raw, list) or not all(isinstance(item, dict) for item in raw):
        raise SystemExit("error: --lines-json must be a JSON array of objects")
    lines = []
    for item in raw:
        try:
            lines.append(
                new_line(
                    description=item.get("description", "item"),
                    quantity=float(item["quantity"]),
                    unit_price=float(item["unit_price"]),
                    discount_pct=float(item.get("discount_pct", 0.0)),
                )
            )
        except KeyError as e:
            raise SystemExit(f"error: line object missing key {e}")
        except ValueError as e:
            raise SystemExit(f"error: invalid line value: {e}")
    return lines


def cmd_total(args):
    lines = _parse_lines(args.lines_json)
    result = calculate_invoice_total(lines, tax_rate_pct=args.tax_rate)
    print(json.dumps(result, indent=2))
    return 0


def cmd_save(args):
    lines = _parse_lines(args.lines_json)
    invoice = new_invoice(
        customer=args.customer, lines=lines, tax_rate_pct=args.tax_rate
    )
    from .storage import save_invoice

    save_invoice(invoice, args.out)
    print(invoice["id"] if isinstance(invoice, dict) else invoice.id)
    return 0


def cmd_show(args):
    invoice = load_invoice(args.path)
    from .core import format_invoice

    print(format_invoice(invoice))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="invcalc", description="Invoice calculator")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("total", help="calculate totals for a JSON line list")
    p.add_argument("--lines-json", required=True)
    p.add_argument("--tax-rate", type=float, default=0.0)
    p.set_defaults(func=cmd_total)

    p = sub.add_parser("save", help="create + persist an invoice")
    p.add_argument("--customer", required=True)
    p.add_argument("--lines-json", required=True)
    p.add_argument("--tax-rate", type=float, default=0.0)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_save)

    p = sub.add_parser("show", help="render a saved invoice")
    p.add_argument("path")
    p.set_defaults(func=cmd_show)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
