"""Static analysis benchmarks for the AllClaws benchmark suite."""

import json
import os
import re
from pathlib import Path
from typing import Optional

from .utils import (
    BenchmarkResult,
    Metric,
    detect_toolchain,
    load_config,
    now_timestamp,
    size_of,
)


# Directories to exclude from file/LOC counting (matching bash script)
_EXCLUDED_DIRS = {
    ".git", "node_modules", "target", "vendor", "__pycache__",
    ".venv", "venv", "dist", "build", ".next", "coverage",
    ".turbo", ".claude",
}


class StaticBenchmark:
    """Run static code analysis benchmarks across all platforms."""

    def __init__(self, config_path: str, output_dir: str,
                 platforms: list = None, skip: list = None):
        self.config = load_config(config_path)
        self.output_dir = Path(output_dir)
        self.platforms = platforms or list(self.config["supported_platforms"])
        self.skip = skip or []
        self.toolchain = detect_toolchain()
        self.metrics: list[Metric] = []
        self.skipped: list[dict] = []
        self.languages = self.config.get("platform_languages", {})

    def run(self) -> BenchmarkResult:
        """Execute all static benchmarks and return results."""
        for platform in self.platforms:
            if platform in self.skip:
                continue
            self._benchmark_platform(platform)
        return self._build_result()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _add_metric(self, platform, metric, value, unit, notes=""):
        self.metrics.append(Metric(
            platform=platform, metric=metric, value=value,
            unit=unit, notes=notes,
        ))

    def _skip_platform(self, platform, reason):
        self.skipped.append({"platform": platform, "reason": reason})
        print(f"  SKIP: {reason}")

    def _build_result(self) -> BenchmarkResult:
        return BenchmarkResult(
            timestamp=now_timestamp(),
            engine_version="3.0.0",
            command="static",
            toolchain=self.toolchain,
            metrics=self.metrics,
            skipped=self.skipped,
        )

    def _platform_path(self, platform: str) -> Optional[Path]:
        """Resolve platform directory from config or fallback."""
        rel = self.config.get("platform_paths", {}).get(platform)
        if rel:
            p = (Path(__file__).resolve().parent.parent / rel).resolve()
            if p.is_dir():
                return p
        fallback = Path(__file__).resolve().parent.parent.parent / platform
        if fallback.is_dir():
            return fallback
        return None

    def _platform_language(self, platform: str) -> str:
        """Get the language for a platform from config."""
        return self.languages.get(platform, "Unknown")

    # ------------------------------------------------------------------
    # Platform benchmark
    # ------------------------------------------------------------------

    def _benchmark_platform(self, platform: str):
        path = self._platform_path(platform)
        lang = self._platform_language(platform)
        print(f"--- {platform} ({lang}) ---")

        if not path:
            self._skip_platform(platform, "submodule not populated")
            print()
            return

        # Universal metrics
        self._add_metric(platform, "repo_size",
                         self._get_repo_size(path), "KB")

        readme_lines = self._get_readme_lines(path)
        self._add_metric(platform, "readme_lines", readme_lines, "lines")

        docs_size = self._get_docs_size(path)
        self._add_metric(platform, "docs_size", docs_size, "KB")

        ci_workflows = self._count_ci_workflows(path)
        self._add_metric(platform, "ci_workflows", ci_workflows, "files")

        ci_steps = self._count_ci_steps(path)
        self._add_metric(platform, "ci_steps", ci_steps, "steps")

        dockerfiles = self._count_dockerfiles(path)
        self._add_metric(platform, "dockerfiles", dockerfiles, "files")

        makefile_targets = self._count_makefile_targets(path)
        self._add_metric(platform, "makefile_targets", makefile_targets, "targets")

        test_files = self._count_test_files(path)
        self._add_metric(platform, "test_files", test_files, "files")

        i18n_files = self._count_i18n_files(path)
        self._add_metric(platform, "i18n_files", i18n_files, "files")

        top_level_dirs = self._count_top_level_dirs(path)
        self._add_metric(platform, "top_level_dirs", top_level_dirs, "dirs")

        # Language-specific metrics
        if lang == "Rust":
            self._benchmark_rust(platform, path)
        elif lang == "TypeScript":
            self._benchmark_typescript(platform, path)
        elif lang == "Go":
            self._benchmark_go(platform, path)
        elif lang == "Python":
            self._benchmark_python(platform, path)
        elif lang == "Verilog":
            self._benchmark_verilog(platform, path)

        print()

    # ------------------------------------------------------------------
    # Language-specific static analysis
    # ------------------------------------------------------------------

    def _benchmark_rust(self, platform, path):
        self._add_metric(platform, "rust_files",
                         self._count_files(path, "rs"), "files")
        self._add_metric(platform, "rust_loc",
                         self._count_loc(path, "rs"), "lines")
        self._add_metric(platform, "toml_files",
                         self._count_files(path, "toml"), "files")
        cargo_deps = self._count_cargo_deps(path)
        self._add_metric(platform, "cargo_deps", cargo_deps, "deps")

    def _benchmark_typescript(self, platform, path):
        self._add_metric(platform, "ts_files",
                         self._count_files(path, "ts"), "files")
        self._add_metric(platform, "ts_loc",
                         self._count_loc(path, "ts"), "lines")
        self._add_metric(platform, "tsx_files",
                         self._count_files(path, "tsx"), "files")
        self._add_metric(platform, "tsx_loc",
                         self._count_loc(path, "tsx"), "lines")
        self._add_metric(platform, "json_files",
                         self._count_files(path, "json"), "files")
        npm_deps = self._count_npm_deps(path)
        self._add_metric(platform, "npm_deps", npm_deps, "deps")

    def _benchmark_go(self, platform, path):
        self._add_metric(platform, "go_files",
                         self._count_files(path, "go"), "files")
        self._add_metric(platform, "go_loc",
                         self._count_loc(path, "go"), "lines")
        go_deps = self._count_go_deps(path)
        self._add_metric(platform, "go_deps", go_deps, "deps")

    def _benchmark_python(self, platform, path):
        self._add_metric(platform, "py_files",
                         self._count_files(path, "py"), "files")
        self._add_metric(platform, "py_loc",
                         self._count_loc(path, "py"), "lines")
        py_deps = self._count_py_deps(path)
        self._add_metric(platform, "py_deps", py_deps, "deps")

    def _benchmark_verilog(self, platform, path):
        self._add_metric(platform, "verilog_files",
                         self._count_files(path, "v"), "files")
        self._add_metric(platform, "verilog_loc",
                         self._count_loc(path, "v"), "lines")
        self._add_metric(platform, "systemverilog_files",
                         self._count_files(path, "sv"), "files")
        workspace_dirs = 0
        ws = path / "workspace"
        if ws.is_dir():
            workspace_dirs = sum(1 for d in ws.iterdir() if d.is_dir())
        self._add_metric(platform, "workspace_dirs", workspace_dirs, "dirs")

    # ------------------------------------------------------------------
    # File counting utilities
    # ------------------------------------------------------------------

    def _walk_files(self, path: Path, maxdepth: int = 5):
        """Walk directory tree, excluding build/venv dirs."""
        for dirpath, dirnames, filenames in os.walk(path):
            depth = dirpath[len(str(path)):].count(os.sep) + 1
            if depth > maxdepth:
                dirnames.clear()
                continue
            dirnames[:] = [d for d in dirnames if d not in _EXCLUDED_DIRS]
            for f in filenames:
                yield os.path.join(dirpath, f)

    def _count_files(self, path: Path, ext: str, maxdepth: int = 5) -> int:
        """Count files with a given extension."""
        count = 0
        for f in self._walk_files(path, maxdepth):
            if f.endswith(f".{ext}"):
                count += 1
        return count

    def _count_loc(self, path: Path, ext: str, maxdepth: int = 5) -> int:
        """Count total lines of code for files with given extension."""
        total = 0
        for f in self._walk_files(path, maxdepth):
            if f.endswith(f".{ext}"):
                try:
                    with open(f) as fh:
                        total += sum(1 for _ in fh)
                except OSError:
                    pass
        return total

    def _get_repo_size(self, path: Path) -> int:
        """Repository size in KB excluding build artifacts."""
        return size_of(str(path))

    def _get_readme_lines(self, path: Path) -> int:
        """Count README file lines."""
        for name in sorted(path.iterdir()):
            if name.is_file() and name.name.lower().startswith("readme"):
                try:
                    with open(name) as f:
                        return sum(1 for _ in f)
                except OSError:
                    return 0
        return 0

    def _get_docs_size(self, path: Path) -> int:
        """Documentation directory size in KB."""
        docs = path / "docs"
        if docs.is_dir():
            return size_of(str(docs))
        return 0

    def _count_ci_workflows(self, path: Path) -> int:
        """Count GitHub Actions workflow files."""
        wf_dir = path / ".github" / "workflows"
        if not wf_dir.is_dir():
            return 0
        return sum(1 for f in wf_dir.iterdir()
                   if f.is_file() and f.suffix in (".yml", ".yaml"))

    def _count_ci_steps(self, path: Path) -> int:
        """Count total CI/CD steps across all workflows."""
        wf_dir = path / ".github" / "workflows"
        if not wf_dir.is_dir():
            return 0
        total = 0
        step_re = re.compile(r"^\s*-\s*(uses|run):")
        for f in wf_dir.iterdir():
            if f.is_file() and f.suffix in (".yml", ".yaml"):
                try:
                    text = f.read_text()
                    total += sum(1 for line in text.splitlines()
                                if step_re.match(line))
                except OSError:
                    pass
        return total

    def _count_dockerfiles(self, path: Path) -> int:
        """Count Dockerfiles."""
        count = 0
        for f in self._walk_files(path, maxdepth=4):
            name = os.path.basename(f)
            if name.startswith("Dockerfile") or name.endswith(".dockerfile"):
                count += 1
        return count

    def _count_makefile_targets(self, path: Path) -> int:
        """Count Makefile targets."""
        mf = path / "Makefile"
        if not mf.is_file():
            return 0
        try:
            text = mf.read_text()
            return sum(1 for line in text.splitlines()
                       if re.match(r"^[a-zA-Z_-]+:", line))
        except OSError:
            return 0

    def _count_test_files(self, path: Path) -> int:
        """Count test files across languages."""
        count = 0
        for f in self._walk_files(path, maxdepth=5):
            name = os.path.basename(f)
            if name.endswith("_test.go"):
                count += 1
            elif name.startswith("test_") and name.endswith(".py"):
                count += 1
            elif name.endswith(".test.ts") or name.endswith(".test.tsx"):
                count += 1
            elif name.endswith(".spec.ts") or name.endswith(".spec.tsx"):
                count += 1
            elif "tests" in f.split(os.sep) and name.endswith(".rs"):
                count += 1
        return count

    def _count_i18n_files(self, path: Path) -> int:
        """Count internationalization files."""
        count = 0
        i18n_markers = (".zh-CN.md", ".zh_CN.md", ".zh.md")
        for f in self._walk_files(path, maxdepth=4):
            if any(f.endswith(m) for m in i18n_markers):
                count += 1
            # Check for i18n/locales/messages directories
            parts = f.split(os.sep)
            if any(p in ("i18n", "locales", "messages") for p in parts):
                count += 1
        return min(count, 9999)  # Cap to avoid inflated counts from dir walks

    def _count_top_level_dirs(self, path: Path) -> int:
        """Count top-level directories (complexity indicator)."""
        return sum(1 for d in path.iterdir() if d.is_dir())

    def _count_cargo_deps(self, path: Path) -> int:
        """Count Cargo.toml dependencies."""
        cargo = path / "Cargo.toml"
        if not cargo.is_file():
            return 0
        try:
            text = cargo.read_text()
            # Count lines that look like dependency declarations
            count = sum(1 for line in text.splitlines()
                       if re.match(r'^\w+\s*=\s*"', line))
            if count == 0:
                count = sum(1 for line in text.splitlines()
                           if '"' in line and any(c.isalpha() for c in line))
            return min(count, 9999)
        except OSError:
            return 0

    def _count_npm_deps(self, path: Path) -> int:
        """Count npm dependencies."""
        pkg = path / "package.json"
        if not pkg.is_file():
            return 0
        try:
            data = json.loads(pkg.read_text())
            deps = len(data.get("dependencies", {}))
            dev_deps = len(data.get("devDependencies", {}))
            return deps + dev_deps
        except (OSError, json.JSONDecodeError):
            return 0

    def _count_go_deps(self, path: Path) -> int:
        """Count go.mod dependencies."""
        mod = path / "go.mod"
        if not mod.is_file():
            return 0
        try:
            text = mod.read_text()
            return sum(1 for line in text.splitlines()
                       if re.match(r"^\s+\S+\s+v", line))
        except OSError:
            return 0

    def _count_py_deps(self, path: Path) -> int:
        """Count Python dependencies."""
        # Try pyproject.toml first
        pp = path / "pyproject.toml"
        if pp.is_file():
            try:
                text = pp.read_text()
                return sum(1 for line in text.splitlines()
                           if line.strip().startswith('"')
                           and any(c.isalpha() for c in line))
            except OSError:
                pass
        # Try requirements.txt
        req = path / "requirements.txt"
        if req.is_file():
            try:
                text = req.read_text()
                return sum(1 for line in text.splitlines()
                           if line.strip() and not line.strip().startswith("#"))
            except OSError:
                pass
        return 0
