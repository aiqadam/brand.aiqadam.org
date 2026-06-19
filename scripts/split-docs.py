#!/usr/bin/env python3
"""
Split the legacy single-page docs (index.html) into:
  - index.html      → umbrella landing
  - brand.html      → Pillar 1
  - system.html     → Pillar 2
  - products.html   → Pillar 3

Extracts existing sections from the current index.html by line range,
then wraps each in a fresh shell (head, shared header, footer, script).
The shared chrome lives in this script so all four pages stay in sync.
"""

import re
from pathlib import Path

ROOT = Path("/Users/binali-work/projects/aiqadam/design-system")
SRC = ROOT.read_text() if False else (ROOT / "index.html").read_text()
LINES = SRC.splitlines(keepends=True)


def slice_lines(start: int, end: int) -> str:
    """1-based inclusive line range, as in editor numbering."""
    return "".join(LINES[start - 1:end])


# ----- locate sections (1-based inclusive ranges, verified by reading) -----
# Brand section ............ 827–994
# Foundation > Colors ...... 1005–1037 (the <div id="colors"> block)
# Foundation > Typography .. 1040–1084
# Foundation > Spacing ..... 1087–1102
# Foundation > Radius ...... 1105–1116
# Components section ....... 1122–END_OF_COMPONENTS
# Patterns section ......... 1359–END_OF_PATTERNS
# Mockups section .......... 1903–END_OF_MOCKUPS
# Navigation section ....... 2371–END_OF_NAVIGATION

# Programmatically find section boundaries to be robust:
def find_section_range(section_id: str) -> tuple[int, int]:
    """Find the <section ... id="..."> ... </section> line range (1-based).
    Counts every <section …> so nested non-docs sections (used inside the
    Mockups article structure, for example) don't close us early."""
    start_re = re.compile(rf'<section[^>]*id="{re.escape(section_id)}"')
    open_re = re.compile(r"<section\b")
    close_re = re.compile(r"</section>")
    start = None
    for i, line in enumerate(LINES, 1):
        if start_re.search(line):
            start = i
            break
    if start is None:
        raise SystemExit(f"section #{section_id} not found")
    depth = 1
    for j in range(start + 1, len(LINES) + 1):
        line = LINES[j - 1]
        depth += len(open_re.findall(line))
        depth -= len(close_re.findall(line))
        if depth == 0:
            return start, j
    raise SystemExit(f"unterminated section #{section_id}")


def find_div_range(div_id: str) -> tuple[int, int]:
    """Find a top-level <div id="x"> ... </div> by tracking depth."""
    start_re = re.compile(rf'<div[^>]*id="{re.escape(div_id)}"')
    start = None
    for i, line in enumerate(LINES, 1):
        if start_re.search(line):
            start = i
            break
    if start is None:
        raise SystemExit(f"div #{div_id} not found")
    depth = 1
    for j in range(start + 1, len(LINES) + 1):
        line = LINES[j - 1]
        depth += line.count("<div")
        depth -= line.count("</div>")
        if depth == 0:
            return start, j
    raise SystemExit(f"unterminated div #{div_id}")


brand_s, brand_e = find_section_range("brand")
colors_s, colors_e = find_div_range("colors")
type_s, type_e = find_div_range("typography")
space_s, space_e = find_div_range("spacing")
radius_s, radius_e = find_div_range("radius")
comp_s, comp_e = find_section_range("components")
pat_s, pat_e = find_section_range("patterns")
mock_s, mock_e = find_section_range("mockups")
nav_s, nav_e = find_section_range("navigation")


# Strip leading indentation by trimming 4 leading spaces uniformly (best-effort,
# only when every non-empty line starts with that prefix). Otherwise pass through.
def dedent_block(text: str, n: int = 4) -> str:
    prefix = " " * n
    out = []
    for line in text.splitlines(keepends=True):
        if line.startswith(prefix):
            out.append(line[n:])
        elif line.strip() == "":
            out.append(line)
        else:
            return text  # bail out — irregular indent
    return "".join(out)


brand_html = slice_lines(brand_s, brand_e)
colors_html = slice_lines(colors_s, colors_e)
typo_html = slice_lines(type_s, type_e)
spacing_html = slice_lines(space_s, space_e)
radius_html = slice_lines(radius_s, radius_e)
components_html = slice_lines(comp_s, comp_e)
patterns_html = slice_lines(pat_s, pat_e)
mockups_html = slice_lines(mock_s, mock_e)
navigation_html = slice_lines(nav_s, nav_e)


