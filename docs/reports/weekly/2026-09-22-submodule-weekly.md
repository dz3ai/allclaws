# Submodule 周报 2026-09-22

**检查范围**：AllClaws 全部 29 个 submodule 路径（Claw 生态 11 + External 框架 9 + CLI 编码代理 5 + Human Digital Twin 1 + 双份检出的 agentscope 等按项目计 35 平台中的 29 个仓库路径）。**时间窗**：2026-09-15 ~ 2026-09-22（近 7 天）。数据来源：各 submodule `git submodule update --remote` 同步后的本地 git 日志（本周期完成了全部可同步仓库的 fetch），GitHub API（pushed_at / releases / 热点 issue）交叉验证默认分支漂移。

**总体**：29 个仓库中 **13 个本周有 commit**（openclaw、zeroclaw、nanoclaw、nanobot、hiclaw、hermes-agent、agentscope、praisonai、rocketride-server、eliza、codex、reasonix、kimi-code、kimi-cli、copilot-cli、dify、openworker、browser-use 中按活跃阈值计入 13-18 个；见各节明细），**本周有新 release 的 11 个**：openclaw v2026.9.5、hermes-agent v2026.9.21、praisonai v4.7.10（周内三连发 4.7.8/9/10）、reasonix v1.38.11、kimi-code **2.0.2（1.0→2.0 大版本跨越）**、hiclaw v1.2.4、copilot-cli v1.0.87/1.0.88-rc、nanobot v0.3.5、goclaw v3.15.0-beta.213、agent-zero v2.12（9-09，窗口边缘）。**本周最大事件**：Moonshot 把 kimi-cli 正式归档、入口指向 kimi-code——双产品线合并落地；kimi-code 同步发布 2.0，架构换到 agent-core-v2（DI × Scope 四层）。

---

## 一、Claw 生态（11 个）

### OpenClaw
近 7 天 **3947 commits**（main，团队级流水线，数字含 CI/merge 噪声，实际节奏为持续高频滚动）。本周主线仍是**正确性与性能的系统性收敛**：auth 层修 session pin 变更不越界到未选中的 agent（#155717）、角色变更投递失败时回收缓存权限（#152835）；perf 方面 memory 关键词检索 SQL 卸载（#155719）、sessions 复用 worker membership snapshots（#155620）、state 的 reclamation workers 跨数据库切换保留（#155677）——上周的"成熟期打磨"叙事延续且在加深。channel 侧 discord 视频附件按 duration 分类、matrix 在 runtime context 缺失时恢复进度更新。**发布**：v2026.9.5（09-19，9 月第 5 个正式版）+ release-publish tag 滚动（09-11 ~ 09-14 三个）。**值得记录的信号**：根 AGENTS.md 出现了"Codex sibling runtime hard gate"——任何涉及 Codex 协议/运行时的改动，agent 必须亲自检查 `../codex` 源码才能给结论，官方文档明文规定"subagent 报告不满足此 gate"。OpenClaw 已把"跨运行时依赖审查"制度化进 agent 协作规范，这是 agent 工程治理的罕见样本。

### Hermes-Agent
近 7 天 **4844 commits**（main）。本周叙事主线是 **MCP 的产品化重构：Connectors**。NS-941/942/943 三部曲落地：Desktop 的 Connectors 页面正式取代 MCP tab；**Portable plugins 声明每个 MCP server 依赖的应用**（插件 manifest 里写清楚"我这个 server 需要 XX 应用"），安装时在不支持的主机上直接拒绝；**Application-backed MCP servers** 跟随应用生命周期——live endpoint 每次尝试即探测、工具目录随应用存活状态伸缩、错误信息说明原因。配套 hermes_platform.resolver（locate/inspect/probe 三层 + AppResolver + gh lookup）。这是把 MCP 从"进程配置"提升为"应用依赖对象"的架构级转变，与 install 拒绝机制组合后，MCP 集成第一次有了明确的兼容性契约。另一条线是 kanban 的 connection-scope 查询修复组（连接切换时查询键跟随 activeConnectionId 反应式重建）。**发布**：v2026.9.21（09-21），周级发版节奏稳定。

