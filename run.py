#!/usr/bin/env python3
"""
Single entry point for blog tooling. Run from repo root.

  python run.py generate         Fetch issues, write posts, autolink URLs
  python run.py add-image-attrs  Add lazy loading to images in _site/ (after Jekyll build)
  python run.py migrate-front-matter  One-off: migrate article metadata to Jekyll front matter
"""

import sys
from pathlib import Path

# Ensure we run with repo root as cwd (for scripts that use Path("posts"), Path("_site"))
REPO_ROOT = Path(__file__).resolve().parent
if Path.cwd() != REPO_ROOT:
    import os
    os.chdir(REPO_ROOT)

COMMANDS = {
    "generate": ("scripts.generate", "Fetch issues, write posts, autolink URLs"),
    "add-image-attrs": ("scripts.add_image_attrs", "Add lazy loading to images in _site/"),
    "migrate-front-matter": ("scripts.migrate_front_matter", "Migrate article metadata to front matter"),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__.strip())
        print("\nCommands:")
        for name, (_, desc) in COMMANDS.items():
            print(f"  {name:22}  {desc}")
        sys.exit(1 if len(sys.argv) < 2 else 0)

    cmd = sys.argv[1]
    mod_name, _ = COMMANDS[cmd]
    # Run the script's main() in the same process so cwd is already correct
    import importlib.util
    script_path = REPO_ROOT / (mod_name.replace(".", "/") + ".py")
    spec = importlib.util.spec_from_file_location(
        mod_name.replace(".", "_"),
        script_path,
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


if __name__ == "__main__":
    main()