# ----- shared chrome -----

def head(title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="brand/logo-mark.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components.css">
<link rel="stylesheet" href="docs.css">
</head>
<body>
"""


def header(active: str, suffix: str) -> str:
    """active ∈ {'index','brand','system','products'}"""
    nav_items = [
        ("index.html", "Overview", "index"),
        ("brand.html", "Brand", "brand"),
        ("system.html", "Design system", "system"),
        ("products.html", "Products", "products"),
    ]
    nav_html = "\n      ".join(
        f'<a href="{href}"{" class=\"active\"" if key == active else ""}>{label}</a>'
        for href, label, key in nav_items
    )
    return f"""<header class="app-header">
  <div class="container app-header-inner">
    <a href="index.html" class="brand">
      <span class="brand-mark logo" aria-hidden="true">
        <img src="brand/logo-mark.svg" alt="">
      </span>
      AI Qadam
      <span class="brand-suffix">{suffix}</span>
    </a>
    <nav class="app-nav">
      {nav_html}
    </nav>
    <div class="header-right">
      <button class="btn btn-ghost btn-icon" id="theme-toggle" aria-label="Toggle theme" title="Toggle theme">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
      </button>
    </div>
  </div>
</header>

<a id="top"></a>

"""


FOOTER = """<footer class="doc-footer">
  <div class="container">
    <div class="row">AI Qadam Brand Guidelines · v1 · last updated 2026-06-19</div>
    <div class="row">
      <a href="license.html">Code · MIT</a>
      &nbsp;·&nbsp;
      <a href="brand-use.html">Brand · © AI Qadam — usage policy</a>
      &nbsp;·&nbsp;
      <a href="license-content.html">Content · CC BY 4.0</a>
    </div>
    <div class="row"><a href="https://aiqadam.org">aiqadam.org</a> · <a href="mailto:binali.rustamov@aiqadam.org">binali.rustamov@aiqadam.org</a></div>
  </div>
</footer>
"""


SCRIPT = """<script>
  // Theme toggle ----------------------------------------------------
  const root = document.documentElement;
  const btn = document.getElementById('theme-toggle');
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem('aiqadam-ds-theme', theme); } catch(e){}
    const state = document.getElementById('theme-state');
    if (state) state.textContent = theme;
  }
  (function init(){
    const saved = localStorage.getItem('aiqadam-ds-theme');
    if (saved === 'light' || saved === 'dark') applyTheme(saved);
  })();
  if (btn) btn.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  });

  // Resolve --token values onto swatches (only present on brand.html) ------
  document.querySelectorAll('[data-token]').forEach(el => {
    const t = el.getAttribute('data-token');
    const v = getComputedStyle(root).getPropertyValue(t).trim();
    if (v) el.textContent = v;
  });
