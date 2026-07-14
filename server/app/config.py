import os

PG_DSN = (
    f"host={os.getenv('PG_HOST', 'postgres')} port=5432 dbname=howai user=howai "
    f"password={os.getenv('PG_PASSWORD', '')}"
)
MEILI_URL = os.getenv("MEILI_URL", "http://meilisearch:7700")
MEILI_KEY = os.getenv("MEILI_MASTER_KEY", "")
REDIS_URL = f"redis://:{os.getenv('REDIS_PASSWORD', '')}@{os.getenv('REDIS_HOST', 'redis')}:6379/0"
EMBED_URL = os.getenv("EMBED_URL", "http://embedding:80")

MDBOX_BASE_URL = os.getenv("MDBOX_BASE_URL", "https://api.mdbox.ai")
MDBOX_API_KEY = os.getenv("MDBOX_API_KEY", "")
MODEL_ONLINE = os.getenv("MODEL_ONLINE", "deepseek-v4-pro")   # 在线推荐
MODEL_BATCH = os.getenv("MODEL_BATCH", "deepseek-v4-flash")   # 离线加工

DATA_DIR = os.getenv("DATA_DIR", "/app/data")
CACHE_TTL = int(os.getenv("CACHE_TTL", "86400"))  # 推荐结果缓存 24h
