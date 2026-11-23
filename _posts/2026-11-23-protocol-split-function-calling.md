---
layout: post
title: "The Protocol Split: One Model, Seven Harnesses, One Dividing Line"
date: 2026-11-23 21:08:00 +0800
author: Danny Zeng
categories: [Ecosystem Analysis]
tags: [benchmark, function-calling, coding-agents, local-models, harness-design, qwen3-coder, aider, hermes, openclaw, nanobot, goclaw]
---

Five days ago [we showed](/allclaws/blog/2026/11/18/the-model-harness-interaction/) that the hardest cell in our two-tier benchmark grid was not a model or a harness but a *model×harness interaction* — every driver failed `refactor-multi` on the local 35B, while the same drivers passed it in the cloud. This week we ran the experiment that decomposition demanded: same model, same five tasks, **seven harnesses**. The result is the cleanest effect we have ever measured on this rig.

The dividing line is **how a harness drives the model**: native function-calling (send a tools schema, parse structured `tool_calls`) or a text protocol (ask the model to emit diffs and commands as prose, then parse the prose). On `qwen3-coder-30b` behind our LAN fleet router, the split is total:

| harness | protocol | passes (of 10) |
|---|---|---:|
| reasonix | native | 6 |
| hermes | native | 6 |
| nanobot | native | 6 |
| openclaw | native | 6 |
| goclaw | native | 3 |
| aider | **text** | **0** |
| kimi_code | native* | **0** |

**Native camp: 27/50. Text camp: 0/20.** And on the 35B generalist we benchmarked before, all four original drivers scored 8/10 — protocol didn't matter. Protocol sensitivity, it turns out, is a **model property**, not a harness property.

## What "text protocol failure" looks like

It is not a crash. It is the model *narrating*.

Aider asks for SEARCH/REPLACE diff blocks. Coder-30b replies, in fluent Chinese, with a plan: "I will resolve these issues in order. First, let me run the tests to confirm the problem…" — and then stops. No diff, no edit, exit 0. Median wall time: 55 seconds. Twenty runs, twenty variations of the same narrated intent.

kimi_code grinds instead. Its transcript shows the same opening sentence — "First, let me look at issue-001.md…" — repeated dozens of times across a session until the task timeout. The model knows what it wants to do; it never crosses the gap between *describing the action* and *emitting the structured form the harness parses*.

A coder model tuned for agentic tool-calling loops is, evidently, worse than a generalist at spontaneously producing aider's diff format — the very format that was designed when "the model writes the patch as text" was the only option.

## The kimi-code paradox

The asterisk in the table is the finding we cannot yet close. kimi_code is **native by source**: its kosong provider layer ships a full openai-common `tool_calls` pipeline. Yet across two grids it has never passed a single run on this model. Native protocol is *necessary* — no text harness survives — but not *sufficient*. Something in kimi-code's prompt stack or its local-provider gating keeps the tools from being honored. A reminder that the layer above the wire protocol still owns outcomes.

## The task table got reshuffled

Swap the model and the difficulty ranking inverts in places:

| task | 35B (4 drivers) | coder-30b (7 drivers) |
|---|---:|---:|
| gh-issue-001 | 8/8 | 10/10 |
| triage-burndown | 8/8 | 9/14 |
| feature-crud | 8/8 | 4/14 |
| legacy-migrate | **8/8** | **1/14** |
| refactor-multi | **0/8** | **3/14** |

Two things happen at once. `legacy-migrate` — six-module migration, trivially solved by the 35B — collapses to a single pass (reasonix, once). And `refactor-multi` — the structural-constraint task *no driver ever solved on the 35B* — gets cracked three times, by three different native harnesses, once each, never twice. The structural check ("this formula may appear at most once across the repo") yields to a coder model in a tool loop — stochastically. The model trades breadth for depth: it loses the tasks that reward generalist breadth and wins the one that rewards a code-shaped attention to detail.

This is the same lesson as the protocol split, one level up: **a harness ranking is a (model × harness × task-shape) tensor**, and any leaderboard that collapses it to one axis is measuring the collapse, not the agents.

## How we got seven harnesses

The taxonomy work came first: we materialized all 29 tracked submodules and classified every harness by how it drives the model — **17 native, 1 pure-text (aider, the lone survivor of the diff era), 5 hybrid, 4 frameworks, 2 uninspectable**. The three we promoted to the benchmark this week were chosen from that list, and each needed a different key to unlock headless operation:

- **nanobot** was easy — `agent --message --workspace` skips its TUI entirely; the endpoint rides its config file.
- **openclaw** was easiest of all — `agent exec --config --cwd --json` is *purpose-built* for reproducible headless runs, envelope and deadline included. The biggest platform on our radar turns out to ship exactly the primitive a benchmark needs.
- **goclaw** fought back. It is gateway-centric: the sqlite storage needs a build tag, the DB provider registry silently drops custom base URLs (the working path is a config-file fallback), and the agent workspace is a fixed path keyed by chat *owner* — which we bind to each run's worktree with a symlink. It passes `gh-issue-001` reliably but runs at 850s median, and its 3/10 smells like an iteration budget, not a protocol problem. That investigation is open.

All three debuted at 6/10. When the wiring is right, the protocol predicts the camp, and within the camp the harnesses are interchangeable to a first approximation.

## The takeaway

If you run local models — or any model you didn't pick yourself — check which side of the line your tools are on. A diff-based harness is a bet that the model can write structured prose under pressure; a native-tools harness is a bet that it can fill a schema. On generalist models both bets pay. On coder models, only one does. And the only way to know which kind of model you have is to run the grid.

---

*[中文版](/allclaws/blog/2026/11/23/protocol-split-function-calling-zh/)*

*Data: 70-run grid at [benchmark_results/longrun/2026-11-22T14-46-42](https://github.com/dz3ai/allclaws/tree/main/test_framework/benchmark_results/longrun/2026-11-22T14-46-42); protocol classification in [harness-function-calling-taxonomy.md](https://github.com/dz3ai/allclaws/blob/main/docs/reports/harness-function-calling-taxonomy.md); predecessor post: [The Model-Harness Interaction](/allclaws/blog/2026/11/18/the-model-harness-interaction/).*
