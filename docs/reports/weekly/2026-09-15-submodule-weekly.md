# Submodule 周报 2026-09-15

**检查范围**：AllClaws 全部 29 个 submodule（Claw 生态 11 + External 框架 9 + CLI 编码代理 5 + Human Digital Twin 1 + agent-zero/praisonai/rocketride-server/eliza 4，按项目计）。**时间窗**：2026-09-08 ~ 2026-09-15（近 7 天）。数据来源：各 submodule `git fetch origin` 后的远端分支日志（本地浅克隆的旧 HEAD 多停留在 7 月底，直接用 `origin/<dev-branch>` 引用统计），GitHub API（pushed_at / releases / 热点 issue）交叉验证默认分支漂移。

**总体**：29 个项目中 **16 个活跃**（远端分支近 7 天有 commit），**5 个有新 release**（openclaw、hermes-agent、dify、praisonai、reasonix、kimi-code、goclaw、zeroclaw 等按各自节奏发版），13 个本周无远端动态。零新增 dormant 项目——上周报告里列为不活跃的 aideer、metagpt、qwen-agent、clawteam、maxclaw、claw-ai-lab 本周依旧静默，没有恶化也没有复苏。

---

## 一、Claw 生态（11 个）

### OpenClaw
近 7 天 **4208 commits**（main 分支，团队级流水线），本周持续高频。主题集中在**稳定性与资源占用的系统性收敛**：sessions 复用已编译的 transcript 元数据查询、reminder 维护时减少拉取的数据量、participants 记录时减少数据库写入、cron 在 session pruning 空闲时跳过可用性检查——这是一组典型的"成熟期"优化，说明平台进入打磨阶段而非新功能堆叠。同时有一批 Copilot 相关修复：恢复 credential-only 登录选择、guard GitHub Copilot device flow authority、移除已退役的 Raptor mini 模型、修复 multi-line /steer 消息丢失后续行的问题。**发布**：v2026.9.4（09-11）、v2026.6.35（09-10，6.x 维护分支同天发版）。**热点**：GitHub 上最高评论数的 issue 之一 #80396（`MEDIA:` token 在 fenced code block 内被跳过时的告警，704 评论）仍在开放，是用户长期痛点；另一方向上，"Autofix: add PR review autofix pipeline + Windows daemon"（2500 评论）已关闭——OpenClaw 在用自家 agent 做 PR 自动修复流水线，吃自己的狗粮。

### Hermes-Agent
近 7 天 **2401 commits**，节奏与 OpenClaw 同级。本周叙事主线是 **cron 调度器的正确性攻坚**：一整组 "skewed early fire own its armed slot"、"manual fires before the next occurrence must not consume it"、"reject impossible occurrence completions"、"future occurrence poisoning" 的修复链，把定时任务的边界条件（早触发、手工触发、时钟偏移、未来实例污染）逐一封死——这是长期运行 agent 平台绕不开的工程债。另一条线是 **MoA（Mixture-of-Agents）与 approval 的不变量测试**：non-finite temperature 拒绝、fanout 溢出容忍、unattended 模式下 pattern-key allowlist 生效。还有 gateway 的 agent-cache 压力阀改为度量 cgroup 的 anon charge 而非仅网关自身 RSS——内存治理精细化。**发布**：v0.21.3（v2026.9.14）、v0.21.2（v2026.9.11），双周内两版。**热点**：#75325 "conservative voice barge-in"（592 评论）与 #68499 "fix(delegation): separate lifecycle from task outcome"（173 评论）开放中——语音打断与委派生命周期分离都是多 agent 协作的前沿问题。

