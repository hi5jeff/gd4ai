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

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T11:26:00+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## Next

1. 验证 embedding 服务就绪
2. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
3. 后端 API（检索+编排+校验）→ 226 前端

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T11:32:29+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验）→ 226 前端

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T11:35:13+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T11:44:04+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T12:33:56+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T12:40:05+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T13:00:04+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T13:26:04+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T13:28:16+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T13:34:18+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T13:51:48+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T14:00:40+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T14:04:42+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T14:12:27+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T14:17:27+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T14:50:06+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T14:53:49+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T15:58:36+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T19:30:56+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T19:45:41+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T19:50:22+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T19:57:02+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-14T21:08:26+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T04:42:12+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T05:24:31+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T05:26:38+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T06:24:33+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T13:31:27+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T17:44:50+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T17:57:43+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-15T20:59:04+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T03:23:59+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T14:03:46+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T14:07:11+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T14:24:37+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T14:28:58+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

---

## Session c73d9b70-21b0-4326-b372-762e36940289 — 2026-07-16T14:29:35+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T14:38:54+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T14:44:50+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T15:23:48+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T16:11:47+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

---

## Session ece59992-dea3-47f1-adbf-88cb6c8fc490 — 2026-07-16T17:13:58+08:00

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

## 部署进展（第七轮，2026-07-14）

- ✅ 凭证到手（.env: root@两台, 密码见 .env），两台已装我的公钥，密钥登录 OK
- ✅ 227 (Ubuntu22.04 4C7G): provision 完成 — howai-pg(healthy)/howai-meili/howai-redis/howai-embedding 四容器运行，pgvector 已启用，密钥在 /opt/howai/.env
- ✅ 备份链路实测通过（pg_dump→OSS 内网），cron 每日 4 点；ossutil 用 install.sh 装（原 1.7.19 URL 404 已修）
- ✅ 226 (Alinux4 4C7G): Docker 24.0.9 已装（注意: get.docker.com 不支持 alinux，用 dnf install docker）
- ✅ BGE-M3 就绪（127.0.0.1:8090/embed, 1024维）。坑：TEI 默认 max-batch-tokens=16384 在 4C7G 上预热 OOM（申请8.5G），已加 --max-batch-tokens 1024 --auto-truncate
- ✅ 内存余量健康（used 2.5G / 7.1G）
- 用户在 .env 追加了 Cloudflare Origin 证书（gd4.ai / *.gd4.ai）→ 前端 HTTPS 用
- 建议用户改密码/关密码登录（密码已在 .env 明文）

## 第八轮：GitHub 仓库接入

- ✅ origin = git@github.com:hi5jeff/gd4ai.git，分支已改 main 并推送（推前扫描 git 全历史确认无密码/OSS密钥/证书泄漏）

## 第九轮：gd4.ai 前端上线

- ✅ 226 装 nginx 1.30，Cloudflare Origin 证书部署（验证过证书私钥匹配、SAN、2041 到期）
- ✅ https://gd4.ai 公网 200（Cloudflare→226），80→301；占位落地页在仓库 web/index.html
- ✅ /api/ 已预配反代到 227:9000（后端 API 端口约定 9000；上线前 502 正常）
- 用户要求：服务一律部署服务器，不在本地起（已记入 MEMORY）

## Next

1. 定稿组件 YAML schema + 种子数据 30~50 条（覆盖六类验收用例）
2. 后端 API（检索+编排+校验，部署 227:9000）→ 前端页面迭代（部署 226）

## Open questions

- MVP 形态（搜索引擎 vs 对话推荐 vs 两者结合）待用户确认后再进入工程实现。

## 第十轮：MVP 开发（进行中）
- ✅ LLM 复测通过（flash 7s抽取JSON合法 / pro 13.7s，pro需max_tokens≥2000）
- ✅ data/schema 两个 JSON Schema 定稿
- ✅ 种子数据 36 组件+6 方案包，全部校验通过，GitHub stars 已补全（26个真实仓库）
- ✅ server/ 后端完成：FastAPI + 混合检索(Meili+pgvector RRF) + 闭世界编排(orchestrate.py) + 查空兜底/缺口日志/Redis缓存/LLM降级
- ⏳ 待办：compose加api服务→部署227→ingest→测试→前端→E2E→提交
- ✅ 部署完成: api容器构建成功, ingest 36+6, /api/health 全绿
- ✅ 六类验收+库外兜底全部通过(gap_log/query_log正常记录)
- ✅ 前端正式版上226, https://gd4.ai 公网E2E通过(缓存命中秒回, 新问题20s)
- ✅ SERVERS.md(含明文密码)已gitignore
- 第十轮完成, 待提交

## 第十一轮:深度collection摄取 + awesome-llm-apps导入(进行中)
- 修复ingest_repo.py两bug:norm_ws未定义(致_make_subunit全抛异常"展开0条")、_find_app_dirs递归深度2→4且去掉depth=0乱append
- 深度collection能力:递归找叶子app目录→读各自README→LLM生成描述→逐条入库(以后monorepo通用)
- dry-run验证:awesome-llm-apps质量高(AI金融/法律/房产/招聘/SEO agent团队等)
- 正式导入:detached容器 howai-import-llmapps(daemon托管,不依赖ssh),全76个app目录
- 待:导完查总数→提交

## 第十二轮:用户提交URL + 管理后台(完成)
- submissions表(db.py)+ add/list/update/get/stats helper
- POST /api/submit(公开)· GET /api/admin/submissions · POST /api/admin/submissions/{id}/action(ingest/reject),X-Admin-Token鉴权
- ingest.persist_docs():内存docs直接落PG+Meili+向量(绕过YAML,因api容器/app/data是:ro)
- _do_ingest用dry_run=True(跳过写只读YAML)+persist_docs真入库
- 前端:index.html加"+推荐资源"弹窗→/api/submit;新建admin.html(口令登录/统计/筛选/导入·拒绝按钮)
- ADMIN_TOKEN=2d828b9bb005c26f62070cb7 存227:/opt/howai/.env(gitignored)
- 端到端验证:submit→admin导入dagger/container-use→组件941→942,公网/api代理OK
- awesome-llm-apps导入仍在howai-import-llmapps容器后台跑

## 第十三轮:去重+异步+落库修复(完成)
- 根因: 去重只读YAML种子/独立CLI没开池/YAML当真相. 统一改为"以DB为准"
- load_state叠加DB组件URL+id去重; ingest_repo --persist手动db.pool.open()
- 导入前先判重(component_url_exists),URL已在库秒回跳过不跑LLM
- awesome-llm-apps深度collection真落库179条 → 组件总数1148
- ponytail#4是已在库(误报已修), 同名多条是不同来源URL(非重复)
- 教训: 别挂长Monitor(会话断则死), 直接查状态
- 队列: #4 ponytail已处理(dup跳过), #5-9 五条真实用户提交待审

## 分工(用户2026-07-16定,重要)
- 主session(我): 实时响应/开发/决策/指挥, 绝不挂长Monitor
- monitor分身 = c73d9b70: 监控类长任务派给它
  - 派: clone run c73d9b70 "盯住X完成报结果" → job id
  - 收: clone result <job> (异步查,不--wait)

