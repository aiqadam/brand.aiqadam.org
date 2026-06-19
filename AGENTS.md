# Agent context — AI Qadam Brand Guidelines

> If you're an AI assistant landing in this repo, start here. This is the
> condensed mental model you need before editing.

This repo is the source for **`brand.aiqadam.org`** — the canonical brand and
design reference across the AI Qadam umbrella (Events, Build, People,
Education, Chapters, Merch). It's static HTML + CSS + a few build scripts —
no framework, no bundler, no toolchain you need to install.

## Architecture

Three-pillar umbrella with one landing page:

```
index.html          → Umbrella landing (three pillar cards)
brand.html          → Pillar 1 — Brand
system.html         → Pillar 2 — Design system
products.html       → Pillar 3 — Products
```

- **Brand** is everything that travels beyond digital: identity, voice,
  principles, logo, colour, typography, photography, iconography, merch
  templates. Used by chapter leads, event organisers, designers, partners,
  merch suppliers, printers.
- **Design system** is digital UI only: tokens, components, domain
  patterns, screen mockups, navigation rules. Used by engineers shipping
  product surfaces.
- **Products** is per-product stubs (Events, Build, People, Education,
  Chapters, Merch). Each stub describes which parts of Brand + System a
  product uses, plus product-specific overrides.

The legacy `portal-reference.html` is a screen-by-screen reference library
that pre-dates the pillar split. Leave it as-is unless asked.

## Where new content goes

Decision tree:

- Touches print, merch, decks, posters, social, off-screen? → **Brand**
- Touches a button, component, page layout, digital pattern? → **Design
  system**
- Specific to one stream (Events vs Build vs Merch)? → **Products**
- Doesn't fit any? Talk to Binali — probably new pillar or new section.

Cross-link between pillars rather than duplicate. e.g. `system.html` links
to `brand.html#colors` for tokens instead of redefining them.

## File layout

```
.
├── index.html              ← landing
├── brand.html              ← Pillar 1
├── system.html             ← Pillar 2
├── products.html           ← Pillar 3
├── portal-reference.html   ← legacy screen library (do not refactor)
│
├── tokens.css              ← OKLCH tokens, shadcn-compatible. Light + dark.
├── components.css          ← buttons, inputs, badges, brand-mark slots
├── docs.css                ← page chrome shared by the four pillar pages
├── portal.css              ← styles unique to portal-reference.html
│
├── brand/
│   ├── logo-mark.svg       ← footprint + 4 dots (navbar, favicon, compact)
│   └── logo-full.svg       ← footprint + AI QADAM wordmark (splash, hero)
│
├── LICENSE                 ← MIT — code only
├── BRAND-USE.md            ← custom Brand Usage Policy (draft v1)
├── LICENSE-content         ← CC BY 4.0 — docs content only
├── license.html            ← rendered LICENSE
├── brand-use.html          ← rendered BRAND-USE.md
├── license-content.html    ← rendered LICENSE-content
│
└── scripts/
    ├── render-docs.py      ← regenerates the three legal HTML pages
    ├── split-docs.py       ← legacy splitter, kept for reference
    └── README.md
```

## Conventions

- **Tokens are normative.** All colours come from `tokens.css` semantic
  variables (`--primary`, `--foreground`, `--card`, etc.). Don't write
  raw hex except inside the SVG brand files for `<img>` fallbacks.
- **Brand assets are immutable.** Never recolour, redraw, or substitute
  the mark, wordmark, or four-dot motif. Never use the brand teal as a
  generic accent — it is the brand colour.
- **The full logo lockup must theme correctly.** Letter counters are
  hollow via compound paths with `fill-rule="evenodd"`. Letters fill
  with `var(--aiq-logo-dark, …)` which resolves to `var(--foreground)`
  in inline use, or the hex fallback in `<img>` use. If you're adding
  a new place that shows the full logo on a dark/light surface that
  toggles, inline the SVG — don't `<img>`.
- **Don't duplicate page chrome.** Header, footer, and hero markup are
  copy-pasted across the four pages. If you change one, change all.
  The shared CSS lives in `docs.css`.
- **English in content, Russian in conversation.** The user (Binali)
  writes to AI agents in Russian. The docs at `brand.aiqadam.org` stay
  in English — localisation comes later via the "Multilingual by
  default" principle.

## Build & local dev

It's static HTML — no build for the pillar pages.

```sh
python3 -m http.server 8765
# open http://localhost:8765/
```

The only build step is for the three legal pages. Re-run after editing
`BRAND-USE.md`, `LICENSE`, or `LICENSE-content`:

```sh
python3 -m venv .venv
.venv/bin/pip install markdown
.venv/bin/python scripts/render-docs.py
```

## Licensing

Three artefacts cover non-overlapping material:

| Material | License | File |
|---|---|---|
| Code (CSS, HTML markup, JS, scripts) | MIT | `LICENSE` |
| Brand assets (name, marks, wordmark, four-dot motif, brand teal) | Custom — © AI Qadam Community | `BRAND-USE.md` |
| Editorial content (prose, examples, manifesto excerpts) | CC BY 4.0 | `LICENSE-content` |

When adding new files, file under the right category. Don't try to ship
one LICENSE for everything — it either over-restricts the code or
under-protects the brand.

## Source documents

Brand voice and principles are anchored in source docs at
`~/Library/Mobile Documents/com~apple~CloudDocs/AI_Qadam/docs/`:

- `AI Qadam Manifesto.docx` — the seven community principles. Load-bearing
  for tone-of-voice decisions.
- `decks/AI_Qadam_Partnership_Deck_(May 2026)_upd.pdf` — positioning,
  tagline, region tags, stream model, "what we welcome / what we turn
  down".

The seven principles are already mirrored in `brand.html#voice` — usually
you can read those instead of re-extracting the docx.

## Common mistakes to avoid

- Don't add new pages above the pillar level. The umbrella is three
  pillars + one landing — that's the whole structure.
- Don't relicense brand assets — they are explicitly excluded from MIT.
- Don't AI-generate photography or imagery for the brand. The honesty
  principle applies to images too (see `brand.html#photography`).
- Don't introduce new colour tokens or fonts. The palette is one teal
  + neutrals; the families are Geist / Inter / JetBrains Mono.
- Don't add a JS framework, bundler, or build toolchain. The site is
  static on purpose — chapter leads should be able to fork and host
  without setup.

## Contact

Binali Rustamov · `binali.rustamov@aiqadam.org` · Country Lead UZ, founder.
