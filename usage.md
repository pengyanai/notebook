# Blog framework usage

Jekyll blog with client-side search, Mermaid diagrams, and MathJax support. Posts are standard `_posts/YYYY-MM-DD-slug.md` files — the homepage list auto-generates from `site.posts`.

---

## Prerequisites

- **Ruby** + Bundler: `bundle install`
- **Python 3**: for `run.py` scripts
- **GitHub CLI** (`gh`): only for `run.py generate` (fetch issues)

---

## Project tree

```
.
├── _config.yml              # Jekyll config
├── _includes/
│   ├── head.html            # <head> with preload hints
│   ├── header.html          # Navbar + search trigger + mobile menu
│   └── search-modal.html    # Client-side search (Fuse.js)
├── _layouts/
│   ├── default.html         # Base layout (MathJax + Mermaid + progress bar)
│   └── post.html            # Article layout (title + meta + Schema.org)
├── _posts/                  # Blog posts (YYYY-MM-DD-slug.md)
├── assets/
│   ├── css/style.scss       # All styles (shadcn/ui tokens)
│   ├── images/              # Post images
│   └── scripts/             # Supplementary scripts (e.g. NAS tools)
├── scripts/                 # Python build helpers
│   ├── generate.py          # Fetch issues → write posts (CI only)
│   └── add_image_attrs.py   # Add lazy loading to _site/ images
├── index.html               # Homepage — renders post list from site.posts
├── search.json              # Search index template (Liquid)
├── run.py                   # CLI entry for scripts/
├── README.md                # Project description (GitHub display only)
├── .gitlab-ci.yml           # GitLab Pages deploy
└── .github/workflows/       # GitHub Pages deploy + issue-driven PR
```

---

## Local dev

```bash
# Install deps
bundle install

# Serve with live reload (macOS needs --force_polling for new file detection)
bundle exec jekyll serve --watch --force_polling

# Access at http://localhost:4000
```

---

## Write a post

Create `_posts/YYYY-MM-DD-slug.md`:

```yaml
---
layout: post
title: "Your Title"
date: 2026-06-10
author: Austin
categories: [深度学习, 工具]
tags: [tag1, tag2]
mermaid: true    # enable Mermaid diagrams
---

Your content here.
```

The homepage list updates automatically — no manual index maintenance.

---

## Run a full rebuild

```bash
# Kill old server
lsof -ti:4000 | xargs kill -9

# Clean build
rm -rf _site .sass-cache
bundle exec jekyll build

# Optional: optimize images
python3 run.py add-image-attrs

# Restart
bundle exec jekyll serve --watch --force_polling
```

---

## run.py commands

| Command | Description |
|---------|-------------|
| `generate` | Fetch GitHub issues with label `blog`, write `_posts/*.md`. CI only. |
| `add-image-attrs` | Add `loading="lazy"` to `<img>` in `_site/`. Run after build. |

---

## CI/CD

- **GitHub**: `deploy.yml` — on push to main, build → add-image-attrs → deploy to GitHub Pages
- **GitLab**: `.gitlab-ci.yml` — on push to main, `jekyll build --baseurl "/notebook"` → deploy to GitLab Pages
- **Issue-driven**: `main.yml` — on issue events, `run.py generate` → open PR

---

## Search

Client-side search powered by Fuse.js. Index is built from `search.json` (Liquid template). Eagerly preloaded during idle time — opens instantly.

---

## Mermaid + MathJax

Both are lazy-loaded only when the page contains diagrams (`pre code.language-mermaid`) or math formulas (`$...$` / `$$...$$`). No configuration needed — just use standard markdown.
