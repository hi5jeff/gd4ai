# MEMORY.md — Long-Term Memory
> Project: howAI

## 项目定位
需求驱动的泛 AI 工具生态推荐系统（skill/roles/plugin/MCP/prompt 模板），从小白到专家。核心原则：**闭世界推荐——LLM 只能引用库内组件，输出前校验，查空宁说没有**。完整设计见 DESIGN.md。

## 基础设施（2026-07-14 定型）
- **GitHub**: `git@github.com:hi5jeff/gd4ai.git`（remote origin，分支 main，SSH 可推）。产品域名 gd4.ai 与仓库名对应。推送前已验证 git 历史无密码/密钥。
- **服务器**（内网，账号 root，密码在项目 .env；本机公钥已装，直接 `ssh root@IP`）：
  - 前端: `root@10.0.0.226`（Alinux4, 4C7G/197G，Docker 24 已装；装 Docker 要 `dnf install docker`，get.docker.com 不支持 alinux）
  - 后端+数据: `root@10.0.0.227`（Ubuntu22.04, 4C7G/99G）— **已部署** `/opt/howai/`：howai-pg(PG16+pgvector, 127.0.0.1:5432) / howai-meili(:7700) / howai-redis(:6379) / howai-embedding(BGE-M3 TEI, :8090)，服务密码在服务器 `/opt/howai/.env`
  - 备份：每日 4 点 cron `pg_dump→OSS`（实测通过）；ossutil 用官方 install.sh 装（老版本 URL 已 404）
  - 坑：TEI embedding 默认 max-batch-tokens=16384 在 7G 内存机器预热 OOM → compose 里已加 `--max-batch-tokens 1024 --auto-truncate`
- **域名/HTTPS**: `https://gd4.ai` 已上线（Cloudflare → 226 nginx1.30）。Origin 证书在 226 `/etc/nginx/ssl/`（源头在项目 .env 尾部，有效期到 2041）。nginx 配置 `/etc/nginx/conf.d/gd4.ai.conf`（仓库 infra/nginx-gd4.ai.conf）：80→301，静态根 `/var/www/gd4ai`（占位页在仓库 web/），`/api/` 反代 `10.0.0.227:9000`（**后端 API 端口约定 9000**，上线前 /api 会 502）
- **部署纪律**: 前端/服务一律部署到服务器（226/227），不在本地开发机起服务
- **LLM**: mdbox 网关 `https://api.mdbox.ai/v1`（OpenAI 兼容，key 在 env `MDBOX_API_KEY`）
  - 在线推荐: `deepseek-v4-pro`（实测 8s、JSON 可靠、选择质量最好）
  - 离线加工: `deepseek-v4-flash`
  - 淘汰: glm-4.7（截断+慢）、qwen3.7-plus（冗长+30s）
  - 注意: deepseek-v4 系列带 reasoning_content，max_tokens 要给足（≥2000），否则 JSON 被思维链挤掉
- **Embedding**: 本地 BGE-M3（TEI CPU 容器, 127.0.0.1:8090）— mdbox 无合适文本 embedding
- **OSS**: bucket `hi5`, 前缀 `howai/`, 首尔内网 endpoint；凭证在项目根 `.env`（已 gitignore，勿提交）
- **本项目端口段**: 8070-8074（本机 dev 用，尚未分配服务）

## 数据集：两层粒度（关键架构）
- **粗粒度 components 表**（几千条）：工具/skill/role/mcp/"提示词来源" → 回答"推荐个提示词库"
- **细粒度 prompts 表**（可千万级，HNSW索引）：一条条具体提示词内容 → 回答"香水广告提示词"。字段: source_id/ext_id/title_zh/summary_zh/content/scene_tags/style_tags/quality/embedding。UNIQUE(source_id,ext_id) 去重
- 检索: orchestrate 同时查 components(hybrid) + prompts(search_prompts 向量, score≥0.6 才算强命中)。只命中prompts→intent=prompts直接返回具体提示词; 命中组件→正常编排+附带prompts
- **提示词导入管线** `server/app/import_prompts.py`: 源JSON → 批量过LLM(BATCH=8, deepseek-v4-flash 打质量分+中文标题+场景标签, 垃圾丢弃) → BGE-M3向量化 → prompts表。用法: `docker exec howai-api python -m app.import_prompts <source_id> <json> [--limit N] [--min-quality 0.55]`
- **采集入口路由(待建)**: 新仓库进来先LLM判断 类型(mcp/skill/role/prompt...) + 结构(A单体1条/B合集展开N条/C内容库进prompts表), 按判断路由。用户提交URL复用同一套(LLM审核)

## 踩坑：服务器后台长任务
- `ssh + docker exec ... &` / `docker exec -d` / 容器内 nohup 都不可靠(ssh管道关闭即被杀)。**用 `systemd-run --unit=X --collect docker exec ...`** 彻底脱离会话。查状态 `systemctl is-active X` / `journalctl -u X`

## 首批提示词源
- YouMind-OpenLab/ai-image-prompts-skill: 14779条12类, product-marketing.json(5408条)已导入。对应粗粒度组件 tool-youmind-image-prompts

## MVP 已上线（2026-07-14）
- **https://gd4.ai 全链路可用**：前端(web/index.html→226 /var/www/gd4ai) → nginx /api 反代 → 227:9000 howai-api 容器
- **代码结构**：`data/`（36 组件+6 方案包 YAML+2 个 JSON Schema）、`server/`（FastAPI：config/db/llm/retrieval/ingest/orchestrate/main）、`scripts/`（validate_data.py + enrich_github.py）
- **部署流程**：改代码/数据 → tar 同步到 227:/opt/howai/api/（服务器无 rsync）→ `docker compose build api && up -d api` → 数据变更再跑 `docker exec howai-api python -m app.ingest`；前端 scp index.html 到 226
- **推荐链路**：hybrid(Meili+pgvector RRF) Top14组件+Top3方案包 → v4-pro 闭世界选择(max_tokens 3000) → id 校验剔除库外 → 字段拼装卡片；Redis 缓存24h；查空/不相关→gap_log 表；LLM 挂→降级纯检索
- **验收**：六类用例全过（电商/美女图/省token/游戏动画/平面设计/室内装修），库外问题（修发动机）正确走 no_result 兜底
- **运营表**：gap_log（缺口=下一步采集方向）、query_log（全部提问）在 227 的 PG 里
- ⚠️ SERVERS.md 含明文密码，已 gitignore（连同 .env），永不入库
