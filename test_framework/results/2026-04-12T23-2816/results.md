# Test Results — 2026-04-12T23:2816

| Status | Count |
|--------|-------|
| PASS   | 139 |
| FAIL   | 23 |
| SKIP   | 0 |
| **Total** | **162** |

## All Results

| Status | Test ID | Description | Detail |
|--------|---------|-------------|--------|
| PASS | openclaw.init | Submodule exists and populated | 
 |
| PASS | openclaw.manifest | Has package.json | pass (package.json found)
 |
| PASS | openclaw.source | Has TypeScript source | pass (5941 TypeScript files)
 |
| PASS | openclaw.lock | Has lockfile | pass
 |
| PASS | openclaw.ci_lang | Has TS CI | pass (9 GitHub Actions workflows)
 |
| PASS | openclaw.docker | Has Docker | pass (Docker config found)
 |
| PASS | openclaw.license | Has open-source license | pass
 |
| PASS | openclaw.readme | Has README | pass
 |
| PASS | openclaw.changelog | Has CHANGELOG | pass
 |
| PASS | openclaw.contributing | Has CONTRIBUTING | pass
 |
| PASS | openclaw.gitignore | Has .gitignore | pass
 |
| PASS | openclaw.ci | Has CI configuration | pass
 |
| PASS | clawteam.init | Submodule exists and populated | 
 |
| PASS | clawteam.manifest | Has Python manifest | pass
 |
| PASS | clawteam.source | Has Python source | pass (75 Python source files)
 |
| PASS | clawteam.docker | Has Docker | WARN: no Dockerfile
 |
| PASS | clawteam.ci_lang | Has Python CI | pass (1 GitHub Actions workflows)
 |
| PASS | clawteam.tests_dir | Has tests directory | pass (28 test files)
 |
| PASS | clawteam.license | Has open-source license | pass
 |
| PASS | clawteam.readme | Has README | pass
 |
| FAIL | clawteam.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| FAIL | clawteam.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | clawteam.gitignore | Has .gitignore | pass
 |
| PASS | clawteam.ci | Has CI configuration | pass
 |
| PASS | goclaw.init | Submodule exists and populated | 
 |
| PASS | goclaw.manifest | Has go.mod | pass (go.mod found)
 |
| PASS | goclaw.source | Has Go source files | pass (524 Go source files)
 |
| PASS | goclaw.sum | Has go.sum | pass
 |
| PASS | goclaw.ci_lang | Has Go CI | pass (2 GitHub Actions workflows)
 |
| PASS | goclaw.docker | Has Docker | pass (Dockerfile found)
 |
| PASS | goclaw.makefile | Has Makefile | pass
 |
| FAIL | goclaw.license | Has open-source license | FAIL: no file matching 'LICENSE' found
 |
| PASS | goclaw.readme | Has README | pass
 |
| FAIL | goclaw.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| FAIL | goclaw.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | goclaw.gitignore | Has .gitignore | pass
 |
| PASS | goclaw.ci | Has CI configuration | pass
 |
| PASS | ironclaw.init | Submodule exists and populated | 
 |
| PASS | ironclaw.manifest | Has Cargo.toml | pass (Cargo.toml found)
 |
| PASS | ironclaw.workspace | Workspace structure | pass (workspace detected)
 |
| PASS | ironclaw.source | Has Rust source files | pass (287 Rust source files)
 |
| PASS | ironclaw.lock | Has Cargo.lock | pass
 |
| PASS | ironclaw.clippy | Has clippy config | pass (clippy config found)
 |
| PASS | ironclaw.ci_lang | Has Rust CI | pass (11 GitHub Actions workflows)
 |
| PASS | ironclaw.deny | Has cargo-deny | WARN: no cargo-deny config
 |
| PASS | ironclaw.license | Has open-source license | pass
 |
| PASS | ironclaw.readme | Has README | pass
 |
| PASS | ironclaw.changelog | Has CHANGELOG | pass
 |
| PASS | ironclaw.contributing | Has CONTRIBUTING | pass
 |
| PASS | ironclaw.gitignore | Has .gitignore | pass
 |
| PASS | ironclaw.ci | Has CI configuration | pass
 |
| PASS | maxclaw.init | Submodule exists and populated | 
 |
| PASS | maxclaw.manifest | Has go.mod | pass (go.mod found)
 |
