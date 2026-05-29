# AllClaws 项目状态 — 2026-05-29

## 总览
- 仓库: dz3ai/allclaws (GitHub)
- 平台数: 24 (11 Claw + 8 External + 4 CLI + 1 Digital Twin)
- 最近提交: 96afaa2 — blog: add OpenCode vs Claude Code comparison
- 分支: main, up to date with origin

## 今日活动 (2026-05-29)
1. ⏰ 06:00 晨间简报已自动发送
2. ✅ 移除 3 个平台: rtl-claw, quantumclaw, mcp-agent (commit 5bfb08a)
3. ✅ 新增 2 个平台: kimi-cli (Platform 26), kimi-code (Platform 27) (commit 5bfb08a)
   - 平台净变化: 25 → 24
   - 全文档 EN+ZH 同步 (README, MISSION, ROADMAP, LATEST_UPDATES, platform_comparison)
4. ✅ 子模块批量更新 (commit 454f072)
5. ✅ 新增博客: OpenCode vs Claude Code 对比分析 (commit 96afaa2)
6. ✅ Benchmark Suite CI 通过 (run #26644411437, 27s)
7. ❌ Agent Platform Tests 仍失败 (run #26644411336, 1m26s) — Test openclaw 步骤 fail
8. 📋 讨论 OpenAI Codex CLI (86.8K stars) 加入可行性 — 用户同意加入，尚未执行
9. 📋 讨论 agentscope 加入 — 子任务中断未完成

## 已完成 (累计)
1. ✅ Benchmark 系统 Python 重写 (7 files, 2210 lines, v3.0)
   - cli.py, utils.py, runtime.py, static.py, sandbox.py, report.py
   - N=5 采样统计 (mean/stddev/P95)
   - 纯 stdlib，零外部依赖 (argparse)
2. ✅ CI workflow: benchmark-suite.yml
   - Mon-Fri daily, Sat weekly report, Sun submodules
   - 已验证 green (run #26336478749, #26574334232, #26644411437)
3. ✅ 本地 benchmark 环境设置完成
   - Python venvs: clawteam, nanobot, hermes-agent, aider, hiclaw/copaw
   - Node deps: openclaw, nanoclaw
   - Go mod download: goclaw, maxclaw
   - Go 1.24.4: ~/local/go/bin
   - Rust target: ironclaw (3.1G), zeroclaw
   - 真实数据验证: 59 metrics, cold_start/memory 均非 fallback 值
4. ✅ 平台数修正: 25 → 24 (移除 rtl-claw/quantumclaw/mcp-agent, 新增 kimi-cli/kimi-code)
5. ✅ CI 修复:
   - agent-tests.yml YAML 语法错误 L138 (inline Python 缩进问题)
   - results/ + benchmark_results/ 冒号目录名全部重命名 (48 renames)
   - benchmark_results/ 加入 .gitignore
6. ✅ zh-CN 翻译同步完成 (MISSION, ROADMAP, platform_comparison, LATEST_UPDATES)
7. ✅ 定时任务配置: 23:30 会话保存 + 06:00 晨间恢复
8. ✅ 平台清理: QuantumClaw/RTL-CLAW/mcp-agent 从 11 个文件中移除 (gitmodules, config, docs EN+ZH)

## 进行中 / 待完成
1. 🔴 agent-tests.yml 跑通 — YAML 已修，冒号已修，但 Test openclaw 步骤仍 fail
   (可能是 test script 引用旧 bash 脚本路径, 连续多日失败)
2. 🟠 OpenAI Codex CLI 加入 — 用户确认加入 (86.8K stars, Rust, Apache-2.0)
   待更新: config.json, .gitmodules, README×2, MISSION×2, ROADMAP×2, LATEST_UPDATES×2, platform_comparison×2
3. 🟡 openhuman Rust 编译 — 需要 rustup toolchain install 1.93.0 (网络问题)
4. 🟡 openhuman submodule 未加入 .gitmodules (untracked)
5. 🟡 agentscope 待评估加入 (子任务中断未完成)
6. 🟢 architecture/platform_comparison.md + .zh-CN.md — 移除 3 平台的分析段落可能未清理完全
7. 🟢 GitHub Issue #1 "new players and category" — 内容已覆盖但未关闭
8. 🟢 子模块更新 (3 个 untracked: claw-ai-lab, hermes-agent, nanoclaw)

## 关键文件
- test_framework/benchmark/ — Python benchmark 包 (7 files, v3.0)
- test_framework/config.json — 24 platforms 配置
- .github/workflows/benchmark-suite.yml — CI workflow (Mon-Fri daily)
- .github/workflows/agent-tests.yml — 静态分析 + 基准测试
- architecture/platform_comparison.md + .zh-CN.md — 平台对比矩阵
- docs/MISSION.md + .zh-CN.md — 项目使命
- docs/ROADMAP.md + .zh-CN.md — 路线图
- docs/LATEST_UPDATES.md + .zh-CN.md — 最新动态
- docs/PROJECT_STATUS.md — 本文件

## 工具链
- Go: ~/local/go/bin (export PATH=$PATH:$HOME/local/go/bin)
- Python: system 3.12
- Node: system (v25.8.0)
- Rust: 1.95.0 (openhuman 需要 1.93.0)

## CI 状态
- Benchmark Suite: ✅ green (最近 run #26644411437)
- Agent Platform Tests: ❌ failing (Test openclaw 步骤)
- Deploy Jekyll: ✅ green
