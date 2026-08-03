"""导入 build-your-own-x 中 AI 相关的教程条目（kind=knowledge）。

来源: https://github.com/codecrafters-io/build-your-own-x
仅挑 AI Model / Neural Network / Visual Recognition System 三个分区中质量高、现代、
与 AI 工具生态相关的条目。作为「知识库」(kind=knowledge) 入库，让推荐引擎在
回答「怎么从头学 LLM/RAG/CNN」类问题时能给到。

用法（容器内）:
    python -m app.ingest_byox_ai --persist
    python -m app.ingest_byox_ai --dry-run
"""
import argparse
import json
import urllib.request

from . import ingest, ingest_repo as ir

# 精选：AI Model（3） + Neural Network（8） + Visual Recognition（2） = 13 条
ENTRIES = [
    # === AI Model (核心) ===
    {"name": "LLMs from Scratch", "lang": "Python", "scen": ["llm-training"],
     "title": "A Large Language Model (LLM)",
     "url": "https://github.com/rasbt/LLMs-from-scratch",
     "gh_readme": "rasbt/LLMs-from-scratch"},
    {"name": "Diffusion Models Course", "lang": "Python", "scen": ["image-gen", "llm-training"],
     "title": "Diffusion Models for Image Generation",
     "url": "https://huggingface.co/learn/diffusion-course/en/unit1/3",
     "desc": "Hugging Face 官方扩散模型课程，从零讲清扩散模型原理与图像生成实现。适合想理解 Stable Diffusion 等图像生成模型底层原理的开发者。"},
    {"name": "RAG from Scratch", "lang": "Python", "scen": ["rag"],
     "title": "RAG for Document Search",
     "url": "https://github.com/langchain-ai/rag-from-scratch",
     "gh_readme": "langchain-ai/rag-from-scratch"},

    # === Neural Network (基础但实用) ===
    {"name": "Build Deep Learning From Scratch", "lang": "Python", "scen": ["llm-training"],
     "title": "Reimplement PyTorch Internals across 34 stages",
     "url": "https://github.com/roiamiel1/Build-Deep-Learning-From-Scratch",
     "gh_readme": "roiamiel1/Build-Deep-Learning-From-Scratch"},
    {"name": "SlowTorch", "lang": "Python", "scen": ["llm-training"],
     "title": "PyTorch from the ground up in pure Python",
     "url": "https://github.com/xames3/slowtorch",
     "gh_readme": "xames3/slowtorch"},
    {"name": "Neural Networks: Zero to Hero", "lang": "Python/Video", "scen": ["llm-training", "coding"],
     "title": "Andrej Karpathy 的从零到英雄神经网络课程",
     "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ",
     "desc": "Andrej Karpathy 出品的神经网络从零教学视频系列，涵盖反向传播、Transformer、GPT 等核心主题。AI 入门最佳视频资源之一。"},
    {"name": "A Neural Network in 11 Lines of Python", "lang": "Python", "scen": ["coding"],
     "title": "用 11 行 Python 实现一个神经网络",
     "url": "https://iamtrask.github.io/2015/07/12/basic-python-network/",
     "desc": "经典极简教程，用 11 行 Python 代码讲清神经网络前向传播与梯度下降的核心逻辑。适合零基础入门。"},
    {"name": "Intro to Neural Networks", "lang": "Python", "scen": ["coding"],
     "title": "Implement a Neural Network from Scratch",
     "url": "https://victorzhou.com/blog/intro-to-neural-networks/",
     "desc": "从零手写实现神经网络，配详细图解和 Python 代码，覆盖前向传播、反向传播、梯度下降。"},
    {"name": "Intro to Convolutional Neural Networks", "lang": "Python", "scen": ["cv"],
     "title": "An Introduction to CNNs",
     "url": "https://victorzhou.com/blog/intro-to-cnns-part-1/",
     "desc": "卷积神经网络入门教程，讲清卷积层、池化层、CNN 架构设计。适合想理解图像识别底层的学习者。"},
    {"name": "OCR from Scratch", "lang": "Python", "scen": ["cv"],
     "title": "Optical Character Recognition (OCR)",
     "url": "http://aosabook.org/en/500L/optical-character-recognition-ocr.html",
     "desc": "The Architecture of Open Source Applications 收录的 OCR 教程，从原理到实现一个能识别手写字符的系统。"},
    {"name": "Generate Music with LSTM", "lang": "Python/Keras", "scen": ["coding"],
     "title": "用 LSTM 神经网络生成音乐",
     "url": "https://towardsdatascience.com/how-to-generate-music-using-a-lstm-neural-network-in-keras-68786834d4c5",
     "desc": "用 Keras 实现 LSTM 神经网络生成 MIDI 音乐，展示 RNN 在序列生成上的应用。"},

    # === Visual Recognition (应用) ===
    {"name": "License Plate Recognition with ML", "lang": "Python", "scen": ["cv"],
     "title": "车牌识别系统（机器学习）",
     "url": "https://medium.com/devcenter/developing-a-license-plate-recognition-system-with-machine-learning-in-python-787833569ccd",
     "desc": "用 Python + 机器学习开发一个完整车牌识别系统，覆盖图像预处理、字符分割、模型训练。"},
    {"name": "Facial Recognition Pipeline", "lang": "Python/TensorFlow", "scen": ["cv"],
     "title": "基于深度学习的人脸识别流水线",
     "url": "https://hackernoon.com/building-a-facial-recognition-pipeline-with-deep-learning-in-tensorflow-66e7645015b8",
     "desc": "用 TensorFlow 构建端到端人脸识别流水线：人脸检测→对齐→特征提取→匹配。"},
]