### ZeroClaw
近 7 天 **112 commits**（master 分支）。本周是**功能密度相当高的一周**：新增 Crusoe Managed Inference 作为 first-class OpenAI-compatible provider、Serply web search provider、Matrix 语音回复以 MSC3245 voice notes 交付、`per_user_session` 开关支持群聊共享会话、跨 agent 的 category-scoped memory grants（记忆权限按类别隔离）、docker sandbox 镜像可配置化、`sops/run-detail` RPC 返回完整 step 结果。安全侧有一批值得注意的修复：pairing-code 统一为单一策略并强化默认值、所有 outbound HTTP 强制走 runtime proxy、public health 错误信息脱敏。**发布**：v0.8.5（09-05）。**热点**：#9713 "expose token accounting on history-trim events"（113 评论，开放）——上下文裁剪时的 token 记账透明度是社区强诉求。

### IronClaw
上游默认分支已从 staging 切回 **main**（staging 冻结在 5 月 6 日）。main 分支近 7 天仅 **1 commit**——但这是 v1.4.0（08-28 发布）后的正常节奏：ironclaw-v1.4.0-rc.1 → 1.4.0 的发布周期刚走完，本周 main 上只有 "register the Bot API command menu at activation"（Telegram 命令菜单注册）。依赖机器人（dependabot）在 09-10 ~ 09-13 密集开了 6 个依赖更新分支，说明仓库处于维护-合并循环。**发布**：ironclaw-v1.4.0（08-28）。整体判断：**活跃但低速**，非 dormant。注：.gitmodules 已在 09-08 钉住 main 分支，本地 origin/HEAD 符号引用仍指向 staging，下次 `submodule update --remote` 后会自动对齐。

### GoClaw
近 7 天 **8 commits**（dev 分支）。主题集中在 **teams（多 agent 团队）治理**：delegated lead 获得对自己 team 的读权限、team tasks 按 delegation origin 而非 delivery channel 划定作用域、人类可以从 dashboard 取消并重试卡住的 team tasks、task 详情页显示完整 UUID 一键复制。计费侧有个有趣修复：out-of-band media 按实测时长计价而非按字节数——用量计费从粗粒度走向精细化。新增 GPT Image 2.5 并默认 flare。**发布**：v3.15.0-beta 流水线继续滚动，本周到 beta.212（09-12），日均 1-2 个 beta tag，3.15 正式版临近。

### NanoClaw
近 7 天 **36 commits**（main 分支）。本周主线是 **Mattermost 频道集成与安装器健壮化**：一批 `fix(mattermost)` / `fix(setup)` 提交覆盖了 Mattermost 连接 operator 管理的服务器、原子化持久化所选设置、无 jq 依赖的 setup 响应解析；安装器侧有 OneCLI file staging 可移植自愈、uvx 安装的 pnpm 恢复、绝对路径 system shell 执行下载的 installer、webhook 端口预校验。还有 `add-opencode` 新特性的两段提交（setup 集成 + provider contracts/host authentication）——**NanoClaw 开始把 OpenCode 作为可安装的 agent 运行时纳入自己的宿主体系**，这是个值得记录的生态互操作信号。**发布**：v2.3.0（08-24），本周无新版。

### Nanobot
近 7 天 **93 commits**（main 分支，HKUDS）。修复面铺得很宽：file-read 去重限定到 model context 作用域、email sender header 保留合法形式、会话历史分页搜索、Feishu QR onboarding 用 `/page/cli` 验证 URL、QQ 入站附件校验并拒绝 redirect、cron 在 job 执行期间推迟 timer rearming、编辑 automation 详情时保留 pending runs。WebUI 有一整批移动端打磨（chat toolbar 自适应宽度、mobile context sheet 交互加固、settings 菜单锚定）。**发布**：v0.3.0（07-25）之后未再发 tag，但 commit 流稳定，属于"持续开发、攒着发版"的状态。