| PASS | maxclaw.source | Has Go source files | pass (118 Go source files)
 |
| PASS | maxclaw.sum | Has go.sum | pass
 |
| PASS | maxclaw.ci_lang | Has Go CI | pass (2 GitHub Actions workflows)
 |
| PASS | maxclaw.docker | Has Docker | pass (Dockerfile found)
 |
| PASS | maxclaw.makefile | Has Makefile | pass
 |
| PASS | maxclaw.license | Has open-source license | pass
 |
| PASS | maxclaw.readme | Has README | pass
 |
| PASS | maxclaw.changelog | Has CHANGELOG | pass
 |
| FAIL | maxclaw.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | maxclaw.gitignore | Has .gitignore | pass
 |
| PASS | maxclaw.ci | Has CI configuration | pass
 |
| PASS | nanoclaw.init | Submodule exists and populated | 
 |
| PASS | nanoclaw.manifest | Has package.json | pass (package.json found)
 |
| PASS | nanoclaw.source | Has TypeScript source | pass (61 TypeScript files)
 |
| PASS | nanoclaw.lock | Has lockfile | pass
 |
| PASS | nanoclaw.ci_lang | Has TS CI | pass (4 GitHub Actions workflows)
 |
| PASS | nanoclaw.docker | Has Docker | WARN: no Dockerfile
 |
| PASS | nanoclaw.license | Has open-source license | pass
 |
| PASS | nanoclaw.readme | Has README | pass
 |
| PASS | nanoclaw.changelog | Has CHANGELOG | pass
 |
| PASS | nanoclaw.contributing | Has CONTRIBUTING | pass
 |
| PASS | nanoclaw.gitignore | Has .gitignore | pass
 |
| PASS | nanoclaw.ci | Has CI configuration | pass
 |
| PASS | nanobot.init | Submodule exists and populated | 
 |
| PASS | nanobot.manifest | Has Python manifest | pass
 |
| PASS | nanobot.source | Has Python source | pass (88 Python source files)
 |
| PASS | nanobot.docker | Has Docker | pass (Docker config found)
 |
| PASS | nanobot.ci_lang | Has Python CI | WARN: no CI detected
 |
| PASS | nanobot.tests_dir | Has tests directory | pass (26 test files)
 |
| PASS | nanobot.license | Has open-source license | pass
 |
| PASS | nanobot.readme | Has README | pass
 |
| FAIL | nanobot.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| FAIL | nanobot.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | nanobot.gitignore | Has .gitignore | pass
 |
| FAIL | nanobot.ci | Has CI configuration | FAIL: no file matching '.github' found
 |
| PASS | zeroclaw.init | Submodule exists and populated | 
 |
| PASS | zeroclaw.manifest | Has Cargo.toml | pass (Cargo.toml found)
 |
| PASS | zeroclaw.workspace | Workspace structure | pass (workspace detected)
 |
| PASS | zeroclaw.source | Has Rust source files | pass (227 Rust source files)
 |
| PASS | zeroclaw.lock | Has Cargo.lock | pass
 |
| PASS | zeroclaw.clippy | Has clippy config | pass (clippy config found)
 |
| PASS | zeroclaw.ci_lang | Has Rust CI | pass (4 GitHub Actions workflows)
 |
| PASS | zeroclaw.deny | Has cargo-deny | pass (cargo-deny config found)
 |
| PASS | zeroclaw.license | Has open-source license | pass
 |
| PASS | zeroclaw.readme | Has README | pass
 |
| PASS | zeroclaw.changelog | Has CHANGELOG | pass
 |
| PASS | zeroclaw.contributing | Has CONTRIBUTING | pass
 |
| PASS | zeroclaw.gitignore | Has .gitignore | pass
 |
| PASS | zeroclaw.ci | Has CI configuration | pass
 |
| PASS | hiclaw.init | Submodule exists and populated | 
 |
| FAIL | hiclaw.manifest | Has go.mod | FAIL: go.mod not found
 |
| PASS | hiclaw.source | Has Go source files | pass (23 Go source files)
 |
| PASS | hiclaw.sum | Has go.sum | WARN: no go.sum
 |
| PASS | hiclaw.ci_lang | Has Go CI | pass (7 GitHub Actions workflows)
 |
| PASS | hiclaw.docker | Has Docker | WARN: no Dockerfile
 |
