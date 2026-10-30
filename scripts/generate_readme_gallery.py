#!/usr/bin/env python3
"""Regenerate the Product Gallery section of README.md.

Usage (from the repository root):
    python scripts/generate_readme_gallery.py

Every supported image in Product-Images/ gets an explicit Markdown image
reference between the GALLERY markers in README.md. Optional captions live in
Product-Images/captions.json ({"file.jpg": "Caption"}); without one, the
caption is derived from the file name.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "Product-Images"
README = ROOT / "README.md"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
START, END = "<!-- GALLERY:START -->", "<!-- GALLERY:END -->"
COLS = 2


def caption_for(name, captions):
    if name in captions:
        return captions[name]
    return Path(name).stem.replace("-", " ").replace("_", " ").title()


def build():
    cap_file = IMG_DIR / "captions.json"
    captions = json.loads(cap_file.read_text(encoding="utf-8")) if cap_file.exists() else {}
    files = sorted(p.name for p in IMG_DIR.iterdir() if p.suffix.lower() in EXTS)
    if not files:
        return "_No images found in `Product-Images/` yet._"
    cells = []
    for f in files:
        cap = caption_for(f, captions)
        cells.append(f"![{cap}](Product-Images/{f})<br><sub>{cap}</sub>")
    while len(cells) % COLS:
        cells.append(" ")
    lines = ["| " + " | ".join([" "] * COLS) + " |", "|" + "---|" * COLS]
    for i in range(0, len(cells), COLS):
        lines.append("| " + " | ".join(cells[i:i + COLS]) + " |")
    return "\n".join(lines)


def main():
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        raise SystemExit(f"Markers {START} / {END} not found in README.md")
    new = f"{START}\n\n{build()}\n\n{END}"
    README.write_text(pattern.sub(lambda m: new, text), encoding="utf-8")
    print("README gallery updated.")


if __name__ == "__main__":
    main()
