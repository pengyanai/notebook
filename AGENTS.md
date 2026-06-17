# AGENTS.md

This file provides guidance to Claude Code when working with this repository.

## Git Branch Strategy

- **GitHub** (`origin`): 使用 `gh-pages` 分支
- **GitLab** (`gitlab`): 使用 `main` 分支

推送命令：
```bash
git push origin gh-pages
git push gitlab gh-pages:main
```

## Build & Dev

```bash
bundle install
bundle exec jekyll serve --watch --force_polling   # 本地开发
rm -rf _site .sass-cache && bundle exec jekyll build  # 清理构建
python3 run.py add-image-attrs  # 给 <img> 加 loading="lazy"
```

本地访问：`http://localhost:4000`。端口冲突时：`lsof -ti:4000 | xargs kill -9`

## Key Conventions

- `_config.yml` 是唯一配置源（single source of truth）
- `incremental: false` 不能开，否则新文章检测不到
- macOS 必须加 `--force_polling`
- `limiter: false` — 私有实例无 Redis
