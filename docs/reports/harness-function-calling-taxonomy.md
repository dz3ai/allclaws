# Harness Function-Calling Taxonomy — 按驱动协议分类跟踪的 harness

**日期:** 2026-11-21
**动机:** coder-30b 本地网格（13/40）显示出剧烈的协议分野——原生 function-calling 的 driver 正常工作，依赖模型自发产出结构化文本的 driver 收到「叙述性计划」。本文把 allclaws 跟踪的全部 29 个仓库按「是否原生执行 function-calling」分类。

**方法:** 对 13 个已实体化的 submodule 用 grep 探测两类证据（排除 `.venv/`、`node_modules/`、`/tests/`）：
- 原生命中 = 源码中出现 `tool_calls` / `tool_choice`（发送 tools schema 并解析结构化返回）
- 文本命中 = `SEARCH/REPLACE` / `<tool_call` / `<function_calls` / `edit_format` / `EditBlock` / `udiff`（解析 content 中的结构化文本）

16 个仓库未实体化（git 2.53 refset 问题后按需 materialize），标注「未验证」，按上游文档/知识分类。

## A. 原生 function-calling（源码已验证）

| harness | 原生命中 | 文本命中 | 备注 |
|---|---:|---:|---|
| hermes-agent | 1024 | 17 | 窄腰学说：tools 随每次 API 调用发送。**实测 coder-30b 7/10** |
| codex | 619 | 1 | Responses API function calling（本地 tier 因 wire API 被阻） |
| zeroclaw | 1952 | 257 | 核心原生；另有 SOP/bash-grammar 文本子系统（见 C） |
| ironclaw | 891 | 9 | Rust 框架，原生 |
| nanobot | 251 | 2 | 原生 |
| kimi-cli | 106 | 0 | 已废弃 upstream（banner 指向 kimi-code） |
| kimi-code | 75 | 1 | kosong→openai-common 管线。**⚠️ 实测 coder-30b 0/10**：协议为原生却仍叙事死循环——原生≠兼容，见脚注 |
| goclaw | 83 | 5 | 原生 |
| reasonix | 44 | 6 | 原生。**实测 coder-30b 6/10** |
| maxclaw | 17 | 0 | 轻量原生 |

**脚注（kimi-code 悖论）:** coder-30b 网格里 kimi-code 十次全部「首先，让我查看 issue-001.md…」循环到超时，而同为原生的 hermes/reasonix 合计 13/20。可能原因：kimi-code 的本地 provider（`type="openai"`）未向该模型下发 tools、或其提示词依赖模型对特定工具习惯的服从性。待查 kimi-code 的 provider 能力门控。**这修正了「native vs 文本」二分法：协议兼容是必要条件，不是充分条件。**

## B. 文本协议（解析 content 中的 diff/命令）

| harness | 原生命中 | 文本命中 | 备注 |
|---|---:|---:|---|
| aider | 3 | 234 | SEARCH/REPLACE + editblock/udiff 家族。**实测 coder-30b 0/10**：模型回中文叙述计划，无 diff，20-90 秒快速失败 |
| agent-zero | — | — | 未实体化；上游知识：ToolCaller 从响应文本解析 JSON 调用（未验证） |

## C. 双轨 / hybrid

| harness | 备注 |
|---|---|
| qwen-agent | 未实体化；上游：原生 tool_calls + `<tool_call>` 文本解析兜底（为不支持原生调用的模型设计）（未验证） |
| zeroclaw（侧注） | A 类主体 + SOP/bash-grammar 文本子系统（`zeroclaw-runtime/src/agent` 下 11 处文本命中）——同一仓库两种协议并存 |
| metagpt | 未实体化；框架内既有原生链路也有文本 action（未验证） |

## D. 框架 / 工作流引擎（协议由使用者配置决定）

| harness | 备注 |
|---|---|
| agentscope | ReActAgent 走原生（register_tool）；未验证 |
| dify | LLM 节点 + agent 节点，随 provider 能力而定；未验证 |
| praisonai | 原生优先的框架封装；未验证 |

## E. 骑乘宿主 runtime / 证据不足

| harness | 备注 |
|---|---|
| clawteam | 160 个源文件 0 命中——OpenClaw 扩展包，模型循环属于宿主 |
| openclaw | 未实体化；上游文档与 hermes 同门（tools-on-every-call）→ 应为原生，未验证 |
| browser-use | 未实体化；上游以 tool schema 驱动浏览器操作 → 原生倾向，未验证 |
| eliza | 未实体化；provider 插件层转发原生调用，未验证 |
| openworker / copilot-cli / hiclaw / openhuman / rocketride-server / claw-ai-lab | 未实体化且无明确记载，未定 |

## 与基准实证的对照（coder-30b @ 路由器，2026-11-21）

| driver | 分类 | 结果 | 解读 |
|---|---|---|---|
| hermes | A 原生 | 7/10 | 原生 + 该模型 = 工作组合 |
| reasonix | A 原生 | 6/10 | 同上 |
| kimi-code | A 原生 | 0/10 | **kimi-code 悖论**（见脚注） |
| aider | B 文本 | 0/10 | 模型叙述而不产 diff——文本协议对该模型失效 |

35B（qwen36-35b-mtp）对照：四 driver 全部 8/10，协议不构成分水岭——**协议敏感性是模型属性，不是 harness 属性**。换模型可以翻转 harness 的可用性排序。

## 复现

```bash
# 探测脚本（对单个已实体化仓库）
grep -rE "tool_calls|tool_choice" --include="*.py" --include="*.ts" --include="*.tsx" \
  --include="*.go" --include="*.rs" --include="*.js" <repo> \
  | grep -vE "\.venv/|node_modules/|/vendor/|/dist/|/build/|/tests?/|\.test\.|_test\.|spec\."
```

未实体化仓库 materialize 后应重跑本分类（git 2.53 refset 规避法见 `technical/git-253-clone-branch-head-bug` 记忆）。
