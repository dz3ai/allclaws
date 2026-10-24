"""Single-file harness for the smolagents long-run benchmark driver.

Contract (driver: longrun/drivers/smolagents.py):
    argv:  --prompt TEXT (verbatim task prompt)  [--model ID]
    cwd:   the run worktree (harness operates on cwd, never chdirs)
    stdout: the agent's final answer, then exactly ONE machine-readable line:
            LONGRUN_USAGE {"tokens_in": <int|null>, "tokens_out": <int|null>}
    exit:  0 on success; non-zero on agent exception (traceback to stderr)

smolagents is a LIBRARY (plan §Scope Ruling: "Library → single-file harness"),
not a CLI — this file is that harness. It builds a CodeAgent with the default
toolbox (tools=[], minimal config: the only registered tool is the built-in
final_answer; add_base_tools defaults to False — smolagents/agents.py:301) and
runs the task once. This is a benchmark, not a showcase.

Model selection:
    --model ID  -> LiteLLMModel(model_id=ID); provider credentials come from
                   the environment only (never set here). NOTE: prepare()
                   installs plain `smolagents` (per brief), and litellm is an
                   OPTIONAL extra in smolagents 1.26.0 — LiteLLMModel raises
                   ModuleNotFoundError("Please install 'litellm' extra to use
                   LiteLLMModel: `pip install 'smolagents[litellm]'`")
                   (smolagents/models.py:1261). That guidance surfaces verbatim
                   as the harness failure until the venv adds the extra.
    default     -> smolagents' default model path: InferenceClientModel()
                   (HF Inference Providers; smolagents/models.py:1456), whose
                   constructor default model_id is
                   'Qwen/Qwen3-Next-80B-A3B-Thinking'; token resolves from the
                   environment (HF_TOKEN) at call time — nothing is hardcoded.

Token-usage API (INSPECTED, installed smolagents 1.26.0):
    agent.monitor            - Monitor instance (smolagents/agents.py:350)
    Monitor.get_total_token_counts()
                             -> TokenUsage (smolagents/monitoring.py:37),
                                fields input_tokens / output_tokens /
                                total_tokens (monitoring.py:89)
    Monitor.total_input_token_count / total_output_token_count
                             - raw int accumulators (monitoring.py:81-87)
    The harness reads get_total_token_counts() and emits ints; nulls are only
    emitted if the values are not ints (contract fallback per driver collect()).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

USAGE_PREFIX = "LONGRUN_USAGE "

# When the harness runs as a script, sys.path[0] is the drivers/ directory —
# which contains our sibling smolagents.py DRIVER module that would shadow the
# pip-installed smolagents package on `from smolagents import CodeAgent`.
# Drop this script's directory from sys.path before importing the library.
_HARNESS_DIR = Path(__file__).resolve().parent
sys.path[:] = [
    p for p in sys.path
    if p and Path(p).resolve() != _HARNESS_DIR
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--prompt", required=True, help="task prompt, VERBATIM")
    parser.add_argument(
        "--model",
        default=None,
        help="model ID for LiteLLMModel (e.g. openai/gpt-4o-mini); "
        "omit for smolagents' InferenceClientModel default",
    )
    return parser.parse_args()


def build_model(args: argparse.Namespace):
    if args.model:
        from smolagents import LiteLLMModel

        return LiteLLMModel(model_id=args.model)
    from smolagents import InferenceClientModel

    return InferenceClientModel()  # smolagents default path; env creds only


def main() -> int:
    args = parse_args()

    import smolagents  # noqa: F401  (shadowing guard above must run first)
    from smolagents import CodeAgent

    agent = CodeAgent(tools=[], model=build_model(args))
    answer = agent.run(args.prompt)
    print(answer)

    usage = agent.monitor.get_total_token_counts()
    tokens_in = usage.input_tokens if type(usage.input_tokens) is int else None
    tokens_out = usage.output_tokens if type(usage.output_tokens) is int else None
    print(f"{USAGE_PREFIX}{json.dumps({'tokens_in': tokens_in, 'tokens_out': tokens_out})}")
    return 0


if __name__ == "__main__":
    # No try/except: an agent exception must exit non-zero with the traceback
    # on stderr (collect() then falls back to the chars/4 estimate).
    sys.exit(main())
