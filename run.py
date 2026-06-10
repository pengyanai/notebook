#!/usr/bin/env python3
"""
Blog tooling entry point. Run from repo root.

  python run.py generate         Fetch GitHub Issues → write _posts/*.md
  python run.py add-image-attrs  Add lazy loading to <img> in _site/
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
if Path.cwd() != REPO_ROOT:
    import os
    os.chdir(REPO_ROOT)

COMMANDS = {
    "generate": ("scripts.generate", "Fetch GitHub Issues → write _posts/*.md"),
    "add-image-attrs": ("scripts.add_image_attrs", "Add lazy loading to images in _site/"),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__.strip())
        print("\nCommands:")
        for name, (_, desc) in COMMANDS.items():
            print(f"  {name:22}  {desc}")
        sys.exit(1 if len(sys.argv) < 2 else 0)

    mod_name, _ = COMMANDS[sys.argv[1]]
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        mod_name.replace(".", "_"),
        REPO_ROOT / (mod_name.replace(".", "/") + ".py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


if __name__ == "__main__":
    main()