</script>
</body>
</html>
"""


# ============================================================
# index.html — umbrella landing
# ============================================================
INDEX = head("AI Qadam Brand Guidelines") + header("index", "guidelines / v1") + """<div class="container">
  <section class="doc-hero">
    <h1>AI Qadam Brand Guidelines</h1>
    <p class="tagline">The shared visual and verbal foundation across every AI Qadam product — Events, Build, People, Education, Chapters, and Merch. Use these pages to design, write, and ship on-brand.</p>
    <div class="meta-row">
      <span class="item">v1 · 2026-06</span>
      <span class="item">UZ · KZ · KG · TJ · Turkic world</span>
      <span class="item">Dark-first · Light verified</span>
      <span class="item">EN · RU · UZ · KZ</span>
    </div>
  </section>

  <section style="padding: 24px 0 32px;">
    <div class="umbrella-grid">
      <a href="brand.html" class="umbrella-card">
        <p class="pillar-num">Pillar 01</p>
        <h2 class="pillar-name">Brand</h2>
        <p class="pillar-desc">Identity, voice, principles, logo system, colour, typography, photography, iconography, and merch templates. Everything that travels beyond digital — to decks, print, swag, and stage.</p>
        <div class="pillar-tags">
          <span class="tag">Logo</span>
          <span class="tag">Voice</span>
          <span class="tag">Colour</span>
          <span class="tag">Type</span>
          <span class="tag">Merch</span>
        </div>
        <span class="pillar-go">Read the brand →</span>
      </a>
      <a href="system.html" class="umbrella-card">
        <p class="pillar-num">Pillar 02</p>
        <h2 class="pillar-name">Design system</h2>
        <p class="pillar-desc">Tokens, components, domain patterns, screen mockups, and navigation rules. The product UI vocabulary — for the portal, Build, and any digital surface a chapter ships.</p>
        <div class="pillar-tags">
          <span class="tag">Tokens</span>
          <span class="tag">Components</span>
          <span class="tag">Patterns</span>
          <span class="tag">Mockups</span>
        </div>
        <span class="pillar-go">Open the system →</span>
      </a>
      <a href="products.html" class="umbrella-card">
        <p class="pillar-num">Pillar 03</p>
        <h2 class="pillar-name">Products</h2>
        <p class="pillar-desc">Per-product surfaces under the AI Qadam umbrella — Events, Build, People, Education, Chapters, Merch. Each gets its own brand specifics on top of the shared system.</p>
        <div class="pillar-tags">
          <span class="tag">Events</span>
          <span class="tag">Build</span>
          <span class="tag">People</span>
          <span class="tag">Education</span>
          <span class="tag">Merch</span>
        </div>
        <span class="pillar-go">See products →</span>
      </a>
    </div>

    <div class="landing-meta">
      <div>
        <h4>Who this is for</h4>
        <p>Chapter leads, partners, designers, engineers, event organisers, and anyone producing AI Qadam-branded materials. If you're touching the name, the logo, or the colour, you're in the right place.</p>
      </div>
      <div>
        <h4>How to use</h4>
        <p>Read Brand first — it sets the meaning. Then go to Design system for product UI, or Products for surface-specific rules. When in doubt, default to honesty over hype.</p>
      </div>
      <div>
        <h4>Hosted at</h4>
        <p><span class="codechip">brand.aiqadam.org</span> — single source of truth across the umbrella. Cross-link to it from every chapter site and partner deck.</p>
      </div>
    </div>
  </section>
</div>

""" + FOOTER + SCRIPT


# ============================================================
# brand.html — Pillar 1
# ============================================================
BRAND_BODY = """<div class="container">
  <section class="doc-hero">
    <h1>Brand</h1>
    <p class="tagline">Who we are, how we sound, how we look. Pillar 1 of the AI Qadam guidelines — applies everywhere, from a Telegram post to a printed conference badge.</p>
    <div class="meta-row">
      <span class="item"><a href="index.html" style="color: var(--primary);">← Guidelines overview</a></span>
      <span class="item">Pillar 01</span>
      <span class="item">Last updated 2026-06-19</span>
    </div>
  </section>

  <div class="toc-layout">
    <aside class="toc" aria-label="Table of contents">
      <p class="toc-label">In this pillar</p>
      <a href="#brand" class="section">Brand</a>
      <a href="#identity" class="sub">Identity</a>
      <a href="#logo" class="sub">Logo</a>
      <a href="#brand-color" class="sub">Brand colour</a>
      <a href="#voice" class="sub">Voice &amp; principles</a>
      <a href="#wordmark" class="sub">Writing the name</a>

      <a href="#palette" class="section">Colour palette</a>
      <a href="#colors" class="sub">Tokens</a>

      <a href="#type" class="section">Typography</a>
      <a href="#typography" class="sub">Scale &amp; specimens</a>

      <a href="#photography" class="section">Photography</a>
      <a href="#iconography" class="section">Iconography</a>
      <a href="#merch" class="section">Merch templates</a>
    </aside>

    <main>
"""

# Brand section + Colors + Typography + stubs
brand_extracted = brand_html
colors_extracted = colors_html
typo_extracted = typo_html

# Wrap colors and typography in their own docs-section frames so they read
# as proper subsections within brand.html.
PALETTE_SECTION = f"""      <section class="docs-section" id="palette">
        <p class="section-eyebrow">02 — Colour palette</p>
        <h2 class="section-title display">Colour, by surface and role.</h2>
        <p class="section-lead">Brand teal is the only colour with brand meaning. Everything else is a neutral scale plus four semantic accents (success, warning, destructive, live). Tokens are normative — don't invent new ones.</p>

