"""
Side-by-side review sheet: row 1 = our frames, row 2 = reference frames,
all scaled to the same height.

Usage:
  python scripts/sbs_sheet.py out.jpg --ours a.jpg b.jpg ... --ref r1.jpg r2.jpg ... [--h 640]
"""

import os
import sys
from PIL import Image

if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
    print(__doc__.strip())
    sys.exit(0)

args = sys.argv[1:]
out = args[0]
rows = {"--ours": [], "--ref": []}
cur = None
h = 640
i = 1

while i < len(args):
    a = args[i]
    if a in rows:
        cur = a
    elif a == "--h":
        if i + 1 < len(args):
            h = int(args[i + 1])
            i += 1
    elif cur:
        rows[cur].append(a)
    i += 1

for group, paths in rows.items():
    for p in paths:
        if not os.path.exists(p):
            print(f"[ERROR] Image path does not exist ({group}): {p}")
            sys.exit(1)


def build_row(paths):
    if not paths:
        return None
    ims = [Image.open(p).convert("RGB") for p in paths]
    resized = [im.resize((round(im.width * h / im.height), h), Image.LANCZOS) for im in ims]
    total_w = sum(im.width for im in resized) + 8 * (len(resized) - 1)
    r = Image.new("RGB", (total_w, h), "white")
    x = 0
    for im in resized:
        r.paste(im, (x, 0))
        x += im.width + 8
    return r


rs = [r for r in [build_row(rows["--ours"]), build_row(rows["--ref"])] if r is not None]
if not rs:
    print("[ERROR] No valid images provided to create comparison sheet.")
    sys.exit(1)

max_w = max(r.width for r in rs)
total_h = sum(r.height for r in rs) + 16 * (len(rs) - 1)
sheet = Image.new("RGB", (max_w, total_h), "white")

y = 0
for r in rs:
    sheet.paste(r, (0, y))
    y += r.height + 16

out_dir = os.path.dirname(os.path.abspath(out))
if out_dir:
    os.makedirs(out_dir, exist_ok=True)

sheet.save(out, quality=88)
print(f"[SBS] Sheet created: {out} ({sheet.width}x{sheet.height})")
