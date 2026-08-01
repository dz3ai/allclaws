"""Runtime benchmark logic for the AllClaws benchmark suite."""

import json
import os
from pathlib import Path
from typing import Optional

from .utils import (
    BenchmarkResult,
    Metric,
    detect_toolchain,
    load_config,
    measure_rss,
    now_timestamp,
    sample_metric,
    size_of,
    size_of_raw,
    time_command,
)


# Python platform import mappings: platform -> (import_stmt, import_desc)
_PYTHON_IMPORTS = {
    "clawteam": ("import clawteam", "import clawteam"),
    "nanobot": ("import nanobot", "import nanobot"),
    "hermes-agent": ("from run_agent import main", "from run_agent import main"),
    "claw-ai-lab": ("import researchclaw", "import researchclaw"),
    "smolagents": ("import smolagents", "import smolagents"),
    "langgraph": ("import langgraph", "import langgraph"),
    "crewai": ("import crewai", "import crewai"),
    "autogen": ("import autogen", "import autogen"),
    "swarms": ("import swarms", "import swarms"),
    "aider": ("import aider", "import aider"),
    # China ecosystem (Q3-6)
    "metagpt": ("import metagpt", "import metagpt"),
    "qwen-agent": ("import qwen_agent", "import qwen_agent"),
    "agentscope": ("import agentscope", "import agentscope"),
    # Other external frameworks
    "agent-zero": ("import agentzero", "import agentzero"),
    "praisonai": ("import praisonai", "import praisonai"),
    "openworker": ("import openworker", "import openworker"),
}

# TypeScript platform entry points (searched in order)
_TS_ENTRY_CANDIDATES = [
    "src/index.ts", "src/index.js", "src/main.ts", "src/main.js",
    "src/cli.ts", "src/cli.js",
]


