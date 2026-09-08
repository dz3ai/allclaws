# Submodule 周报 — 2026-09-08（第 37 周）

**检查范围**：AllClaws 全部 submodule（35 平台、29 个本地路径），时间窗 2026-09-01 至 2026-09-08。数据来源：本地 `git fetch` 各活跃分支后统计 `--since="7 days ago"` 非 merge commit + GitHub Releases/Issues API。

**总览**：29 个 submodule 中 16 个有开发活动；6 个正式发布（zeroclaw v0.8.5、ironclaw v1.4.0、codex rust-v0.153.x×5 + 0.154-alpha、hermes-agent v0.21.1、kimi-cli 1.50.0、copilot-cli 1.0.83）。⚠️ 发现 reasonix 分支漂移：上游默认分支已改为 `main-v2`，当前按 `main` 追踪冻结在 5 月，实际开发 302 commits/周。

## 一、Claw 生态

**OpenClaw**（~4244 commits，207 作者）：平台级工程节奏，ui/agents/gateway/plugins 四大面并进。本周主打可靠性与性能：cron 以 secret egress 运行、插件安装重启归属澄清、cloud session 选机型时可选 OS、缓存优先渲染 UI。热点 issue：MEDIA: token 解析（703c）、sessions_yield 长转录（290c）、followup 队列持久化（282c）——会话连续性仍是最大痛点。

**ZeroClaw**（107 commits，v0.8.5 于 9/5 发布，455 commits 大滚动）：**workspace 正式发布 crates.io**；whatsapp-web 移植 whatsapp-rust；Web 多标签多会话；安全重头——插件 wasi:http 强制 host-owned egress policy、zerorelay blind relay + mTLS、SD-JWT 披露解析、MCP resource 聚合预算预检。社区热点在 BlueBubbles iMessage 桥与 SSRF 门禁（80c）。

**IronClaw**（27 commits，v1.4.0 于 8/28 发布）：subagent 后台化（receipt spawns + healing sweeps）、activate() 原语与激活溯源、持久用户收件箱 + 通知中心、托管 per-user 沙箱代理、WASM typed tool response。Reborn 事件溯源架构持续收敛。

**Hermes-Agent**（5000+ commits 窗口，v0.21.1 于 9/7 发布）：主题是 **subagent 可观测性**——CLI/TUI/Desktop 三端 subagent dock、live tail、通过 parent steer/stop、完成分组返回；MCP CLI 设备码授权；GPT-6 Astra baseline。

**NanoBot**（86 commits）：compaction 透明化（summary checkpoint 统一、压缩过程通道可见、WebUI 按轮次可视化 context）；Telegram 流式富消息；AnySearch 免 key 搜索。

**HiClaw**（5 commits）：实验性 **DeepSeek Harness worker runtime**（第五种 worker 运行时）；L2 人类可更新团队内 worker skills。v1.2.3。

**NanoClaw**（11 commits）：setup/runtime/host 三类 provider 契约显式化，instructions 由 core-owned canon 渲染；激活 minimumReleaseAge 供应链门禁。

**GoClaw**：本周 0，但 v3.15.0-beta.198（8/29）维持每周一版 beta 节奏。**ClawTeam/MaxClaw/Claw-AI-Lab** 静默 2-3 个月，下季度 review 候选。

## 二、External 框架

**AgentScope**（31 commits）：**realtime voice agent**（DashScope + 本地传输）；Volcengine Ark；`A2AAgent` 一公民化；MCP Docker 运行时 headers；RAG/管线一批修复。

**Eliza**（889 commits）：全部押注 **eliza.app + Cloud 商业化**——billing 订阅生命周期原子化对账（command lineage 级）、组织配额权威、租户 PostgreSQL WAL 恢复、identity 服务收进 monorepo。热点：staging E2E 就绪 epic（196c）。

**PraisonAI**（317 commits）：**本地模型双线**——desktop 打通 Ollama/LM Studio/vLLM，`Agent(llm="local")` 自动发现；TS 端偿还 28 个 Task engine + 21 个 Agent.chat "被忽略选项"；持久 per-identity 花费账本 + 预算准入；移动端视觉身份与瘦身。v4.7.4。

**Dify**（188 commits）：agent RBAC/ACL 场景、app deployment v2、**知识库 API key 限定单数据集**、workflow 画布键盘操作；大批测试迁移 SQLite。

**rocketride-server**（22 commits，develop）：Claude 5 adaptive thinking-shape、thinking-shape guard、reasoning 截断报因、pgvector/pg16。

**OpenWorker**（0，9/2 刚出窗口）；**MetaGPT**（1 月起）/ **Qwen-Agent**（3 月起）/ **agent-zero**（8/27）无活动。

## 三、CLI 编码代理

**Codex**（347 commits，5 个 stable + 1 alpha 连发）：两条主线——**Memory v2**（consolidation/read prompts、human-evidence 优先、版本化隔离存储）与 **Guardian 上下文治理**（context profiles + registry 集中化）；MCP user verification + macOS Secure Enclave。痛点：chatgpt.com 404（1123c，本周最热）、1M context 请求（132c）、Windows 冻结（110c）。

**Reasonix**（302 commits，main-v2）：**schema-2 append-only DAG session log** ——fork/rewind 即 heads、投影免重放、turn envelope 带 head 引用；pending recovery 重试/对账契约。✅ 已于当日 pin 到 `main-v2`（commit 7a3faaf，submodule 前进至 f5745bae2 / v1.38.2）。

**kimi-cli**（1 commit，1.50.0）：open issue #1707 酝酿 **Python→Bun+TS+React Ink 重写**，与 kimi-code 栈统一。

**kimi-code**（99 commits）：agent-core-v2 收敛——HEIC/BMP 图像、reasoning_details 往返、大文件断点续读、protocol 包并入、全局 human 单例；MCP 结构化结果修复。**copilot-cli** v1.0.83。**aider** 5/22 起静默。

## 四、Human Digital Twin

**OpenHuman**（314 commits）：socket emit 串行化 + teardown drain、status 统一词汇表、channel identity 最后渲染、webhook 副作用门控。

## 五、跨项目洞察

1. **Session 成为有版本的数据结构**：Reasonix append-only DAG、Codex context profiles、NanoBot/Hermes visible compaction 三处合流——长时运行 agent（Q4-4）的基础设施前奏。
2. **Memory 分层化**：Codex Memory v2 / IronClaw AfterTurn curation / NanoBot Dream 两阶段，抽取-固化-检索管道正在标准化。
3. **Subagent 从能 spawn 到可观测**：dock/live tail/steer、后台 receipt spawns、owner 收件箱审批——重心转向可观测性与责任边界。
4. **本地模型接入成标配**：PraisonAI 一周打通三大本地推理 + `llm="local"`。
5. **安全门禁落地为原语**：egress policy、mTLS、MCP user verification、RBAC/单数据集 key。
6. **Eliza 商业化最重投入**：cloud 占 219/889 commits，框架→产品转型样本。
7. **沉寂名单变长**：aider/MetaGPT/Qwen-Agent/ClawTeam/MaxClaw/Claw-AI-Lab，下季度 governance 建议评估 MetaGPT/Qwen-Agent 降 Tier-2。

---

**摘要**：检查 29 个 submodule，16 个本周活跃，6 个新发布；5 个值得重点跟踪的新范式（append-only DAG session log、Memory v2 分层、subagent dock 可观测性、realtime voice、本地模型接入）；基础设施待办 reasonix pin `main-v2` 已于当日完成（7a3faaf）。
