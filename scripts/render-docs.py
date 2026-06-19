#!/usr/bin/env python3
"""
Render the three legal artefacts into browser-readable HTML pages
that share the AI Qadam Brand Guidelines chrome.

  BRAND-USE.md     → brand-use.html       (markdown rendered)
  LICENSE          → license.html         (plain text in <pre>)
  LICENSE-content  → license-content.html (plain text in <pre>)

The .md / plain-text files stay as source of truth — re-run this
script whenever they change.
"""

import html
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Shared chrome — same shape as the docs pages, no nav (legal docs are leaf)
# ---------------------------------------------------------------------------

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


def header() -> str:
    return """<header class="app-header">
  <div class="container app-header-inner">
    <a href="index.html" class="brand">
      <span class="brand-mark logo" aria-hidden="true">
        <img src="brand/logo-mark.svg" alt="">
      </span>
      AI Qadam
      <span class="brand-suffix">legal / v1</span>
    </a>
    <nav class="app-nav">
      <a href="index.html">Overview</a>
      <a href="brand.html">Brand</a>
      <a href="system.html">Design system</a>
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
    <div class="row"><a href="https://aiqadam.org">aiqadam.org</a> · <a href="mailto:brand@aiqadam.org">brand@aiqadam.org</a></div>
  </div>
</footer>
"""


SCRIPT = """<script>
  const root = document.documentElement;
  const btn = document.getElementById('theme-toggle');
  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    try { localStorage.setItem('aiqadam-ds-theme', theme); } catch(e){}
  }
  (function init(){
    const saved = localStorage.getItem('aiqadam-ds-theme');
    if (saved === 'light' || saved === 'dark') applyTheme(saved);
  })();
  if (btn) btn.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  });
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def hero(title: str, lead: str, source_file: str, eyebrow: str) -> str:
    return f"""<div class="container">
  <section class="doc-hero">
    <p class="section-eyebrow" style="color: var(--primary); margin-bottom: 12px;">{html.escape(eyebrow)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="tagline">{lead}</p>
    <div class="meta-row">
      <span class="item"><a href="index.html" style="color: var(--primary);">← Guidelines overview</a></span>
      <span class="item">
        <a class="download-link" href="{source_file}" download>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>
          Download {source_file}
        </a>
      </span>
    </div>
  </section>

"""


HERO_CLOSE = """</div>

"""


def md_page(md_path: Path, out: Path, title: str, lead: str, eyebrow: str):
    src = md_path.read_text()
    body = markdown.markdown(
        src,
        extensions=["extra", "tables", "sane_lists", "toc"],
        output_format="html5",
    )
    page = (
        head(title)
        + header()
        + hero(title, lead, md_path.name, eyebrow)
        + f'<article class="legal-doc">\n{body}\n</article>\n'
        + HERO_CLOSE
        + FOOTER
        + SCRIPT
    )
    out.write_text(page)
    print(f"{out.name:25} ← {md_path.name:18} ({len(page):>6} bytes)")


def text_page(txt_path: Path, out: Path, title: str, lead: str, eyebrow: str):
    src = html.escape(txt_path.read_text())
    page = (
        head(title)
        + header()
        + hero(title, lead, txt_path.name, eyebrow)
        + f'<article class="legal-doc plain"><pre>{src}</pre></article>\n'
        + HERO_CLOSE
        + FOOTER
        + SCRIPT
    )
    out.write_text(page)
    print(f"{out.name:25} ← {txt_path.name:18} ({len(page):>6} bytes)")


# ---------------------------------------------------------------------------
# Render the three legal artefacts
# ---------------------------------------------------------------------------

md_page(
    ROOT / "BRAND-USE.md",
    ROOT / "brand-use.html",
    "Brand Usage Policy",
    "How the AI Qadam name, marks, wordmark, four-dot motif and brand teal may be used — and how they may not. Sits alongside the MIT code licence and CC BY 4.0 content licence as one of three legal artefacts at the foot of every page.",
    "Legal · Brand",
)

text_page(
    ROOT / "LICENSE",
    ROOT / "license.html",
    "Code · MIT Licence",
    "The MIT licence covering the source code in this repository — CSS, HTML markup, JavaScript, and build scripts. Brand assets and editorial content are licensed separately.",
    "Legal · Code",
)

text_page(
    ROOT / "LICENSE-content",
    ROOT / "license-content.html",
    "Content · CC BY 4.0",
    "Creative Commons Attribution 4.0 International licence for the editorial prose — the manifesto excerpts, examples and explanations that read like sentences. Brand assets and source code are licensed separately.",
    "Legal · Content",
)
