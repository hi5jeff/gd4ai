---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T04:15:12+08:00

# Active Session State

_This file is automatically injected into Claude's context at the start of every session and before any compaction. Update it whenever you make a significant decision or change._

## Current task

用户提出 howAI 的产品方向：根据用户需求智能推荐 AI 编程生态内容（skill/roles/plugin/MCP/prompt 模板），从小白到专家可用。本轮任务：系统设计分析，产出 DESIGN.md。

## Decisions

- 技术路线：不自训 LLM；用「结构化数据集 + 混合检索 + 现成 LLM 做意图理解与方案组合」（RAG + 编排）。
- 差异化：竞品（smithery / mcp.so / PulseMCP / glama / claudeskills.info / ccmarket.dev 等）都是"目录+搜索"，缺"需求→整套方案"的组合推荐。howAI 做场景化方案包（playbook）+ 实测验证 + 中文。
- 数据集三层：组件库（统一 schema）、方案库（playbook）、用法语料（QA/how-to）。

## Files in progress

- DESIGN.md — 系统设计分析文档（本轮产出）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

