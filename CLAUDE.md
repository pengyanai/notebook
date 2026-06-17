# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Dev

```bash
bundle install                                                    # install deps
bundle exec jekyll serve --watch --force_polling                  # local dev (macOS needs --force_polling)
rm -rf _site .sass-cache && bundle exec jekyll build              # clean build
python3 run.py add-image-attrs                                    # post-process images (after build)
```

Local server: `http://localhost:4000`. Port conflict: `lsof -ti:4000 | xargs kill -9`.

## Architecture

Jekyll 3.9 blog with minima theme, custom shadcn/ui-style layout. All config in `_config.yml` (single source of truth).

**Template layering:**
- `_layouts/default.html` — base shell (MathJax, Mermaid, reading progress, search modal). All CDN URLs reference `site.cdn.xxx` from config.
- `_layouts/post.html` — article layout (extends default). Renders title, date, author, Schema.org markup.
- `_includes/` — partials: `head.html` (preload hints), `header.html` (data-driven nav from `_data/navigation.yml`), `search-modal.html` (Fuse.js client-side search).

**Post list:** Auto-generated from `site.posts` in `index.html`. No manual index — just add files to `_posts/`.

**Search:** Client-side Fuse.js. Index built from `search.json` (Liquid template, truncates content to 300 chars). Eagerly preloaded during `requestIdleCallback`. Prefetches target pages on hover.

## Writing Posts

Add `YYYY-MM-DD-slug.md` to `_posts/`. Minimal front matter:

```yaml
---
title: "Your Title"
date: 2026-06-10
---
```

`layout: post` and `author: Joseph` auto-applied via `defaults:` in `_config.yml`. Optional: `categories`, `tags`, `mermaid: true`.

Internal cross-references use permalink format: `[text](/2026/06/10/slug.html)` — NOT `/posts/slug.html`.

## Key Conventions

- **No hardcoded URLs in templates.** CDN URLs, nav links, feature flags all come from `_config.yml` or `_data/`.
- **`_data/navigation.yml`** — add/remove nav entries here. Active state auto-applied.
- **`incremental: false`** in config — must stay off, otherwise new files in `_posts/` aren't detected by `--watch`.
- **`--force_polling`** required on macOS for reliable new-file detection.
- **`limiter: false`** — private instance, no Redis. Enabling without Valkey causes ERROR log flood.
- **Old post naming:** Legacy posts use `YYYY-MM-DD-N.md` format (e.g., `2023-05-12-92.md`). New posts use descriptive slugs.

## Deployment

- **GitLab Pages:** `.gitlab-ci.yml` builds on push to `main`, deploys with `--baseurl "/notebook"`.
- **GitHub Pages:** `.github/workflows/deploy.yml` builds on push, deploys to `pengyanai.github.io`.
- **Feed:** `/feed.xml` (Atom) via `jekyll-feed`. Auto-discovery `<link>` in head.
- **Sitemap:** `/sitemap.xml` via `jekyll-sitemap`. Referenced in `robots.txt`.

## Scripts (run.py)

| Command | When |
|---------|------|
| `generate` | CI only — fetches GitHub Issues with label `blog`, writes `_posts/*.md` |
| `add-image-attrs` | After build — adds `loading="lazy"` to `<img>` in `_site/` |
