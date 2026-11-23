---
layout: post
title: "协议分层：同一个模型、七个 harness、一条分界线"
lang: zh
date: 2026-11-23 21:00:00 +0800
author: Danny Zeng
categories: [生态分析]
tags: [benchmark, function-calling, coding-agents, local-models, harness-design, qwen3-coder, aider, hermes, openclaw, nanobot, goclaw]
---

五天前[我们说过](/allclaws/blog/2026/11/18/the-model-harness-interaction/)：这个基准测试里最难的格子，不是某个模型，也不是某个 harness，而是**模型和 harness 的组合**——本地 35B 上所有 driver 都过不了 refactor-multi，同样的 driver 换到云端就能过。本周我们做了那个结论要求的实验：同一个模型、同样的五个任务、**七个 harness**。这是这套测试台到目前为止测到的最干净的一个效应。

分界线是** harness 怎么驱动模型**：原生 function-calling（发一份 tools 定义，解析结构化的 `tool_calls` 返回），还是文本协议（让模型用文字写出 diff 和命令，再去解析这些文字）。在路由器后面的 `qwen3-coder-30b` 上，结果一分为二：

| harness | 协议 | 通过数（满分 10）|
|---|---|---:|
| reasonix | 原生 | 6 |
| hermes | 原生 | 6 |
| nanobot | 原生 | 6 |
| openclaw | 原生 | 6 |
| goclaw | 原生 | 3 |
| aider | **文本** | **0** |
| kimi_code | 原生* | **0** |

**原生阵营 27/50，文本阵营 0/20。**而在这之前测的 35B 通用模型上，四个 driver 全是 8/10——协议根本不影响结果。所以结论是：**协议敏感性是模型的属性，不是 harness 的属性。**

## 「文本协议失败」长什么样

不是崩溃，是模型在**旁白**。

aider 要求模型输出 SEARCH/REPLACE 格式的 diff。coder-30b 的回复是一段流畅的中文计划：「我将按照顺序解决这些问题。首先，让我运行测试来确认问题……」——然后就停了。没有 diff，没有修改，正常退出。中位耗时 55 秒。二十次运行，二十个同样开场白的变体。

kimi_code 是另一种死法。它的对话记录里，同一句「首先，让我查看 issue-001.md……」在会话里重复几十遍，直到任务超时。模型知道它想做什么，但始终跨不过去：从「描述这个动作」到「输出 harness 能解析的结构化形式」之间的那道缝。

一个为工具调用循环调出来的代码模型，自发写 aider 那种 diff 格式的能力反而不如通用模型——而 diff 格式恰恰是「模型把补丁当文字写」那个年代唯一的选项。

## kimi-code 悖论

表格里的星号是目前关不上的一个发现。kimi_code 从源码看是**原生**的：它的 kosong 层带了完整的 openai-common `tool_calls` 管线。但两轮网格里，它在这个模型上一次都没过。原生协议是**必要条件**——文本协议的 harness 全灭——但不是**充分条件**。kimi_code 的提示词层或者本地 provider 的门控里，有什么东西让工具没被真正执行。这提醒我们：线上协议的上面那层，仍然决定结果。

## 任务难度表被重排了

换一个模型，难度排名部分倒置：

| 任务 | 35B（4 driver）| coder-30b（7 driver）|
|---|---:|---:|
| gh-issue-001 | 8/8 | 10/10 |
| triage-burndown | 8/8 | 9/14 |
| feature-crud | 8/8 | 4/14 |
| legacy-migrate | **8/8** | **1/14** |
| refactor-multi | **0/8** | **3/14** |

两件事同时发生。legacy-migrate——六个模块的迁移，35B 上轻松全过——塌缩到只过一次（reasonix，一次）。而 refactor-multi——35B 上**没有任何 driver 解开过**的结构性任务——被破了三次，三个不同的原生 harness，各一次，没有谁破两次。那道结构性检查（「这个公式在全仓库最多出现一次」）在工具循环里的代码模型面前松动了——但是概率性的。这个模型用广度换深度：丢掉了奖励通用广度的任务，赢下了奖励代码形态细节的那一个。

这和协议分层是同一课的上一层：**harness 排名是一个（模型 × harness × 任务形态）的张量**。任何把它压成单一维度的榜单，测的是压缩本身，不是 agent。

## 七个 harness 是怎么凑齐的

先做的是分类：把跟踪的全部 29 个仓库实体化，按驱动方式给每个 harness 定类——**原生 17、纯文本 1（aider，diff 时代的独苗）、混合 5、框架 4、无法检验 2**。本周升入基准的三个就从这份名单里挑，每个的解锁钥匙都不一样：

- **nanobot** 顺利——`agent --message --workspace` 自带单发模式，端点走配置文件。
- **openclaw** 最顺利——`agent exec --config --cwd --json` 就是为可复现的无头运行设计的，连结果信封和超时都带。我们雷达上最大的平台，恰好出厂就带着基准测试需要的那个原语。
- **goclaw** 对抗到底。它是网关架构：sqlite 存储要加构建标签；数据库里的 provider 会悄悄丢掉自定义 base_url（能用的路径是配置文件兜底）；agent 工作区是按会话**属主**固定的路径——我们用软链接把它指到每次运行的任务目录。它能稳定通过 gh-issue-001，但中位 850 秒，3/10 的成绩闻起来像迭代预算问题，不是协议问题。这条线还在查。

三个新 driver 首秀都是 6/10。接线正确的时候，协议决定了阵营；阵营之内，harness 之间的差异一阶近似可以忽略。

## 结论

如果你在跑本地模型——或者任何不是你自己挑的模型——先查一下你的工具站在线的哪一边。基于 diff 的 harness 赌的是模型能在压力下写出结构化的文字；原生工具的 harness 赌的是它能填好一个 schema。通用模型上两个赌注都赢。代码模型上只有一个赢。而要知道手上的模型是哪一种，唯一的办法是把网格跑一遍。

---

*[English version](/allclaws/blog/2026/11/23/protocol-split-function-calling/)*

*数据：70 次运行的网格 [benchmark_results/longrun/2026-11-22T14-46-42](https://github.com/dz3ai/allclaws/tree/main/test_framework/benchmark_results/longrun/2026-11-22T14-46-42)；协议分类见 [harness-function-calling-taxonomy.md](https://github.com/dz3ai/allclaws/blob/main/docs/reports/harness-function-calling-taxonomy.md)；前作：[The Model-Harness Interaction](/allclaws/blog/2026/11/18/the-model-harness-interaction/)。*