| PASS | hiclaw.makefile | Has Makefile | pass
 |
| PASS | hiclaw.license | Has open-source license | pass
 |
| PASS | hiclaw.readme | Has README | pass
 |
| FAIL | hiclaw.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| FAIL | hiclaw.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | hiclaw.gitignore | Has .gitignore | pass
 |
| PASS | hiclaw.ci | Has CI configuration | pass
 |
| PASS | rtl-claw.init | Submodule exists and populated | 
 |
| PASS | rtl-claw.readme | Has README | pass
 |
| PASS | rtl-claw.source | Has Verilog source files | pass (28 Verilog/HDL source files)
 |
| FAIL | rtl-claw.makefile | Has Makefile | FAIL: no file matching 'Makefile' found
 |
| PASS | rtl-claw.docker | Has Docker | pass
 |
| PASS | rtl-claw.license | Has open-source license | pass
 |
| PASS | rtl-claw.readme | Has README | pass
 |
| FAIL | rtl-claw.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| FAIL | rtl-claw.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | rtl-claw.gitignore | Has .gitignore | pass
 |
| FAIL | rtl-claw.ci | Has CI configuration | FAIL: no file matching '.github' found
 |
| PASS | quantumclaw.init | Submodule exists and populated | 
 |
| PASS | quantumclaw.manifest | Has package.json | pass (package.json found)
 |
| FAIL | quantumclaw.source | Has TypeScript source | FAIL: no TypeScript source files
 |
| PASS | quantumclaw.lock | Has lockfile | pass
 |
| PASS | quantumclaw.ci_lang | Has TS CI | pass (2 GitHub Actions workflows)
 |
| PASS | quantumclaw.docker | Has Docker | pass (Docker config found)
 |
| PASS | quantumclaw.license | Has open-source license | pass
 |
| PASS | quantumclaw.readme | Has README | pass
 |
| PASS | quantumclaw.changelog | Has CHANGELOG | pass
 |
| PASS | quantumclaw.contributing | Has CONTRIBUTING | pass
 |
| PASS | quantumclaw.gitignore | Has .gitignore | pass
 |
| PASS | quantumclaw.ci | Has CI configuration | pass
 |
| PASS | claw-ai-lab.init | Submodule exists and populated | 
 |
| FAIL | claw-ai-lab.manifest | Has Python manifest | FAIL: no Python package manifest found
 |
| PASS | claw-ai-lab.source | Has Python source | pass (217 Python source files)
 |
| PASS | claw-ai-lab.docker | Has Docker | WARN: no Dockerfile
 |
| PASS | claw-ai-lab.ci_lang | Has Python CI | WARN: no CI detected
 |
| PASS | claw-ai-lab.tests_dir | Has tests directory | WARN: no tests/ directory
 |
| FAIL | claw-ai-lab.license | Has open-source license | FAIL: no file matching 'LICENSE' found
 |
| PASS | claw-ai-lab.readme | Has README | pass
 |
| FAIL | claw-ai-lab.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| FAIL | claw-ai-lab.contributing | Has CONTRIBUTING | FAIL: no file matching 'CONTRIBUTING' found
 |
| PASS | claw-ai-lab.gitignore | Has .gitignore | pass
 |
| FAIL | claw-ai-lab.ci | Has CI configuration | FAIL: no file matching '.github' found
 |
| PASS | hermes-agent.init | Submodule exists and populated | 
 |
| PASS | hermes-agent.manifest | Has Python manifest | pass
 |
| PASS | hermes-agent.source | Has Python source | pass (822 Python source files)
 |
| PASS | hermes-agent.docker | Has Docker | pass (Docker config found)
 |
| PASS | hermes-agent.ci_lang | Has Python CI | pass (6 GitHub Actions workflows)
 |
| PASS | hermes-agent.tests_dir | Has tests directory | pass (524 test files)
 |
| PASS | hermes-agent.license | Has open-source license | pass
 |
| PASS | hermes-agent.readme | Has README | pass
 |
| FAIL | hermes-agent.changelog | Has CHANGELOG | FAIL: no file matching 'CHANGELOG' found
 |
| PASS | hermes-agent.contributing | Has CONTRIBUTING | pass
 |
| PASS | hermes-agent.gitignore | Has .gitignore | pass
 |
| PASS | hermes-agent.ci | Has CI configuration | pass
 |

