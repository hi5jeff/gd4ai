import json
import time
import httpx
from . import config


def extract_json(text: str):
    """从 LLM 输出里稳健提取 JSON：去 ```围栏、截取首个 {/[ 到配对的 }/]，容忍尾部多余文字。"""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1].rsplit("```", 1)[0].strip() if "\n" in t else t.strip("`")
    # 直接解析
    try:
        return json.loads(t)
    except Exception:
        pass
    # 找第一个 { 或 [，做括号配对截取（忽略字符串内的括号）
    start = min((i for i in (t.find("{"), t.find("[")) if i >= 0), default=-1)
    if start < 0:
        raise ValueError("无 JSON")
    open_ch = t[start]
    close_ch = "}" if open_ch == "{" else "]"
    depth, in_str, esc = 0, False, False
    for i in range(start, len(t)):
        c = t[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == open_ch:
                depth += 1
            elif c == close_ch:
                depth -= 1
                if depth == 0:
                    return json.loads(t[start:i + 1])
    raise ValueError("JSON 括号不配对")


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
            return extract_json(content)
        except Exception as e:  # 解析失败或网络错误则退避重试
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"LLM 调用失败: {last_err}")
