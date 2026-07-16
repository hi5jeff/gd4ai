---
name: taste-skill
description: >-
  Anti-slop frontend design skills for AI-generated UIs. A collection of pluggable
  agent skills that upgrade AI-built interfaces with stronger layout, typography,
  motion, spacing, and taste — so they don't look templated or boilerplate. USE WHEN
  the user asks for a landing page, portfolio, redesign, premium UI, brutalist UI,
  minimalist UI, high-end visual design, image-to-code pipeline, or brand-kit image
  generation. Also use when the user says "make it look better", "add design taste",
  "anti-slop design", "make it premium", "fix the design", or complains the output
  looks like generic AI. Installation via `/plugin marketplace add
  Leonxlnx/taste-skill` or `npx skills add`. 设计品味技能，反"AI味"前端设计，让AI生成
  的界面不再模板化。
allowed-tools: Bash, Read
---

# Taste Skill — anti-slop frontend design for AI agents

Installs and drives the **Taste Skill** plugin library (Leonxlnx, MIT) — a set of
portable Agent Skills that enforce design taste, layout variety, motion quality, and
typography in AI-generated frontends. Use it to prevent boilerplate / slop output from
Claude, Codex, Cursor, or any coding agent.

## When to use

- User asks for a **landing page**, **portfolio**, **marketing site**, or **redesign**.
- "Make it look better / premium / high-end / polished / expensive / designer-quality."
- "Anti-slop design", "add design taste", "fix the AI-looking UI", "it looks generic."
- A specific visual direction is chosen: **brutalist**, **minimalist**, **soft/luxury**,
  **editorial**, **Linear/Notion-style**, **industrial**, **Awwwards-tier**.
- User wants **image-first** workflow: generate design references → then code.
- "Output keeps getting cut off" → the output-skill enforces full generation.
- Image-generation ask: "generate a brand kit", "make web comps", "mobile mockups".

Not for: dashboards, data tables, complex multi-step product UI, or backend logic.

## How to use

### 1. Install the plugin (once)

In Claude Code:
```
/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill
```

Or via `npx` (works on Codex, Cursor, Copilot, etc.):
```bash
npx skills add https://github.com/Leonxlnx/taste-skill
```

Install a single skill by its install name:
```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

### 2. Pick the right skill for the ask

See `references/skill-catalog.md` for the full table. Quick guide:

| When the user says... | Use |
|---|---|
| "Build a landing page / portfolio" | `design-taste-frontend` (default, v2) |
| "Make it look premium / expensive" | `high-end-visual-design` (soft-skill) |
| "Brutalist / industrial style" | `industrial-brutalist-ui` |
| "Clean / minimalist / Notion-style" | `minimalist-ui` |
| "Redesign this existing site" | `redesign-existing-projects` |
| "Generate design images first" | `imagegen-frontend-web` or `imagegen-frontend-mobile` |
| "Build a brand kit / identity" | `brandkit` |
| "Image → analyze → code pipeline" | `image-to-code` |
| "Output keeps getting truncated" | `full-output-enforcement` |
| "I need the old v1 behavior" | `design-taste-frontend-v1` |

### 3. Tune the dials (taste-skill v2 only)

In the skill file, three 1-10 dials adjust the output:
- **DESIGN_VARIANCE** (default 8): layout experimentation — low=centered/clean, high=asymmetric/modern.
- **MOTION_INTENSITY** (default 6): animation depth — low=hover only, high=scroll/magnetic/GSAP.
- **VISUAL_DENSITY** (default 4): information per viewport — low=airy, high=dense cockpit.

The agent reads these and adjusts accordingly. The user can override in chat: "make it more asymmetric" or "tone down the motion."

## Notes

- Framework-agnostic: works with React, Vue, Svelte, Next.js, etc. — rules target design
  intent, not a specific framework API.
- Taste Skill has no token/coin/crypto project — any token using its name is unaffiliated.
- Upstream: https://github.com/Leonxlnx/taste-skill (MIT, by Leonxlnx).
- This skill wraps the plugin; it does not reimplement the design rules. If a skill
  isn't found, confirm the plugin is installed and the CLI was restarted.