class RuntimeBenchmark:
    """Run local runtime benchmarks across all platforms."""

    def __init__(self, config_path: str, output_dir: str,
                 platforms: list = None, skip: list = None, runs: int = 5):
        self.config = load_config(config_path)
        self.output_dir = Path(output_dir)
        self.platforms = platforms or list(self.config["supported_platforms"])
        self.skip = skip or []
        self.runs = runs
        self.toolchain = detect_toolchain()
        self.metrics: list[Metric] = []
        self.skipped: list[dict] = []

    def run(self) -> BenchmarkResult:
        """Execute all runtime benchmarks and return results."""
        self._run_rust_platforms()
        self._run_go_platforms()
        self._run_typescript_platforms()
        self._run_python_platforms()
        self._run_cli_platforms()
        return self._build_result()

    # ------------------------------------------------------------------
    # Metric helpers
    # ------------------------------------------------------------------

    def _add_metric(self, platform, metric, value, unit, notes="",
                    samples=None, stats=None):
        self.metrics.append(Metric(
            platform=platform, metric=metric, value=value,
            unit=unit, notes=notes, samples=samples, stats=stats,
        ))

    def _skip_platform(self, platform, reason):
        self.skipped.append({"platform": platform, "reason": reason})
        print(f"  SKIP: {reason}")

    def _build_result(self) -> BenchmarkResult:
        return BenchmarkResult(
            timestamp=now_timestamp(),
            engine_version="3.0.0",
            command="runtime",
            toolchain=self.toolchain,
            metrics=self.metrics,
            skipped=self.skipped,
        )

    # ------------------------------------------------------------------
    # Platform path resolution
    # ------------------------------------------------------------------

    def _platform_path(self, platform: str) -> Optional[Path]:
        """Resolve platform directory from config or fallback."""
        rel = self.config.get("platform_paths", {}).get(platform)
        if rel:
            p = (Path(__file__).resolve().parent.parent / rel).resolve()
            if p.is_dir():
                return p
        # Fallback: try ../platform relative to test_framework
        fallback = Path(__file__).resolve().parent.parent.parent / platform
        if fallback.is_dir():
            return fallback
        return None

    def _find_venv_python(self, platform_path: Path) -> Optional[str]:
        """Find venv python binary if it exists."""
        for venv_name in (".venv", "venv"):
            vpy = platform_path / venv_name / "bin" / "python3"
            if vpy.is_file():
                return str(vpy)
        return None

    # ------------------------------------------------------------------
    # Rust platforms
    # ------------------------------------------------------------------

    def _run_rust_platforms(self):
        platforms = ["ironclaw", "zeroclaw", "openfang", "openhuman"]
        for p in platforms:
            if p in self.skip or p not in self.platforms:
                continue
            self._benchmark_rust(p)

    def _benchmark_rust(self, platform: str):
        path = self._platform_path(platform)
        print(f"--- {platform} (Rust) ---")

        if not path or not (path / "Cargo.toml").exists():
            self._skip_platform(platform, "not found or no Cargo.toml")
            print()
            return

        # Binary size
        release_dir = path / "target" / "release"
        if release_dir.is_dir():
            for bin_file in release_dir.iterdir():
                if bin_file.is_file() and os.access(bin_file, os.X_OK):
                    self._add_metric(
                        platform, f"binary_{bin_file.name}_size",
                        size_of_raw(str(bin_file)), "KB",
                    )
        else:
            self._add_metric(platform, "binary_size", 0, "KB",
                             "no target/release (not built)")

        # Install footprint (target/)
        self._add_metric(platform, "install_footprint",
                         size_of_raw(str(path / "target")), "KB",
                         "target/ directory")

        # Build proxy: cargo check (sampled)
        if self.toolchain.get("cargo"):
            m = sample_metric(
                platform, "build_proxy_time",
                ["cargo", "check"], "ms", runs=self.runs,
                notes="cargo check",
            )
            rc, _ = time_command(["cargo", "check"], timeout=300)
            m.notes = "cargo check" if rc == 0 else f"cargo check failed (rc={rc})"
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)
        else:
            self._add_metric(platform, "build_proxy_time", 0, "ms",
                             "cargo not available")

        # Cold start: binary --help (sampled, if built)
        main_bin = self._find_main_binary(release_dir, platform)
        if main_bin:
            m = sample_metric(
                platform, "cold_start_time",
                ["timeout", "5", str(main_bin), "--help"], "ms",
                runs=self.runs, notes=f"{main_bin.name} --help",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)

            # Memory measurement
            if self.toolchain.get("time_v"):
                rc, peak_kb = measure_rss(
                    ["timeout", "5", str(main_bin), "--help"],
                )
                if peak_kb > 0:
                    self._add_metric(platform, "memory_idle_mb",
                                     round(peak_kb / 1024, 1), "MB")
                else:
                    self._add_metric(platform, "memory_idle_mb", 0, "MB",
                                     "measurement failed")
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "binary not built")

        print()

    def _find_main_binary(self, release_dir: Path, platform: str) -> Optional[Path]:
        """Find the main executable binary in target/release/."""
        if not release_dir.is_dir():
            return None
        for name in (platform, "main"):
            candidate = release_dir / name
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return candidate
        # Fallback: any executable file
        for f in sorted(release_dir.iterdir()):
            if f.is_file() and os.access(f, os.X_OK) and not f.name.endswith(".d"):
                return f
        return None

    # ------------------------------------------------------------------
    # Go platforms
    # ------------------------------------------------------------------

    def _run_go_platforms(self):
        platforms = ["goclaw", "maxclaw", "hiclaw"]
        for p in platforms:
            if p in self.skip or p not in self.platforms:
                continue
            self._benchmark_go(p)

    def _benchmark_go(self, platform: str):
        path = self._platform_path(platform)
        print(f"--- {platform} (Go) ---")

        if not path:
            self._skip_platform(platform, "not found or no go.mod")
            print()
            return

        # go.mod might be in root or a subdirectory (monorepo)
        go_mod = path / "go.mod"
        if not go_mod.exists():
            # Search one level deep
            for child in path.iterdir():
                child_mod = child / "go.mod"
                if child_mod.exists():
                    go_mod = child_mod
                    path = child
                    break

        if not go_mod.exists():
            self._skip_platform(platform, "not found or no go.mod")
            print()
            return

        # Binary size
        built_bins = []
        bin_dir = path / "bin"
        if bin_dir.is_dir():
            for f in bin_dir.iterdir():
                if f.is_file() and os.access(f, os.X_OK):
                    built_bins.append(f)
        main_candidate = path / platform
        if main_candidate.is_file() and os.access(main_candidate, os.X_OK):
            built_bins.append(main_candidate)

        if built_bins:
            for bin_file in built_bins:
                self._add_metric(platform, f"binary_{bin_file.name}_size",
                                 size_of_raw(str(bin_file)), "KB")
        else:
            self._add_metric(platform, "binary_size", 0, "KB", "not built")

        # Install footprint (vendor/)
        vendor_size = size_of_raw(str(path / "vendor"))
        if vendor_size > 0:
            self._add_metric(platform, "install_footprint", vendor_size,
                             "KB", "vendor/ directory")
        else:
            self._add_metric(platform, "install_footprint", 0, "KB",
                             "no vendor/; go mod download proxy")

        # Build proxy: go vet
        if self.toolchain.get("go"):
            rc_vet, ms_vet = time_command(["go", "vet", "./..."],
                                           timeout=120)
            if rc_vet == 0:
                m = sample_metric(
                    platform, "build_proxy_time",
                    ["go", "vet", "./..."], "ms", runs=self.runs,
                    notes="go vet ./...",
                )
                self._add_metric(platform, m.metric, m.value, m.unit,
                                 notes=m.notes, samples=m.samples, stats=m.stats)
            else:
                # Try go build as fallback
                rc_build, ms_build = time_command(
                    ["go", "build", "-o", "/dev/null", "./..."], timeout=120,
                )
                if rc_build == 0:
                    m = sample_metric(
                        platform, "build_proxy_time",
                        ["go", "build", "-o", "/dev/null", "./..."], "ms",
                        runs=self.runs, notes="go build (vet failed)",
                    )
                    self._add_metric(platform, m.metric, m.value, m.unit,
                                     notes=m.notes, samples=m.samples,
                                     stats=m.stats)
                else:
                    self._add_metric(platform, "build_proxy_time", ms_vet,
                                     "ms", f"go vet failed (rc={rc_vet})")

            # mod download time
            m = sample_metric(
                platform, "mod_download_time",
                ["go", "mod", "download"], "ms", runs=self.runs,
                notes="go mod download",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)
        else:
            self._add_metric(platform, "build_proxy_time", 0, "ms",
                             "go toolchain not available")
            self._add_metric(platform, "mod_download_time", 0, "ms",
                             "go toolchain not available")

        # Cold start
        if built_bins:
            m = sample_metric(
                platform, "cold_start_time",
                ["timeout", "5", str(built_bins[0]), "--help"], "ms",
                runs=self.runs,
                notes=f"{built_bins[0].name} --help",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)

            # Memory
            if self.toolchain.get("time_v"):
                rc, peak_kb = measure_rss(
                    ["timeout", "5", str(built_bins[0]), "--help"],
                )
                if peak_kb > 0:
                    self._add_metric(platform, "memory_idle_mb",
                                     round(peak_kb / 1024, 1), "MB")
                else:
                    self._add_metric(platform, "memory_idle_mb", 0, "MB",
                                     "measurement failed")
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "binary not built")

        print()

    # ------------------------------------------------------------------
    # TypeScript platforms
    # ------------------------------------------------------------------

    def _run_typescript_platforms(self):
        platforms = ["openclaw", "nanoclaw",
                     "openagents", "copilot-cli",
                     "eliza", "dify"]
        for p in platforms:
            if p in self.skip or p not in self.platforms:
                continue
            self._benchmark_typescript(p)

    def _benchmark_typescript(self, platform: str):
        path = self._platform_path(platform)
        print(f"--- {platform} (TypeScript) ---")

        if not path or not (path / "package.json").exists():
            self._skip_platform(platform,
                                "not found or no package.json")
            print()
            return

        # node_modules size
        nm_dir = path / "node_modules"
        if nm_dir.is_dir():
            self._add_metric(platform, "install_footprint",
                             size_of_raw(str(nm_dir)), "KB",
                             "node_modules/")
        else:
            self._add_metric(platform, "install_footprint", 0, "KB",
                             "node_modules/ not installed")

        # Dependency count
        try:
            pkg = json.loads((path / "package.json").read_text())
            deps = len(pkg.get("dependencies", {}))
            dev_deps = len(pkg.get("devDependencies", {}))
            self._add_metric(platform, "npm_deps", deps + dev_deps, "deps")
        except (OSError, json.JSONDecodeError):
            self._add_metric(platform, "npm_deps", 0, "deps")

        # Binary size (dist/ or build/)
        for build_dir in ("dist", "build"):
            bd = path / build_dir
            if bd.is_dir():
                self._add_metric(platform, "binary_size",
                                 size_of_raw(str(bd)), "KB",
                                 f"{build_dir}/ directory")
                break
        else:
            self._add_metric(platform, "binary_size", 0, "KB",
                             "no dist/ or build/ directory")

        # Cold start: node parse time
        if self.toolchain.get("node"):
            main_entry = self._find_ts_entry(path)
            if main_entry:
                cmd = ["timeout", "10", "node", "-e",
                       f"try {{ require('{main_entry}'); }} catch(e) {{ }}"
                       " process.exit(0);"]
                m = sample_metric(
                    platform, "cold_start_time", cmd, "ms",
                    runs=self.runs, notes="node parse time (no runtime init)",
                )
                self._add_metric(platform, m.metric, m.value, m.unit,
                                 notes=m.notes, samples=m.samples, stats=m.stats)
            else:
                m = sample_metric(
                    platform, "cold_start_time",
                    ["node", "-e", "process.exit(0)"], "ms",
                    runs=self.runs,
                    notes="bare node startup (no entry found)",
                )
                self._add_metric(platform, m.metric, m.value, m.unit,
                                 notes=m.notes, samples=m.samples, stats=m.stats)

            # Response latency proxy
            m = sample_metric(
                platform, "response_latency_ms",
                ["timeout", "10", "node", "-e",
                 "console.log('READY'); process.exit(0)"],
                "ms", runs=self.runs, notes="echo benchmark",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)

            # Memory measurement
            if self.toolchain.get("time_v"):
                rc, peak_kb = measure_rss(["node", "-e",
                    "const fs = require('fs'); const path = require('path');"
                    " process.exit(0);"])
                if peak_kb > 0:
                    self._add_metric(platform, "memory_idle_mb",
                                     round(peak_kb / 1024, 1), "MB")
                else:
                    self._add_metric(platform, "memory_idle_mb", 0, "MB",
                                     "measurement failed")
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "node not available")

        print()

    def _find_ts_entry(self, path: Path) -> Optional[str]:
        """Find the main TypeScript entry point."""
        for candidate in _TS_ENTRY_CANDIDATES:
            if (path / candidate).is_file():
                return str(path / candidate)
        return None

    # ------------------------------------------------------------------
    # Python platforms
    # ------------------------------------------------------------------

    def _run_python_platforms(self):
        internal = ["clawteam", "nanobot", "hermes-agent", "claw-ai-lab"]
        external = ["smolagents", "langgraph",
                    "crewai", "autogen", "swarms", "aider",
                    "metagpt", "qwen-agent", "agentscope",
                    "agent-zero", "praisonai", "openworker"]
        for p in internal + external:
            if p in self.skip or p not in self.platforms:
                continue
            self._benchmark_python(p)

    def _benchmark_python(self, platform: str):
        path = self._platform_path(platform)
        print(f"--- {platform} (Python) ---")

        if not path:
            self._skip_platform(platform,
                                "not checked out — tracked via documentation only")
            print()
            return

        # Manifest files might be in root or a subdirectory (monorepo)
        has_pyproject = (path / "pyproject.toml").is_file()
        has_requirements = (path / "requirements.txt").is_file()
        has_setup = (path / "setup.py").is_file()

        # Search up to 2 levels deep for monorepos
        # (e.g. claw-ai-lab/backend/agent/, praisonai/src/praisonai-agents/)
        if not has_pyproject and not has_requirements and not has_setup:
            for child in path.rglob("pyproject.toml"):
                if ".venv" in str(child) or "node_modules" in str(child):
                    continue
                path = child.parent
                has_pyproject = True
                break
            if not has_pyproject:
                for child in path.rglob("requirements.txt"):
                    if ".venv" in str(child) or "node_modules" in str(child):
                        continue
                    path = child.parent
                    has_requirements = True
                    break

        if not has_pyproject and not has_requirements and not has_setup:
            self._skip_platform(platform,
                                "no pyproject.toml, requirements.txt, or setup.py")
            print()
            return

        # Dependency count
        if has_pyproject:
            try:
                text = (path / "pyproject.toml").read_text()
                count = sum(1 for line in text.splitlines()
                           if line.strip().startswith('"')
                           and any(c.isalpha() for c in line))
                self._add_metric(platform, "py_deps", count, "deps")
            except OSError:
                self._add_metric(platform, "py_deps", 0, "deps")
        elif has_requirements:
            try:
                text = (path / "requirements.txt").read_text()
                count = sum(1 for line in text.splitlines()
                           if line.strip() and not line.strip().startswith("#"))
                self._add_metric(platform, "py_deps", count, "deps")
            except OSError:
                self._add_metric(platform, "py_deps", 0, "deps")

        # Install footprint
        venv_python = self._find_venv_python(path)
        venv_size = 0
        for venv_name in (".venv", "venv"):
            vpath = path / venv_name
            if vpath.is_dir():
                venv_size = size_of_raw(str(vpath))
                self._add_metric(platform, "install_footprint", venv_size,
                                 "KB", f"{venv_name}/")
                break
        else:
            self._add_metric(platform, "install_footprint", 0, "KB",
                             "no venv found")

        # Import info
        import_info = _PYTHON_IMPORTS.get(platform)
        import_stmt = ""
        import_desc = ""
        if import_info:
            import_stmt, import_desc = import_info

        # Cold start: real package import (sampled)
        if self.toolchain.get("python3") and import_stmt:
            # Try venv python first
            py_bin = venv_python or "python3"
            import_cmd = [
                py_bin, "-c",
                "import sys\n"
                f"try:\n    {import_stmt}\n"
                "except Exception:\n    sys.exit(2)\n"
                "sys.exit(0)",
            ]

            # Check if import works
            rc, _ = time_command(import_cmd, timeout=15)
            if rc == 2:
                # Try system python
                import_cmd = ["python3", "-c",
                              "import sys\n"
                              f"try:\n    {import_stmt}\n"
                              "except Exception:\n    sys.exit(2)\n"
                              "sys.exit(0)"]
                rc, _ = time_command(import_cmd, timeout=15)

            m = sample_metric(
                platform, "cold_start_time", import_cmd, "ms",
                runs=self.runs,
                notes=f"python {import_desc}" if rc != 2
                      else f"import failed ({import_desc}) — not installed",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)
        elif self.toolchain.get("python3"):
            m = sample_metric(
                platform, "cold_start_time",
                ["python3", "-c", "pass"], "ms",
                runs=self.runs,
                notes="bare python startup (no module found)",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "python3 not available")

        # Response latency proxy
        if self.toolchain.get("python3"):
            m = sample_metric(
                platform, "response_latency_ms",
                ["timeout", "10", "python3", "-c",
                 "import sys; sys.stdout.write('READY\\n'); "
                 "sys.stdout.flush()"],
                "ms", runs=self.runs, notes="echo benchmark",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)

        # Memory: idle
        if self.toolchain.get("time_v") and self.toolchain.get("python3"):
            rc, peak_kb = measure_rss(["timeout", "10", "python3", "-c",
                "import sys, os, time; time.sleep(0.5)"])
            if peak_kb > 0:
                self._add_metric(platform, "memory_idle_mb",
                                 round(peak_kb / 1024, 1), "MB",
                                 "bare python process")
            else:
                self._add_metric(platform, "memory_idle_mb", 0, "MB",
                                 "measurement failed")

            # Memory: active (with real import)
            if import_stmt and venv_python:
                mem_cmd = [venv_python, "-c",
                    "import sys, time\n"
                    f"try:\n    {import_stmt}\n"
                    "except Exception:\n    pass\n"
                    "time.sleep(0.3)"]
                rc, peak_kb = measure_rss(mem_cmd)
                if peak_kb > 0:
                    self._add_metric(platform, "memory_active_mb",
                                     round(peak_kb / 1024, 1), "MB",
                                     f"python {import_desc} (venv)")
                else:
                    self._add_metric(platform, "memory_active_mb", 0, "MB",
                                     "package not importable (not installed)")
            elif import_stmt:
                mem_cmd = ["python3", "-c",
                    "import sys, time\n"
                    f"try:\n    {import_stmt}\n"
                    "except Exception:\n    pass\n"
                    "time.sleep(0.3)"]
                rc, peak_kb = measure_rss(mem_cmd)
                if peak_kb > 0:
                    self._add_metric(platform, "memory_active_mb",
                                     round(peak_kb / 1024, 1), "MB",
                                     f"python {import_desc} (system)")
                else:
                    self._add_metric(platform, "memory_active_mb", 0, "MB",
                                     "package not importable (not installed)")
            else:
                self._add_metric(platform, "memory_active_mb", 0, "MB",
                                 "package not importable (no venv or module unknown)")

        print()

    # ------------------------------------------------------------------
    # CLI agent platforms
    # ------------------------------------------------------------------

    def _run_cli_platforms(self):
        """Benchmark CLI coding agents.

        These are not library imports — they are executable binaries.
        We measure static metrics (source size, dependency count) and,
        if the binary is available, cold-start time via --version/--help.
        """
        cli_platforms = ["kimi-cli", "kimi-code", "codex",
                         "reasonix", "rocketride-server"]
        for p in cli_platforms:
            if p in self.skip or p not in self.platforms:
                continue
            self._benchmark_cli(p)

    def _benchmark_cli(self, platform: str):
        path = self._platform_path(platform)
        print(f"--- {platform} (CLI Agent) ---")

        if not path:
            self._skip_platform(platform,
                                "not checked out — tracked via documentation only")
            print()
            return

        # Source size
        self._add_metric(platform, "source_size",
                         size_of(str(path)), "KB",
                         "repo checkout size")

        # Detect type and measure accordingly
        has_pkg = (path / "package.json").exists()
        has_cargo = (path / "Cargo.toml").exists()
        has_py = (path / "pyproject.toml").exists() or \
                 (path / "setup.py").exists()

        if has_pkg:
            self._benchmark_cli_node(platform, path)
        elif has_cargo:
            self._benchmark_cli_rust(platform, path)
        elif has_py:
            self._benchmark_cli_python(platform, path)
        else:
            self._skip_platform(platform, "unknown project type")

        print()

    def _benchmark_cli_node(self, platform: str, path: Path):
        """Benchmark a Node-based CLI agent."""
        import json as _json
        try:
            pkg = _json.loads((path / "package.json").read_text())
        except Exception:
            pkg = {}

        deps = pkg.get("dependencies", {})
        dev_deps = pkg.get("devDependencies", {})
        total_deps = len(deps) + len(dev_deps)
        self._add_metric(platform, "npm_deps", total_deps, "deps")

        # node_modules size (if installed)
        nm = path / "node_modules"
        if nm.is_dir():
            self._add_metric(platform, "install_footprint",
                             size_of(str(nm)), "KB", "node_modules/")
        else:
            self._add_metric(platform, "install_footprint", 0, "KB",
                             "node_modules/ not installed")

        # dist/ size (if built)
        dist = path / "dist"
        bin_built = dist.is_dir() and any(dist.iterdir())
        self._add_metric(platform, "binary_size",
                         size_of(str(dist)) if bin_built else 0, "KB",
                         "dist/" if bin_built else "no dist/ (not built)")

        # Cold start: try bin entry --version
        if self.toolchain.get("node"):
            bin_field = pkg.get("bin", {})
            main_entry = pkg.get("main", "./dist/index.js")

            if isinstance(bin_field, dict) and bin_field:
                bin_path = path / list(bin_field.values())[0].lstrip("./")
            else:
                bin_path = path / main_entry.lstrip("./")

            # Monorepo fallback: if root has no usable entry, search subdirs
            if not bin_path.is_file():
                for child in path.iterdir():
                    if not child.is_dir() or child.name.startswith(".") or \
                       child.name in ("node_modules", "dist", "target"):
                        continue
                    sub_pkg = child / "package.json"
                    if sub_pkg.is_file():
                        try:
                            sub = _json.loads(sub_pkg.read_text())
                            sub_bin = sub.get("bin", {})
                            sub_main = sub.get("main", "")
                            if isinstance(sub_bin, dict) and sub_bin:
                                bin_path = child / list(sub_bin.values())[0].lstrip("./")
                                break
                            elif sub_main:
                                candidate = child / sub_main.lstrip("./")
                                if candidate.is_file():
                                    bin_path = candidate
                                    break
                        except Exception:
                            continue

            if bin_path.is_file():
                m = sample_metric(
                    platform, "cold_start_time",
                    ["timeout", "5", "node", str(bin_path), "--version"],
                    "ms", runs=self.runs,
                    notes=f"node {bin_path.name} --version",
                )
                self._add_metric(platform, m.metric, m.value, m.unit,
                                 notes=m.notes, samples=m.samples,
                                 stats=m.stats)

                if self.toolchain.get("time_v"):
                    _, peak_kb = measure_rss(
                        ["timeout", "5", "node", str(bin_path), "--version"],
                    )
                    if peak_kb > 0:
                        self._add_metric(platform, "memory_idle_mb",
                                         round(peak_kb / 1024, 1), "MB")
            else:
                self._add_metric(platform, "cold_start_time", 0, "ms",
                                 "entry point not found (not built)")
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "node not available")

    def _benchmark_cli_rust(self, platform: str, path: Path):
        """Benchmark a Rust-based CLI agent (e.g. codex)."""
        release_dir = path / "target" / "release"

        if release_dir.is_dir():
            for bin_file in release_dir.iterdir():
                if bin_file.is_file() and os.access(bin_file, os.X_OK):
                    self._add_metric(
                        platform, f"binary_{bin_file.name}_size",
                        size_of_raw(str(bin_file)), "KB",
                    )
        else:
            self._add_metric(platform, "binary_size", 0, "KB",
                             "no target/release (not built)")

        self._add_metric(platform, "install_footprint",
                         size_of_raw(str(path / "target")), "KB",
                         "target/ directory")

        # cargo check as build proxy
        if self.toolchain.get("cargo"):
            m = sample_metric(
                platform, "build_proxy_time",
                ["cargo", "check"], "ms", runs=self.runs,
                notes="cargo check",
            )
            rc, _ = time_command(["cargo", "check"], timeout=300)
            m.notes = "cargo check" if rc == 0 else \
                f"cargo check failed (rc={rc})"
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)
        else:
            self._add_metric(platform, "build_proxy_time", 0, "ms",
                             "cargo not available")

        # Cold start if binary exists
        main_bin = self._find_main_binary(release_dir, platform)
        if main_bin:
            m = sample_metric(
                platform, "cold_start_time",
                ["timeout", "5", str(main_bin), "--version"], "ms",
                runs=self.runs, notes=f"{main_bin.name} --version",
            )
            self._add_metric(platform, m.metric, m.value, m.unit,
                             notes=m.notes, samples=m.samples, stats=m.stats)
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "binary not built")

    def _benchmark_cli_python(self, platform: str, path: Path):
        """Benchmark a Python-based CLI agent (e.g. kimi-code)."""
        req = path / "requirements.txt"
        pyproj = path / "pyproject.toml"
        dep_count = 0
        if req.is_file():
            dep_count = sum(1 for line in req.read_text().splitlines()
                            if line.strip() and not line.startswith("#"))
        elif pyproj.is_file():
            text = pyproj.read_text()
            dep_count = text.count("\n")
        self._add_metric(platform, "py_deps", dep_count, "deps")

        # venv size
        venv = path / ".venv"
        if venv.is_dir():
            self._add_metric(platform, "install_footprint",
                             size_of(str(venv)), "KB", ".venv/")
        else:
            self._add_metric(platform, "install_footprint", 0, "KB",
                             "no .venv")

        # Cold start via import
        venv_python = self._find_venv_python(path)
        python_bin = venv_python or "python3"

        import_stmt = _PYTHON_IMPORTS.get(platform)
        if import_stmt:
            cmd = [python_bin, "-c",
                   f"import time; t=time.time(); {import_stmt[0]}; "
                   f"print(f'{{(time.time()-t)*1000:.2f}}ms')"]
            rc, out = time_command(cmd, timeout=30)
            if rc == 0 and out.strip().endswith("ms"):
                try:
                    val = float(out.strip().rstrip("ms"))
                    self._add_metric(platform, "cold_start_time",
                                     round(val, 2), "ms",
                                     f"python {import_stmt[1]}")
                except ValueError:
                    self._add_metric(platform, "cold_start_time", 0, "ms",
                                     "import failed")
            else:
                self._add_metric(platform, "cold_start_time", 0, "ms",
                                 "package not importable")
        else:
            self._add_metric(platform, "cold_start_time", 0, "ms",
                             "no import mapping")
