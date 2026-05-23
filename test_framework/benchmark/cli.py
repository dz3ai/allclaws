"""CLI entry point for the AllClaws Benchmark Suite v3.0."""

import argparse
import os
import sys
from pathlib import Path

from .report import ReportGenerator
from .runtime import RuntimeBenchmark
from .sandbox import SandboxBenchmark
from .static import StaticBenchmark
from .utils import now_timestamp, write_json, write_markdown, write_summary_table


def _resolve_defaults(args):
    """Resolve default config path and output directory based on script location."""
    # Base directory is test_framework/ (parent of benchmark/)
    base_dir = Path(__file__).resolve().parent.parent

    if args.config is None:
        default_config = base_dir / "config.json"
        if default_config.is_file():
            args.config = str(default_config)

    if args.output_dir is None:
        args.output_dir = str(base_dir / "benchmark_results" / now_timestamp())

    return args


def main():
    parser = argparse.ArgumentParser(
        description="AllClaws Benchmark Suite v3.0",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Global options (shared parent parser)
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--config", default=None,
                        help="Config file path (default: ../config.json)")
    parent.add_argument("--output-dir", default=None,
                        help="Output directory for results")
    parent.add_argument("--json-only", action="store_true",
                        help="Output JSON only (skip Markdown)")
    parent.add_argument("--platform", default=None,
                        help="Target platform(s), comma-separated")
    parent.add_argument("--skip", default=None,
                        help="Skip platform(s), comma-separated")

    # runtime subcommand
    rt = subparsers.add_parser("runtime", parents=[parent],
                               help="Local runtime benchmarks")
    rt.add_argument("--runs", type=int, default=5,
                    help="Sample count for timing metrics (default: 5)")

    # static subcommand
    subparsers.add_parser("static", parents=[parent],
                          help="Static code analysis")

    # sandbox subcommand
    subparsers.add_parser("sandbox", parents=[parent],
                          help="Container health checks")

    # report subcommand
    rp = subparsers.add_parser("report", parents=[parent],
                               help="Aggregate N runs into summary")
    rp.add_argument("--last", type=int, default=5,
                    help="Number of recent runs to aggregate (default: 5)")
    rp.add_argument("--regression", type=int, default=20,
                    help="Regression threshold %% (default: 20)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Apply parent defaults
    args = _resolve_defaults(args)

    # Parse platform/skip lists
    platforms = None
    if args.platform:
        platforms = [p.strip() for p in args.platform.split(",")]

    skip_list = []
    if args.skip:
        skip_list = [s.strip() for s in args.skip.split(",")]

    # Ensure output directory has command-specific suffix
    output_dir = args.output_dir
    if not output_dir.endswith(args.command):
        output_dir = os.path.join(output_dir, args.command)

    # Dispatch
    result = None

    if args.command == "runtime":
        if not args.config:
            print("ERROR: config.json not found. Use --config to specify.")
            sys.exit(1)
        runs = getattr(args, "runs", 5)
        bench = RuntimeBenchmark(
            config_path=args.config,
            output_dir=output_dir,
            platforms=platforms or [],
            skip=skip_list or [],
            runs=runs,
        )
        result = bench.run()

    elif args.command == "static":
        if not args.config:
            print("ERROR: config.json not found. Use --config to specify.")
            sys.exit(1)
        bench = StaticBenchmark(
            config_path=args.config,
            output_dir=output_dir,
            platforms=platforms or [],
            skip=skip_list or [],
        )
        result = bench.run()

    elif args.command == "sandbox":
        if not args.config:
            print("ERROR: config.json not found. Use --config to specify.")
            sys.exit(1)
        bench = SandboxBenchmark(
            config_path=args.config,
            output_dir=output_dir,
            platforms=platforms or [],
            skip=skip_list or [],
        )
        result = bench.run()

    elif args.command == "report":
        # For report, results_dir is the base benchmark_results directory
        results_dir = str(Path(output_dir).parent)
        last = getattr(args, "last", 5)
        regression = getattr(args, "regression", 20)
        gen = ReportGenerator(
            results_dir=results_dir,
            output_dir=output_dir,
            last=last,
            regression_pct=regression,
        )
        # Determine which command to aggregate (default: runtime)
        result = gen.generate(command="runtime")
        if result is None:
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)

    if result is None:
        print("ERROR: No results produced.")
        sys.exit(1)

    # Write output files
    json_path = os.path.join(output_dir, f"{args.command}_benchmark_results.json")
    md_path = os.path.join(output_dir, f"{args.command}_benchmark_results.md")
    summary_path = os.path.join(output_dir, "summary.md")

    write_json(result, json_path)
    print(f"\nJSON:    {json_path}")

    if not args.json_only:
        write_markdown(result, md_path)
        print(f"Report: {md_path}")

        summary = write_summary_table(result)
        with open(summary_path, "w") as f:
            f.write(summary)
            f.write("\n")
        print(f"Summary: {summary_path}")

    print(f"\nDone. {len(result.metrics)} metrics, "
          f"{len(result.skipped)} skipped.")


if __name__ == "__main__":
    main()
