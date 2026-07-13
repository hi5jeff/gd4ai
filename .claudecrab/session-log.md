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

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T04:26:23+08:00

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

## Decisions (第二轮，已写入 DESIGN.md §7)

- 存储：YAML in git（策展层）+ PostgreSQL + pgvector + Meilisearch（服务/索引层），全开源。
- 输出：可执行方案包（装/配/首条prompt/验证），命令从字段拼装，LLM 不现写命令。
- LLM：MVP 用便宜国产 API（DeepSeek 级），不自建 GPU；离线加工后期可迁自建小模型。
- 规模：LLM 只看检索 Top-K 候选，不接触全量数据。

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T04:34:40+08:00

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

## Decisions (第二轮，已写入 DESIGN.md §7)

- 存储：YAML in git（策展层）+ PostgreSQL + pgvector + Meilisearch（服务/索引层），全开源。
- 输出：可执行方案包（装/配/首条prompt/验证），命令从字段拼装，LLM 不现写命令。
- LLM：MVP 用便宜国产 API（DeepSeek 级），不自建 GPU；离线加工后期可迁自建小模型。
- 规模：LLM 只看检索 Top-K 候选，不接触全量数据。

## Decisions (第三轮，已写入 DESIGN.md §7.5)

- 部署定阿里云托管：RDS PostgreSQL(pgvector) + OSS + 1×ECS(Meilisearch/爬虫/沙箱) + 百炼 Qwen API（替代 DeepSeek，推理成本归零）+ Redis(Tair) 仅做缓存/队列。
- Redis 定位：推荐结果缓存/限流/任务队列，不替代 PG 主存储。

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

