#!/usr/bin/env python3
"""
Post-process Jekyll build output to add lazy loading and async decoding to images.
Adds loading="lazy" and decoding="async" to <img> tags for faster initial page load.
Images are only loaded when they scroll into view.
"""

import re
import sys
from pathlib import Path

SITE_DIR = Path("_site")


def process_html(html: str) -> str:
    """Add loading and decoding attributes to img tags that don't have them."""
    # Match <img ...> - add loading="lazy" decoding="async" if not present
    # Skip if already has loading= (e.g. loading="eager" for LCP image)
    def replace_img(match):
        tag = match.group(0)
        if "loading=" in tag:
            return tag  # Already has loading, don't change
        # Insert before closing > or />
        if "decoding=" in tag:
            suffix = ' loading="lazy"'
        else:
            suffix = ' loading="lazy" decoding="async"'
        tag = re.sub(r'(\s*)(/?)\s*>', suffix + r'\1\2>', tag, count=1)
        return tag

    return re.sub(r'<img\s[^>]*>', replace_img, html, flags=re.IGNORECASE | re.DOTALL)


def process_file(filepath: Path) -> bool:
    """Process a single HTML file. Returns True if modified."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Skip {filepath}: {e}", file=sys.stderr)
        return False

    new_content = process_html(content)
    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return True
    return False


def main():
    if not SITE_DIR.exists():
        print(f"Directory {SITE_DIR} not found. Run 'jekyll build' first.")
        sys.exit(1)

    modified = 0
    for html_file in SITE_DIR.rglob("*.html"):
        if process_file(html_file):
            modified += 1
            print(f"Updated: {html_file}")

    if modified:
        print(f"\nAdded lazy loading to images in {modified} file(s)")
    else:
        print("No files needed updates")


if __name__ == "__main__":
    main()
