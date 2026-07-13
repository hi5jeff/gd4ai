# MDBOX models — choosing one

> Loaded on demand (progressive disclosure). The authoritative, live list is always
> `mdbox guide`; `/api/pricing` is the source of truth for prices. This file only
> gives selection guidance — do not hardcode model ids from here into commands.

## How to get the live list
```
mdbox guide        # models, capabilities, and example commands
```

## Picking a model (general guidance)
- **Image, fast/cheap drafts** — use the lightest image model the guide lists; good for
  iterating on composition before a final render.
- **Image, high fidelity** — use the highest-quality image model for final deliverables
  (posters, hero images, product shots).
- **Video** — video models cost markedly more and take longer; confirm the user wants a
  video (not an image) and keep clips short unless asked otherwise.

## Cost awareness
- Always surface the rough cost/'档位' to the user before generating expensive media
  (especially video) when the request is ambiguous.
- Prefer one good prompt over many speculative generations.

## Output convention
- Always `--out ./generated_images/<descriptive-name>.png` (or the right extension).
- Use descriptive filenames (`hero-banner-v1.png`, not `image.png`).
