"""
Extracts shot frame ranges, crossfade windows, flash frames, and impact kicks
from story.ts and writes shots.json for scripts/short_qa.py.

Usage:
  python scripts/bridge_shots.py [story_ts_path] [--out shots_json_path]
"""

import argparse
import json
import os
import re
import sys


def parse_story(src_path, out_path):
    if not os.path.exists(src_path):
        print(f"[ERROR] Story file not found: {src_path}")
        sys.exit(1)

    with open(src_path, "r", encoding="utf-8") as f:
        src = f.read()

    total_match = re.search(r"TOTAL\s*=\s*(\d+)", src)
    total_frames = int(total_match.group(1)) if total_match else 2025

    shots = []
    for i, a, b in re.findall(r"\{\s*id:\s*(\d+),\s*a:\s*(\d+),\s*b:\s*(\w+),", src):
        b_val = total_frames if b == "TOTAL" else int(b)
        shots.append({"id": int(i), "a": int(a), "b": b_val})

    xf = {}
    xf_match = re.search(r"XFADE[^=]*=\s*\{([^}]*)\}", src)
    if xf_match:
        xf = {int(k): int(v) for k, v in re.findall(r"(\d+):\s*(\d+)", xf_match.group(1))}

    flash_match = re.search(r"FLASH_AT\s*=\s*(\d+)", src)
    flash = int(flash_match.group(1)) if flash_match else None

    xfade = [[s["a"] - xf[s["id"]] // 2, s["a"] + xf[s["id"]] // 2] for s in shots if s["id"] in xf]
    cuts = [[int(f), int(f)] for f in re.findall(r"\{\s*f:\s*(\d+),\s*cut:\s*true", src)]

    consts = {k: float(v) for k, v in re.findall(r"(SNAP|DROP0|DROP1)\s*=\s*([\d.]+)", src)}
    kicks = []
    m = re.search(r"const\s+KICKS[^=]*=\s*\[(.*?)\];", src, re.DOTALL)
    if m:
        for t0, _ in re.findall(r"\[([\w.]+),\s*([\d.]+)\]", m.group(1)):
            f0 = round((consts[t0] if t0 in consts else float(t0)) * 30)
            kicks.append([f0, f0 + 8])

    out_data = {
        "shots": shots,
        "xfade": xfade,
        "flash": [flash, flash + 4] if flash is not None else [],
        "planned": cuts + kicks,
    }

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_data, f, indent=2)

    print(f"[SHOTS] Extracted {len(shots)} shots -> {out_path}")
    print(f"  Crossfades: {len(xfade)}, Flash: {flash}, Cuts: {len(cuts)}, Kicks: {len(kicks)}")


def main():
    parser = argparse.ArgumentParser(description="Parse story.ts into shots.json for QA.")
    parser.add_argument("story", nargs="?", default="src/videos/bridge/story.ts",
                        help="Path to story.ts (default: src/videos/bridge/story.ts)")
    parser.add_argument("--out", "-o", default="out/bridge/shots.json",
                        help="Output path for shots.json (default: out/bridge/shots.json)")
    args = parser.parse_args()
    parse_story(args.story, args.out)


if __name__ == "__main__":
    main()