### ZeroClaw
近 7 天 **127 commits**（master 分支）。**WhatsApp 一等公民化**是本周主题：whatsapp-web 通道外发图片带 inline previews（#10982）、出站消息渲染 WhatsApp 方言的 Markdown（#10475）、poll 工具投递原生投票（#10984）、LINE 群消息要求 sender authorization（#9427）——channel 层在从"能收发"走向"原生体验"。providers 层：reasoning_effort 经 opt-in passthrough 转发（#10916）、Anthropic rolling cache breakpoint 在图片结尾消息上保留（#10895）、signed reasoning 过 seam sanitizers 不再被误洗（#10953）。runtime 侧亮点：**interruption scope keys 改用 length-prefixed 编码防边界碰撞**（#10958）、历史裁剪改 trim 到低水位目标而非上限（#10696）——上下文管理的正确性打磨。**发布**：v0.8.5（09-05）。

### IronClaw
本周 tracked main 分支 **0 commits**（main 最后 commit 09-10），但 pushed_at 09-21——交叉验证显示活动在 **release/2026-08-26 分支**（09-20 有 commit）和 dependabot 分支群。上周报告说"默认分支已切回 main"的判断需要修正：main 确实是默认分支，但**开发主阵地又漂移到了 release 分支**——这是 ironclaw 继 staging→main 之后的第二次分支漂移，v1.4.0（08-28）发布后的主线工作在 release/2026-08-26 上进行。**发布**：无新版（最近仍是 ironclaw-v1.4.0）。建议下次同步时评估是否把 tracked branch 钉到 release/2026-08-26。

### GoClaw
tracked 分支（origin/HEAD 解析）本周 **0 commits**，但 dev 分支（默认分支）本周 **1 commit** + **v3.15.0-beta.211/212/213 三连发**（09-10/09-12/09-21，tag 均打在 dev 上）。本周唯一功能 commit 值得注意：`feat(agents): let create opt out of background summoning with "summon": false`（#1570）——**agent 创建时显式控制是否被后台召唤**，多 agent 系统里"实例化 ≠ 可用"的显式化。3.15 正式版临近（beta 已到 213）。**发布**：v3.15.0-beta.213（09-21）。低频但持续，未死。

### NanoClaw
近 7 天 **12 commits**（main）。本周几乎全部投入 **setup/bootstrap 安装链路加固**：sudo retry 提示永不出现（改为用户自有 npm prefix fallback）、corepack pnpm shim 装进 ~/.local/bin（全局 bin 只读时）、~/.local/bin 不可用时保持 bootstrap fallback 存活、setup.sh 源码检查替换 stubbed bootstrap harness——这是"新用户第一小时体验"的系统性清障。另一条线：session reconcile/drain 并发化 + 固定速率投递轮询、cross-session-context 的 echo fan 限制在热集合并移出唤醒路径（perf）。**发布**：v2.3.0（08-24）后无新版。

### Nanobot
近 7 天 **82 commits**（main）。**WebUI + OAuth 账号体系的双线打磨周**：WebUI 侧上下文消息控件精简（#5831）、markdown 表格包裹、移动端 sidebar 双击导航与 tooltip 防护、TUI Markdown 链接可点击（#5829）；OAuth 侧 **Copilot device sign-in 完整浏览器流程**（#5829 前后一批）、OAuth 过期时隐藏模型选项、fallback model 响应时通知聊天、OAuth 模型目录授权失败显式暴露——"账号态不明"这个 agent 客户端的经典模糊态在被逐一消灭。日志可靠性一组三修（rotation 被阻塞时保持可用、后台日志大小上限、关联性改进）。**发布**：v0.3.5（09-16，本周内）。

### HiClaw
近 7 天 **53 commits**（main），v1.2.4（09-21）**当日发布当日 README 官宣**。本周架构级亮点：**subagent model routing**（#1294）——declare（声明路由）→ team default（团队默认）→ hot-apply（热应用）→ L1-only API 四件套，子代理的模型选择成为一等配置面。人机协作继续深化：**worker-scoped humans 只读访问自己被分配的 workers**（#1277）、human scope 变更全审计（#1278）、read-only worker chats proxy 让管理员可见会话（#1295）。可靠性：worker 后端探测通过才报 Ready（#1275）、K8s MinIO 静态凭证初始化、complete_project 拒绝在非终态任务上执行。**发布**：v1.2.4（09-21）。HiClaw 的"人机混合团队"定位与 OpenWorker 本周的 team approvals 形成呼应。

### ClawTeam / Maxclaw / Claw-AI-Lab
三者本周零提交。ClawTeam 最后 commit 07-04、Maxclaw 06-13、Claw-AI-Lab 06-15——分别静默 11、14、14 周。上期周报的判断维持：**季度 review 的 Tier-1 占位候选**，治理规则（6 个月 + 无战略意义 + 无 roadmap 相关才可归档）尚未满足时间门槛，但连续三周无任何活动信号。

---