### HiClaw
近 7 天 **13 commits**（main 分支）。本周亮点是 **TaskFlow 的可视化与人类协作深化**：`mermaid workflow rendering + task-level inspection API`（#1230）——工作流以 mermaid 图渲染并可逐任务检查；`team-scoped worker tool approval endpoints for L2 humans`（#1216）——人类审批通道下沉到 team 作用域；`persist durable task continuation state`（#1183）——任务续跑状态持久化；Matrix room 加入时给人类成员授予权限等级。还有 read-only skill catalog 端点、human update endpoint。**发布**：v1.2.3（08-22）。HiClaw 的"人机混合团队"定位持续兑现。

### ClawTeam / Maxclaw / Claw-AI-Lab
三者本周远端零提交。ClawTeam 最后 commit 07-04（v0.3.0+openclaw2）、Maxclaw 06-13、Claw-AI-Lab 06-15，均进入 stale 观察区（>60 天无动态）。治理上这三家是下次季度 review 的重点候选（Tier 1 占位 vs 实际活跃度）。

---

## 二、External 框架（9 个）

### AgentScope
近 7 天 **33 commits**（main 分支）。主题明显围绕 **realtime 语音会话的稳定性**：reconnect 前先发文本输入、重连时丢弃上一 session 的 terminal events、caller-committed turn 后请求 response、tool call 参数进 event stream。其他还有 Anthropic streaming content blocks 保留、AG-UI message ID 唯一化、`launch_realtime_ui` 语音会话 TUI 入口、ollama 模型卡（qwen3-8b/llama3.2/phi4-mini）。**发布**：v2.0.8（09-08）。

### Dify
近 7 天 **120 commits**（main 分支）。本周叙事是**企业化与性能的并进**：RBACResourceService 显式传 session（权限模型收紧）、`OpenShell runtime backend` 进入 dify-agent（agent 运行时获得真实 shell 执行能力——Dify 从工作流平台向 agent 平台又迈一步）、dataset list 批量化、batch segment import 避免 per-row MAX(position) 查询、annotation CSV 保留字面 NA、阿里云 trace 捕获 HTTP 请求快照。**发布**：v1.17.1（09-10，bug fixes）。**热点**：#30781 "feat: collaboration"（175 评论）已合并——Dify 的多人协作能力落地。

### Eliza (elizaOS)
近 7 天 **515 commits**（develop 分支）。主题分散但两条线清晰：**Cloud 上市后的收尾**（"Cloud 10-user launch — tracker" 1077 评论已关闭、retained compute subject 删除策略、legacy quota clock 去重、Pages 部署别名 reconcile）与**本地推理优化**（embedding 硬件选择复用、Dedicated embeddings 注册、Codex SDK 子进程用 runtime request 取消）。goals/calendar 插件也在补测试与全日事件支持。**发布**：无正式版，仓库以 pr-evidence-* tag 记录 PR 评审证据——elizaOS 的发布面走 Cloud 产品而非 repo tag。

### PraisonAI
近 7 天 **177 commits**（main 分支，其中相当比例是文档 parity 自动同步与 triage bot，原始开发 commit 约数十个）。本周是一个**质量收敛周**：framework registry 成为默认路由的唯一事实源（修复 #5016）、gateway `__init__.py` 懒加载、supervisor shutdown 覆盖测试 + deadline watchdog 加固、`aclose()` 释放 LLM client、cancel_token 贯穿完整流式工具路径、sandbox 死代码清理。**发布**：v4.7.8（09-14）、v4.7.7（09-10），周内双版。**热点**：#4966 "octal-encoded loopback bypassed the spider SSRF guard"（292 评论）已修复——SSRF 防护被八进制编码绕过，安全敏感。

### RocketRide-Server
近 7 天 **74 commits**（develop 分支；main 冻结——已知默认分支漂移案例）。本周最大动作是 **`rocketride otel`：OpenTelemetry bridge 覆盖文档化的 ingester 协议**，可观测性成为一等公民。此外 context window optimizer node（token 预算管理节点）进入节点库、Chroma 检索阈值可调、`tool_http_request` 阻断 SSRF 目的地（与 PraisonAI 同周修 SSRF，巧合但值得并读）、MinIO 改从 quay.io 拉取（Docker Hub 仓库没了）。**发布**：无 tag。

