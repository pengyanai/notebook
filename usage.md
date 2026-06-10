# Developer Reference

Detailed technical docs for this Jekyll blog. For project overview, see [README.md](README.md).

---

## Project structure

```
_config.yml               ← All config (single source of truth)
_data/navigation.yml      ← Nav links (data-driven)
_includes/                ← head.html, header.html, search-modal.html
_layouts/                 ← default.html, post.html
_posts/                   ← Articles (YYYY-MM-DD-slug.md)
assets/css/style.scss     ← Styles (shadcn/ui tokens)
search.json               ← Search index template (Liquid)
scripts/                  ← generate.py, add_image_attrs.py
run.py                    ← CLI entry for scripts/
```

---

## Key configuration (_config.yml)

| Section | Purpose |
|---------|---------|
| `cdn:` | CDN URLs for MathJax, Mermaid, Fuse.js — referenced by templates as `site.cdn.xxx` |
| `features:` | Feature flags — `site.features.xxx` for conditional loading |
| `defaults:` | Auto-applied to all posts (layout, author, reading_progress) |
| `permalink:` | URL structure: `/:year/:month/:day/:slug:output_ext` |

---

## Navigation

Edit `_data/navigation.yml` to add/remove nav links. Active state auto-applied via `page.url` comparison.

---

## Writing posts

Add `YYYY-MM-DD-slug.md` to `_posts/`:

```yaml
---
title: "Your Title"
date: 2026-06-10
categories: [深度学习]
tags: [tag1, tag2]
mermaid: true    # lazy-load Mermaid
---
```

`layout: post` and `author: Austin` are auto-applied via `defaults:` — no need to specify.

Internal links use permalink format: `[text](/2026/06/10/slug.html)`

---

## Local dev

```bash
bundle install
bundle exec jekyll serve --watch --force_polling   # macOS needs --force_polling
```

---

## Build & deploy

```bash
# Clean rebuild
rm -rf _site .sass-cache && bundle exec jekyll build

# Post-process images (CI does this)
python3 run.py add-image-attrs
```

**CI**: GitLab (`.gitlab-ci.yml`) and GitHub (`.github/workflows/`) both build on push to `main`.

---

## Scripts (run.py)

| Command | Description |
|---------|-------------|
| `generate` | Fetch GitHub Issues with label `blog` → write `_posts/*.md`. CI only. |
| `add-image-attrs` | Add `loading="lazy"` to `<img>` in `_site/`. Run after build. |

---

## Features

| Feature | How it works |
|---------|-------------|
| **Search** | Fuse.js client-side search. Index from `search.json`. Eagerly preloaded. |
| **RSS** | `/feed.xml` (Atom) via `jekyll-feed`. Auto-discovery in `<head>`. |
| **Sitemap** | `/sitemap.xml` via `jekyll-sitemap`. Referenced in `robots.txt`. |
| **MathJax** | Lazy-loaded when `$...$` or `$$...$$` detected. |
| **Mermaid** | Lazy-loaded when `pre code.language-mermaid` detected. HF color theme. |
| **Reading progress** | Top bar progress indicator on article pages. |
| **SEO** | `jekyll-seo-tag` generates meta tags. |
