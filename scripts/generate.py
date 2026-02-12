#!/usr/bin/env python3
"""
Generate blog content from GitHub issues and run article optimizations.

This script (run in generate phase):
- Fetches open issues with blog label, generates README.md and post .md files
- Auto-links bare URLs in posts (wrap in angle brackets for Kramdown)

Build phase (Jekyll + add_image_attrs) runs separately – add_image_attrs
modifies built HTML in _site/, so it must run after jekyll build (see deploy.yml).
"""

import json
import logging
import re
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO)

GH = "gh"
POSTS_DIR = Path("posts")
LABELS = set(["blog"])
TIMEOUT = 20

# --- Autolink: wrap bare URLs for Kramdown ---
URL_PATTERN = re.compile(r"(https?://[^\s<>\)\]\]]+)", re.IGNORECASE)


def _wrap_bare_urls_in_content(content: str) -> str:
    """Wrap bare URLs in angle brackets, skipping those in links/attributes."""
    lines = content.split("\n")
    result = []
    for line in lines:
        placeholder_map = {}
        pid = [0]

        def protect(m):
            u = m.group(1)
            k = f"__AUTOLINK_{pid[0]}__"
            placeholder_map[k] = u
            pid[0] += 1
            return f"]({k})"

        s = re.sub(r"\]\((https?://[^\)]+)\)", protect, line)

        # Fix src="<url>" or href="<url>"
        s = re.sub(r'(src|href)=["\']<(https?://[^"\']+)>["\']', r'\1="\2"', s)
        s = re.sub(r'(src|href)=["\']<(https?://[^"\']+)["\']>', r'\1="\2"', s)

        def protect_attr(m):
            a, u = m.group(1), m.group(2)
            k = f"__AUTOLINK_{pid[0]}__"
            placeholder_map[k] = f'{a}="{u}"'
            pid[0] += 1
            return k

        s = re.sub(r'(src|href)=["\'](https?://[^"\']+)["\']', protect_attr, s)

        def protect_angle(m):
            u = m.group(1)
            k = f"__AUTOLINK_{pid[0]}__"
            placeholder_map[k] = f"<{u}>"
            pid[0] += 1
            return k

        s = re.sub(r"<((?:https?://[^>]+))>", protect_angle, s)
        s = URL_PATTERN.sub(lambda m: f"<{m.group(1)}>", s)
        for k, v in placeholder_map.items():
            s = s.replace(k, v)
        result.append(s)
    return "\n".join(result)


def _autolink_article(filepath: Path) -> bool:
    """Apply autolink to one article. Returns True if modified."""
    text = filepath.read_text(encoding="utf-8")
    parts = text.split("\n---\n", 2)
    if len(parts) < 2:
        new_text = _wrap_bare_urls_in_content(text)
    else:
        if len(parts) == 2:
            fm, body = parts[0] + "\n---\n", parts[1]
        else:
            fm = parts[0] + "\n---\n" + parts[1] + "\n---\n"
            body = parts[2]
        new_text = fm + _wrap_bare_urls_in_content(body)
    if new_text != text:
        filepath.write_text(new_text, encoding="utf-8")
        return True
    return False


def run_autolink() -> int:
    """Run autolink on all posts. Returns count of modified files."""
    if not POSTS_DIR.exists():
        return 0
    n = 0
    for f in sorted(POSTS_DIR.glob("*.md")):
        if _autolink_article(f):
            n += 1
            logging.info("autolink: %s", f.name)
    return n


def main():
    ## 1. find all issues with specific labels
    issues_json = subprocess.check_output(
        "gh issue list --state open --json title,url,author,number,labels,updatedAt,createdAt",
        shell=True,
        timeout=TIMEOUT,
    )
    logging.info("issues_json: %s", issues_json)

    issues = json.loads(issues_json)
    issues = [
        i for i in issues
        if LABELS.intersection(set(label["name"] for label in i["labels"]))
    ]
    logging.info("issues with filter: %s", issues)

    ## 2. generate README.md
    # Use .md links for GitHub compatibility (Jekyll will convert to .html in index.html)
    with open("README.md", "w") as f:
        for issue in issues:
            link = f"{POSTS_DIR}/{issue['number']}.md"
            updated = issue["createdAt"].split("T")[0]
            f.write(f"- #{issue['number']} {updated} [{issue['title']}]({link})\n")

    ## 3. generate posts
    for issue in issues:
        r = subprocess.check_output(
            f"gh issue view {issue['number']} --json title,url,author,number,labels,createdAt,updatedAt,body",
            shell=True,
            timeout=TIMEOUT,
        )
        issue = json.loads(r)
        logging.info("process issue: %s", issue)
        with open(POSTS_DIR / f"{issue['number']}.md", "w") as f:
            f.write("---\n")
            f.write("layout: default\n")
            f.write(f'title: "{issue["title"]}"\n')
            f.write(f"author: {issue['author']['login']}\n")
            f.write(f"labels: {' '.join([label['name'] for label in issue['labels']])}\n")
            f.write(f"date: {issue['createdAt']}\n")
            f.write(f"link: {issue['url']}\n")
            f.write("---\n\n")
            f.write(issue["body"])

    ## 4. autolink: wrap bare URLs in all posts
    run_autolink()


if __name__ == "__main__":
    main()
