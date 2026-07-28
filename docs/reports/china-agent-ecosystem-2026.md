# China's AI Agent Ecosystem: The Parallel Universe

**Date:** 2026-07-28
**Scope:** 14 Chinese-origin AI agent projects on GitHub, plus foundation model and regulatory context
**Basis:** GitHub API data (stars, forks, licenses, activity timestamps) fetched 2026-07-28; regulatory analysis from public policy documentation; architectural analysis from repository descriptions and documentation
**AllClaws Context:** 31 platforms currently tracked. AgentScope (modelscope/agentscope) is the sole Chinese representative. This report identifies candidates to close that gap.

---

## Executive Summary: Why China's Agent Ecosystem Demands Attention

AllClaws tracks 31 agent platforms. One — AgentScope — represents the entire Chinese ecosystem. This is a structural blind spot.

The numbers tell a story of scale that the Western agent community systematically underestimates. Dify alone carries 150,556 GitHub stars, more than every AllClaws-tracked platform combined. MetaGPT's 69,565 stars would make it the third most-starred agent project in the world after OpenAI's Codex (86.9K) and Dify. AgentScope itself, already tracked but underweight in our analysis, has grown to 28,353 stars since January 2024 — a trajectory that outpaces most Western frameworks launched in the same window.

But star counts are the least interesting thing about this ecosystem. What matters is that China has built a **parallel agent stack** — parallel in the literal sense. It runs on different foundation models (Qwen, DeepSeek, GLM, Kimi — not GPT or Claude). It deploys through different channels (WeChat mini-programs, Douyin, enterprise clouds — not Slack or Discord). It operates under different rules (the Cyberspace Administration of China's generative AI regulations impose filing requirements and content controls that no Western agent platform faces). And it is solving problems that Western agent platforms don't encounter, because the operating environment is fundamentally different.

This report maps that parallel universe. It draws on GitHub data for 14 projects, categorizes them within AllClaws's existing design framework, and recommends which projects should enter the tracking set.

---

## Part 1: The Ecosystem Map

Fourteen projects, four architectural archetypes. The Chinese agent ecosystem is not a monolith — it contains the same fundamental divisions as the Western ecosystem (frameworks vs. platforms, single-agent vs. multi-agent, code-first vs. visual-first), but the center of gravity sits in different places.

### Tier 1: The Application Platforms (Infrastructure Layer)

These are the Drones of the Chinese ecosystem — visual, no-code or low-code platforms where non-developers assemble agent workflows. They occupy the same design space as rocketride-server and enterprise gateway platforms in AllClaws's framework, but at a scale that dwarfs their Western counterparts.

**Dify** (langgenius/dify) is the phenomenon. 150,556 stars. 23,721 forks. TypeScript primary. Created April 2023, and as of July 28, 2026, it received a push *today* — this project has not gone quiet. Its description reads: "Build Agentic workflows, RAG pipelines, with rich AI model and tool support on one collaborative workspace. Deploy on cloud, VPC, or self-host." It is, in effect, the Chinese agent ecosystem's answer to the question "what if LangChain had a UI and was actually usable in production?"

But Dify's license tells a story the star count obscures. It is technically Apache 2.0, but modified with two significant restrictions. First, multi-tenant deployments require a commercial license — you cannot host Dify as a SaaS for multiple customers without paying. Second, the LOGO and copyright information in the frontend cannot be removed or modified. This is the "open-core" pattern perfected by companies like MongoDB and Elastic, applied to agent infrastructure. It means Dify is open-source for self-hosting but commercially protected against cloud competitors — a strategy that makes sense in a market where Alibaba Cloud, Tencent Cloud, and Volcano Engine all want to offer agent platforms as managed services.

**Bisheng** (dataelement/bisheng) is Dify's domestic competitor. 11,784 stars, 1,920 forks, Python, Apache 2.0 (unmodified). Created August 2023, pushed July 28, 2026 — active today. Its full description is revealing: "BISHENG is an open LLM devops platform for next generation Enterprise AI applications. Powerful and comprehensive features include: GenAI workflow, RAG, Agent, Unified model management, Evaluation, SFT, Dataset Management, Enterprise-level System Management, Observability and more." The word "devops" is doing heavy lifting here. Bisheng isn't just a workflow builder — it's attempting to be the full lifecycle platform: build, deploy, evaluate, fine-tune, manage. This puts it closer to GoClaw and HiClaw in AllClaws's Enterprise Gateway category than to Dify's Pipeline Engine position.

**Coze Studio** (coze-dev/coze-studio) is ByteDance's entry, and its trajectory is the most aggressive in the dataset. 21,274 stars, 3,090 forks, TypeScript, Apache 2.0. Created June 26, 2025 — barely a year old — and already the third most-starred Chinese agent project. Its description: "An AI agent development platform with all-in-one visual tools, simplifying agent creation, debugging, and deployment." The topics tell the full story: `coze`, `kouzi` (扣子, its Chinese name), `workflow`, `rag`, `agent-platform`, `no-code`, `low-code-ai`. Coze is the visual agent builder that ByteDance launched as a commercial product, then open-sourced the core. It is the Chinese equivalent of what OpenAI's GPTs and Custom GPTs tried to be, but with a real development platform underneath.

Coze's last push was April 20, 2026 — a gap of three months. Whether this represents a deliberate release cadence (commercial product with periodic open-source syncs) or strategic indecision about open-source commitment is unclear from public data alone.

### Tier 2: The Agent Frameworks (Developer Layer)

These are the building blocks — Python (and one Go) libraries that developers use to construct agent systems programmatically. They occupy AllClaws's Orchestration Framework position alongside CrewAI, AutoGen, LangGraph, and SmolAgents.

**Qwen-Agent** (QwenLM/Qwen-Agent) is Alibaba's first-party agent framework, tightly coupled to the Qwen model family. 16,860 stars, 1,683 forks, Python, Apache 2.0. Created September 2023. Its description: "Agent framework and applications built upon Qwen>=3.0, featuring Function Calling, MCP, Code Interpreter, RAG, Chrome extension, etc." Three things stand out. First, "Qwen>=3.0" — this framework is designed for Qwen 3 and beyond, meaning Alibaba has rebuilt the agent layer around their latest model capabilities. Second, "MCP" — the Model Context Protocol, Anthropic's open standard, appears in a Chinese framework's feature list. This is significant: MCP adoption is not a Western-only phenomenon. Third, "Chrome extension" — Qwen-Agent ships as both a framework and a consumer-facing browser extension, blurring the line between developer tool and end-user product.

Qwen-Agent's last push was March 4, 2026 — five months ago. This is a concern for active tracking, though it may reflect Alibaba's release cadence (major pushes aligned with Qwen model releases rather than continuous development).

**ModelScope-Agent** (modelscope/modelscope-agent) is Alibaba's other agent framework — lighter weight, more research-oriented. 4,347 stars, 512 forks, Python, Apache 2.0. Created August 2023, pushed today (July 28, 2026). Its description: "MS-Agent: a lightweight framework to empower agentic execution of complex tasks." The "MS-Agent" branding connects it to the ModelScope platform, Alibaba's equivalent of Hugging Face. The 512-fork count relative to 4,347 stars suggests a more specialized audience than Dify or Qwen-Agent — this is a framework for researchers and platform developers, not end users.

**AgentScope** (modelscope/agentscope) is already tracked by AllClaws, but its numbers deserve re-examination. 28,353 stars, 3,268 forks, Python, Apache 2.0. Created January 2024, pushed today. Its description: "Build and run agents you can see, understand and trust." The emphasis on "see, understand and trust" is architecturally significant — it signals an emphasis on observability and interpretability that goes beyond pure capability. Its topics include `react-agent`, `mcp`, `multi-modal`, and `multi-agent`, placing it squarely in the same space as CrewAI and AutoGen but with a distinctive focus on agent transparency.

**MetaGPT** (geekan/MetaGPT) is the conceptual pioneer. 69,565 stars, 8,868 forks, Python, MIT license (notable — the only MIT-licensed major Chinese agent project). Created June 2023. Its description: "🌟 The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming." MetaGPT's contribution was the "AI software company" metaphor — assigning LLM agents roles like Product Manager, Architect, Engineer, and QA, then having them collaborate to produce software. This concept influenced the entire multi-agent subfield, including Western projects like ChatDev and CrewAI.

MetaGPT's last push was January 21, 2026 — six months ago. The project may be in maintenance mode or between major versions. Its open-source topics (`agent`, `gpt`, `llm`, `metagpt`, `multi-agent`) and MIT license suggest it began as an academic/research project and may not have transitioned to sustained commercial development.

**agentUniverse** (agentuniverse-ai/agentUniverse, formerly antgroup/agentUniverse) is Ant Group's contribution. 2,311 stars, 415 forks, Python, Apache 2.0. Created April 2024, pushed today. Its description: "agentUniverse is a LLM multi-agent framework that allows developers to easily build multi-agent applications." The Ant Group lineage matters — Ant is the financial technology affiliate of Alibaba, operating Alipay. A multi-agent framework from the company that built the world's largest mobile payment platform suggests enterprise deployment patterns optimized for financial services: high reliability, regulatory compliance, audit trails. The star count is modest compared to MetaGPT or Qwen-Agent, but Ant's internal deployment scale likely dwarfs what's visible on GitHub.

**Eino** (cloudwego/eino) is the outlier — the only Go-based framework in the dataset. 12,513 stars, 1,042 forks, Go, Apache 2.0. Created December 2024, pushed today. Its description: "The ultimate LLM/AI application development framework in Go." CloudWeGo is ByteDance's open-source microservices framework group. Eino extends that infrastructure into the LLM/agent domain. The choice of Go is architecturally significant: it means ByteDance is building its agent infrastructure with the same performance- and concurrency-oriented toolchain it uses for production microservices, not the Python-first approach dominant in Western agent frameworks. This is the agent framework equivalent of building on gRPC instead of REST — a bet on performance and type safety.

### Tier 3: The Autonomous Agents (Application Layer)

These are not frameworks — they are complete agent systems designed to solve specific classes of problems autonomously.

**ChatDev** (OpenBMB/ChatDev) is the multi-agent software company, now at version 2.0. 33,847 stars, 4,226 forks, Python, Apache 2.0. Created August 2023, pushed July 24, 2026. Its description: "ChatDev 2.0: Dev All through LLM-powered Multi-Agent Collaboration." OpenBMB is the research group from Tsinghua University — ChatDev is as much an academic artifact as a software project. The "2.0" designation indicates a significant rewrite, and the "Dev All" framing suggests it has expanded beyond software development into broader task automation.

**XAgent** (OpenBMB/XAgent) is ChatDev's sibling from the same Tsinghua group — and it tells a cautionary tale. 8,529 stars, 904 forks, Python, Apache 2.0. Its description: "An Autonomous LLM Agent for Complex Task Solving." But the critical data point: **last pushed August 12, 2024**. Nearly two years of silence. 63 open issues, none being addressed. XAgent appears to be an abandoned project — or at minimum, a project that has been superseded by ChatDev 2.0 within the OpenBMB group. This is the first cautionary data point in the Chinese ecosystem: not every project with significant stars is alive. The GitHub star count is a historical artifact, not a signal of current vitality.

**UI-TARS** (bytedance/UI-TARS) is ByteDance's GUI automation agent — the Chinese equivalent of computer-use agents like Anthropic's Computer Use. 11,240 stars, 854 forks, Python, Apache 2.0. Created January 2025, pushed January 27, 2026. Its description: "Pioneering Automated GUI Interaction with Native Agents." UI-TARS represents a distinct category: agents that interact with graphical user interfaces the way humans do — clicking, typing, navigating windows. This is the most direct Chinese competitor to Western computer-use paradigms, and its provenance (ByteDance, with deep expertise in mobile interfaces from TikTok/Douyin) gives it a credible foundation for GUI interaction.

### Tier 4: The Supporting Cast

**InternLM/lagent** is a lightweight agent framework from the InternLM team (Shanghai AI Laboratory). 2,273 stars, 237 forks, Python, Apache 2.0. Created August 2023, pushed today. "A lightweight framework for building LLM-based agents." Small but active, and connected to the InternLM model family — another Chinese foundation model ecosystem.

**LangBot** (langbot-app/langbot) bridges the Chinese and Western messaging ecosystems. 17,149 stars, 1,520 forks, Python, Apache 2.0. Created December 2022 — the oldest project in this survey. Its description is the most revealing in the entire dataset: "Production-grade platform for building agentic IM bots — 生产级多平台智能机器人开发平台 / Agent、知识库编排、插件系统 / Bots for Discord / Slack / LINE / Telegram / WeChat(企业微信)." The channel list tells the whole story: Discord, Slack, LINE, Telegram — and WeChat (Enterprise WeChat). LangBot is the only project in this survey that explicitly bridges Chinese and international messaging platforms. It occupies the same Plugin Empire position as OpenClaw and eliza in AllClaws's framework, but with WeChat as a first-class citizen rather than an afterthought.

---

## Part 2: The GFW Effect — How the Great Firewall Shapes Architecture

The most consequential architectural difference between Chinese and Western agent ecosystems is not a design choice. It is a constraint imposed by the Great Firewall (GFW), China's system of internet access control. This constraint ripples through every layer of the agent stack.

### The Foundation Model Constraint

Western agent frameworks assume OpenAI. The default model in LangChain's tutorials is GPT-4. CrewAI's examples use OpenAI. AutoGen's canonical examples reference OpenAI. Even when frameworks support multiple providers, the architectural assumptions — token limits, function calling formats, context window sizes — are calibrated to OpenAI's API.

Chinese developers cannot reliably access OpenAI's API. Anthropic's API is equally inaccessible. The result is a completely different default stack:

- **Qwen** (Alibaba) — open-weight models from 0.5B to 72B+ parameters, with Qwen 3.x as the current generation. Qwen-Agent is built specifically for Qwen>=3.0.
- **DeepSeek** — the model that stunned the world in January 2025 when DeepSeek R1 demonstrated reasoning capabilities rivaling OpenAI's o1 at a fraction of the training cost. DeepSeek's open-weight release forced a global reckoning about the cost of frontier model training.
- **GLM** (Zhipu AI / Z.ai) — the ChatGLM lineage, now at GLM-4.5+. Zhipu is the commercial spinout from Tsinghua University, the same institution behind OpenBMB.
- **Kimi** (Moonshot AI) — the long-context specialist, with Kimi K2 representing a generational leap in agentic capabilities. Kimi already appears in AllClaws's tracking via kimi-cli and kimi-code.
- **Doubao** (ByteDance), **ERNIE** (Baidu), **Hunyuan** (Tencent), **Spark** (iFlytek) — the big-tech proprietary models, less visible in open-source but dominant in consumer-facing deployments.

This domestic model reliance is not merely a substitution — it creates architectural consequences. Qwen-Agent's tight coupling to Qwen>=3.0 is not a limitation; it is an optimization. When you control both the model and the framework, you can co-design function calling formats, optimize context window usage, and align the agent's reasoning patterns with the model's training distribution. Western frameworks, supporting dozens of model providers, cannot achieve this level of integration.

The DeepSeek moment — January 2025, when R1's open-weight release proved that frontier reasoning capability could be achieved without OpenAI-scale compute budgets — had a specific effect on the agent ecosystem. It validated the domestic-first approach. If Chinese models could match Western reasoning capability, then Chinese agent frameworks built on those models were not compromises. They were legitimate alternatives.

### The Deployment Constraint

Chinese enterprise deployment preferences diverge from Western patterns in ways that affect agent architecture:

**On-premise preference.** Chinese enterprises, particularly state-owned enterprises and financial institutions, have strong preferences for on-premise deployment. Data sovereignty regulations, industry-specific compliance requirements, and institutional risk aversion all push toward local deployment. This is why Bisheng emphasizes "Enterprise-level System Management" and why Dify's self-hosting capability is central to its value proposition. The cloud-first assumption of many Western agent platforms does not hold in the Chinese enterprise market.

**Domestic cloud alternatives.** For cloud deployment, Chinese developers use Alibaba Cloud, Tencent Cloud, Huawei Cloud, and Volcano Engine (ByteDance) — not AWS, GCP, or Azure. Eino's Go-based architecture is designed for CloudWeGo, ByteDance's microservices framework that runs on Volcano Engine. The infrastructure choices are end-to-end domestic.

**Huawei Ascend and the hardware layer.** The US export controls on advanced AI chips (Nvidia H100, H200, B200) have accelerated adoption of Huawei's Ascend AI processors. Agent inference workloads increasingly run on domestic hardware, creating a hardware-software co-optimization loop that is invisible to Western observers. When Qwen-Agent or ModelScope-Agent are optimized for Ascend, the performance characteristics differ from what you'd see on Nvidia hardware.

### The API Access Constraint

The absence of direct OpenAI/Anthropic API access has a subtle but pervasive effect on agent design patterns. Western agent frameworks have converged on OpenAI's function calling format as a de facto standard. Chinese frameworks have no such convergence point — each domestic model provider implements function calling differently, and the frameworks must abstract over these differences.

ModelScope-Agent and AgentScope both position themselves as model-agnostic frameworks that abstract over multiple Chinese model providers. This is the same value proposition as LangChain's model abstraction, but the abstraction layer is thicker because the underlying models are more diverse in their API conventions.

### Censorship and Content Compliance

This is the constraint that is most often discussed and least well understood from outside China. The Cyberspace Administration of China (CAC) requires generative AI services to register their models, implement content filtering, and maintain records of generated outputs. For agent platforms specifically, this creates a tension: an autonomous agent that can take actions (send emails, modify files, make purchases) introduces a compliance surface that a chatbot does not.

The compliance patterns visible in the Chinese agent ecosystem include:

- **Content filtering at the model layer**, not the agent layer. Most Chinese foundation models ship with built-in safety alignment that filters politically sensitive content. Agent frameworks inherit this filtering rather than reimplementing it.
- **Human-in-the-loop requirements for consequential actions.** The emphasis on "agents you can see, understand and trust" (AgentScope's tagline) reflects a regulatory environment where unmonitored autonomous action is legally risky.
- **Audit logging.** Bisheng's "Observability" feature and enterprise management capabilities are not just nice-to-haves — they are compliance infrastructure.

These compliance requirements have an unexpected architectural benefit: they force a level of observability and governance into Chinese agent platforms that many Western platforms treat as optional. AgentScope's transparency focus and Bisheng's enterprise management depth are partially emergent properties of operating in a regulated environment.

---

## Part 3: Chinese vs. Western Design Patterns

The parallel evolution of Chinese and Western agent ecosystems has produced convergent and divergent design patterns. The convergences are predictable — everyone discovers that multi-agent orchestration is hard, that RAG is necessary, that function calling needs standardization. The divergences are more interesting.

### Pattern 1: Framework-First vs. Platform-First

The Western agent ecosystem was built framework-first. LangChain (2022) came before most agent platforms. CrewAI, AutoGen, LangGraph — all frameworks. The platforms (OpenAI's GPTs, custom agent deployments) came later, built on top of framework abstractions.

The Chinese ecosystem inverts this. Dify (April 2023), Coze (commercial product before open-source), Bisheng — the platforms came first or simultaneously. The frameworks (Qwen-Agent, AgentScope, ModelScope-Agent) serve the platforms, not the other way around. Dify is a platform that happens to be open-source. LangChain is a framework that happens to have a platform (LangSmith) bolted on.

This inversion has consequences. Chinese platforms are more polished, more visual, and more accessible to non-developers. Western frameworks are more flexible, more composable, and more embedded in the developer workflow. When a Chinese developer wants to build an agent, they open Dify's web UI. When a Western developer wants to build an agent, they `pip install langchain`.

### Pattern 2: The Missing CLI Agent

AllClaws tracks five CLI coding agents: aider, copilot-cli, reasonix, kimi-cli, and codex. Four are Western. One — kimi-cli — is Chinese. This ratio reflects a real gap: the Chinese ecosystem has not produced a terminal-native coding agent with the cultural impact of aider or codex.

This is not because Chinese developers don't use terminal agents. Kimi's CLI tools exist. But the center of gravity for Chinese developer tooling is in IDE plugins (Trae, ByteDance's AI IDE) and cloud-based development environments, not in terminal-native tools. The Western "hacker aesthetic" of CLI-first development, exemplified by aider and codex, has a weaker cultural foothold in the Chinese developer community, where visual IDEs and cloud workspaces dominate.

### Pattern 3: Model Coupling as Feature, Not Bug

Western agent frameworks treat model-agnosticism as a virtue. LangChain's entire value proposition is that you can swap GPT-4 for Claude for Llama with a one-line change. This is seen as obviously correct.

Chinese frameworks are more willing to couple tightly to specific models. Qwen-Agent is built for Qwen. ModelScope-Agent defaults to ModelScope-hosted models. This coupling is treated as a feature, not a limitation — the argument being that deep integration with one model family produces better agent behavior than shallow integration with many.

The data partially supports this argument. Qwen-Agent's tight coupling allows it to exploit Qwen 3.0's specific capabilities (function calling format, context window characteristics, reasoning patterns) in ways that a model-agnostic framework cannot. The trade-off is lock-in: if you build your agent on Qwen-Agent, migrating to DeepSeek or GLM requires reworking the integration layer.

### Pattern 4: The Go Difference

Eino is the only Go-based agent framework in either the Chinese or Western ecosystem that has achieved significant adoption (12,513 stars). Go's presence in the agent space is otherwise minimal — most Western frameworks are Python, with TypeScript for platform/UI layers.

ByteDance's choice of Go for Eino reflects a different architectural bet. Go's strengths — compiled performance, goroutine-level concurrency, static typing, small deployment footprint — matter in high-throughput production environments. Python's strengths — ecosystem breadth, ML library access, developer ergonomics — matter in research and prototyping. Eino's existence suggests that ByteDance is optimizing for the deployment phase of agent infrastructure, where Python's overhead becomes a bottleneck. This is a pattern worth watching: if agent infrastructure follows the same trajectory as web infrastructure (where Go displaced Python in high-performance services), Eino may be early to a trend.

### Pattern 5: The WeChat Distribution Channel

No Western agent platform has a distribution channel comparable to WeChat. LangBot's explicit support for WeChat (including Enterprise WeChat) is not a minor feature — it is access to a platform with over 1.3 billion monthly active users. WeChat mini-programs can host agent interactions, and Enterprise WeChat is the dominant workplace communication tool in Chinese enterprises.

This distribution advantage means that Chinese agent platforms can reach users through channels that Western platforms cannot replicate. A Dify workflow deployed as a WeChat mini-program reaches an audience that no Slack or Discord bot can access. The architectural implication is that Chinese agent platforms are designed for multi-channel deployment from the start, with WeChat as a primary target.

---

## Part 4: Government AI Governance and Its Impact on Agent Development

China's AI governance regime is the most developed in the world — not necessarily in sophistication, but in specificity. The government has issued more targeted AI regulations than any other jurisdiction, and these regulations directly shape how agent platforms are built and deployed.

### The Regulatory Stack

The foundation is the **Interim Measures for the Management of Generative AI Services**, effective August 2023. These measures require:

- Registration and security assessment of generative AI services before public release
- Content that "reflects socialist core values" and does not contain content subverting state power or promoting discrimination
- Labeling of AI-generated content
- User data protection and algorithm transparency requirements

For agent platforms, these measures create a specific compliance burden. An agent that can autonomously generate content — write emails, post to social media, create documents — must ensure that all generated content complies with content rules. This is technically challenging: an agent's output is less predictable than a chatbot's, because agents chain multiple model calls and tool invocations.

### The Model Registration Regime

Beyond the interim measures, China has established a **model registration/filing system** administered by the CAC. Foundation models intended for public use must be filed with the government, undergo security testing, and receive approval. This applies to the models (Qwen, DeepSeek, GLM, etc.) that power agent platforms.

The practical effect on agents is indirect but significant. Because the foundation models are pre-filtered for compliance, agent frameworks that use registered models inherit a baseline level of content safety. But agents can still produce non-compliant output through tool use (e.g., an agent that reads from a non-compliant data source and incorporates that content into its output). This creates an ongoing compliance challenge that platforms like Bisheng address through observability and audit logging features.

### Impact on Agent Autonomy

The regulatory environment creates a persistent tension with agent autonomy. An agent that can autonomously take consequential actions — make purchases, modify production systems, send communications — introduces legal liability that the content rules were not designed to address.

The visible response in the Chinese ecosystem is a preference for **human-in-the-loop architectures** and **constrained autonomy**. AgentScope's "agents you can see, understand and trust" is not just marketing — it reflects a design philosophy shaped by regulatory constraints. The emphasis on observability in Bisheng and the workflow-visualization focus of Dify and Coze are partially responses to the need for human oversight of agent behavior.

This contrasts with the Western agent ecosystem, where maximal autonomy is often treated as an unalloyed good. The Chinese regulatory environment has, perhaps paradoxically, pushed agent platforms toward more responsible design patterns — not because developers are more responsible, but because the legal environment demands it.

### The Governance Export Question

China's AI governance model is being studied by other countries, particularly in Southeast Asia, the Middle East, and Africa. If Chinese agent platforms are designed for compliance with Chinese regulations, they may be more easily adaptable to other regulated markets than Western platforms that assume a permissive regulatory environment. This could give Chinese agent platforms a structural advantage in markets that adopt governance frameworks inspired by the Chinese model.

---

## Part 5: Activity Analysis — Who Is Alive?

GitHub star counts measure historical interest, not current vitality. The push timestamps in this dataset reveal a more nuanced picture.

### Actively Maintained (pushed within 30 days of data collection, July 28, 2026)

| Project | Last Push | Assessment |
|---------|-----------|------------|
| Dify | 2026-07-28 (today) | Hyperactive. The most actively maintained project in the dataset. |
| ModelScope-Agent | 2026-07-28 (today) | Active. Consistent development cadence. |
| AgentScope | 2026-07-28 (today) | Active. Already tracked by AllClaws; trajectory remains strong. |
| Bisheng | 2026-07-28 (today) | Active. Enterprise-focused development continues. |
| Eino | 2026-07-28 (today) | Active. ByteDance investing in Go-based agent infrastructure. |
| agentUniverse | 2026-07-28 (today) | Active. Ant Group's multi-agent framework under continuous development. |
| InternLM/lagent | 2026-07-28 (today) | Active. Lightweight framework, steady development. |
| ChatDev | 2026-07-24 (4 days ago) | Active. Version 2.0 development ongoing. |
| LangBot | 2026-07-27 (1 day ago) | Active. Oldest project in the survey, still maintained. |

### Slowing (pushed 3-6 months ago)

| Project | Last Push | Assessment |
|---------|-----------|------------|
| Qwen-Agent | 2026-03-04 (5 months ago) | Concerning. May follow Qwen model release cadence, but 5 months is a long gap. |
| MetaGPT | 2026-01-21 (6 months ago) | Likely maintenance mode. The MIT license and academic origin suggest this may be a completed research project. |
| UI-TARS | 2026-01-27 (6 months ago) | Unclear. ByteDance may have shifted GUI automation efforts to internal teams. |
| Coze Studio | 2026-04-20 (3 months ago) | Watch. Commercial product with periodic open-source syncs is a plausible explanation. |

### Abandoned (no push for 12+ months)

| Project | Last Push | Assessment |
|---------|-----------|------------|
| XAgent | 2024-08-12 (23 months ago) | Abandoned. 8,529 stars but effectively dead. Succeeded by ChatDev 2.0 within OpenBMB. |

The activity data reveals an important pattern: the Chinese agent ecosystem's vitality is concentrated in platform projects (Dify, Bisheng, Coze) and corporate-backed frameworks (AgentScope, Eino, ModelScope-Agent, Qwen-Agent). Independent or academic projects (MetaGPT, XAgent) are more likely to stall. This mirrors the Western ecosystem, where corporate-backed projects (OpenAI's codex, Anthropic's Claude tools) maintain development velocity while independent projects (AutoGPT, BabyAGI) have largely gone quiet.

---

## Part 6: Platform Recommendations for AllClaws

AllClaws currently tracks 31 platforms. AgentScope is the sole Chinese representative. This is a structural gap that should be closed. Based on the data collected in this report, the following projects are recommended for inclusion, ranked by priority.

### Priority 1: Immediate Addition

**Dify** (langgenius/dify) — 150K stars, the most starred agent project in the world. It occupies the Pipeline Engine position in AllClaws's framework, alongside rocketride-server. But Dify is not just another pipeline engine — its modified Apache 2.0 license, its multi-model support, and its deployment flexibility (cloud, VPC, self-hosted) make it architecturally distinctive. Its active development (pushed today) and massive community (23K forks) mean it is a living, evolving platform that AllClaws cannot afford to ignore. **AllClaws Position: Pipeline Engine / Enterprise Gateway hybrid.**

**Qwen-Agent** (QwenLM/Qwen-Agent) — 16.8K stars, Alibaba's first-party agent framework. Despite the 5-month push gap, this project is significant for two reasons: it is the canonical example of model-framework co-design (built specifically for Qwen>=3.0), and it has adopted MCP, making it interoperable with the Western agent tooling ecosystem. It occupies the Orchestration Framework position. **AllClaws Position: Orchestration Framework, with Personal Sovereign characteristics (Chrome extension).**

### Priority 2: Strong Candidates

**MetaGPT** (geekan/MetaGPT) — 69.5K stars, the conceptual originator of the "AI software company" multi-agent pattern. Despite slowing development, its influence on the multi-agent subfield is undeniable. Its MIT license and academic provenance make it a reference implementation rather than a production platform. **AllClaws Position: Orchestration Framework (reference implementation).**

**Coze Studio** (coze-dev/coze-studio) — 21.3K stars, ByteDance's visual agent platform. The fastest-growing project in the dataset (21K stars in one year). Its commercial backing and visual-first approach make it the Chinese equivalent of OpenAI's Custom GPTs, but with a real development platform underneath. **AllClaws Position: Pipeline Engine / Plugin Empire hybrid.**

**ChatDev** (OpenBMB/ChatDev) — 33.8K stars, the multi-agent software company now at version 2.0. Tsinghua-origin, actively maintained, and representing the academic research track of Chinese agent development. **AllClaws Position: Autonomous Agent / Orchestration Framework.**

### Priority 3: Watch List

**Eino** (cloudwego/eino) — 12.5K stars, the only Go-based agent framework of significance. ByteDance-backed. Its architectural choice (Go over Python) makes it unique in both ecosystems. Worth tracking for the signal it sends about production agent infrastructure. **AllClaws Position: Orchestration Framework (Go variant).**

**Bisheng** (dataelement/bisheng) — 11.8K stars, enterprise-focused LLM devops platform. The emphasis on SFT, evaluation, and enterprise management makes it the most governance-heavy platform in the dataset. **AllClaws Position: Enterprise Gateway.**

**UI-TARS** (bytedance/UI-TARS) — 11.2K stars, GUI automation agent. The Chinese computer-use agent. If computer-use becomes a major agent paradigm (as Anthropic's bet on Computer Use suggests), UI-TARS is the Chinese entry. **AllClaws Position: Autonomous Agent (GUI interaction).**

**LangBot** (langbot-app/langbot) — 17.1K stars, the multi-platform IM bot framework with WeChat support. The only project that bridges Chinese and Western messaging ecosystems. **AllClaws Position: Plugin Empire (WeChat variant).**

### Not Recommended for Addition

**XAgent** (OpenBMB/XAgent) — 8.5K stars but abandoned since August 2024. Tracking a dead project adds noise. Its conceptual contribution (autonomous task decomposition) is already represented by ChatDev 2.0.

**ModelScope-Agent** (modelscope/modelscope-agent) — 4.3K stars. Valuable but overlaps significantly with AgentScope (both Alibaba/ModelScope ecosystem). Track one, not both. AgentScope is the better choice given its larger community and active development.

**agentUniverse** (agentuniverse-ai/agentUniverse) — 2.3K stars. Active but small. Ant Group's internal deployment may be significant, but the open-source project is not yet at the scale that warrants AllClaws tracking. Monitor.

**InternLM/lagent** — 2.3K stars. Lightweight and active, but too small for current inclusion. Worth revisiting if the InternLM model ecosystem gains broader adoption.

---

## Part 7: Limitations and Caveats

This report is based on publicly available data, primarily GitHub API responses fetched on July 28, 2026. Several limitations should be acknowledged.

**GitHub stars measure global attention, not Chinese adoption.** A project with 150K GitHub stars may have lower actual deployment in China than a project with 5K stars that is distributed through domestic channels (Gitee, ModelScope, internal corporate deployment). The Chinese developer ecosystem uses GitHub, but it also uses domestic alternatives that are invisible to GitHub-based analysis. Dify's global star count may overstate its domestic Chinese market share relative to a platform like Bisheng that is more China-focused.

**Star counts do not capture commercial products.** ByteDance's Coze, Baidu's AppBuilder, Alibaba's Tongyi, and Tencent's Yuanbao are all commercial agent platforms with potentially massive user bases that are invisible on GitHub. Coze Studio's open-source release (June 2025) is a partial window into the Coze commercial product, but the commercial product's actual deployment scale is unknown from public data. The Manus agent (Monica.im), which generated enormous attention in early 2025 as a general-purpose autonomous agent, is entirely closed-source and invisible to this analysis.

**Activity timestamps are noisy signals.** A project that hasn't been pushed in 5 months may be between major versions, reorganizing its team, or shifting to a different repository. MetaGPT's 6-month gap may indicate maintenance mode or may precede a MetaGPT 3.0 release. Qwen-Agent's 5-month gap may align with Qwen model release cycles. Push timestamps are necessary but insufficient signals of project health.

**Architectural analysis is based on descriptions, not code review.** This report infers architectural patterns from repository descriptions, topics, and documentation snippets. A full architectural analysis — of the kind AllClaws conducts for its tracked platforms — would require reading the source code, testing the frameworks, and benchmarking their capabilities. The categorizations in this report are preliminary and should be validated before formal tracking begins.

**Regulatory analysis is simplified.** China's AI governance regime is complex, evolving, and partially opaque. The interim measures and model registration requirements described here are real and publicly documented, but the enforcement details, the specific technical requirements imposed on registered models, and the practical experience of compliance are not fully visible from outside China. The compliance patterns attributed to Chinese agent platforms (content filtering, human-in-the-loop, audit logging) are inferred from feature descriptions and general regulatory context, not from verified compliance documentation.

**The ecosystem moves faster than this report.** The Chinese AI agent ecosystem in mid-2026 is in rapid flux. New models (Qwen 3.x, DeepSeek V3/R1 successors, GLM updates) arrive monthly. New platforms launch and pivot. Government regulations evolve. Any specific claim in this report — a star count, a push date, a regulatory description — may be outdated within weeks. The structural observations (parallel stack, GFW constraints, platform-first pattern) are more durable than the specific data points.

---

## Appendix: Raw GitHub Data

All data fetched via `gh repo view` and `gh api` on 2026-07-28.

| Repository | Stars | Forks | Language | License | Created | Last Push | Status |
|------------|-------|-------|----------|---------|---------|-----------|--------|
| langgenius/dify | 150,556 | 23,721 | TypeScript | Modified Apache 2.0 | 2023-04-12 | 2026-07-28 | Active |
| geekan/MetaGPT | 69,565 | 8,868 | Python | MIT | 2023-06-30 | 2026-01-21 | Slowing |
| modelscope/agentscope | 28,353 | 3,268 | Python | Apache 2.0 | 2024-01-12 | 2026-07-28 | Active (tracked) |
| coze-dev/coze-studio | 21,274 | 3,090 | TypeScript | Apache 2.0 | 2025-06-26 | 2026-04-20 | Active |
| langbot-app/langbot | 17,149 | 1,520 | Python | Apache 2.0 | 2022-12-07 | 2026-07-27 | Active |
| QwenLM/Qwen-Agent | 16,860 | 1,683 | Python | Apache 2.0 | 2023-09-22 | 2026-03-04 | Slowing |
| cloudwego/eino | 12,513 | 1,042 | Go | Apache 2.0 | 2024-12-04 | 2026-07-28 | Active |
| dataelement/bisheng | 11,784 | 1,920 | Python | Apache 2.0 | 2023-08-28 | 2026-07-28 | Active |
| bytedance/UI-TARS | 11,240 | 854 | Python | Apache 2.0 | 2025-01-19 | 2026-01-27 | Slowing |
| OpenBMB/ChatDev | 33,847 | 4,226 | Python | Apache 2.0 | 2023-08-28 | 2026-07-24 | Active |
| OpenBMB/XAgent | 8,529 | 904 | Python | Apache 2.0 | 2023-10-16 | 2024-08-12 | Abandoned |
| modelscope/modelscope-agent | 4,347 | 512 | Python | Apache 2.0 | 2023-08-03 | 2026-07-28 | Active |
| agentuniverse-ai/agentUniverse | 2,311 | 415 | Python | Apache 2.0 | 2024-04-23 | 2026-07-28 | Active |
| InternLM/lagent | 2,273 | 237 | Python | Apache 2.0 | 2023-08-20 | 2026-07-28 | Active |

**Total combined stars across 14 projects: 392,531**

For comparison, AllClaws's 31 currently tracked platforms represent a combined star count that Dify and MetaGPT alone exceed.

---

*Report prepared for AllClaws Q3-6 task. Data collection date: 2026-07-28. Methodology: GitHub API queries via `gh repo view` and `gh api`. No web scraping or automated crawling was used. All star/fork/date figures are point-in-time snapshots and will change.*
