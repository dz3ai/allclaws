"""CLI entry for long-run benchmarks: list / run / report (mirrors benchmark.cli)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from longrun.cost import BUDGET_CEILING_USD, KNOWN_MODELS, SpendLedger
from longrun.report import load_runs, summarize, write_report
from longrun.runner import DEFAULT_RESULTS_ROOT, BudgetExhausted, run_grid
from longrun.spec import TASK_TYPES, load_all_tasks


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def cmd_list(args: argparse.Namespace) -> int:
    tasks = load_all_tasks(Path(args.tasks_root))
    if not tasks:
        print("no tasks found under", args.tasks_root)
        return 1
    print(f"{len(tasks)} tasks:")
    for t in tasks:
        print(
            f"  {t.id:<18} type={t.type:<20} diff={t.difficulty or '?':<7} "
            f"timeout={t.timeout_minutes}min cap=${t.cost_cap_usd}"
        )
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    drivers = [d.strip() for d in args.drivers.split(",") if d.strip()]
    tasks = [t.strip() for t in args.tasks.split(",") if t.strip()]
    if not drivers or not tasks:
        print("--drivers and --tasks must be non-empty")
        return 2
    print(
        f"[longrun] grid: {len(drivers)} drivers x {len(tasks)} tasks x {args.repeats} "
        f"repeats | model={args.model or 'env'} | ceiling ${BUDGET_CEILING_USD}"
    )
    try:
        out = run_grid(
            drivers=drivers,
            task_ids=tasks,
            tasks_root=Path(args.tasks_root),
            dry_run=args.dry_run,
            repeats=args.repeats,
            model=args.model,
        )
    except BudgetExhausted as e:
        print(f"[longrun] BUDGET HARD STOP: {e}", file=sys.stderr)
        return 3
    print(f"[longrun] done: {len(out['runs'])} runs -> {out['run_root']}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    if args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        candidates = sorted(DEFAULT_RESULTS_ROOT.glob("*-*-*T*"))
        if not candidates:
            print("no timestamped run dirs under", DEFAULT_RESULTS_ROOT)
            return 1
        run_dir = candidates[-1]
    if not run_dir.is_dir():
        print("not a dir:", run_dir)
        return 1
    out = write_report(run_dir)
    runs = load_runs(run_dir)
    summary = summarize(runs)
    print(f"[longrun] report written: {out} ({summary['total_runs']} runs)")
    return 0


def cmd_budget(args: argparse.Namespace) -> int:
    ledger = SpendLedger(Path(args.ledger))
    print(f"ceiling:        ${ledger.ceiling:.2f}")
    print(f"spent:          ${ledger.total_usd():.4f}")
    print(f"remaining:      ${ledger.remaining_budget():.2f}")
    print(f"entries:        {len(ledger.entries)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="longrun",
        description="Long-running agent benchmarks (Q4-4) — run / list / report / budget",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("list", help="list available tasks")
    sp.add_argument("--tasks-root", default=str(Path(__file__).resolve().parent.parent / "tasks"))
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("run", help="run a drivers x tasks grid")
    sp.add_argument("--drivers", required=True, help="comma-separated driver names")
    sp.add_argument("--tasks", required=True, help="comma-separated task ids")
    sp.add_argument("--tasks-root", default=str(Path(__file__).resolve().parent.parent / "tasks"))
    sp.add_argument("--repeats", type=int, default=1)
    sp.add_argument("--model", default=None, help=f"pin model for this batch ({', '.join(KNOWN_MODELS[:4])}...)")
    sp.add_argument("--dry-run", action="store_true",
                    help="build ProcSpec + validate spec/driver wiring, no launch")
    sp.set_defaults(func=run_wrapper)

    sp = sub.add_parser("report", help="generate report.md + summary.json for a run dir")
    sp.add_argument("--run-dir", default=None, help="timestamped dir; default = latest")
    sp.set_defaults(func=cmd_report)

    sp = sub.add_parser("budget", help="show spend ledger status")
    sp.add_argument("--ledger", default=str(DEFAULT_RESULTS_ROOT / "spend_ledger.json"))
    sp.set_defaults(func=cmd_budget)

    return p


def run_wrapper(args: argparse.Namespace) -> int:
    return cmd_run(args)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
