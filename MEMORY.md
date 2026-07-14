# MEMORY.md — Long-Term Memory
> Project: howAI

## 项目定位
需求驱动的泛 AI 工具生态推荐系统（skill/roles/plugin/MCP/prompt 模板），从小白到专家。核心原则：**闭世界推荐——LLM 只能引用库内组件，输出前校验，查空宁说没有**。完整设计见 DESIGN.md。

## 基础设施（2026-07-14 定型）
- **服务器**（内网，账号 root，密码在项目 .env；本机公钥已装，直接 `ssh root@IP`）：
  - 前端: `root@10.0.0.226`（Alinux4, 4C7G/197G，Docker 24 已装；装 Docker 要 `dnf install docker`，get.docker.com 不支持 alinux）
  - 后端+数据: `root@10.0.0.227`（Ubuntu22.04, 4C7G/99G）— **已部署** `/opt/howai/`：howai-pg(PG16+pgvector, 127.0.0.1:5432) / howai-meili(:7700) / howai-redis(:6379) / howai-embedding(BGE-M3 TEI, :8090)，服务密码在服务器 `/opt/howai/.env`
  - 备份：每日 4 点 cron `pg_dump→OSS`（实测通过）；ossutil 用官方 install.sh 装（老版本 URL 已 404）
- **LLM**: mdbox 网关 `https://api.mdbox.ai/v1`（OpenAI 兼容，key 在 env `MDBOX_API_KEY`）
  - 在线推荐: `deepseek-v4-pro`（实测 8s、JSON 可靠、选择质量最好）
  - 离线加工: `deepseek-v4-flash`
  - 淘汰: glm-4.7（截断+慢）、qwen3.7-plus（冗长+30s）
  - 注意: deepseek-v4 系列带 reasoning_content，max_tokens 要给足（≥2000），否则 JSON 被思维链挤掉
- **Embedding**: 本地 BGE-M3（TEI CPU 容器, 127.0.0.1:8090）— mdbox 无合适文本 embedding
- **OSS**: bucket `hi5`, 前缀 `howai/`, 首尔内网 endpoint；凭证在项目根 `.env`（已 gitignore，勿提交）
- **本项目端口段**: 8070-8074（本机 dev 用，尚未分配服务）

## 数据集三层
组件库（YAML in git → PG）、方案库 playbook、用法语料。命令/配置从字段拼装，LLM 不现写。
