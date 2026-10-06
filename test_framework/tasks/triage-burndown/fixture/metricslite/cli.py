"""metricslite command line: ``python -m metricslite.cli``."""

from __future__ import annotations

import argparse
import json
import sys

from . import percentile, summarize


def _samples(text: str) -> list[float]:
    return [float(part) for part in text.split(",") if part.strip()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="metricslite", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_sum = sub.add_parser("summarize", help="count/mean/min/max for a sample list")
    p_sum.add_argument("--samples", required=True, help="comma-separated numbers")

    p_pct = sub.add_parser("percentile", help="p-th percentile of a sample list")
    p_pct.add_argument("--samples", required=True, help="comma-separated numbers")
    p_pct.add_argument("--p", type=float, required=True, help="percentile in 0..100")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "summarize":
            print(json.dumps(summarize(_samples(args.samples)), sort_keys=True))
        else:
            payload = {"p": args.p, "value": percentile(_samples(args.samples), args.p)}
            print(json.dumps(payload, sort_keys=True))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
