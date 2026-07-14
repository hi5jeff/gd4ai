import json
import time
import httpx
from . import config


def chat_json(prompt: str, model: str | None = None, max_tokens: int = 3000, retries: int = 1) -> dict:
    """调 mdbox 网关并解析 JSON 输出。deepseek-v4 系列带思维链，max_tokens 必须给足。
    重试带指数退避（504/限流常见），退避 1s,2s,4s...。"""
    model = model or config.MODEL_ONLINE
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    last_err = None
    for attempt in range(retries + 1):
        try:
            resp = httpx.post(
                f"{config.MDBOX_BASE_URL}/v1/chat/completions",
                headers={"Authorization": f"Bearer {config.MDBOX_API_KEY}"},
                json=body,
                timeout=120,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(content)
        except Exception as e:  # 解析失败或网络错误则退避重试
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM 调用失败: {last_err}")
