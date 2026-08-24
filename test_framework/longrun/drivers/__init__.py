"""Driver registry for long-run benchmarks.

Drivers are discovered by module name: `longrun.drivers.aider` -> AiderDriver.
Each driver module MUST export exactly one DriverBase subclass ending in
"Driver".
"""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path

from longrun.drivers.base import DriverBase, DriverError


def load_driver(name: str, repo_root: Path) -> DriverBase:
    """Import longrun.drivers.<name> and instantiate its Driver subclass."""
    module_name = name.replace("-", "_").replace(".", "_")
    try:
        mod = importlib.import_module(f"longrun.drivers.{module_name}")
    except ImportError as e:
        raise DriverError(f"no driver module 'longrun.drivers.{module_name}': {e}") from e

    candidates = [
        obj
        for _, obj in inspect.getmembers(mod, inspect.isclass)
        if issubclass(obj, DriverBase)
        and obj is not DriverBase
        and obj.__module__ == mod.__name__
        and obj.__name__.endswith("Driver")
    ]
    if not candidates:
        raise DriverError(f"driver module {mod.__name__} exports no *Driver class")
    if len(candidates) > 1:
        raise DriverError(f"driver module {mod.__name__} exports multiple Driver classes")
    return candidates[0](repo_root=Path(repo_root))


AVAILABLE_DRIVERS = ("aider", "codex", "kimi_cli", "reasonix", "opencode", "smolagents", "hermes")