def fetch_gh_readme(repo):
    """从 GitHub raw 取 README.md (master/main 都试)。失败返回空串。"""
    for branch in ("master", "main"):
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/README.md"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "gd4ai-bot/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception:
            continue
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--persist", action="store_true")
    ap.add_argument("--chunk", type=int, default=20)
    args = ap.parse_args()

    from . import db
    if db.pool.closed:
        db.pool.open()
    existing, used = ir.load_state()

    docs = []
    skipped = {}
    for it in ENTRIES:
        name = f"{it['name']} ({it['lang']})"
        url = it["url"]
        desc = it.get("desc") or f"{it['title']} — 来自 build-your-own-x 的{it['lang']}教程。"
        doc, why = ir.make_component({
            "name": name, "description_zh": desc, "url": url,
            "type": "knowledge", "kind": "knowledge",
            "scenarios": it.get("scen", ["other"]), "ai_related": True, "keep": True,
        }, used, existing)
        if not doc:
            skipped[why] = skipped.get(why, 0) + 1
            print(f"  ✗ {name}: {why}", flush=True)
            continue
        doc["tags"] = ["build-your-own-x", "tutorial", it["lang"].split("/")[0].lower()]
        doc.setdefault("install", {})["notes_zh"] = f"教程链接：{url}"
        if "github.com" in url:
            doc["source"]["origin"] = "https://github.com/codecrafters-io/build-your-own-x"
        else:
            doc["source"]["origin"] = "https://github.com/codecrafters-io/build-your-own-x"
        # 对有 GitHub README 的，跑 understand() 补「怎么用/对谁有帮助」
        if it.get("gh_readme"):
            print(f"  取 README: {it['gh_readme']}", flush=True)
            md = fetch_gh_readme(it["gh_readme"])
            if len(md) > 200:
                u = ir.understand(name, "knowledge", url, md)
                if u:
                    ir.apply_understanding(doc, u)
                    print(f"    ✓ understand OK", flush=True)
                else:
                    print(f"    (LLM 空，保留原 desc)", flush=True)
        docs.append(doc)
        if args.dry_run:
            inst = doc.get("install", {})
            print(f"  ✓ {doc['name']}", flush=True)
            print(f"    desc: {doc['description_zh'][:80]}", flush=True)
            print(f"    usage: {(inst.get('usage') or '')[:80]}", flush=True)

    print(f"\n产出 {len(docs)} 条，跳过 {skipped}", flush=True)
    if args.dry_run or not args.persist:
        print("(未落库)")
        return
    saved = ingest.persist_docs(docs)
    ingest.flush_reco_cache()
    print(f"✅ 落库 {saved} 条", flush=True)


if __name__ == "__main__":
    main()
