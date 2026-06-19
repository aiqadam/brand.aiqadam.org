# AI Qadam Brand Guidelines

Source for **[brand.aiqadam.org](https://brand.aiqadam.org)** — the canonical
brand and design reference across the AI Qadam umbrella: the four streams
(Events, Education, People, Accelerator), the Build infrastructure that
powers them, and the chapter and merch surfaces that carry the brand.

Static HTML + CSS. No framework, no bundler. Fork it, host it.

## Pillars

- **[Brand](brand.html)** — identity, voice, principles, logo, colour,
  typography, photography, iconography, merch templates. Travels beyond
  digital.
- **[Design system](system.html)** — tokens, components, domain patterns,
  screen mockups, navigation rules. Digital product UI only.

## Run it

```sh
python3 -m http.server 8765
# open http://localhost:8765/
```

Or open `index.html` directly — works with `file://` too.

## Deploy

Drag the directory into Cloudflare Pages, Vercel, Netlify, or any
static host. Point DNS:

```
brand.aiqadam.org   CNAME   <your-host>.pages.dev
```

## Edit

- Brand content → `brand.html`
- Design system content → `system.html`
- Page chrome (header, footer, hero) → duplicated across all pillar pages
  on purpose; if you change one, change all
- Shared styles → `docs.css`
- Tokens (colour, type, radius, motion) → `tokens.css`
- Component primitives → `components.css`

Brand assets (logo SVGs) live under `brand/`. Don't recolour or redraw.

## Speaker deck templates

For anyone speaking at an AI Qadam meetup:

- [`brand/decks/aiqadam-speaker-template.pptx`](brand/decks/aiqadam-speaker-template.pptx) —
  PPTX skeleton, 16:9, six slides (title · bio · section · content · quote · closing).
  Hand-edit in PowerPoint or Keynote.
- [`speaker-deck.html`](speaker-deck.html) — same skeleton as a static HTML deck.
  Edit `<section data-kind="...">` blocks; keyboard nav with ← → space.
  AI-friendly: ask Claude/ChatGPT to draft slides directly into it.

## Legal docs

Three artefacts at the bottom of every page:

- [`LICENSE`](LICENSE) — MIT, code only
- [`BRAND-USE.md`](BRAND-USE.md) — Brand Usage Policy (v1)
- [`LICENSE-content`](LICENSE-content) — CC BY 4.0, docs content only

Rendered HTML versions: [`license.html`](license.html),
[`brand-use.html`](brand-use.html),
[`license-content.html`](license-content.html). Regenerate after
editing the source files:

```sh
python3 -m venv .venv
.venv/bin/pip install markdown
.venv/bin/python scripts/render-docs.py
```

## License summary

| Material | License |
|---|---|
| Source code (CSS, HTML markup, JS, scripts) | MIT |
| Brand assets (name, marks, wordmark, four-dot motif, brand teal) | © AI Qadam Community — see `BRAND-USE.md` |
| Editorial content (prose, examples, manifesto excerpts) | CC BY 4.0 |

## Contact

For a partnership, a chapter, a brand-use question:
**brand@aiqadam.org**

For agent / AI context when editing this repo: see [`AGENTS.md`](AGENTS.md).