### Browser-Use
近 7 天 **14 commits**（main 分支），全部是 **README/文档重做**：品牌化产品路径、driving-test demo、llms.txt 指引 AI 爬虫、`bu-30b-a3b-preview` 模型指向 self-hosting 而非 Cloud。**发布**：0.13.10（09-04）。代码静默 + 文档重做，判断为产品叙事调整期。

### MetaGPT / Qwen-Agent / OpenWorker
三者本周远端零提交。MetaGPT 最后 push 2026-01-21、Qwen-Agent 2026-03-04——早已超过 dormant 阈值，维持上周报告的 Tier-2 降级建议。OpenWorker 最后 push 09-03（两周内），低频但未死。

---

## 三、CLI 编码代理（5 个）

### Codex (OpenAI)
近 7 天 **342 commits**（main 分支）。本周叙事最丰富：**Guardian 审查体系成型**——8 个连续提交把 Guardian approval routing、review reporting、denial accounting、reviewer lifecycle、assessment parsing、circuit breaker 全部收敛进 reviewer extension，这是 Codex 在 agent 自审（agent 审查 agent 输出）上的架构级投入。**Windows sandbox 持续投入**：service-managed package registration、registered package execution、daemon 包从独立 CLI 安装中拆出、service 重启后恢复 sandbox 注册。daemon 包显式替换、attachment 上传/解析 API、非 ephemeral fork 保留 thread attachments、TUI 独立渲染 display math。**发布**：rust-v0.154.0（09-09）。**痛点**：#28756 "404 Not Found … chatgpt.com/backend-api/codex/responses"（1123 评论，开放）与 #28879 "rate-limit cost per token jumped ~10-20x since June 16"（211 评论）——**服务端配额/计费争议是 Codex 用户最大痛点**，token 消耗速度相关 issue（#14593 630 评论、#13568 325 评论）长期占据热度榜首。

### Reasonix
近 7 天 **346 commits**（main-v2 分支——09-08 已钉住的活跃分支）。本周是 **v1.38.9 发布周**：desktop/npm/v1.38.9 三 tag 已于 09-15 打出，中英双语 changelog 准备提交（#10361）。功能主线是**会话架构升级**："Adopt SessionID-only Desktop persistence"（#10326）统一会话标识、"Harness-style loop 取代双重会话 turn 权威"——turn 循环向 Harness 模式靠拢、"fast recovery and independent history"（#10267）、"从持久化会话日志分叉已结束轮次"。还有 bash 跨前台调用保留 cwd 与环境、无 Electron 外壳的会话接入 CDP browser、会话资源上限。**发布**：desktop-v1.38.9 / v1.38.9（09-15）。**热点**：#8688（51 评论，已关闭）"思考输出时滚动条反复上闪下闪"——TUI 渲染稳定性是中文用户群的突出痛点。

### Kimi-Code
近 7 天 **67 commits**（main 分支）。主题：**agent-core-v2 的资源治理**——completed subagent scopes 走 LRU 驱逐、session event bus 按 agent id 分片、disposed agent scopes 从 DI 依赖图释放、swarm 取消不再崩 CLI；TUI 侧 agent swarm 进度批量缓存渲染、diff code block 高亮。`dynamically_loaded_tools` 为官方模型声明并加 per-server MCP deferred disclosure——MCP 工具延迟披露，减少首屏 token 开销。**发布**：@moonshot-ai/kimi-code@0.43.1（09-15）、0.43.0（本周内）。

### Kimi-CLI
近 7 天 0 commits，最后 push 09-01（bump 1.50.0）。低频稳定期。

### Copilot-CLI
近 7 天 **4 commits**，全部是依赖与流程维护（actions/stale 9→11、github-script 7→9、SHA pin、第三方服务声明修订）。功能静默。

