# Skill catalog — Taste Skill

Upstream: https://github.com/Leonxlnx/taste-skill (MIT, by Leonxlnx).

All skills install via the same plugin. Each skill does one job. The `Install name`
column is the value you pass to `--skill` when installing individually.

## Implementation skills (output code)

| Skill | Install name | What it does |
|---|---|---|
| **taste-skill** (v2, experimental) | `design-taste-frontend` | Default. Reads the brief, infers the design language, tunes three dials (VARIANCE / MOTION / DENSITY). Brief inference, design-system map, hard em-dash ban, canonical GSAP code skeletons, redesign-audit protocol, strict pre-flight check. Actively iterating toward v2.0.0 stable. |
| **taste-skill-v1** | `design-taste-frontend-v1` | Original v1, preserved for projects depending on its exact behavior. Use only if the v2 default breaks something specific in your workflow. |
| **gpt-tasteskill** | `gpt-taste` | Stricter variant for GPT/Codex: higher layout variance, stronger GSAP direction, aggressive anti-slop. |
| **image-to-code-skill** | `image-to-code` | Image-first pipeline: generate site references, analyze them, then implement the frontend to match. |
| **redesign-skill** | `redesign-existing-projects` | Existing projects: audit the UI first, then fix layout, spacing, hierarchy, styling. |
| **soft-skill** | `high-end-visual-design` | Polished, calm, expensive UI with softer contrast, whitespace, premium fonts, spring motion. |
| **output-skill** | `full-output-enforcement` | When the model ships half-finished work: full output, no placeholder comments. |
| **minimalist-skill** | `minimalist-ui` | Editorial product UI (Notion/Linear vibes), restrained palette, crisp structure. |
| **brutalist-skill** | `industrial-brutalist-ui` | Hard mechanical language: Swiss type, sharp contrast, experimental layout. |
| **stitch-skill** | `stitch-design-taste` | Google Stitch-compatible rules, including optional `DESIGN.md` export format. |

## Image-generation skills (output images only, no code)

| Skill | Install name | What it does |
|---|---|---|
| **imagegen-frontend-web** | `imagegen-frontend-web` | Website comps: hero, landing, multi-section with strong typography, spacing, anti-slop art direction. One image per section. |
| **imagegen-frontend-mobile** | `imagegen-frontend-mobile` | Mobile screens and flows: iOS/Android/cross-platform, mockups, readable type, coherent sets. |
| **brandkit** | `brandkit` | Brand-kit boards: logo directions, palettes, type, identity applications across categories. |

## Which one to pick

- Start with **taste-skill** (`design-taste-frontend`) for the safest general default.
- If the user depends on exact v1 behavior, use **taste-skill-v1**.
- Use **gpt-taste** for stricter GPT/Codex-oriented rules with stronger motion/layout.
- Use **image-to-code-skill** for image → analyze → code website workflows.
- Use **redesign-skill** to improve an existing codebase instead of greenfield styling.
- Add **soft-skill**, **minimalist-skill**, or **brutalist-skill** when the visual direction is already chosen.
- Add **output-skill** if the agent keeps truncating output.
- Use **imagegen-frontend-web**, **imagegen-frontend-mobile**, or **brandkit** when the deliverable is **images** (comps, flows, identity boards), then pass results to your coding agent.

## For image-first workflows

State the pipeline in the prompt: `follow the skill: generate images, then analyze, then code`.

Feed the image references into ChatGPT Images, Codex image mode, or any agent that generates images — then pass the renders to your coding agent (Claude Code, Cursor, etc.) for implementation.