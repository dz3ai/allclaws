"""Sandbox/container health check benchmarks for the AllClaws benchmark suite."""

import json
import re
import subprocess
from pathlib import Path
from typing import Optional

from .utils import (
    BenchmarkResult,
    Metric,
    detect_toolchain,
    load_config,
    now_timestamp,
)


class SandboxBenchmark:
    """Run Docker/Podman container health checks across all platforms."""

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

        # Detect container runtime
        self.container_cmd = None
        self.compose_cmd = None
        if self.toolchain.get("podman"):
            self.container_cmd = "podman"
            self.compose_cmd = "podman-compose"
        elif self.toolchain.get("docker"):
            self.container_cmd = "docker"
            self.compose_cmd = "docker-compose"

    def run(self) -> BenchmarkResult:
        """Execute sandbox health checks and return results."""
        if not self.container_cmd:
            print("WARN: No container runtime found (docker or podman required)")
            # Add a finding metric about missing runtime
            self.metrics.append(Metric(
                platform="all", metric="finding",
                value=1, unit="critical",
                notes="no container runtime available (docker or podman required)",
            ))
        else:
            print(f"Container runtime: {self.container_cmd}")
            print(f"Compose command:   {self.compose_cmd}")
            print()
            for platform in self.platforms:
                if platform in self.skip:
                    continue
                self._check_platform(platform)

        return self._build_result()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _add_metric(self, platform, metric, value, unit, notes=""):
        self.metrics.append(Metric(
            platform=platform, metric=metric, value=value,
            unit=unit, notes=notes,
        ))

    def _add_finding(self, platform, category, severity, message, action=""):
        """Add a finding as a metric. Severity becomes the unit."""
        self._add_metric(platform, "finding", 1, severity,
                         f"{category} | {message}" +
                         (f" | Action: {action}" if action else ""))

    def _skip_platform(self, platform, reason):
        self.skipped.append({"platform": platform, "reason": reason})
        print(f"  SKIP: {reason}")

    def _build_result(self) -> BenchmarkResult:
        return BenchmarkResult(
            timestamp=now_timestamp(),
            engine_version="3.0.0",
            command="sandbox",
            toolchain=self.toolchain,
            metrics=self.metrics,
            skipped=self.skipped,
        )

    def _platform_language(self, platform: str) -> str:
        return self.languages.get(platform, "Unknown").lower()

    def _container_name(self, platform: str) -> str:
        return f"{platform}-test"

    def _exec(self, args: list, timeout: int = 30) -> tuple:
        """Run command in container context. Returns (returncode, stdout, stderr)."""
        try:
            proc = subprocess.run(
                args, capture_output=True, text=True, timeout=timeout,
            )
            return (proc.returncode, proc.stdout, proc.stderr)
        except subprocess.TimeoutExpired:
            return (-1, "", "timeout")
        except OSError as e:
            return (-1, "", str(e))

    def _container_running(self, name: str) -> bool:
        """Check if a container is running."""
        rc, out, _ = self._exec([
            self.container_cmd, "ps", "--format", "{{.Names}}",
        ])
        if rc == 0:
            return name in out.splitlines()
        return False

    def _exec_in_container(self, name: str, cmd: list,
                           timeout: int = 30) -> tuple:
        """Execute command inside a container. Returns (rc, stdout, stderr)."""
        return self._exec(
            [self.container_cmd, "exec", name] + cmd,
            timeout=timeout,
        )

    # ------------------------------------------------------------------
    # Platform checks
    # ------------------------------------------------------------------

    def _check_platform(self, platform: str):
        lang = self._platform_language(platform)
        container = self._container_name(platform)
        print(f"--- {platform} ({lang}) ---")

        if not self._container_running(container):
            self._add_finding(
                platform, "container", "critical",
                "Container not running",
                f"Start with: {self.compose_cmd} up -d {platform}-sandbox",
            )
            print(f"  Container not running: {container}")
            print()
            return

        print(f"  Container running: {container}")

        # Language-specific checks
        if lang == "rust":
            self._check_rust(platform, container)
        elif lang == "go":
            self._check_go(platform, container)
        elif lang == "python":
            self._check_python(platform, container)
        elif lang == "typescript":
            self._check_typescript(platform, container)
        elif lang == "verilog":
            self._check_verilog(platform, container)

        print()

    def _check_rust(self, platform: str, container: str):
        # Check Rust version
        rc, out, _ = self._exec_in_container(
            container, ["cargo", "--version"])
        if rc == 0:
            version = re.search(r"cargo (\S+)", out)
            ver_str = version.group(1) if version else "unknown"
            print(f"  Rust: {ver_str}")

            # Check edition2024 requirement
            rc2, out2, _ = self._exec_in_container(
                container, ["grep", "-q", 'edition = "2024"', "/workspace/Cargo.toml"])
            if rc2 == 0 and ver_str != "unknown":
                major, minor = ver_str.split(".")[:2]
                if int(major) < 1 or (int(major) == 1 and int(minor) < 84):
                    self._add_finding(
                        platform, "build", "error",
                        f"Rust {ver_str} doesn't support edition2024 (requires 1.84+)",
                        "Update docker-compose.yml: rust:alpine (latest)",
                    )

        # Try cargo check
        print("  Running cargo check...")
        rc, out, err = self._exec_in_container(
            container, ["cargo", "check"], timeout=300)
        if rc == 0:
            self._add_finding(platform, "build", "success", "cargo check passed")
            print("  cargo check passed")
        elif "error:" in err or "error:" in out:
            self._add_finding(
                platform, "build", "error", "cargo check failed",
                "Check Cargo.toml dependencies and Rust version",
            )
            print("  cargo check failed")

    def _check_go(self, platform: str, container: str):
        # Check Go version
        rc, out, _ = self._exec_in_container(
            container, ["go", "version"])
        if rc == 0:
            version = re.search(r"go(\S+)", out)
            ver_str = version.group(1) if version else "unknown"
            print(f"  Go: {ver_str}")

            # Check go.mod version requirement
            rc2, out2, _ = self._exec_in_container(
                container, ["grep", "-oP", r"go \K[0-9.]+", "/workspace/go.mod"])
            if rc2 == 0 and ver_str != "unknown":
                req_str = out2.strip()
                cur_parts = ver_str.split(".")
                req_parts = req_str.split(".")
                if (len(cur_parts) >= 2 and len(req_parts) >= 2 and
                        (int(cur_parts[0]) < int(req_parts[0]) or
                         (int(cur_parts[0]) == int(req_parts[0]) and
                          int(cur_parts[1]) < int(req_parts[1])))):
                    self._add_finding(
                        platform, "build", "error",
                        f"go.mod requires go {req_str}, sandbox has go {ver_str}",
                        f"Update docker-compose.yml: golang:1.{req_parts[1]}-alpine or golang:latest",
                    )

        # Try go build
        print("  Running go build...")
        rc, out, err = self._exec_in_container(
            container, ["go", "build", "-v", "./..."], timeout=300)
        if rc == 0:
            self._add_finding(platform, "build", "success", "go build passed")
            print("  go build passed")
        elif "error" in err or "error" in out:
            self._add_finding(
                platform, "build", "error", "go build failed",
                "Check go.mod dependencies and Go version",
            )
            print("  go build failed")

    def _check_python(self, platform: str, container: str):
        # Check Python version
        rc, out, _ = self._exec_in_container(container, ["python", "--version"])
        if rc == 0:
            print(f"  {out.strip()}")

        # Check for pytest
        rc, _, _ = self._exec_in_container(
            container, ["python", "-c", "import pytest"])
        if rc != 0:
            self._add_finding(
                platform, "test", "warning", "pytest not installed in sandbox",
                "Add to requirements.txt or Dockerfile",
            )
            print("  pytest not installed")

        # Check for manifest
        for manifest in ("pyproject.toml", "requirements.txt"):
            rc, _, _ = self._exec_in_container(
                container, ["test", "-f", f"/workspace/{manifest}"])
            if rc == 0:
                print(f"  Found {manifest}")
                break
        else:
            self._add_finding(
                platform, "build", "warning",
                "No pyproject.toml or requirements.txt",
                "Add Python dependency manifest",
            )

        # Try importing main module
        module_name = platform.replace("-", "")
        rc, _, _ = self._exec_in_container(
            container, ["python", "-c", f"import {module_name}"])
        if rc == 0:
            self._add_finding(platform, "build", "success",
                              "Module import successful")
            print("  Module import successful")

    def _check_typescript(self, platform: str, container: str):
        # Check Node version
        rc, out, _ = self._exec_in_container(container, ["node", "--version"])
        if rc == 0:
            print(f"  Node: {out.strip()}")

        # Check package.json exists
        rc, _, _ = self._exec_in_container(
            container, ["test", "-f", "/workspace/package.json"])
        if rc == 0:
            print("  Found package.json")

            # Check for build scripts
            rc2, out2, _ = self._exec_in_container(
                container, ["grep", "-q", '"build"', "/workspace/package.json"])
            if rc2 == 0:
                print("  Build script found")

                # Check for node_modules
                rc3, _, _ = self._exec_in_container(
                    container, ["test", "-d", "/workspace/node_modules"])
                if rc3 == 0:
                    self._add_finding(platform, "build", "success",
                                      "Dependencies installed")
                    print("  node_modules present")
                else:
                    self._add_finding(
                        platform, "build", "warning",
                        "node_modules missing (read-only mount prevents npm install)",
                        "Add writable volume for node_modules or use multi-stage build",
                    )
                    print("  node_modules missing (read-only mount)")

    def _check_verilog(self, platform: str, container: str):
        """Verilog/hardware platforms — limited checks."""
        self._add_finding(
            platform, "build", "info",
            "Hardware description language — limited sandbox checks",
        )