### Aider
近 7 天 0 commits，最后 push 2026-05-22。**已连续多周静默**（>100 天），维持 stale 判定——aider 的维护节奏自 5 月下旬起实质性放缓。

---

## 四、Human Digital Twin（1 个）

### OpenHuman
近 7 天 **2242 commits**（main 分支）。发布节奏极快：**v0.63.26（09-15）当天打出**，且 tag 序列显示 09-03 一天连发 v0.63.20/v0.63.21。本周功能主线是**桌面应用的文件体验与 OAuth 可靠性**：assistant composer 接受拖拽与粘贴文件、composer 文件摄取串行化、文件列表 snapshot 后再入队、OpenRouter sign-in 可取消且 Deny 后不再误报 "signed in"、webview 拒绝导航到外部页面（安全边界）、tauri.localhost 非默认端口视为外部。配套一批 coverage matrix 文档行——**OpenHuman 在用"每个修复都补一条覆盖矩阵行"的方式做质量内控**，这个工程实践本身值得记录。单作者 commit 占比极高的特征依旧（历史数据 4547/4884），解读活跃度时需打折。

---

## 跨项目洞察

**1. "正确性攻坚"成为头部平台的共同阶段特征。** OpenClaw 做资源占用收敛、Hermes 做 cron 边界条件封死、Codex 把 Guardian 审查能力收敛为 extension 架构、Reasonix 重写会话 turn 权威模型——都不是加功能，而是把长周期运行暴露的并发/状态/生命周期问题系统性清偿。这印证了 ROADMAP Q4-4（long-running benchmarks）的问题意识：平台成熟度的分水岭正从"能不能跑"转向"跑七天之后还对不对"。

**2. Agent 自审（agent reviewing agents）浮出水面。** Codex 的 Guardian 体系（approval routing、circuit breaker、denial accounting 全部 extension 化）与 OpenClaw 的 PR autofix 流水线（自家 agent 修自家 PR）是同一趋势的两个实现：把审查/修复环节本身 agent 化并制度化。这是上周五个新兴范式之外的新信号，建议纳入 Q4-8 的观察清单。

**3. SSRF 防御同周两例。** PraisonAI 修 octal-encoded loopback 绕过、RocketRide 的 `tool_http_request` 阻断 SSRF 目的地——agent 获得任意 URL 访问能力后，SSRF 成为共性攻击面。企业治理研究（enterprise-governance）可跟踪这个维度。

**4. 会话持久化与分叉成为 CLI agent 的竞争焦点。** Reasonix 的 SessionID-only persistence + 从持久化日志分叉已完成轮次、Kimi-Code 的 subagent scope LRU 驱逐、Codex 的 thread attachments 跨 fork 保留——长会话的存储模型、恢复语义、分叉能力正在成为 CLI 编码代理的差异化战场。

**5. 计费透明度是用户侧最大痛点。** Codex 的 404/rate-limit/token 消耗争议（三个 200+ 评论 issue）、ZeroClaw 社区要求的 history-trim token 记账——agent 平台的用量可观测性（token 去了哪里）是跨生态的未满足需求。

**6. 生态互操作新信号。** NanoClaw 把 OpenCode 作为可安装 agent 运行时纳入宿主体系；Browser-Use 文档全面转向 self-hosting 叙事。平台间的"宿主-寄生"关系与开源产品的商业化叙事调整，都在重塑边界。

**7. 默认分支漂移持续。** 本周确认 ironclaw 默认分支已切 main（本地 origin/HEAD 仍旧，属缓存滞后非配置错误）；eliza 拉取时出现 ref 冲突（`origin/staging` 目录冲突），已用 develop 分支数据兜底，建议下次同步前 `git remote prune`。

**值得重点跟踪**：Codex Guardian 体系（agent 自审架构化）、Reasonix v1.38.9 会话架构重写、Hermes cron 正确性链条、HiClaw mermaid 工作流可视化、Dify OpenShell runtime。