## 二、External 框架（9 个）

### AgentScope
近 7 天 **33 commits**（main）。两条线：其一 **chat model routing middleware + Jev classifier**（#2758）——模型路由做成中间件层，与 HiClaw 的 subagent model routing 是同一范式在框架层的实现；其二 **工具正确性周**：Bash 工具 written-lines 计数与 Read 对齐（#2734）、每个 sed -e 表达式都过 denylist（#2747）、ripgrep 输出按路径排序让 Grep 分页稳定（#2726）——把"工具输出与编辑器语义一致"当正确性约束。RAG 侧保留 image-only/header-only Excel sheet（#2666）、ApproxTokenChunker 丢弃空白 chunk。**发布**：v2.0.8（09-08）。

### Dify
近 7 天 **221 commits**（main）。本周叙事：**API 合同化 + 后端架构瘦身**。`feat(openapi)`：在 /openapi/v1 发布 op catalog、per-mode run ops、server-built hints（#42487）——OpenAPI 文档从静态描述变成带运行提示的合同层。api 层延续 thin controllers + application services 迁移（end-users 迁移 #41398、console controllers 瘦身 #42511），文件格式查询与 plugin readme 迁移到 generated contracts。工程侧 tsx 替换为 Node 原生 TypeScript 执行（#42742）、setuptools/pydantic-settings/guzzle CVE 修复（#42717）。Marketplace 单页轮播与 self-hosted 版外部打开细节。**发布**：1.17.1（09-10）。

### Eliza (elizaOS)
近 7 天 **451 commits**（develop 分支，默认分支漂移的已知案例）。本周从 AGENTS.md 与 commit 流看有两条值得记录的工程实践：其一 **crash-only error doctrine 全面落地**——"fail fast inside, handle at the boundary"写进了仓库级 agent 规范，J1-J7 七类豁免需逐处注释 `// error-policy:J<N>`，配合 `bun run check:comment-only` 做机器检查；"Not loaded ≠ zero/empty"（禁止 `?? 0` 掩盖管道故障）被立为 UI 三态规则。其二 **"Definition of Done"三定律**：真模型轨迹（非 proxy）、真实路径 E2E、无残留——agent 贡献的 PR 必须附视频/截图/结构化日志证据。commit 层面：Docker dependency closure 简化 + consolidation CI 修复（#32051）、credentials refresh writes fencing + 加密账号兼容（#31972）、planner instructions 的 batch-scope 规则只在提示里说一次（schema 保持短指针，#31482）、provider trajectories 保留 turn identities（#32045）。**发布**：无正式 tag（发布面走 Cloud 产品）。

### PraisonAI
近 7 天 **75 commits**（main，含文档 parity 自动同步）。**质量收敛周**：Gateway operator control-frame 路径加 request idempotency（#5193）、multi-observer Gateway session contract（#5192）、knowledge registries 全锁 + compaction mapping 去重（#5190）——三个 issue 级修复都指向"操作可重入、状态可对账"。chat 的 --tools/--toolset 限制贯通交互会话（#5140）。**发布**：v4.7.8（09-14）、v4.7.9（09-18）、v4.7.10（09-22）——周内三连发，修复驱动。

### RocketRide-Server
近 7 天 **34 commits**（develop，main 冻结的已知漂移案例）。**开发者体验成为主题**：`rocketride diff` 语义化 .pipe diff（布局噪声免疫）+ PR 评论 Action（#1607）；SQL UI 大改（statement runner、真实错误文本、schema-aware 补全、EXPLAIN、"诚实的设计器"，#2282）；appdev 在开发者默认浏览器调试 + 断点绑定修复（#2386）。数据侧 chunker 保留 Unicode token 边界（#2328）、SEC period scope 强制（#2327）。**发布**：client-mcp-v1.5.0-prerelease（09-14）。

### Browser-Use
近 7 天 **1 commit**（docs: require the PZERO key explicitly）。0.13.10（09-03）后代码面持续静默，上周"产品叙事调整期"的判断维持。

### OpenWorker
近 7 天 **40 commits**（main）。**团队审批治理周**：resolved approvals 不因延迟更新重现、审批卡按 exact tool call identity 对账、**approval owner 不可用时 fail closed**、explicit approval guidance 进入 team reviews——审批从 UI 态走向有身份、有失败语义的协议。团队面板大团队规模下可搜索、team coordination 事件驱动且安静化、incremental board reads + immutable team artifacts。**发布**：无（v0.2.1 08-25 后攒版中）。

