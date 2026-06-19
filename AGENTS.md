# Agent context — AI Qadam Brand Guidelines

> If you're an AI assistant landing in this repo, start here. This is the
> condensed mental model you need before editing.

This repo is the source for **`brand.aiqadam.org`** — the canonical brand and
design reference across the AI Qadam umbrella: the four streams (Events,
Education, People, Accelerator), the Build infrastructure that powers
them, and the chapter and merch surfaces that carry the brand. It's
static HTML + CSS + a few build scripts — no framework, no bundler, no
toolchain you need to install.

## Architecture

Two-pillar umbrella with one landing page:

```
index.html          → Umbrella landing (two pillar cards)
brand.html          → Pillar 1 — Brand
system.html         → Pillar 2 — Design system
```

- **Brand** is everything that travels beyond digital: identity, voice,
  principles, logo, colour, typography, photography, iconography, merch
  templates. Used by chapter leads, event organisers, designers, partners,
  merch suppliers, printers.
- **Design system** is digital UI only: tokens, components, domain
  patterns, screen mockups, navigation rules. Used by engineers shipping
  product surfaces.

Per-stream (Events, Education, People, Accelerator) and Build-infrastructure
overrides live inside the relevant pillar — under Brand for off-screen
specifics, under Design system for product UI. There is no separate
Streams or Build pillar at the top level.

## Where new content goes

Decision tree:

- Touches print, merch, decks, posters, social, off-screen? → **Brand**
- Touches a button, component, page layout, digital pattern? → **Design
  system**
- Specific to one stream (Events / Education / People / Accelerator) or
  to Build infrastructure? → goes inside whichever pillar fits, as a
  subsection
- Doesn't fit either? Talk to Binali.

Cross-link between pillars rather than duplicate. e.g. `system.html` links
to `brand.html#colors` for tokens instead of redefining them.

## File layout

```
.
├── index.html              ← landing
├── brand.html              ← Pillar 1
├── system.html             ← Pillar 2
│
├── tokens.css              ← OKLCH tokens, shadcn-compatible. Light + dark.
├── components.css          ← buttons, inputs, badges, brand-mark slots
├── docs.css                ← page chrome shared by landing + both pillar pages
│
├── brand/
│   ├── logo-mark.svg                       ← footprint + 4 dots (navbar, favicon, compact)
│   ├── logo-full.svg                       ← footprint + AI QADAM wordmark (splash, hero)
│   └── decks/
│       └── aiqadam-speaker-template.pptx   ← PPTX skeleton, hand-maintained binary
│
├── merch/                                  ← product photos shown on brand.html#merch
│   ├── shopper.jpeg
│   ├── notepad.jpeg
│   └── pen.jpeg
│
├── speaker-deck.html       ← HTML speaker deck template (AI-friendly, semantic <section data-kind>)
│
├── LICENSE                 ← MIT — code only
├── BRAND-USE.md            ← custom Brand Usage Policy (v1)
├── LICENSE-content         ← CC BY 4.0 — docs content only
├── license.html            ← rendered LICENSE
├── brand-use.html          ← rendered BRAND-USE.md
├── license-content.html    ← rendered LICENSE-content
│
├── CNAME                   ← brand.aiqadam.org — GitHub Pages custom domain
├── robots.txt              ← allow all + explicit AI crawlers + sitemap pointer
├── sitemap.xml             ← seven public URLs with lastmod + priority
├── llms.txt                ← structured markdown index for LLM agents (llmstxt.org)
│
├── brand/og-image.svg      ← shared 1200×630 OG/Twitter Card image
│
└── scripts/
    ├── render-docs.py        ← regenerates the three legal HTML pages
    ├── bump-assets.py        ← appends ?v=<md5-8> to CSS link tags
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
  copy-pasted across the three pages (index + two pillars). If you
  change one, change all.
  The shared CSS lives in `docs.css`.
- **English in content, Russian in conversation.** The user (Binali)
  writes to AI agents in Russian. The docs at `brand.aiqadam.org` stay
  in English — localisation comes later via the "Multilingual by
  default" principle.
- **Per-page meta is non-negotiable on every HTML page.** Every public
  page must carry: unique `<meta name="description">`, OpenGraph block
  (`og:type`, `og:site_name`, `og:title`, `og:description`, `og:url`,
  `og:image`, `og:image:width`, `og:image:height`, `og:locale`), Twitter
  Card (`twitter:card=summary_large_image`, `twitter:title`,
  `twitter:description`, `twitter:image`), `<link rel="canonical">`, and
  `<meta name="theme-color" content="#3CA29E">`. Shared `og:image` is
  `brand/og-image.svg`. The canonical shape lives in
  `scripts/render-docs.py` `head()` — mirror it.
- **CSS link tags use cache-bust query strings.** Every `<link href="*.css">`
  carries a `?v=<md5-8>` suffix that `scripts/bump-assets.py` rewrites
  from current file content. Don't manually edit these — run the script.
- **Chrome elements on every pillar page.** Top-right GitHub corner
  (links to repo) and footer `aiq-build-badge` (mark + "an AI Qadam
  Build project", links to `https://build.aiqadam.org`) are part of the
  page chrome. When duplicating chrome, include both.

