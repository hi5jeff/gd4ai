# howAI 系统设计分析

> 目标：根据用户需求，智能推荐 AI 编程生态内容（skill / roles / plugin / MCP / prompt 模板 / 辅助工具），并告诉用户**怎么组合、怎么用**。覆盖从小白到专家的全部用户。
> 日期：2026-07-14

## 1. 问题的本质

用户的痛点不是"找不到东西"，而是四个递进的问题：

1. **发现（Discovery）** — 不知道存在什么。GitHub 每天更新，awesome 列表几百个。
2. **匹配（Matching）** — 不知道自己的任务需要什么。"我要做网站" ≠ 会搜 "mcp server playwright"。
3. **组合（Composition）** — 不知道怎么配合使用。skill + role + MCP + prompt 是一套流程，不是单件商品。
4. **信任（Trust）** — 不知道哪个能用、是否维护、是否安全（恶意 MCP server 是真实风险）。

现有竞品（smithery.ai、mcp.so、PulseMCP、glama、claudeskills.info、ccmarket.dev、aitmpl 等）全部停在第 1 层——目录 + 关键词搜索，按类型割裂（只做 MCP 或只做 skill）。**第 2、3、4 层是空白，也是 howAI 的差异化。**

## 2. 技术路线决策：搜索引擎 vs 自建 LLM

| 路线 | 结论 | 原因 |
|---|---|---|
| 自训 LLM | ❌ 不做 | 成本高；生态每天变，模型练完即过时；没有数据优势时无护城河 |
| 纯搜索引擎 | ❌ 不够 | 用户表达的是"需求"，不是组件关键词；且无法做组合推荐 |
| **结构化数据集 + 混合检索 + 现成 LLM 编排（RAG）** | ✅ 采用 | 数据天天更新只需重建索引；LLM 负责意图理解、任务拆解、方案组合、解释说明 |

唯一值得"自有模型"的地方：后期用点击/采纳/跑通数据微调 **embedding / rerank 小模型**，提升检索排序——这是数据飞轮的产物，不是起点。

**护城河 = 数据集的结构化质量 + 方案库 + 真实"跑通率"反馈数据**，不是模型。

## 3. 系统架构（五层）

```
┌─────────────────────────────────────────────────┐
│ ⑤ 应用层    小白向导 / 搜索+筛选 / 专家API+CLI      │
├─────────────────────────────────────────────────┤
│ ④ 推荐编排层  意图理解→任务拆解→检索→重排→组装方案包  │
├─────────────────────────────────────────────────┤
│ ③ 索引层    BM25关键词 + 向量 + facet 过滤（混合检索）│
├─────────────────────────────────────────────────┤
│ ② 加工层    LLM抽取统一schema / 去重 / 打分 / 安全扫描│
├─────────────────────────────────────────────────┤
│ ① 采集层    GitHub / 官方registry / 各marketplace / 博客│
└─────────────────────────────────────────────────┘
                    ↑ 反馈闭环：采纳率、跑通率、评分 ↑
```

### ① 采集层
- 数据源：GitHub topic/awesome 列表、registry.modelcontextprotocol.io（官方）、smithery/mcp.so/PulseMCP、Claude plugin marketplace、prompt 网站、技术博客。
- 方式：定时增量爬取（GitHub API + cron），记录 `last_seen / last_commit`。
- 关键点：**竞品目录本身也是我们的数据源**——做聚合层而不是重复造目录。

### ② 加工层（核心价值所在）
- **LLM 抽取**：把 README/文档转成统一 schema（见 §4）。
- **去重**：同一个 MCP server 在 5 个目录都有——按 repo URL / 包名归一。
- **质量打分**：stars、最近提交、issue 响应、文档完整度、下载量 → maintenance_score。
- **安全扫描**：MCP server 要求什么权限、是否要 token、有无已报告漏洞 → security_notes。这既是必需品也是卖点。
- **难度标注**：是否零配置可用（小白友好）vs 需要申请 API key / 自部署（进阶）。

### ③ 索引层
- 混合检索：Meilisearch/Elasticsearch（关键词）+ pgvector/Qdrant（语义向量）。
- Facet 维度：宿主工具（Claude Code / Codex / Kimi / OpenClaw…）、类型、场景、难度、是否免配置、语言。

