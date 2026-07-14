#!/bin/bash
# howAI 后端服务器初始化 — 在 howairoot@10.0.0.227 上以 root 权限运行一次。
# 用法: bash provision.sh   (需同目录有 docker-compose.yml)
set -euo pipefail

APP_DIR=/opt/howai
mkdir -p "$APP_DIR"

# 1. Docker
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
  systemctl enable --now docker
fi

# 2. 目录与文件
cp -f "$(dirname "$0")/docker-compose.yml" "$APP_DIR/"
[ -f "$(dirname "$0")/backup.sh" ] && cp -f "$(dirname "$0")/backup.sh" "$APP_DIR/" && chmod +x "$APP_DIR/backup.sh"

# 3. 生成密钥（只生成一次，重跑不覆盖）
if [ ! -f "$APP_DIR/.env" ]; then
  cat > "$APP_DIR/.env" << EOF
PG_PASSWORD=$(openssl rand -hex 24)
MEILI_MASTER_KEY=$(openssl rand -hex 24)
REDIS_PASSWORD=$(openssl rand -hex 24)
EOF
  chmod 600 "$APP_DIR/.env"
  echo "已生成 $APP_DIR/.env"
fi

# 4. 启动
cd "$APP_DIR"
docker compose up -d

# 5. 等 PG 就绪后开启 pgvector 扩展
echo "等待 PostgreSQL 就绪..."
for i in $(seq 1 30); do
  docker exec howai-pg pg_isready -U howai >/dev/null 2>&1 && break
  sleep 2
done
docker exec howai-pg psql -U howai -d howai -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 6. ossutil（备份用）
if ! command -v ossutil64 >/dev/null 2>&1; then
  curl -fsSL -o /usr/local/bin/ossutil64 https://gosspublic.alicdn.com/ossutil/1.7.19/ossutil64 \
    && chmod +x /usr/local/bin/ossutil64 || echo "WARN: ossutil 下载失败，备份前需手动安装"
fi

# 7. 每日备份 cron（凌晨4点，需先在 $APP_DIR/.env 里补充 OSS_* 变量）
( crontab -l 2>/dev/null | grep -v howai-backup ; echo "0 4 * * * $APP_DIR/backup.sh >> /var/log/howai-backup.log 2>&1 # howai-backup" ) | crontab -

echo
echo "=== 完成。服务状态: ==="
docker compose ps
echo
echo "提醒: 把 OSS_ACCESS_KEY_ID / OSS_ACCESS_KEY_SECRET / OSS_ENDPOINT / OSS_BUCKET / OSS_OBJECT_PREFIX 追加到 $APP_DIR/.env 以启用备份。"
