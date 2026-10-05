"""Resize and compress site photos into docs/assets/img as WebP.

Run locally from the repo root:  python scripts/optimize_images.py
Requires Pillow. Originals in images/ and Figures/ are never modified.
"""
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "img"

# source file -> (output name, widths to generate)
IMAGES = {
    "images/Home_Hero.jpg": ("home-hero", [800, 1600]),
    "images/Construction.jpg": ("card-construction", [400]),
    "images/Building.jpg": ("card-building", [400]),
    "images/card_reuse_station.jpg": ("card-reuse-station", [400]),
    "images/Circular_Purchasing.jpg": ("card-purchasing", [400]),
    "images/gateway_circular_purchasing_hero.jpg": ("purchasing-hero", [740]),
    "images/Recovery.jpg": ("card-recovery", [400]),
    "Figures/construction_source_separation.jpg": ("construction-hero", [800, 1600]),
    "Figures/permasteelisa_curtainwall_bunks.JPEG": ("curtainwall-bunks", [800]),
    "Figures/reusable_shipping_systems.JPEG": ("reusable-ductwork", [800]),
    "Figures/salvaged_tree_furniture.png": ("tree-to-table", [733]),
    "Figures/bobcat_t7x_gateway.jpg": ("bobcat-t7x", [800]),
    "images/gateway_building_systems_hero.jpg": ("building-hero", [800, 1536]),
    "images/gateway_reuse_hero.jpeg": ("reuse-hero", [800, 1600]),
    "Figures/gateway_reuse_station_2nd_floor.jpg": ("reuse-station", [600]),
    "Figures/gateway_reusables_kitchen_shelf.jpg": ("reusables-shelf", [700]),
    "images/gateway_recovery_hero.jpg": ("recovery-hero", [720]),
    "Figures/gateway_mill.jpg": ("mill", [800]),
    "Figures/gateway_compost_mill_scraps.jpg": ("compost", [400]),
    "Figures/gateway_battery_bin.jpg": ("batteries", [400]),
    "Figures/gateway_ewaste_bin.jpg": ("ewaste", [400]),
}

QUALITY = 72


def export(src, name, widths):
    image = ImageOps.exif_transpose(Image.open(ROOT / src)).convert("RGB")
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
# og image is made by hand: 1200x630 centre crop of images/Home_Hero.jpg (docs/assets/img/home-hero-og.jpg)