{colors_extracted}      </section>

"""

TYPE_SECTION = f"""      <section class="docs-section" id="type">
        <p class="section-eyebrow">03 — Typography</p>
        <h2 class="section-title display">Three families, one voice.</h2>
        <p class="section-lead">Geist for display (titles, hero, brand). Inter for everything you read in a paragraph. JetBrains Mono for technical detail (times, IDs, tags). Both Cyrillic and Latin must read equally well — Central Asia uses both.</p>

{typo_extracted}      </section>

"""

PHOTO_SECTION = """      <section class="docs-section" id="photography">
        <p class="section-eyebrow">04 — Photography</p>
        <h2 class="section-title display">Real rooms, real people.</h2>
        <p class="section-lead">Photography for AI Qadam is documentary, not staged. Real speakers mid-sentence, real laptops, real Q&amp;A hands going up. Avoid stock-AI tropes (blue circuit brains, white robots, glowing data orbs). The honesty principle applies to images too.</p>

        <p class="subsection-meta">Style guidelines — draft</p>
        <div class="photo-grid">
          <div class="photo-cell"><span class="photo-label">Documentary · meetup floor</span></div>
          <div class="photo-cell"><span class="photo-label">Speaker mid-slide · natural light</span></div>
          <div class="photo-cell"><span class="photo-label">Hands &amp; laptops · close crop</span></div>
          <div class="photo-cell"><span class="photo-label">Room wide · audience visible</span></div>
        </div>

        <p class="subsection-meta" style="margin-top: 32px;">Don't</p>
        <div class="dont-grid">
          <div class="dont-cell"><span class="dont-mark">✕</span><p>No AI-generated humans, robots, brain graphics, or glowing-data backgrounds.</p></div>
          <div class="dont-cell"><span class="dont-mark">✕</span><p>No corporate handshake shots, staged smiles, or empty boardroom posing.</p></div>
          <div class="dont-cell"><span class="dont-mark">✕</span><p>No heavy filters, vignettes, or duotone overlays — keep the colour honest.</p></div>
          <div class="dont-cell"><span class="dont-mark">✕</span><p>No watermarks. Photographer credit goes in caption, not on the image.</p></div>
        </div>

        <p class="subsection-meta" style="margin-top: 32px;">Photo library</p>
        <div class="brand-card" style="background: var(--card); border: 1px dashed var(--border);">
          <p class="brand-positioning" style="font-size: 18px;">Coming soon — curated photo bank for chapter leads &amp; partners.</p>
          <p class="brand-tagline" style="font-style: normal;">After Meetup #2 (June 20, 2026) we'll publish the first batch. Until then, ask the country lead for raw assets.</p>
        </div>
      </section>

"""

ICON_SECTION = """      <section class="docs-section" id="iconography">
        <p class="section-eyebrow">05 — Iconography</p>
        <h2 class="section-title display">Lucide line · brand teal for accents.</h2>
        <p class="section-lead">Product UI uses <a href="https://lucide.dev" style="color: var(--primary); border-bottom: 1px solid currentColor;">Lucide</a> at 2px stroke, 24×24 viewBox. For brand surfaces (decks, merch, posters) the footprint-with-dots motif from the logo is the only allowed pictogram — never duplicate it; never substitute it.</p>

        <p class="subsection-meta">Product iconography — line, 2px stroke</p>
        <div class="icon-grid">
          <div class="icon-cell"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/></svg><span>Event</span></div>
          <div class="icon-cell"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg><span>Community</span></div>
          <div class="icon-cell"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 8-6 4 6 4V8Z"/><rect x="2" y="6" width="14" height="12" rx="2"/></svg><span>Talk</span></div>
          <div class="icon-cell"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg><span>Build</span></div>
          <div class="icon-cell"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg><span>Edit</span></div>
          <div class="icon-cell"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg><span>Chapter</span></div>
        </div>

        <p class="subsection-meta" style="margin-top: 32px;">Rules</p>
        <div class="dont-grid">
          <div class="dont-cell"><span class="dont-mark">✕</span><p>Don't fill brand-mark dots into other icons. The four-dot motif lives in the logo only.</p></div>
          <div class="dont-cell"><span class="dont-mark">✕</span><p>Don't mix icon families. Lucide everywhere; never Heroicons + Phosphor + Lucide in one surface.</p></div>
          <div class="dont-cell"><span class="dont-mark">✕</span><p>Don't recolour icons. Inherit <span class="codechip">currentColor</span> from text.</p></div>
        </div>
      </section>

