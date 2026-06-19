# Build scripts

One helper. Safe to re-run idempotently.

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
