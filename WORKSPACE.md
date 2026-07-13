# Workspace Info (auto-generated, do not edit)

## Workspace: smartj

- **smartj_site Chat** [site] (project: smartj_site, dir: /home/claudecrab/storage/projects/06827e88-1071-4e1e-bc91-cbb0da622476) — mode: confirm
- **smartj-tool Chat** [tool] (project: smartj-tool, dir: /home/claudecrab/storage/projects/00fe7e96-93ea-48d1-a0d0-b75d306b5a73) — mode: confirm

## Shared Directory
A `shared/` directory is available in your project root for cross-project file exchange.

Rules:
- Write files to `shared/` when other projects need them
- After writing files to `shared/`, ALWAYS notify other projects using `__notify__`
- When you receive a shared file notification, check `shared/` for new files
- Do NOT modify or delete files created by other projects unless instructed

## How to notify a related bot
Include this JSON in your response:
```json
{"__notify__": {"target": "bot_name_here", "message": "description of changes"}}
```
The bot system will route your message to the target bot's Claude session.

## How to ask a related bot a question
Include this JSON in your response to ask another bot and wait for their answer:
```json
{"__ask__": {"target": "bot_name_here", "question": "your question here"}}
```
The bot system will send your question to the target bot, wait for their answer, and feed it back to you.

## How to create a TODO task for a related bot
Include this JSON in your response to assign a task to another bot:
```json
{"__todo__": {"target": "bot_name_here", "title": "task title", "description": "detailed description"}}
```
The bot system will create a TODO task and notify the target bot.

## How to mark a TODO task as completed
After completing a task from your TODO.md, include this in your response:
```json
{"__todo_done__": {"id": "task-uuid-from-TODO.md", "result": "what you did"}}
```