### ④ 推荐编排层（LLM pipeline）
```
用户需求（自然语言，可能很模糊）
  → 意图理解（模糊则追问 2-3 个问题：预算？技术背景？部署到哪？）
  → 任务拆解（"做电商网站" → 前端生成/数据库/支付/部署/SEO）
  → 每个子任务混合检索候选组件
  → 重排（质量分 × 难度匹配 × 兼容性）
  → 组装成「方案包」：组件清单 + 安装命令 + 配置步骤 + 使用流程 + 配合说明
```

### ⑤ 应用层（按用户分层，同一数据不同界面）
| 用户 | 形态 |
|---|---|
| 小白 | 对话式向导 + 场景卡片首页（做网站/做小程序/数据分析/自动化办公）→ 一键方案，甚至生成可直接执行的安装脚本 |
| 中级 | 搜索 + facet 筛选 + 组件对比 + 方案库浏览 |
| 专家 | API / CLI、高级过滤、原始数据导出、"本周新增" changelog 订阅 |

**分发妙招**：把 howAI 自己做成一个 skill/MCP server——用户在 Claude Code 里直接问"我要做爬虫需要装什么"，agent 调 howAI 的 API 拿方案。工具生态的推荐器就该活在工具里。

## 4. 数据集设计（三层）

### 4.1 组件库（原子层）— 统一 schema
```yaml
id: mcp-playwright
type: skill | role | plugin | mcp | prompt | workflow | tool
name: Playwright MCP
description_zh / description_en: 浏览器自动化…
host_tools: [claude-code, codex, cursor]          # 兼容哪些宿主
categories: [browser-automation]
scenarios: [web-testing, scraping, web-dev]        # 场景标签（推荐的关键）
install: {method: npx, command: "claude mcp add ..."}
config_required: [无 | API_KEY | 自部署]
difficulty: beginner | intermediate | advanced
quality:
  stars: 12000
  last_commit: 2026-07-01
  maintenance_score: 0.92
  verified: true            # 我们沙箱实测跑通过
  security_notes: 需要浏览器权限，无网络外发
relations:
  works_with: [skill-web-design]    # 组合关系
  alternatives: [mcp-puppeteer]
  requires: [node>=18]
source: {repo, registry_urls: [...]}
docs_chunks: [...]           # 供 RAG 引用的文档切片
```

### 4.2 方案库（组合层，Playbook）— 最大差异化
```yaml
id: playbook-ecommerce-site
title: 用 Claude Code 从零做一个电商网站
scenario: web-dev
audience: beginner
host_tool: claude-code
components:
  - {ref: skill-frontend-design, 作用: 页面生成}
  - {ref: mcp-postgres, 作用: 数据库}
  - {ref: role-fullstack-architect, 作用: 架构评审}
  - {ref: prompt-seo-audit, 作用: 上线前检查}
steps: [装什么 → 配什么 → 先跑哪个 prompt → 常见坑]
verified_at: 2026-07-10      # 实测跑通日期
success_rate: 0.87            # 用户反馈跑通率
```
来源：人工策展起步 → LLM 生成 + 沙箱验证 → 用户投稿 + 跑通反馈。

### 4.3 用法语料（知识层）
从官方文档、博客、GitHub issues 提取的 how-to / 踩坑 QA 片段，供 RAG 回答"怎么配合使用"这类问题。

### 数据质量的杀手锏：沙箱实测
定期在容器里真实安装、真实调用每个组件，标记 `verified`。所有竞品都只列 stars，没人告诉用户"这个昨天还能跑通"。这一条就能建立信任。

## 5. MVP 路径（避免一上来铺全生态）

**第一阶段（4-6 周）**：
- 只做 1 个宿主工具（Claude Code）× 3 个场景（做网站、数据分析、内容创作）。
- 人工策展 ~200 个组件 + 20 个实测跑通的 playbook。
- 产品形态：一个网页 = 对话推荐框 + 场景卡片 + 简单搜索。
- 验证指标：用户从提问到"环境跑通"的成功率与耗时。