## Build & local dev

It's static HTML — no build for the pillar pages.

```sh
python3 -m http.server 8765
# open http://localhost:8765/
```

The HTML speaker deck (`speaker-deck.html`) and the PPTX template
(`brand/decks/aiqadam-speaker-template.pptx`) are both hand-edited —
no build needed.

## Deploy

The site is hosted on **GitHub Pages** from the `main` branch root, with
DNS via Cloudflare:

- Custom domain: `brand.aiqadam.org` (set via `CNAME` file in repo root)
- DNS: Cloudflare CNAME `brand.aiqadam.org` → `aiqadam.github.io`,
  DNS-only / grey-cloud (so GitHub's Let's Encrypt SSL provisioning works)
- HTTPS enforced via GitHub Pages settings

**Deploy sequence** when CSS or legal-doc sources have changed:

```sh
# 1. Regenerate legal pages from BRAND-USE.md / LICENSE / LICENSE-content
.venv/bin/python scripts/render-docs.py

# 2. Refresh ?v=<hash> on every CSS link in every HTML file
python3 scripts/bump-assets.py

# 3. Commit and push — GitHub Pages auto-rebuilds (~90 sec)
git add -A && git commit && git push origin main
```

Order matters: `render-docs.py` first (it rewrites the three legal HTML
files), `bump-assets.py` after (so newly-generated legal pages also get
their `?v=<hash>` query strings). HTML changes alone don't need the
script — just `git push`.

After push, check Pages status with `gh api repos/aiqadam/brand.aiqadam.org/pages`.

When **adding a new URL** to the site, update three files manually:
`sitemap.xml`, `llms.txt`, and (if a new pillar) the file layout above.

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

**`LICENSE-content` is the AI-Qadam-wide canonical text.** Other AI
Qadam repos (e.g. `build.aiqadam.org`) carry a short `LICENSE-content`
pointer file declaring CC BY 4.0 and linking to
`brand.aiqadam.org/license-content.html` for the canonical terms. Keep
the prose in `LICENSE-content` here generic across all AI Qadam
repositories — don't re-scope it to brand-only. After editing the
prose, run `scripts/render-docs.py` to regenerate
`license-content.html`; consumer repos pick up the new text
automatically through the cross-origin link.

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

- Don't add new pages above the pillar level. The umbrella is two
  pillars + one landing — that's the whole structure.
- Don't relicense brand assets — they are explicitly excluded from MIT.
- Don't AI-generate photography or imagery for the brand. The honesty
  principle applies to images too (see `brand.html#photography`).
- Don't introduce new colour tokens or fonts. The palette is one teal
  + neutrals; the families are Geist / Inter / JetBrains Mono.
- Don't add a JS framework, bundler, or build toolchain. The site is
  static on purpose — chapter leads should be able to fork and host
  without setup.
- Don't hand-edit `?v=<hash>` query strings on CSS link tags — run
  `scripts/bump-assets.py` instead. If you forget, browsers may serve
  stale CSS after deploy.
- Don't skip per-page meta when adding a new HTML page. Description,
  OG, Twitter Card, canonical, and theme-color are required — mirror
  the shape from `scripts/render-docs.py` `head()`.
- Don't push raw secrets or local-only configs. `.claude/settings.local.json`
  is already gitignored; check for Cloudflare/GitHub tokens before
  committing.
