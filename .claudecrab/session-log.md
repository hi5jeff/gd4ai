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

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T04:51:16+08:00

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

## Decisions (第四轮，已写入 DESIGN.md §7.6)

- 核心约束：闭世界推荐（LLM 只能引用检索返回的组件 id，输出前校验）、查空兜底（宁说没有不许编）、缺口日志驱动采集、意图先分型（单件型 vs 方案型）再检索。
- 范围扩大确认：不限编程 — 覆盖泛 AI 工具生态（图像生成/平面设计/室内装修等垂直场景）。

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T10:35:26+08:00

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

## Decisions (第四轮，已写入 DESIGN.md §7.6)

- 核心约束：闭世界推荐（LLM 只能引用检索返回的组件 id，输出前校验）、查空兜底（宁说没有不许编）、缺口日志驱动采集、意图先分型（单件型 vs 方案型）再检索。
- 范围扩大确认：不限编程 — 覆盖泛 AI 工具生态（图像生成/平面设计/室内装修等垂直场景）。

## Decisions (第五轮，已写入 DESIGN.md §7.5 修订)

- 初期不买 RDS/托管搜索：用户提供一台专用 ECS（建议 4C8G/100G ESSD, Ubuntu 22.04），我用 Docker Compose 配全套（PG16+pgvector / Meilisearch / Redis / 应用 / 沙箱）。
- 可行依据：真相源在 git YAML，库可重建；只备份运营数据（每日 pg_dump → OSS）。
- 安全：数据服务只绑内网，公网仅应用端口+SSH。后期 pg_dump 迁 RDS。
- 等待用户提供：ECS IP + SSH 凭证（+ 可选 OSS bucket AK 用于备份）。

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T11:04:21+08:00

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

## Decisions (第四轮，已写入 DESIGN.md §7.6)

- 核心约束：闭世界推荐（LLM 只能引用检索返回的组件 id，输出前校验）、查空兜底（宁说没有不许编）、缺口日志驱动采集、意图先分型（单件型 vs 方案型）再检索。
- 范围扩大确认：不限编程 — 覆盖泛 AI 工具生态（图像生成/平面设计/室内装修等垂直场景）。

## Decisions (第五轮，已写入 DESIGN.md §7.5 修订)

- 初期不买 RDS/托管搜索：用户提供一台专用 ECS（建议 4C8G/100G ESSD, Ubuntu 22.04），我用 Docker Compose 配全套（PG16+pgvector / Meilisearch / Redis / 应用 / 沙箱）。
- 可行依据：真相源在 git YAML，库可重建；只备份运营数据（每日 pg_dump → OSS）。
- 安全：数据服务只绑内网，公网仅应用端口+SSH。后期 pg_dump 迁 RDS。
- 等待用户提供：ECS IP + SSH 凭证（+ 可选 OSS bucket AK 用于备份）。

## Decisions (第六轮，进入实施；已写入 DESIGN.md §7.7 + MEMORY.md)

- LLM 实测定型：在线推荐 deepseek-v4-pro（8s, JSON可靠），离线加工 deepseek-v4-flash；glm-4.7/qwen3.7-plus 淘汰（慢/截断）。走 mdbox 网关（OpenAI 兼容）。
- Embedding：mdbox 无合适文本模型 → 227 上本地 BGE-M3（TEI CPU 容器）。
- 拓扑：226=前端，227=后端+全部数据服务。OSS 凭证在 .env（已 gitignore）。
- 已产出 infra/docker-compose.yml + provision.sh + backup.sh。

## Blocked

- ⚠️ 两台服务器 SSH 拒绝（无公钥）。已把本机 ~/.ssh/id_ed25519.pub 给用户，等安装后才能部署。

## Next (机器可登录后)

1. 227: 上传 infra/ → 跑 provision.sh → 验证 4 容器 + pgvector + 备份 cron
2. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
3. 后端 API（检索+编排+校验）→ 226 前端

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T11:14:31+08:00

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

## Decisions (第四轮，已写入 DESIGN.md §7.6)

- 核心约束：闭世界推荐（LLM 只能引用检索返回的组件 id，输出前校验）、查空兜底（宁说没有不许编）、缺口日志驱动采集、意图先分型（单件型 vs 方案型）再检索。
- 范围扩大确认：不限编程 — 覆盖泛 AI 工具生态（图像生成/平面设计/室内装修等垂直场景）。

## Decisions (第五轮，已写入 DESIGN.md §7.5 修订)

- 初期不买 RDS/托管搜索：用户提供一台专用 ECS（建议 4C8G/100G ESSD, Ubuntu 22.04），我用 Docker Compose 配全套（PG16+pgvector / Meilisearch / Redis / 应用 / 沙箱）。
- 可行依据：真相源在 git YAML，库可重建；只备份运营数据（每日 pg_dump → OSS）。
- 安全：数据服务只绑内网，公网仅应用端口+SSH。后期 pg_dump 迁 RDS。
- 等待用户提供：ECS IP + SSH 凭证（+ 可选 OSS bucket AK 用于备份）。

## Decisions (第六轮，进入实施；已写入 DESIGN.md §7.7 + MEMORY.md)

- LLM 实测定型：在线推荐 deepseek-v4-pro（8s, JSON可靠），离线加工 deepseek-v4-flash；glm-4.7/qwen3.7-plus 淘汰（慢/截断）。走 mdbox 网关（OpenAI 兼容）。
- Embedding：mdbox 无合适文本模型 → 227 上本地 BGE-M3（TEI CPU 容器）。
- 拓扑：226=前端，227=后端+全部数据服务。OSS 凭证在 .env（已 gitignore）。
- 已产出 infra/docker-compose.yml + provision.sh + backup.sh。

## Blocked

- ⚠️ 两台服务器登录仍失败。已试过：howairoot@227 / webserverroot@226 / root@两台 的密钥登录（无公钥被拒）；root + 密码"howairoot"/"webserverroot"（密码错）。shared/ 和本机均无凭证。等用户直接提供 root 密码（拿到后先 ssh-copy-id 装公钥再干活）。

## Next (机器可登录后)

1. 227: 上传 infra/ → 跑 provision.sh → 验证 4 容器 + pgvector + 备份 cron
2. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
3. 后端 API（检索+编排+校验）→ 226 前端

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