**第二阶段**：自动化采集加工 pipeline，扩到 MCP 全量 + 多宿主工具，上线 facet 搜索和 API。

**第三阶段**：反馈闭环（跑通率数据）、howAI 自身的 skill/CLI 分发、订阅制"本周生态周报"。

## 6. 风险与对策

| 风险 | 对策 |
|---|---|
| 生态规范频繁变化（skill 格式、MCP spec 修订） | 每个宿主工具一个 adapter，schema 加版本字段 |
| 恶意/失效组件损害信任 | 安全扫描 + 沙箱实测 + verified 标记，宁缺毋滥 |
| 目录类竞品多且免费 | 不拼收录量，拼"需求→跑通方案"的端到端体验 + 中文市场 |
| LLM 推荐幻觉（推荐不存在的组件） | 推荐只能从数据集检索结果里选，LLM 只做组合和解释，不凭空生成 |
| 数据加工成本 | 增量处理 + 只对高质量候选（stars/活跃度门槛）做 LLM 深加工 |

## 7. 技术选型决策（2026-07-14 讨论确认）

### 7.1 数据集存储
- **策展层**：组件/方案 = YAML 文件，放 git 仓库（可版本、可 PR 投稿、审核即 code review）。
- **服务层**：PostgreSQL 唯一真相源（实体表 + 关系表 + JSONB），构建脚本从 git 编译入库。
- **索引**：pgvector（向量）+ Meilisearch 或 PG 全文检索（关键词/facet）。全开源零费用，单机可跑。
- 原始爬取物（README/文档）存文件/对象存储，不入库。

### 7.2 输出形态（区别于谷歌式结果）
推荐单位 = 可执行方案包，每条必带：干什么用 / 怎么装（install.command）/ 怎么配（配置片段）/ 第一条 prompt + 验证方法。
**命令与配置从数据库字段拼装，LLM 不现写命令** → 杜绝幻觉命令。终极形态：一键脚本 / 一键导入配置。

### 7.3 LLM 选型
- 离线加工（抽取/打标/翻译）：开源模型胜任，量大价低。
- Embedding：开源 BGE-M3 / Qwen-embedding，零成本。
- 在线推荐对话：需 DeepSeek-V3 级开源大模型；自建 7B~14B 不够稳。
- **决策：MVP 用便宜国产 API（一次推荐 <5 分钱），不自购 GPU**；规模化后再把离线加工迁自建小模型。
- 架构故意把智力要求做低：检索靠数据库、命令靠拼装，LLM 只做理解/挑选/解释 → 中档模型即够。

### 7.4 数据规模与 LLM 的关系
LLM 不接触全量数据。流程：需求 → LLM 拆子任务 → 数据库混合检索 → 每子任务 Top 20~50 候选（几千 token）→ LLM 挑选组合 → 模板拼装。10 万组件对检索层是毫秒级小数据。数据越多候选越好，不构成 LLM 负担。

### 7.5 部署选型：阿里云托管服务（2026-07-14 确认，云资源可随意使用）

原则：**架构不变，自维护组件换托管版**。

| 组件 | 阿里云方案 |
|---|---|
| 主存储 | RDS PostgreSQL（开 pgvector 扩展）— 唯一真相源 |
| 关键词搜索 | MVP：ECS 自跑 Meilisearch；量大后迁托管 Elasticsearch |
| 原始爬取物 | OSS 对象存储 |
| LLM / Embedding | 百炼平台：qwen-plus（在线推荐）、qwen-turbo（离线批量加工）、text-embedding-v4（向量）→ 推理成本归零，替代原 DeepSeek API 方案 |
| 缓存/队列 | Redis(Tair)：推荐结果缓存（省 ~90% 重复 LLM 调用）、限流、爬虫任务队列。仅缓存定位，不替代 PG 主存储 |
| 沙箱实测 / 爬虫 | 一台 ECS 跑 Docker + cron |

MVP 最小集合：RDS PG + OSS + 1×ECS + 百炼 API（+ Redis 可选）。不上 ACK/消息队列/数仓，有流量再说。

