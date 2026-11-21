# Harness Function-Calling Taxonomy — 按驱动协议分类跟踪的 harness

**日期:** 2026-11-21（2026-11-22 全量实体化后升级为 29/29 源码验证）
**动机:** coder-30b 本地网格（13/40）显示出剧烈的协议分野——原生 function-calling 的 driver 正常工作，依赖模型自发产出结构化文本的 driver 收到「叙述性计划」。本文把 allclaws 跟踪的全部 29 个仓库按「是否原生执行 function-calling」分类。

**方法:** 29/29 仓库已实体化（2026-11-22，单 SHA fetch 规避 git 2.53 refset bug；全部 HEAD 落在 gitlink pin）。对每仓 grep 两类证据（排除 `.venv/`、`node_modules/`、`/tests/`、`/dist/`）：
- 原生命中 = 源码中 `tool_calls` / `tool_choice`（发送 tools schema 并解析结构化返回）
- 文本命中 = `SEARCH/REPLACE` / `<tool_call` / `<function_calls` / `edit_format` / `EditBlock` / `udiff`

计数是启发式；分类以「主循环走哪条路径」为准，边界案例逐一抽查源码定案（qwen-agent、agent-zero、kimi-code、nanoclaw）。

## A. 原生 function-calling（主循环发送 tools schema、解析 tool_calls）

| harness | native / text | 备注 |
|---|---|---|
| hermes-agent | 1024 / 17 | 窄腰学说：tools 随每次 API 调用发送。**实测 coder-30b 7/10** |
| codex | 619 / 1 | Responses API function calling（本地 tier 因 wire API 被阻） |
| openhuman | 552 / 64 | 原生主体；text 命中为 legacy provider 解析 |
| eliza | 546 / 30 | provider 插件层转发原生调用 |
| agentscope | 488 / 0 | ReActAgent 走原生（框架，见 D） |
| ironclaw | 891 / 9 | Rust 框架，原生 |
| zeroclaw | 1952 / 257 | 原生核心 + SOP/bash-grammar 文本子系统并存（见 C 侧注） |
| nanobot | 251 / 2 | 原生 |
| kimi-cli | 106 / 0 | 已废弃 upstream |
| browser-use | 105 / 0 | 以 tool schema 驱动浏览器操作——此前「未验证」现确证 |
| goclaw | 83 / 5 | 原生 |
| **kimi-code** | 75 / 1 | kosong→openai-common 管线，原生。**⚠️ 实测 coder-30b 0/10**（kimi-code 悖论，见脚注） |
| reasonix | 44 / 6 | 原生。**实测 coder-30b 6/10** |
| rocketride-server | 61 / 0 | 原生 |
| openclaw | 182 / 4 | 与 hermes 同门（tools-on-every-call），48K 文件实体化后确证 |
| maxclaw | 17 / 0 | 轻量原生 |
| hiclaw | 6 / 0 | 轻量原生 |

**脚注（kimi-code 悖论）:** coder-30b 网格里 kimi-code 十次全部「首先，让我查看 issue-001.md…」循环到超时，而同为原生的 hermes/reasonix 合计 13/20。可能原因：kimi-code 的本地 provider（`type="openai"`）未向该模型下发 tools、或其提示词依赖模型对特定工具习惯的服从性。**协议兼容是必要条件，不是充分条件。**

## B. 纯文本协议（解析 content 中的结构化文本）

| harness | native / text | 备注 |
|---|---|---|
| aider | 3 / 234 | SEARCH/REPLACE + editblock/udiff 家族。**实测 coder-30b 0/10**：模型回中文叙述计划，无 diff，20-90 秒快速失败。**全生态唯一的纯文本实现** |

## C. 双轨 hybrid（两种协议并存于主路径）

| harness | 证据 | 备注 |
|---|---|---|
| qwen-agent | 75 / 13 + `utils.py`、`fncall_prompts/` 中的 `<tool_call>` 解析 | 原生 tool_calls 为主、`<tool_call>` 文本解析兜底（为不支持原生调用的模型设计）——上游设计意图源码确证 |
| agent-zero | 69 / 0 + `helpers/extract_tools.py`「Text tool calls allow one request per turn」 | **文本优先**循环（normalize_tool_request 解析响应文本中的 JSON 工具请求）+ LiteLLM 原生层 |
| zeroclaw（侧注） | A 类主体 + `zeroclaw-runtime/src/agent` 下 SOP/bash-grammar 文本子系统 | 同一仓库两种协议并存 |
| openworker | 164 / 9 | 原生为主，含少量文本解析 |
| claw-ai-lab | 49 / 9 | 实验室管线，混合 |

## D. 框架 / 工作流引擎（协议由使用者配置决定，原生优先）

agentscope（488 native）· dify（70）· praisonai（1104/53）· metagpt（13）——LLM 节点随 provider 能力与配置选择协议，框架本身的原生集成是默认路径。

## E. 骑乘宿主 / 本地不可检

| harness | 备注 |
|---|---|
| clawteam | 233 个源文件 0 命中——OpenClaw 扩展包，模型循环属于宿主（归 openclaw 的 A 类） |
| copilot-cli | **闭源安装器**（仓库仅 install.sh + 文档，19 文件 0/0 命中）——harness 跑在 GitHub 服务端，本地无从检验 |
| nanoclaw | 1248 文件 0/0 命中——调用层可能完全经由依赖 SDK（待深查，暂缓定性 |

## 与基准实证的对照（coder-30b @ 路由器，2026-11-21）

| driver | 分类 | 结果 | 解读 |
|---|---|---|---|
| hermes | A 原生 | 7/10 | 原生 + 该模型 = 工作组合 |
| reasonix | A 原生 | 6/10 | 同上 |
| kimi-code | A 原生 | 0/10 | kimi-code 悖论（见脚注） |
| aider | B 文本 | 0/10 | 模型叙述而不产 diff——文本协议对该模型失效 |

35B（qwen36-35b-mtp）对照：四 driver 全部 8/10，协议不构成分水岭——**协议敏感性是模型属性，不是 harness 属性**。

## 结论

29 仓分类定案：**A 原生 17 · B 纯文本 1 · C 混合 5 · D 框架 4 · E 宿主/不可检 2**。生态压倒性地押注原生 function-calling；aider 是纯文本协议的孤例（也是 coder-30b 上受害最重的）；混合双轨（qwen-agent、agent-zero）以文本兜底换取弱模型兼容性，代价是继承文本协议的全部失败模式。

## 复现

```bash
grep -rE "tool_calls|tool_choice" --include="*.py" --include="*.ts" --include="*.tsx" \
  --include="*.go" --include="*.rs" --include="*.js" <repo> \
  | grep -vE "\.venv/|node_modules/|/vendor/|/dist/|/build/|/tests?/|\.test\.|_test\.|spec\."
```

实体化方法（git 2.53 refset bug 规避）：见 `technical/git-253-clone-branch-head-bug` 记忆的单 SHA fetch 配方。
