<p align="center">
  <a href="https://gd4.ai"><img src="https://gd4.ai/og.png" alt="gd4.ai" width="720"></a>
</p>

<h1 align="center">gd4.ai</h1>

<p align="center">
  <b>Tell us what you want to do — get a ready-to-run AI tool stack.</b><br>
  Which Skills · MCPs · plugins · agents · prompts to use, with install, config and the first step — not a pile of links to figure out yourself.
</p>

<p align="center">
  <a href="https://gd4.ai"><img src="https://img.shields.io/badge/Live-gd4.ai-e7ad5f" alt="live"></a>
  <img src="https://img.shields.io/badge/Verified%20resources-1%2C462-1f6feb" alt="resources">
  <img src="https://img.shields.io/badge/Copy--ready%20prompts-13%2C225-2ea043" alt="prompts">
  <a href="./README.zh.md"><img src="https://img.shields.io/badge/中文-README-8b8b93" alt="zh"></a>
</p>

---

## What is this

**gd4.ai is a needs-driven AI tool ecosystem recommender.**

Describe what you want to do in plain words — *"build an e-commerce site"*, *"prompts for a perfume ad"*, *"give me an AI agent that does UI design"* — and it tells you exactly **which AI Skills, MCP servers, plugins, expert agents and prompts to use**, plus **how to install, how to configure, and the first step to run.**

In one line: **others hand you a pile of links; we hand you a stack you can actually run.**

---

## We are not a search engine

A search engine (Google / Bing) **indexes the whole web and ranks it**, then drops a list of links on you — and **whether each thing is real, good, usable, or how to use it is entirely on you** to click, read, test and assemble. It gives you *information*, not an *answer*; *leads*, not a *solution*.

gd4.ai does the opposite: you state a need, and we pick the things that actually work from a **vetted library** and **assemble them into a stack you can follow step by step.**

> In one line: **a search engine gives you a pile of "maybe useful links"; gd4.ai gives you a "ready-to-run plan."**

| | Search engine (Google/Bing) | gd4.ai |
|---|---|---|
| Core job | Index the web + rank by relevance | Vet & build a library + assemble by need |
| Must know the tool's name first | ✅ Yes | ❌ No — just say what you want |
| What you get | A list of links to sift and test | A runnable plan (install / config / first step) |
| Search for a prompt | A link to some repo's homepage | The **copy-ready prompt itself** |
| Trust / quality | Whole web — you vet it yourself | **AI double gate** — only vetted items shown |
| When nothing fits | Pads results with irrelevant hits | Honestly says "we don't have it" — never fabricates |
| Depth of coverage | "Tool name + blurb" | "How to use it, who it helps, first step" |

---

## What makes us different

### ⭐ The core: an AI double gate — everything that gets in is reviewed, everything recommended is in the library

This is what separates gd4.ai from *"let an AI answer from memory."* AI guards **both** ends:

- **In: AI reviews and curates.** Every resource — whether we collected it or a user submitted it — must first be reviewed, understood and broken down by AI before it enters the library: *what it is, whether it's worth keeping, how to use it, who it helps.* Junk, duplicates, pure ads, and anything with no clear usage get stopped at the door.
- **Out: AI can only filter and recommend.** When building your plan, the AI **can only select and combine from that vetted library** — it cannot invent, cannot cite anything outside the library, and every item is validated before output.

> The result: every recommendation you see **really exists, has been verified by us, and can actually be followed.** If it's not in the library, we tell you so — instead of making up a plausible answer that doesn't actually work.

### 1 · Need → a full stack, not a keyword search
Ask *"I want to do website UI design"* and you get **UI UX Pro Max (skill) + a UI/UX Designer (agent) + Figma**, each with why it's there and how to use it — not a long result list you assemble yourself.

### 2 · Usable content, not a pile of links
Ask for *"perfume ad prompts"* and you get the **copy-ready prompt itself**, not a GitHub repo to go dig through.

### 3 · AI reads each resource and writes how to actually use it
During intake review, the AI understands usage from the resource's real docs (README / official site), strictly grounded — it never invents usage. So the "how to install, first step" in a recommendation is real and followable.

### 4 · Two levels of granularity
- **Component level**: one tool / skill / library = one entry (with install & config)
- **Prompt level**: each individual prompt is its own searchable, copy-ready entry
> That's why *"perfume ad prompts"* returns the exact prompt — not a link to a prompt library.

### 5 · Multilingual
Ask in any language, get the answer in that language (data is stored once; the AI translates output into the language you asked in).

### 6 · From beginner to expert
Beginners get step-by-step instructions and the first command; experts get straight to the specific component.

### 7 · Always growing, anyone can contribute
Found a great GitHub repo / prompt library / tool site? Submit the URL — after AI review and understanding it's broken down and added. The library keeps getting richer.

---

## What's in the library today

**1,462 human-verified components** + **13,225 copy-ready prompts**

| Type | Count | | Type | Count |
|---|---|---|---|---|
| Skill | 448 | | MCP server | 119 |
| Tool | 393 | | Plugin | 191 |
| Role / Agent | 289 | | Workflow | 17 |

Covers **Claude Code, Cursor, Codex** and more — and goes beyond coding: engineering, graphic design, e-commerce, games, interior design, marketing copy, and more.

---

## Try it

👉 **[gd4.ai](https://gd4.ai)** — it's just a box. Type what you want to do.

Shareable search deep links work too: `https://gd4.ai/?q=build an e-commerce site`

---

## How it works

```
need  →  hybrid retrieval (keyword + semantic)  →  candidates  →  closed-world AI orchestration  →  validate  →  runnable plan
```

- **Structured dataset**: a unified-schema component library + a prompt library
- **Hybrid retrieval**: Meilisearch (keyword) + pgvector (semantic vectors), fused with RRF
- **Closed-world orchestration**: the AI can only pick from retrieved candidates and is validated before output — never cites anything outside the library
- **Vectors & reasoning**: local BGE-M3 embeddings + a DeepSeek-class LLM (online reasoning / offline enrichment)
- **Stack**: FastAPI backend + a lightweight static frontend

Data sources: our own seed set + automatic understanding-and-ingestion from GitHub repos / web pages / prompt libraries + user submissions (reviewed). The database is the source of truth; the library can be rebuilt.

---

<p align="center"><sub>gd4.ai · every recommendation comes from a human-verified library — commands are ready to copy and run</sub></p>