**修订（2026-07-14）：初期成本优先，单台 ECS 全包**。RDS/托管搜索单独购买偏贵，MVP 改为一台专用 ECS（建议 4C8G/100G ESSD，Ubuntu 22.04）用 Docker Compose 跑全套：PostgreSQL16+pgvector、Meilisearch、Redis、应用、沙箱实测。可行性依据：真相源是 git 里的 YAML，库可重建；需备份的只有用户反馈/缺口日志，每日 pg_dump → OSS。安全：PG/Meili/Redis 只绑内网，公网仅开应用端口+SSH。流量起来后 pg_dump 迁 RDS，架构不变。

### 7.6 推荐约束机制：库是唯一依据（2026-07-14 确认，核心需求）

用户问题极多样（例：美女图提示词 / 省token的skill / 游戏动画工具 / 平面设计 / 室内装修 / 做电商网站）。原则：**LLM 不用自身认知作答，只能基于库**。落地为四条硬约束：

1. **闭世界推荐**：LLM 的候选只来自检索返回的组件 id 列表；输出前有校验层，逐条核对推荐的 id / 命令 / 链接确实存在于库中，对不上就剔除。LLM 的角色 = 从候选里挑 + 解释怎么配合，永远不产生库外内容。
2. **查空兜底**：检索无合格结果（相关性低于阈值）时，明确回答"库里暂无验证过的方案"，可附最接近的替代项并标注"非精确匹配"。宁可说没有，不许编。
3. **缺口日志（unmet demand log）**：每次查空/低分命中都记录原始 query → 聚类后成为采集和策展的优先级队列。用户的问题驱动库的扩张，这是最值钱的运营数据。
4. **意图先分型再检索**：
   - 单件型（"美女图提示词"、"省token的skill"）→ 直接检索对应 type，返回 Top 几个组件卡片；
   - 方案型（"做电商网站"、"室内装修"）→ 拆子任务 → 组装 playbook；
   - 分型由 LLM 判断，但两条路的产出都只从库里取。

**范围推论**：平面设计/室内装修说明用户需求不限于编程——库的场景体系要覆盖"泛 AI 工具生态"（图像生成、设计、行业垂直场景），场景分类 = 预设场景树（自顶向下）+ 真实 query 聚类（自底向上）持续扩充。

### 7.7 LLM 与部署拓扑定型（2026-07-14，实测后确认）

**LLM 走 mdbox 网关**（OpenAI 兼容，`https://api.mdbox.ai/v1`，key 在环境变量 `MDBOX_API_KEY`）。四个候选用真实任务实测（意图分型 + 闭世界选择 + 严格 JSON 输出）：

| 模型 | 延迟 | 结果 | 结论 |
|---|---|---|---|
| deepseek-v4-pro | 8.0s | JSON 正确，选择最完整（含 SEO 检查） | ✅ 在线推荐主力 |
| deepseek-v4-flash | 8.4s | JSON 正确，选择合格，输出最省 | ✅ 离线批量加工 |
| glm-4.7 | 23.7s | 输出被截断，JSON 解析失败 | ❌ |
| qwen/qwen3.7-plus | 30.2s | 正确但输出冗长（1150 tokens） | ❌ 太慢 |

**Embedding**：mdbox 无合适文本 embedding（仅 doubao-vision/nv-embed-v1）→ 后端服务器本地跑 **BGE-M3**（TEI CPU 容器，中英双语，免费）。

**部署拓扑（两台内网服务器）**：
- `webserverroot@10.0.0.226` — 前端（网页）
- `howairoot@10.0.0.227` — 后端 API + PG16/pgvector + Meilisearch + Redis + BGE-M3 + 爬虫/沙箱，数据服务只绑 127.0.0.1
- OSS：bucket `hi5`、前缀 `howai/`、首尔内网 endpoint（凭证在项目 .env，已 gitignore），每日 pg_dump 备份保留 30 份
- 部署产物：`infra/docker-compose.yml`、`infra/provision.sh`、`infra/backup.sh`

## 8. 一句话总结

**不做模型，做数据；不做目录，做方案。** 用结构化数据集 + RAG 编排回答"我要做 X，该装什么、怎么配、怎么用"，用沙箱实测和跑通率数据建立目录站给不了的信任。