### MetaGPT / Qwen-Agent
MetaGPT 最后 push **2026-01-21**（8 个月静默）、Qwen-Agent **2026-03-04**（6.5 个月）——维持 dormant 判定与 Tier-2 降级建议，无新信号。

### Agent-Zero
本地与远端 main 均无本周 commit（main 最后 09-09，v2.12 当日发布）；pushed_at 09-20 经查为 issue/PR 活动而非代码。development/testing/ready 分支也停在 6 月。**活跃度实质放缓**，从上周"低频"下调为"接近 dormant"。

---

## 三、CLI 编码代理（5 个）

### Codex (OpenAI)
近 7 天 **409 commits**（main）。上周成型的 **Guardian 体系本周默认启用**：Guardian thread context by default（#47275）、sync review across compaction hash differences（#47272）、extra-policy snapshot for retained instructions（#47287）——agent 自审从"架构存在"推进到"默认开启且跨压缩稳定"。**AgentControl 抽象落地**：`LocalAgentControl`（#47271）集中 agent resume 处理（#47244）、multi-agent spawning 统一走 SpawnRequest（#47235）、agent snapshots 从 close_agent 返回并流式订阅（#47267/#47252）——多 agent 生命周期管理正在收敛为单一控制面。app-server v2 持续演进（hosted plugin extensions 摘要、MCP resource reads 带 app/account targets、MCP 请求 trace context 跨 transport workers 保留）。message board 订阅语义修复一组（发帖者订阅频道、显式退订保留、后代频道帖不进 retained history）。**发布**：rust-v0.155.1（09-18）。**痛点**：#28756 chatgpt.com backend 404（1123 评论，开放）仍是第一痛点；#19464 请求 1M context（132c）、Windows 冻结（#20214，111c）、macOS syspolicyd CPU 失控（#25719，90c）——桌面端稳定性与配额/计费并列为两大痛点群。

### Reasonix
近 7 天 **360 commits**（main-v2）。**桌面端深水区周**：native graphics fault recovery（#10644）、macOS Dock icon 缩放保留、桌面历史会话生命周期与关闭恢复（#10634）、新建会话的升级安全移除（#10631）、Windows junction 路径身份与升级恢复（#10656）。会话语义修复一组：canonical inbox identity + settled tool state（#10646）、**queued guidance 可编辑并重排**（#10626）、用户消息行不再被本轮输出插前（#10639）、重复压缩 admission 与会话回执（#10628）、/compact 反馈与历史判定（#10642）。内置浏览器运行时升级 + 会话诊断（#10635）、MiMo API 接入说明 + DeepSeek Flash 官方目录刷新（#10624/#10655）。**发布**：desktop-v1.38.11 / v1.38.11（09-21，一周两版 1.38.10→11）。双语 commit 持续。

### Kimi-Code
近 7 天 **66 commits**（main）。**本周生态最大事件在此发生**：Moonshot 于 09-21 将 **kimi-cli 归档**（#2659），入口 short-circuit 到 Kimi Code 安装器（#2666），kimi-code 同步发布 **2.0.2**（09-19）——0.43.x 直跳 2.0，产品线合并完成。架构面（从 AGENTS.md 与 commit 可见）：**agent-core-v2 是 DI × Scope 四层引擎**（App/Workspace/Session/Agent 四级 LifecycleScope + Service/Fiber 单元层），配 kap-server（REST+WS）、klient SDK（zod 校验的 contract-driven facade）、transcript 四层数据层（L1 粒度存储 → L4 框架无关视图注册）、minidb（snapshot+WAL 的嵌入式 JSON 文档库）。本周 commit：MCP OAuth 请求 offline_access（#3979）、**CLI 启动时间与内存削减**（native binary + config reads，#3975）、auto_session_title 配置（#3962）、cold-folded steps 带 step timing 与 usage（#3938）、filesystem watch 默认关闭（#3931）。**发布**：2.0.0/2.0.1/2.0.2 三连（09-19 前后）。

### Kimi-CLI
**归档**（09-21）：`chore: archive kimi-cli and point users to Kimi Code CLI`（#2659）+ 1.51.0 终版 + 入口重定向。AllClaws 追踪名单需在下次治理 review 处理：这是 Tier-1 名单内**第一个被上游正式归档的平台**。

### Copilot-CLI
近 7 天 **3 commits**，全部为 changelog 更新（1.0.85/86/87 三版，周二-周日节奏）。**发布**：v1.0.87（09-21 GitHub Release）+ v1.0.88-0/1 tag（09-21，预发布通道）。稳定小步快跑。

