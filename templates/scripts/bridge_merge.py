"""
Merge look sandboxes back into the main video folder, organized by owned files.
Backs up main first (backup/<name>_<timestamp>/), copies each sandbox's owned files,
and reports which owned files are missing or unchanged.

Usage:
  python scripts/bridge_merge.py [cam,world,mat,char,post] [--root PATH] [--name NAME]
"""

import argparse
import filecmp
import os
import shutil
import sys
import time

OWN = {
    "cam": ["story.ts"],
    "world": ["world.ts", "lights.ts", "shade.ts", "grade.ts"],
    "mat": ["paint.ts", "build.ts"],
    "char": ["toon.ts", "cast.ts", "cardshade.ts"],
    "post": ["ink.ts", "Bridge.tsx", "lensblur.ts"],
}


def find_project_root(cli_root):
    if cli_root:
        return os.path.abspath(os.path.expanduser(cli_root))
    if os.environ.get("REMOTION_PROJECT_DIR"):
        return os.path.abspath(os.path.expanduser(os.environ["REMOTION_PROJECT_DIR"]))
    
    # Check current directory and parents for package.json
    cur = os.path.abspath(os.getcwd())
    while cur:
        if os.path.exists(os.path.join(cur, "package.json")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return os.path.abspath(os.getcwd())


def main():
    parser = argparse.ArgumentParser(description="Merge sandbox video files into main Remotion video folder.")
    parser.add_argument("sandboxes", nargs="?", default="all",
                        help="Comma-separated list of sandboxes to merge (e.g. cam,world,mat,char,post) or 'all'")
    parser.add_argument("--root", "-r", default=None,
                        help="Path to the Remotion project root (defaults to REMOTION_PROJECT_DIR or current repo)")
    parser.add_argument("--name", "-n", default="bridge",
                        help="Video/composition directory name in src/videos/<name> (default: bridge)")
    
    args = parser.parse_args()
    root = find_project_root(args.root)
    name = args.name
    main_dir = os.path.join(root, "src", "videos", name)

    which = list(OWN.keys()) if args.sandboxes in ("all", None, "") else args.sandboxes.split(",")
    invalid = [w for w in which if w not in OWN]
    if invalid:
        print(f"[ERROR] Unknown sandbox name(s): {invalid}. Valid options: {list(OWN.keys())}")
        sys.exit(1)

    if not os.path.exists(main_dir):
        print(f"[ERROR] Main video directory not found: {main_dir}")
        print("Please specify the project root with --root <path> or check the --name argument.")
        sys.exit(1)

    backup_dir = os.path.join(root, "backup", f"{name}_{time.strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(os.path.dirname(backup_dir), exist_ok=True)
    shutil.copytree(main_dir, backup_dir)
    print(f"[BACKUP] Main folder saved -> {backup_dir}")

    for box in which:
        src = os.path.join(root, "src", "videos", f"{name}_{box}")
        if not os.path.exists(src):
            print(f"  {box}: sandbox folder not found ({src}) - skipping")
            continue

        for f in OWN[box]:
            a, b = os.path.join(src, f), os.path.join(main_dir, f)
            if not os.path.exists(a):
                print(f"  {box}: {f} not in sandbox (skipped)")
                continue
            if os.path.exists(b) and filecmp.cmp(a, b, shallow=False):
                print(f"  {box}: {f} unchanged")
                continue
            shutil.copy2(a, b)
            print(f"  {box}: {f} -> main (updated)")

    print("[DONE] Merge complete. Run 'npx tsc --noEmit' to verify TypeScript compilation.")


if __name__ == "__main__":
    main()
