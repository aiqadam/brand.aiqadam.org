#!/usr/bin/env python3
"""
Bump cache-bust query strings on CSS asset links in all HTML files.

Computes an 8-char content hash of each tracked CSS file and rewrites
every `<link rel="stylesheet" href="<file>">` (with or without an existing
?v=... query) to use that hash.

Run before commit when CSS has changed. If a file's content didn't
change, its hash stays the same and HTML files won't be touched.

Run order: this script must run AFTER any HTML generator (e.g.
render-docs.py) so the cache-bust is applied to generated files too.

Idempotent. Safe to re-run.
"""

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ASSETS = ["tokens.css", "components.css", "docs.css"]


def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()[:8]


def main() -> int:
    versions = {}
    for a in ASSETS:
        p = ROOT / a
        if not p.exists():
            print(f"  WARN: {a} not found, skipping", file=sys.stderr)
            continue
        versions[a] = file_hash(p)

    html_files = sorted(ROOT.glob("*.html"))
    changed = 0
    for hf in html_files:
        src = hf.read_text(encoding="utf-8")
        new = src
        for asset, ver in versions.items():
            pattern = re.compile(
                rf'href="({re.escape(asset)})(?:\?v=[^"]*)?"'
            )
            new = pattern.sub(rf'href="\1?v={ver}"', new)
        if new != src:
            hf.write_text(new, encoding="utf-8")
            changed += 1
            print(f"  updated {hf.name}")

    print()
    print(f"scanned {len(html_files)} HTML files · updated {changed}")
    print("asset versions:")
    for a, v in versions.items():
        print(f"  {a}: ?v={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
