---
name: mdbox-media
description: Generate and process media — images, video, audio, music — and read text from images (OCR). Use whenever the user asks to create / draw / render an image, make a video, generate audio/music, do image-to-image / image-to-video, remove a background (cutout), upscale, or extract / recognize text from an image, scan, or document (作图 / 生成图片 / 生成视频 / 配音 / 海报 / 识别文字 / 提取文字 / OCR / 扫描).
allowed-tools: Bash
---

# MDBOX media generation

Generate and process media with the platform `mdbox` CLI (already installed; uses the
org gateway, no API key needed here). Supports text-to-image/video/audio, image-to-image,
image-to-video, background cutout, and upscaling.

## Where to save — ALWAYS `./generated_images/`
Save every file the user should see/download into `./generated_images/` (run
`mkdir -p generated_images` first). Only this folder is publicly served for the project.

## How to deliver — paste the REAL public URL
The project's public base is in the env var `$PROJECT_MEDIA_BASE`. For a file
`generated_images/<name>.<ext>`, its URL is `${PROJECT_MEDIA_BASE}generated_images/<name>.<ext>`.
Output it in chat **by type** so it renders in web and Telegram/Discord:
- Image → `![<alt>](<url>.png)` — shows inline
- Video → `[<title>](<url>.mp4)` — web embeds a player; TG/Discord show a link
- Audio → `[<title>](<url>.mp3)` — web embeds an audio player
- PDF / HTML / Excel / Word / PPT / other → `[<filename>](<url>.<ext>)` — clickable link

Always give the user the link — never just say "saved to generated_images/".

## Generating — ALWAYS use the `__media__` directive
To generate ANY image/video/audio you MUST emit a `__media__` directive — do NOT run
`mdbox gen` for generation (it blocks your whole turn). Emit it on its own line and
finish your reply right away; the system submits it, shows a live progress card, and
delivers the result into the chat automatically.

```
{"__media__": {"kind": "image", "model": "nano-banana-pro", "prompt": "a red fox in snow, cinematic"}}
```

- `kind`: image | video | audio. `model`: pick from `mdbox models`. `prompt`: required.
- Image-to-image / image-to-video: first `mdbox upload <file>` to get its URL, then pass it
  in `params`, e.g.
  `{"__media__": {"kind":"image","model":"nano-banana","prompt":"make it watercolor","params":{"metadata":{"image":"<url>"}}}}`.
- Emit the directive ONCE per file; don't also run `mdbox gen` for the same thing.

## The mdbox CLI (non-generation)
- `mdbox guide` — full reference (commands + current models). The model list lives here;
  never hardcode model names.
- `mdbox models` — list current models (for the `model` field above).
- `mdbox upload <file>` — local file → the https URL that reference inputs require.
- `mdbox gen --model <model> --prompt "<text>" -o generated_images/<name>.png` — SYNCHRONOUS
  (blocking) generation. Use ONLY when you need the file IN THE SAME TURN (e.g. make an
  image then immediately feed it into a video). Never for a plain request — use `__media__`.

## Reading text from images (OCR)
To extract text FROM an image (scan, screenshot, photo of a document, receipt…), use
`mdbox ocr` — it is SYNCHRONOUS and fast (~1s), so run it directly in your turn (do NOT
use `__media__`, that's only for generation).

- `mdbox ocr <image>...` — one or more local paths or https URLs (1–16 images). Local
  files are auto-uploaded. Prints the recognized text (layout order).
- `mdbox ocr <image> --json` — full JSON: `full_text`, per-image `pages[]`,
  `low_confidence_words[]` (with bbox), and `stats` (word count, avg confidence).
- `--lang ko,zh` — optional BCP-47 hint(s); omit to auto-detect (~99 languages).
- `-o out.txt` — write the text to a file instead of stdout.

Example: `mdbox ocr ./invoice.png --lang en` → prints the invoice text. Then answer the
user's question about it, or paste the extracted text back into chat.

See `references/models.md` for model-selection guidance (read on demand).
