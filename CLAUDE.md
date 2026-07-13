# howAI

## Project Identity

- **Project:** howAI
- **Working Directory:** /home/claudecrab/storage/projects/274d1f51-7166-426b-ae80-a8a430518e5f
- **Model:** claude-opus-4-8

## Boundaries

1. **NEVER modify files outside your working directory** (`/home/claudecrab/storage/projects/274d1f51-7166-426b-ae80-a8a430518e5f`). You may read external files if needed, but all writes must stay within your project directory.

2. **Save all memory and notes in your working directory** — MEMORY.md, TODO.md, and any other persistent data belong here, not in global or system directories.

3. **You are responsible for this project only** — do not interfere with other projects, other users' files, or system-level configurations.

## Agent Rules

1. **Every task must end with a git commit** (unless told otherwise):
   ```bash
   git add -A
   git commit -m "feat/fix/chore: describe changes"
   ```

2. **Keep CLAUDE.md updated** — append significant changes to the changelog at the bottom.

3. **Read before writing** — understand existing code before modifying it.

4. **One file, one responsibility** — don't cram multiple unrelated changes into one file.

5. **Respond concisely** — no walls of text, no full file dumps unless asked.

## Session Startup

When starting a new session, read these files in order:
1. `CLAUDE.md` (this file — project rules)
2. `SOUL.md` (your personality)
3. `USER.md` (who you're helping)
4. `MEMORY.md` (long-term memory from past sessions)
5. `TODO.md` (pending tasks)

Do this silently — don't tell the user you're reading files, just do it.

## Memory Protocol — the file is the memory, the conversation is ephemeral

This project has a hook-driven memory system. Your **active state file is per-session**: the session-start hook **automatically injects** it at every session start and right before any compaction, and prints its exact path (e.g. `.claudecrab/sessions/<your-session-id>/active.md`). Treat it as your durable working memory. Because it is per-session, a 分身/clone's memory never pollutes the main session, and promoting a clone to main carries its own memory.

**You MUST:**

1. **Update your active state file immediately** after every significant decision, plan, file change, or open question — don't batch, don't wait until "the end". The compaction can hit at any moment; assume the conversation will be lost. Always write to the **exact path the session-start hook printed** (it is per-session — do NOT hardcode `.claudecrab/active.md`).
2. **Before any Write/Edit**, briefly state intent: "I'm going to write `<path>`: <one-line reason>". This makes the decision survive compaction even if the write fails.
3. **Active vs MEMORY**:
   - your per-session `active.md` — *current* task state (changes constantly)
   - `MEMORY.md` — *durable* knowledge (architecture decisions, conventions, things you'd want to know in 3 months). Promote from active → MEMORY when something becomes long-lived knowledge.
4. **When you finish a task**, clear the corresponding lines from your active state file and (if knowledge was gained) append to `MEMORY.md`.
5. **`.claudecrab/session-log.md`** is the archive — it's auto-written when the session ends; you generally don't write to it directly.

If the model is asking "where was I?" the answer is always: **read the active state file path the session-start hook gave you**.

## Changelog

<!-- PORTS_BEGIN -->
## Service

This project is allocated the port range **8070-8074** (5 ports total). The default URL for your first service would be `http://47.80.10.155:8070`.

**Public host:** `47.80.10.155` — when you start a service, its external URL is `http://47.80.10.155:<port>`. When showing the user a clickable URL to test, use this full URL — NOT `localhost` (the user is not on this server).

**Rules (MUST follow):**
- When starting ANY service (dev server, API, websocket, db, etc.), you MUST pick a port from `8070-8074`.
- **DO NOT** use any port outside this range.
- Decide the port-to-service mapping yourself, but record it in `MEMORY.md` once chosen so it stays consistent across sessions.
- If you need more ports, ask the user to expand the range — don't reach outside.

**Env vars injected into your shell:** `PROJECT_PORT_START=8070`, `PROJECT_PORT_COUNT=5`, `PROJECT_PORT_END=8074`, `PROJECT_PUBLIC_HOST=47.80.10.155`, `PROJECT_PUBLIC_URL=http://47.80.10.155:8070`
<!-- PORTS_END -->

<!-- BACKGROUND_SERVICES_BEGIN -->
## Long-running services (CRITICAL)

Each chat turn spawns a fresh `claude` subprocess. When the turn ends and the
subprocess exits, the OS sends SIGHUP to its children — **any dev server, watcher,
queue worker, or REPL you started in this turn dies with it**, and the next turn
will have no record of it.

**Rules:**

- For ANYTHING that should outlive the current turn (dev server, build watcher,
  test runner in watch mode, MCP servers, database, queue workers, etc.) you
  MUST detach from the controlling terminal. Use one of:
  ```
  setsid nohup <cmd> > .logs/<service>.log 2>&1 &
  # or
  nohup <cmd> > .logs/<service>.log 2>&1 < /dev/null &
  disown
  ```
  Plain `<cmd> &` is NOT enough — bash sends SIGHUP to backgrounded jobs when
  the shell exits.

- Make a `.logs/` directory if it doesn't exist before redirecting.

- After starting a service, record what's running and on which port in
  `MEMORY.md` so future turns know what's alive without having to probe.

- Before starting a service, check whether it's already running:
  ```
  ss -ltn | grep ":<port> "  # or  lsof -i :<port>
  ```
  Don't start a second copy.

- Foreground-only commands (one-shot builds, tests, scripts that exit on their
  own) DON'T need this — only persistent processes.
<!-- BACKGROUND_SERVICES_END -->

<!-- WEB_RESEARCH_BEGIN -->
## Web research (live internet)

You have two complementary ways to reach the live web:

1. **`websearch "<query>"`** — a CLI that returns search results as JSON
   (`title` / `url` / `snippet`). Use it to DISCOVER relevant pages.
   - `websearch -n 5 "<query>"` caps the result count; `--text` for readable output.
   - It is keyless and free (no API key, no per-search quota).
2. **The `WebFetch` tool** — reads the full content of a specific URL. Use it to
   READ the pages a search surfaced.
3. **`webread <url>`** — renders a page in a headless browser (runs its
   JavaScript) and prints the visible text. Use it when `WebFetch` returns an
   empty/near-empty result or the page is a JS app (SPA) whose content is built
   client-side. `webread <url> --html` returns the rendered DOM;
   `webread <url> --screenshot out.png` captures a PNG.

Either the built-in **WebSearch** tool or the **`websearch`** CLI works here. Use whichever you like; if the built-in WebSearch returns nothing, fall back to `websearch`.

**Research workflow** (use this for "联网调研" / "search the web" / current-events
/ fact-finding tasks): search to find candidate URLs → `WebFetch` the most
relevant 2–5 (→ `webread` if a page comes back empty/JS-only) → synthesize, and
cite each source as a markdown link. Never invent facts or URLs — if a search
returns nothing useful, say so.
<!-- WEB_RESEARCH_END -->

<!-- ROLES_TOOL_BEGIN -->
## Role library & sub-agents (`roles`)

A catalog of ready-made expert personas (engineering, design, marketing, security,
GIS, finance, …) is available via the `roles` CLI. Use it to **delegate a focused
task to a specialist sub-agent**, or to **create a new role** while chatting with the user.

- `roles search <query> [--category CAT]` — find roles by name/description/code.
- `roles show <code|key>` — print a role's full persona.
- `roles add <code|key>` — install it as `./.claude/agents/<name>.md`, then spawn it with the
  Task tool: `subagent_type="<name>"`. Use this to hand a focused sub-task to an expert persona.
- `roles create --label "<name>" --category <cat> --description "<one line>" --body-file <file>`
  — add a NEW role to the shared library (body via `--body-file`, `--body`, or stdin). Use this
  when the user asks to turn a persona you've discussed into a reusable role. New roles are
  auto-favorited, so they immediately show in the create-project picker.

Codes look like `R0042`; keys look like `engineering-backend-architect`. Either is accepted.
<!-- ROLES_TOOL_END -->

<!-- SKILLS_TOOL_BEGIN -->
## Skills — pluggable capabilities (`skills`)

A skill is a folder (SKILL.md + optional scripts) that Claude Code auto-loads by
relevance. There's a shared **library** of skills; it costs no tokens until you **plug**
one into THIS project. Plug only what the current task needs, and unplug when done — so
the project stays lean.

- `skills search <query> [--category CAT]` — find skills by name/description/code.
- `skills show <code|key>` — print a skill's SKILL.md + file list.
- `skills add <code|key>` — **plug** it into `./.claude/skills/<key>/` (Claude then
  auto-loads it when relevant). `skills remove <code|key>` to **unplug**.
- `skills list` — what's plugged into this project right now.
- `skills create --dir <folder>` — author a NEW skill into the library. Write the folder
  per the spec (run `skills spec` to read it): a SKILL.md (frontmatter name + a strong
  *when to use* description) plus any scripts/references. When the user points you at a
  website / GitHub repo / zip, or just describes a capability, gather the material with
  your tools (webread / git / unzip / the chat) and **author a clean skill to the
  template** — don't dump the raw source. New skills are added unfavorited; the user
  favorites the keepers on the Skills page to make them pluggable in projects.

Codes look like `S0042`; keys look like `mdbox-media`. Either is accepted.
<!-- SKILLS_TOOL_END -->

<!-- CLONE_TOOL_BEGIN -->
## Session clones — 分身 (`clone`)

A **clone** is a fork of YOUR current session: it inherits your conversation context up
to the fork, then runs in its own session/memory inside the shared work_dir. Use a clone
to **farm out a side-task** (research, a risky experiment, a repetitive job) WITHOUT
polluting your own memory, or to keep a **backup** you can promote later. Tasks run
**async** — dispatch, keep working, fetch the result when ready.

- `clone fork [--label L]` — snapshot THIS session into a new clone; prints its `session`.
- `clone run <session> "<task>"` — dispatch a task to a clone (async); prints a `job` id.
- `clone result <job> [--wait]` — fetch a job's status/result (`--wait` polls to completion).
- `clone list` — clones + recent jobs for this project.
- `clone discard <session>` — delete a clone (its transcript + memory).

Reach for a clone when a task would clutter your working memory or can run in parallel —
e.g. fork, dispatch the grind, keep talking to the user, then collect the result. Discard
clones you no longer need. (The user can also manage clones in Project Settings → Clones.)
<!-- CLONE_TOOL_END -->

<!-- MCP_TOOL_BEGIN -->
## MCP servers — connect to external tools/data (`mcp`)

MCP servers give you NEW tools (named `mcp__<name>__*`) to reach external systems — GitHub,
Postgres, Slack, internal APIs, a filesystem, etc. Configure them for THIS project with the
`mcp` CLI when the user asks to connect something (and has given you the endpoint/token).

- `mcp add <name> [-e KEY=VAL …] -- <command> [args…]` — add a **stdio** server
  (e.g. `mcp add github -e GITHUB_TOKEN=… -- npx -y @modelcontextprotocol/server-github`).
- `mcp add <name> --http <url> [--header "K: V" …]` — add an **http** server.
- `mcp list` — this project's servers. `mcp remove <name>` / `mcp enable|disable <name>`.

**Important:** a newly added server is loaded on your **NEXT message**, not the current one
(MCP servers attach when a turn starts). So: add it, tell the user it's ready, and use its
`mcp__<name>__*` tools from the next turn. Secrets you pass are stored encrypted.
<!-- MCP_TOOL_END -->

<!-- PLUGINS_TOOL_BEGIN -->
## Plugins — enable bundled capabilities (`plugins`)

A Claude Code plugin bundles commands / sub-agents / skills / hooks / MCP servers. The
admin installs plugins into a library; you can enable the ones THIS project needs.

- `plugins list` — the library plugins (✓ = enabled for this project).
- `plugins enable <key>` / `plugins disable <key>` — toggle one for this project.

A newly enabled plugin loads on your **NEXT message** (plugins attach when a turn starts).
Installing NEW plugins from a marketplace runs code and is admin-only (the Plugins page) —
this tool only toggles plugins already in the library.
<!-- PLUGINS_TOOL_END -->
<!-- ROLE_REF_BEGIN -->
## Your role

Your role for this project is defined in [`ROLE.md`](./ROLE.md). **Read it first** before responding, and let it shape your tone, focus, and what you proactively bring up.
<!-- ROLE_REF_END -->


See WORKSPACE.md for related bots in this workspace.