"""

MERCH_SECTION = """      <section class="docs-section" id="merch">
        <p class="section-eyebrow">06 — Merch templates</p>
        <h2 class="section-title display">Wearables, swag, print.</h2>
        <p class="section-lead">Merch is brand made tangible — the highest-stakes surface for our visual identity. Every item ships from one of the templates below. Don't deviate; don't add taglines that aren't in the approved list.</p>

        <p class="subsection-meta">Approved formats</p>
        <div class="streams-grid">
          <div class="stream-card draft">
            <span class="stream-status">Template</span>
            <h4 class="stream-name">T-shirt</h4>
            <p class="stream-desc">Black or off-white only. Full lockup on the chest, centred, ~30% of front width. Back is bare or carries a single line in mono: <span class="codechip">#AIQadam</span> or the meetup hashtag.</p>
            <div class="stream-uses"><span class="codechip">Cotton 180g+</span><span class="codechip">Screen print</span></div>
          </div>
          <div class="stream-card draft">
            <span class="stream-status">Template</span>
            <h4 class="stream-name">Sticker — die-cut mark</h4>
            <p class="stream-desc">The footprint silhouette only, in brand teal on a white peelable backing. 40mm or 70mm. No wordmark on small stickers — it becomes unreadable.</p>
            <div class="stream-uses"><span class="codechip">Vinyl</span><span class="codechip">Glossy</span></div>
          </div>
          <div class="stream-card draft">
            <span class="stream-status">Template</span>
            <h4 class="stream-name">Conference badge</h4>
            <p class="stream-desc">A6 portrait. Full lockup top-centre. Name in Geist 36, role in Inter 14 muted, optional org in mono 11. Lanyard hole 5mm centred. One QR code bottom-right.</p>
            <div class="stream-uses"><span class="codechip">300gsm matte</span></div>
          </div>
          <div class="stream-card draft">
            <span class="stream-status">Template</span>
            <h4 class="stream-name">Poster · A2</h4>
            <p class="stream-desc">Dark background. Hero in Geist 96. Event meta in mono. Lockup bottom-right, never bottom-centre. Use the photo bank for backgrounds — never AI-generated imagery.</p>
            <div class="stream-uses"><span class="codechip">A2 · 420×594mm</span></div>
          </div>
        </div>

        <div class="brand-card" style="margin-top: 32px; background: var(--card); border: 1px dashed var(--border);">
          <p class="brand-positioning" style="font-size: 18px;">Print-ready files — request from your country lead.</p>
          <p class="brand-tagline" style="font-style: normal;">CMYK PDF/X-1a originals for each template will land here once the first batches ship (T-shirts at Meetup #2). Until then: brand teal prints as Pantone <span class="codechip">7716 C</span> for safe colour-matching across suppliers.</p>
        </div>
      </section>

"""

BRAND_HTML = (
    head("Brand · AI Qadam Guidelines")
    + header("brand", "brand / v1")
    + BRAND_BODY
    + brand_extracted
    + "\n"
    + PALETTE_SECTION
    + TYPE_SECTION
    + PHOTO_SECTION
    + ICON_SECTION
    + MERCH_SECTION
    + """    </main>
  </div>
</div>

"""
    + FOOTER
    + SCRIPT
)


# ============================================================
# system.html — Pillar 2
# ============================================================
SYSTEM_BODY = """<div class="container">
  <section class="doc-hero">
    <h1>Design system</h1>
    <p class="tagline">Tokens, components, patterns, and screen mockups for AI Qadam product surfaces — the portal, Build, chapter sites, and any digital surface a chapter ships. Pillar 2 of the guidelines.</p>
    <div class="meta-row">
      <span class="item"><a href="index.html" style="color: var(--primary);">← Guidelines overview</a></span>
      <span class="item">Pillar 02</span>
      <span class="item">Tailwind 4 + shadcn/ui</span>
      <span class="item">OKLCH color space</span>
    </div>
  </section>

  <div class="toc-layout">
    <aside class="toc" aria-label="Table of contents">
      <p class="toc-label">In this pillar</p>
      <a href="#foundation" class="section">Foundation</a>
      <a href="#spacing" class="sub">Spacing</a>
      <a href="#radius" class="sub">Radius</a>

      <a href="#components" class="section">Components</a>
      <a href="#buttons" class="sub">Buttons</a>
      <a href="#inputs" class="sub">Inputs</a>
      <a href="#badges-tags" class="sub">Badges &amp; tags</a>
      <a href="#avatars" class="sub">Avatars</a>
      <a href="#controls" class="sub">Checkbox / Radio / Switch</a>
      <a href="#tooltip-skeleton" class="sub">Tooltip / Skeleton</a>

      <a href="#patterns" class="section">Domain patterns</a>
      <a href="#event-card" class="sub">EventCard</a>
      <a href="#speaker-card" class="sub">SpeakerCard</a>
      <a href="#leaderboard" class="sub">LeaderboardRow</a>
      <a href="#badge-showcase" class="sub">BadgeShowcase</a>
      <a href="#stat-card" class="sub">StatCard</a>
      <a href="#activity" class="sub">ActivityFeedItem</a>
      <a href="#empty" class="sub">EmptyState</a>

      <a href="#mockups" class="section">Mockups</a>
      <a href="#country-home" class="sub">Country homepage</a>
      <a href="#event-page" class="sub">Event detail</a>
      <a href="#profile-page" class="sub">User profile</a>

      <a href="#navigation" class="section">Navigation</a>

      <p class="toc-label" style="margin-top: 24px;">Related</p>
      <a href="brand.html#colors" class="sub">Colour tokens →</a>
      <a href="brand.html#typography" class="sub">Type scale →</a>
    </aside>

    <main>
      <section class="docs-section" id="foundation">
        <p class="section-eyebrow">01 — Foundation</p>
        <h2 class="section-title display">Spacing &amp; radius</h2>
        <p class="section-lead">Colour and typography live in <a href="brand.html#palette" style="color: var(--primary); border-bottom: 1px solid currentColor;">Brand</a> — they apply everywhere, not just to digital. Below: the two foundation primitives that only matter inside a UI.</p>

""" + spacing_html + "\n" + radius_html + """      </section>

"""

SYSTEM_HTML = (
    head("Design system · AI Qadam Guidelines")
    + header("system", "design system / v1")
    + SYSTEM_BODY
    + components_html
    + "\n"
    + patterns_html
    + "\n"
    + mockups_html
    + "\n"
    + navigation_html
    + """
    </main>
  </div>
</div>

"""
    + FOOTER
    + SCRIPT
)


# ============================================================
# products.html — Pillar 3
# ============================================================
PRODUCTS_BODY = """<div class="container">
  <section class="doc-hero">
    <h1>Products</h1>
    <p class="tagline">The surfaces that already carry AI Qadam identity. Each one is a real or in-progress product under the umbrella — with its own brand specifics layered on top of the shared system. Pillar 3.</p>
    <div class="meta-row">
      <span class="item"><a href="index.html" style="color: var(--primary);">← Guidelines overview</a></span>
      <span class="item">Pillar 03</span>
      <span class="item">Stubs — fills in as products mature</span>
    </div>
  </section>

  <section style="padding: 24px 0 64px;">
    <p class="subsection-meta" style="margin-bottom: 16px;">Streams from the partnership deck</p>
    <div class="streams-grid">
      <div class="stream-card live">
        <span class="stream-status">Live</span>
        <h3 class="stream-name">Events</h3>
        <p class="stream-desc">Meetups, Fuck-Up Nights, hackathons — the engine of the community. Real cases, real practitioners. Lead: Viktor Drukker.</p>
        <div class="stream-uses">
          <span class="codechip">Mark · navbar</span>
          <span class="codechip">Full · poster</span>
          <span class="codechip">Hashtag</span>
        </div>
        <span class="stream-link">Guidelines coming →</span>
      </div>

      <div class="stream-card draft">
        <span class="stream-status">Roadmap</span>
        <h3 class="stream-name">Build</h3>
        <p class="stream-desc">The accelerator. Turns advanced builders into companies — engineering, grants, investor access. Surfaces: web portal, application flow, partner portal.</p>
        <div class="stream-uses">
          <span class="codechip">Design system</span>
          <span class="codechip">Pitch decks</span>
        </div>
        <span class="stream-link">Guidelines coming →</span>
      </div>

      <div class="stream-card draft">
        <span class="stream-status">In progress</span>
        <h3 class="stream-name">People — Suhbat</h3>
        <p class="stream-desc">Community-led social projects. First initiative: Suhbat, an AI-assisted anonymous mental-health support tool. Ethics-first surface design.</p>
        <div class="stream-uses">
          <span class="codechip">Mobile</span>
          <span class="codechip">Tone: gentle</span>
        </div>
        <span class="stream-link">Guidelines coming →</span>
      </div>

      <div class="stream-card draft">
        <span class="stream-status">Roadmap</span>
        <h3 class="stream-name">Education</h3>
        <p class="stream-desc">Honest skill assessment and practitioner-built programs. Surfaces: course pages, certificates, assessment tooling.</p>
        <div class="stream-uses">
          <span class="codechip">Mark · cert</span>
          <span class="codechip">Type · long-form</span>
        </div>
        <span class="stream-link">Guidelines coming →</span>
      </div>

      <div class="stream-card live">
        <span class="stream-status">Live · UZ · KZ</span>
        <h3 class="stream-name">Chapters</h3>
        <p class="stream-desc">Federation of country chapters under one brand. Each chapter localises language and partners; the brand itself stays the same. UZ active, KZ launching June 2026, KG/TJ on the roadmap.</p>
        <div class="stream-uses">
          <span class="codechip">uz.aiqadam.com</span>
          <span class="codechip">kz.aiqadam.com</span>
        </div>
        <span class="stream-link">Chapter playbook coming →</span>
      </div>

      <div class="stream-card draft">
        <span class="stream-status">Template</span>
        <h3 class="stream-name">Merch</h3>
        <p class="stream-desc">T-shirts, stickers, badges, posters — the wearable and printable side of the brand. Templates live in <a href="brand.html#merch" style="color: var(--primary); border-bottom: 1px solid currentColor;">Brand → Merch</a>.</p>
        <div class="stream-uses">
          <span class="codechip">Print-ready</span>
          <span class="codechip">CMYK</span>
        </div>
        <a href="brand.html#merch" class="stream-link">Open templates →</a>
      </div>
    </div>

    <div class="landing-meta" style="margin-top: 64px;">
      <div>
        <h4>Got a product to add?</h4>
        <p>If you're a chapter lead or partner shipping something that uses AI Qadam identity, ping Binali. We'll add a card here and write its specifics.</p>
      </div>
      <div>
        <h4>What lives in a product page</h4>
        <p>Surface-specific brand notes: tone overrides (Education is more formal, People is gentler), accent overlays (chapter colours on top of brand teal), and print/screen template variants.</p>
      </div>
      <div>
        <h4>What doesn't</h4>
        <p>The logo, the wordmark, the brand teal — those never change per product. If you want a different mark, you want a different brand.</p>
      </div>
    </div>
  </section>
</div>

"""

PRODUCTS_HTML = (
    head("Products · AI Qadam Guidelines")
    + header("products", "products / v1")
    + PRODUCTS_BODY
    + FOOTER
    + SCRIPT
)


# ============================================================
# write all four files
# ============================================================
(ROOT / "index.html").write_text(INDEX)
(ROOT / "brand.html").write_text(BRAND_HTML)
(ROOT / "system.html").write_text(SYSTEM_HTML)
(ROOT / "products.html").write_text(PRODUCTS_HTML)

print(f"index.html    -> {len(INDEX)} bytes")
print(f"brand.html    -> {len(BRAND_HTML)} bytes")
print(f"system.html   -> {len(SYSTEM_HTML)} bytes")
print(f"products.html -> {len(PRODUCTS_HTML)} bytes")
print()
print("section ranges located:")
print(f"  brand:      {brand_s}-{brand_e}")
print(f"  colors:     {colors_s}-{colors_e}")
print(f"  typography: {type_s}-{type_e}")
print(f"  spacing:    {space_s}-{space_e}")
print(f"  radius:     {radius_s}-{radius_e}")
print(f"  components: {comp_s}-{comp_e}")
print(f"  patterns:   {pat_s}-{pat_e}")
print(f"  mockups:    {mock_s}-{mock_e}")
print(f"  navigation: {nav_s}-{nav_e}")
