#!/bin/bash
# 每日备份: pg_dump → gzip → OSS (内网 endpoint)。由 provision.sh 装入 cron。
set -euo pipefail
APP_DIR=/opt/howai
set -a; source "$APP_DIR/.env"; set +a

STAMP=$(date +%Y%m%d-%H%M)
FILE=/tmp/howai-pg-$STAMP.sql.gz
docker exec howai-pg pg_dump -U howai howai | gzip > "$FILE"

ossutil64 cp "$FILE" "oss://${OSS_BUCKET}/${OSS_OBJECT_PREFIX}backup/$(basename "$FILE")" \
  -e "$OSS_ENDPOINT" -i "$OSS_ACCESS_KEY_ID" -k "$OSS_ACCESS_KEY_SECRET"
rm -f "$FILE"

# 只保留最近30份
ossutil64 ls "oss://${OSS_BUCKET}/${OSS_OBJECT_PREFIX}backup/" -e "$OSS_ENDPOINT" \
  -i "$OSS_ACCESS_KEY_ID" -k "$OSS_ACCESS_KEY_SECRET" | grep -o "oss://.*\.sql\.gz" | sort | head -n -30 | \
  while read -r obj; do
    ossutil64 rm "$obj" -e "$OSS_ENDPOINT" -i "$OSS_ACCESS_KEY_ID" -k "$OSS_ACCESS_KEY_SECRET" -f
  done
echo "backup ok: $STAMP"
