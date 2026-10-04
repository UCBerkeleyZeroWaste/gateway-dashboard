"""Resize and compress site photos into docs/assets/img as WebP.

Run locally from the repo root:  python scripts/optimize_images.py
Requires Pillow. Originals in images/ and Figures/ are never modified.
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "img"

# source file -> (output name, widths to generate)
IMAGES = {
    "images/Home_Hero.jpg": ("home-hero", [800, 1600]),
    "images/Construction.jpg": ("card-construction", [400]),
    "images/Building.jpg": ("card-building", [400]),
    "images/Reuse.jpg": ("card-reuse", [400]),
    "images/Circular_Purchasing.jpg": ("card-purchasing", [400]),
    "images/Recovery.jpg": ("card-recovery", [400]),
}

QUALITY = 72


def export(src, name, widths):
    image = Image.open(ROOT / src).convert("RGB")
    for width in widths:
        target = min(width, image.width)
        height = round(image.height * target / image.width)
        resized = image.resize((target, height), Image.LANCZOS)
        out_path = OUT / f"{name}-{width}.webp"
        resized.save(out_path, "WEBP", quality=QUALITY, method=6)
        print(f"{out_path.relative_to(ROOT)}  {target}x{height}  {out_path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for src, (name, widths) in IMAGES.items():
        export(src, name, widths)