### Aider
0 commits，最后 push 2026-05-22（约 17 周静默）。维持长期 stale 判定。

---

## 四、Human Digital Twin（1 个）

### OpenHuman
近 7 天 **1425 commits**（main）。**todos/tasks 域大重构**：thread-scoped stores 替换为 session-scoped（#1ce239e）、移除 legacy task board migration 与文件存储、"board card tracking"概念整体退场、goals-and-todos 文档澄清 agent 工作态并重命名 TodoOnly 变体——任务域从"看板隐喻"迁移到"会话原生"。**hermes-prompt-diet PR 合并**（#6436）：多个 agents/tools 的 prompt budget ceilings 下调——在 agent 平台间传染的"prompt 瘦身"运动又添一例（上周 ZeroClaw 的 low-water trim、Eliza 的 batch-scope 单次声明同属此列）。日志轮转与关联性、toolpacks tasks pack 修正。单作者占比极高的特征依旧，活跃度解读需打折。**发布**：v0.63.21（09-03）后无新 tag，但 tag 历史（09-03 一天三连 v0.63.17/20/21）说明发版按需触发。

---

## 跨项目洞察

**1. 模型路由成为本周最强的跨项目范式信号。** HiClaw 的 subagent model routing（declare/team default/hot-apply）、AgentScope 的 chat model routing middleware + Jev classifier、kimi-code 的 model upgrade——三个不相干仓库同周把"哪个 agent 用哪个模型"提升为显式配置面。多 agent 系统的模型分配正在从"全局默认 + 临时覆盖"走向"声明式路由层"，这与 ROADMAP Q4-8 的 subagent observability 观察项直接相关。

**2. MCP 的产品化重构出现两条路线。** Hermes 的 Connectors（MCP server 声明应用依赖、生命周期跟随应用、install 拒绝不兼容主机）把 MCP 当**应用依赖管理问题**；Codex 的 MCP resource reads 带 app/account targets、trace context 跨 transport 保留把 MCP 当**多租户协议问题**。加上 kimi-code 的 MCP OAuth offline_access，MCP 集成正在从"进程启动时挂载"演进为有依赖契约、有身份、有 OAuth 生命周期的完整集成体系。

**3. 审批（approval）语义在多 agent 场景下持续深化。** OpenWorker 的 exact tool call identity 对账 + owner 不可用 fail closed、HiClaw 的 human scope 审计、Reasonix 的 settled tool state、Codex Guardian 的默认启用——审批从 UI 交互态进化为有身份、有失败语义、可审计的协议对象。enterprise-governance 研究线的核心论断持续得到验证。

**4. Prompt/token 瘦身运动扩散。** OpenHuman 的 hermes-prompt-diet（预算上限下调）、Eliza 的 batch-scope 规则单次声明、ZeroClaw 的 low-water trim、kimi-code 的 CLI 启动内存削减——头部平台不约而同在砍上下文与启动开销。这是 token 成本压力传导到架构层的直接证据，也是 Q4-4 long-running benchmark 的核心测量维度。

**5. Moonshot 产品线合并（kimi-cli → kimi-code）是追踪名单的结构性事件。** Tier-1 35 席中第一个上游正式归档的成员出现。治理上这次不用等 6 个月门槛——上游已官宣，下次季度 review 应启动移除或 Tier-2 降级（保留 kimi-code 即可覆盖该生态位）。

**6. 分支漂移新增两个案例。** ironclaw 的开发阵地从 main 又漂到 release/2026-08-26；goclaw 的 tracked origin/HEAD 落后 dev（beta.213 已在 dev 上）。加上既有的 eliza（develop）、rocketride（develop）、zeroclaw（master）、reasonix（main-v2），**6/29 仓库的实际开发分支 ≠ tracked 分支**，周报数据的默认分支交叉验证已成为必需流程。

**7. 桌面客户端质量成为 CLI agent 的第二战场。** Codex 的 Windows 冻结 + macOS syspolicyd 失控（两个 90+ 评论 issue）、Reasonix 的 graphics fault recovery + 关闭恢复、nanobot 的 Copilot browser sign-in——当 CLI agent 桌面化后，图形栈、系统服务交互、升级迁移成为新的痛点聚集地。

**值得重点跟踪**：kimi-code 2.0 的 agent-core-v2 架构（DI × Scope 引擎能否成为多 agent 会话管理的新基准）、Hermes Connectors 的应用依赖模型（MCP 产品化路线）、Codex Guardian 默认启用后的实际审查质量、HiClaw subagent model routing 的 hot-apply 实现、kimi-cli 归档后的治理动作。
