# Blog framework usage

This repo is a Jekyll blog whose content is driven by **GitHub Issues** (with label `blog`). Tooling is a single Python entry point: `run.py`.

---
## Prerequisites

- **Ruby** (for Jekyll): install Ruby and Bundler, then run `bundle install` in the repo root.
- **Python 3**: used by `run.py` for generate / image-optimization scripts.
- **GitHub CLI** (`gh`): only needed when running `run.py generate` (fetch issues locally).

---
## Project tree

```
.
├── _config.yml          # Jekyll config (site title, baseurl, kramdown, exclude, etc.)
├── _includes/           # Jekyll partials
│   ├── head.html
│   └── header.html
├── _layouts/
│   └── default.html     # Default layout for pages and posts
├── _site/               # Generated output (created by `jekyll build`, do not edit)
├── assets/
│   └── css/
│       └── style.scss  # Site styles
├── posts/               # Blog posts (one .md per post, e.g. 155.md)
├── index.html           # Home page (renders README.md as content)
├── README.md            # Home page content + post list (links to posts/xxx.html)
├── run.py               # Single entry for all blog tooling (see below)
├── scripts/             # Python helpers (invoked via run.py only)
│   ├── generate.py         # Fetch issues → write posts + README, autolink URLs
│   ├── add_image_attrs.py  # Add lazy loading to images in _site/
│   └── migrate_front_matter.py  # One-off migration of metadata to front matter
├── Gemfile / Gemfile.lock
├── CNAME                # Custom domain (if used)
└── .github/workflows/
    ├── main.yml         # On issue events: run generate, open PR
    └── deploy.yml       # On push to main: Jekyll build → add-image-attrs → deploy to Pages
```

---
## Build and local serve

From the repo root:

```bash
# One-time: install Jekyll deps
bundle install

# Build site into _site/
bundle exec jekyll build

# Optional: add lazy loading to images (same as in CI)
python3 run.py add-image-attrs

# Start local server (default port 4000)
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

- **URL:** http://localhost:4000/
- Use `--watch` to auto-rebuild on file changes:  
  `bundle exec jekyll serve --host 0.0.0.0 --port 4000 --watch`

---
## Kill process on port 4000

If something is already using port 4000 (e.g. an old `jekyll serve`):

```bash
# macOS / Linux
lsof -ti:4000 | xargs kill -9
```

Then start `jekyll serve` again.

---
## Full rebuild and restart

```bash
# 1. Free the port
lsof -ti:4000 | xargs kill -9

# 2. Rebuild
bundle exec jekyll build
python3 run.py add-image-attrs

# 3. Start server (with watch)
bundle exec jekyll serve --host 0.0.0.0 --port 4000 --watch
```

---
## run.py commands

All tooling is behind one entry point. Run from repo root:

```bash
python3 run.py
```

Shows:

| Command | Description |
|--------|-------------|
| `generate` | Fetch open GitHub issues with label `blog`, write `posts/*.md` and `README.md`, then autolink bare URLs. Used in CI on issue events. |
| `add-image-attrs` | Add `loading="lazy"` and `decoding="async"` to `<img>` in `_site/`. Run after `jekyll build` (CI does this in deploy). |
| `migrate-front-matter` | One-off: move article metadata from blockquotes into Jekyll front matter. |

Examples:

```bash
python3 run.py generate
python3 run.py add-image-attrs
python3 run.py migrate-front-matter
```

---
## CI overview

- **main.yml**: On issue open/edit/label events, runs `python3 run.py generate` and opens a PR with updated `posts/` and `README.md`.
- **deploy.yml**: On push to `main`/`master`, runs Jekyll build, then `python3 run.py add-image-attrs`, then deploys to GitHub Pages.

No need to run `generate` locally unless you are testing issue-driven content; build + add-image-attrs + serve is enough for local preview.
