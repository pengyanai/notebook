# Joseph's Notebook

Personal technical blog — LLM training/inference, systems engineering, tooling.

**Live**: [pengyanai.github.io](https://pengyanai.github.io) · [GitLab Pages](https://11088830.gitlab.example.com/notebook/)

## Stack

- Jekyll 3.9 + minima theme
- Custom shadcn/ui-style layout
- Client-side search (Fuse.js)
- Mermaid + MathJax support
- Deployed via GitHub Pages + GitLab Pages CI

## Local dev

```bash
bundle install
bundle exec jekyll serve --watch --force_polling
```

## Write a post

Add `YYYY-MM-DD-slug.md` to `_posts/` with front matter:

```yaml
---
layout: post
title: "Your Title"
date: 2026-06-10
author: Austin
---
```

The post list on the homepage auto-updates from `site.posts`. No manual index maintenance needed.
