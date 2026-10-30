#!/usr/bin/env python3
"""Validate the repository.

Usage (from the repository root):
    python scripts/check_repo.py

Checks: required files exist, every image in Product-Images/ appears in the
README, and every relative Markdown link/image in every .md file resolves.
Files listed in PENDING are reported as "pending" (not errors) because they
have not been supplied yet.
"""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = [
    "README.md", "LICENSE", ".gitignore",
    "Manual/README.md", "Manual/User-Manual.pdf",
    "Datasheet/README.md",
    "Circuits/Arduino-Nano/README.md", "Circuits/Arduino-Nano/circuit-diagram.png", "Circuits/Arduino-Nano/circuit-diagram.pdf",
    "Circuits/ESP32-DevKit/README.md", "Circuits/ESP32-DevKit/circuit-diagram.png", "Circuits/ESP32-DevKit/circuit-diagram.pdf",
    "Circuits/ESP32-S3/README.md", "Circuits/ESP32-S3/circuit-diagram.png", "Circuits/ESP32-S3/circuit-diagram.pdf",
]
PENDING = [
    "Datasheet/9-Sensor-Array-Datasheet.pdf", "Datasheet/9-Sensor-Array-Datasheet.docx",
    "Manual/User-Manual.docx",
]
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

errors = 0
for rel in REQUIRED:
    if not (ROOT / rel).exists():
        print(f"MISSING  {rel}"); errors += 1
for rel in PENDING:
    if not (ROOT / rel).exists():
        print(f"pending  {rel}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for p in sorted((ROOT / "Product-Images").iterdir()):
    if p.suffix.lower() in IMG_EXTS and f"Product-Images/{p.name}" not in readme:
        print(f"NOT IN README GALLERY  {p.name}"); errors += 1

for md in ROOT.rglob("*.md"):
    body = re.sub(r"```.*?```|`[^`\n]*`", "", md.read_text(encoding="utf-8"), flags=re.S)
    for target in LINK.findall(body):
        if re.match(r"^(https?:|mailto:|#)", target):
            continue
        path = unquote(target.split("#")[0])
        if path and not (md.parent / path).exists():
            print(f"BROKEN LINK  {md.relative_to(ROOT)} -> {target}"); errors += 1

print("OK" if not errors else f"{errors} problem(s) found")
sys.exit(1 if errors else 0)
