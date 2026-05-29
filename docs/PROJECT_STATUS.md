# AllClaws 项目状态 — 2026-05-28

## 总览
- 仓库: dz3ai/allclaws (GitHub)
- 平台数: 25 (13 Claw + 8 External + 3 CLI + 1 Digital Twin)
- 最近提交: f787ab2 — feat: add Reasonix as 25th tracked platform
- 分支: main, up to date with origin

## 今日活动 (2026-05-28)
1. ⏰ 06:00 晨间简报已自动发送
2. ✅ Benchmark Suite CI 定时运行成功 (run #26574334232, 17s)
3. ❌ Agent Platform Tests 仍失败 (run #26519138201, 1m19s) — Test openclaw 步骤 fail
4. 📋 会话中调研 tirith 终端安全扫描器 (sheeki03/tirith, Rust crate v0.3.1)
5. 📋 13 个 submodule 有新 commit 未更新 (工作树有 modified submodules)

## 已完成 (累计)
1. ✅ Benchmark 系统 Python 重写 (7 files, 2210 lines, v3.0)
   - cli.py, utils.py, runtime.py, static.py, sandbox.py, report.py
   - N=5 采样统计 (mean/stddev/P95)
   - 纯 stdlib，零外部依赖 (argparse)
2. ✅ CI workflow: benchmark-suite.yml
   - Mon-Fri daily, Sat weekly report, Sun submodules
   - 已验证 green (run #26336478749, #26574334232)
3. ✅ 本地 benchmark 环境设置完成
   - Python venvs: clawteam, nanobot, hermes-agent, aider, hiclaw/copaw
   - Node deps: openclaw, nanoclaw, quantumclaw
   - Go mod download: goclaw, maxclaw
   - Go 1.24.4: ~/local/go/bin
   - Rust target: ironclaw (3.1G), zeroclaw
   - 真实数据验证: 59 metrics, cold_start/memory 均非 fallback 值
4. ✅ 文档更新: 24→25 平台 (OpenFang + Reasonix)
5. ✅ CI 修复:
   - agent-tests.yml YAML 语法错误 L138 (inline Python 缩进问题)
   - results/ + benchmark_results/ 冒号目录名全部重命名 (48 renames)
   - benchmark_results/ 加入 .gitignore
6. ✅ zh-CN 翻译同步完成 (MISSION, ROADMAP, platform_comparison)
7. ✅ 定时任务配置: 23:30 会话保存 + 06:00 晨间恢复

## 进行中 / 待完成
1. 🔴 agent-tests.yml 跑通 — YAML 已修，冒号已修，但 Test openclaw 步骤仍 fail
   (可能是 test script 引用旧 bash 脚本路径)
2. 🟡 openhuman Rust 编译 — 需要 rustup toolchain install 1.93.0 (网络问题)
3. 🟡 openhuman submodule 未加入 .gitmodules (untracked)
4. 🟢 P3 文档修复 (低优先级)
5. 🟢 ROADMAP checklist: MCP ecosystem deep-dive, Enterprise governance
6. 🟢 GitHub Issue #1 "new players and category" — 内容已覆盖但未关闭
7. 🟢 13 个 submodule 有新 commit，需 weekly update

## 关键文件
- test_framework/benchmark/ — Python benchmark 包 (7 files, v3.0)
- test_framework/config.json — 25 platforms 配置
- .github/workflows/benchmark-suite.yml — CI workflow (Mon-Fri daily)
- .github/workflows/agent-tests.yml — 静态分析 + 基准测试
- docs/platform_comparison.md + .zh-CN.md — 平台对比矩阵
- architecture/ — 设计文档
- docs/PROJECT_STATUS.md — 本文件

## 工具链
- Go: ~/local/go/bin (export PATH=$PATH:$HOME/local/go/bin)
- Python: system 3.12
- Node: system (v25.8.0)
- Rust: 1.95.0 (openhuman 需要 1.93.0)

## CI 状态
- Benchmark Suite: ✅ green (最近 run #26574334232)
- Agent Platform Tests: ❌ failing (Test openclaw 步骤)
- Deploy Jekyll: ✅ green
