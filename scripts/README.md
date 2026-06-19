# Build scripts

Two helpers; both safe to re-run idempotently.

## `split-docs.py`

Reconstructs `index.html`, `brand.html`, `system.html`, `products.html`
from the legacy single-page source. Currently kept for reference and
in case we ever need to re-extract sections from a fresh `index.html`
backup — the pillar pages are now hand-edited, so don't run this without
backing up first.

```sh
python3 scripts/split-docs.py
```

## `render-docs.py`

Converts the three legal artefacts into browser-readable HTML:

```
BRAND-USE.md    → brand-use.html         (markdown rendered)
LICENSE         → license.html           (plain text in <pre>)
LICENSE-content → license-content.html   (plain text in <pre>)
```

Re-run after editing any of the source files. Needs Python `markdown`
package (`pip install markdown`); a venv works fine — anything outside
PEP 668's protected system Python.

```sh
python3 -m venv .venv
.venv/bin/pip install markdown
.venv/bin/python scripts/render-docs.py
```
