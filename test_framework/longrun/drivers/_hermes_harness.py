"""Single-file harness for the hermes long-run benchmark driver.

Contract (driver: longrun/drivers/hermes.py):
    argv:  --prompt TEXT (verbatim task prompt)  [--model ID]  [--max-turns N]
    cwd:   the run worktree (harness operates on cwd, never chdirs)
    stdout: run_agent.main's human transcript (banner, summary block, final
            answer); collect() chars/4-estimates it and parses turns from the
            LAST summary block only
    exit:  0 when main() returns — including the key-less init-failure case,
           where hermes prints "❌ Failed to initialize agent: ..." and
           returns instead of raising (run_agent.py:1539-1541; see driver
           docstring); non-zero only on harness/import errors (traceback to
           stderr, no try/except — collect() falls back to chars/4).

Choice rationale (plan §Scope Ruling: "Library → single-file harness"):
run_agent.main is a plain kwarg function (run_agent.py:1490-1494). Its argv
front-ends are the console script (`hermes-agent = "run_agent:main"`,
pyproject.toml:434 — called with NO arguments, so it would run the default
demo query, run_agent.py:1543-1544) and fire (run_agent.py:1559-1561; `fire`
IS a declared dependency, "fire==0.7.1", pyproject.toml:43, but its argv
scanning re-tokenizes a multi-KB verbatim prompt). The harness therefore
calls run_agent.main directly with explicit kwargs: the prompt crosses as a
Python str with zero argv mangling, and the console-script footgun is
bypassed entirely.

Model selection: --model ID → run_agent.main(model=ID) (OpenRouter format
"provider/model", run_agent.py:1500-1503). Omitted → main's model="" default,
which resolves provider/model/credentials through hermes' own config +
dotenv chain (run_agent.py:112-117) — the driver/harness never hardcode keys.

max-turns → run_agent.main(max_turns=N) → AIAgent(max_iterations=...) (run_agent.py:1535);
main's own default of 10 (run_agent.py:1491) is far below long-run budgets.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# When the harness runs as a script, sys.path[0] is the drivers/ directory —
# our sibling hermes.py DRIVER module would shadow hermes-agent's top-level
# `hermes` package (and other flat module names could collide the same way).
# Drop this script's directory from sys.path, then put the hermes-agent
# submodule root at the front so `import run_agent` resolves to
# <repo>/hermes-agent/run_agent.py (repo root = parents[2] of this directory,
# matching the driver's parents[3] layout).
_HARNESS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _HARNESS_DIR.parents[2]
sys.path[:] = [p for p in sys.path if p and Path(p).resolve() != _HARNESS_DIR]
sys.path.insert(0, str(_REPO_ROOT / "hermes-agent"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--prompt", required=True, help="task prompt, VERBATIM")
    parser.add_argument(
        "--model",
        default=None,
        help='model in OpenRouter "provider/model" format; omit for hermes\' '
        "own config/dotenv resolution (run_agent.py model=\"\" default)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=None,
        help=" forwarded to run_agent.main(max_turns=...); default keeps "
        "run_agent.main's own default (10)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    import run_agent  # noqa: E402  (sys.path surgery above must run first)

    kwargs = {"query": args.prompt}
    if args.model:
        kwargs["model"] = args.model
    if args.max_turns is not None:
        kwargs["max_turns"] = args.max_turns
    run_agent.main(**kwargs)
    return 0


if __name__ == "__main__":
    # No try/except: an import/agent exception must exit non-zero with the
    # traceback on stderr (collect() falls back to the chars/4 estimate).
    sys.exit(main())
