# Build scripts

Two helpers. Both idempotent and safe to re-run.

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

## `bump-assets.py`

Adds (or refreshes) cache-bust query strings on every `<link>` to
`tokens.css`, `components.css`, `docs.css` in every HTML file in the
repo root. Version = first 8 chars of the file's MD5. If a CSS file
didn't change, its hash doesn't change, and HTML files aren't touched.

```sh
python3 scripts/bump-assets.py
```

**Run order:** always after `render-docs.py` — the generated legal pages
need their CSS links versioned too, and `render-docs.py` would overwrite
those versions if it ran second. No deps; pure stdlib.

```sh
# canonical deploy prep:
.venv/bin/python scripts/render-docs.py
python3 scripts/bump-assets.py
git add -A && git commit && git push
```
