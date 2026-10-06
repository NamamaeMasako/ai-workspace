from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageChops
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer


PROJECT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT / "source"
PARTS_DIR = SOURCE_DIR / "parts"
STAGING = SOURCE_DIR / "包子_rebuilt.psd"
MASTER = SOURCE_DIR / "包子.psd"
PREVIEW = PROJECT / "preview" / "source_restructure" / "parts_composite.png"

DRAW_ORDER = [
    "body_base",
    "mouth_interior",
    "left_pupil",
    "right_pupil",
    "left_lower_lid",
    "right_lower_lid",
    "left_upper_lid",
    "right_upper_lid",
    "lower_lip",
    "upper_lip",
    "left_brow",
    "right_brow",
    "glasses",
    "hands_book",
]


def add_cropped_layer(canvas: PSDImage, image: Image.Image, name: str) -> None:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        PixelLayer.frompil(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), canvas, name=name)
        return
    PixelLayer.frompil(image.crop(bbox), canvas, name=name, left=bbox[0], top=bbox[1])


def read_part(path: Path) -> Image.Image:
    psd = PSDImage.open(path)
    if len(psd) != 1:
        raise ValueError(f"{path.name} must contain exactly one pixel layer")
    layer = next(iter(psd))
    if layer.kind != "pixel":
        raise ValueError(f"{path.name} must contain a pixel layer")
    image = Image.new("RGBA", psd.size, (0, 0, 0, 0))
    image.alpha_composite(layer.composite().convert("RGBA"), (layer.left, layer.top))
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild the Bao master PSD from canonical part PSDs.")
    parser.add_argument("--apply", action="store_true", help="Replace source/包子.psd after creating a timestamped backup.")
    args = parser.parse_args()

    images: dict[str, Image.Image] = {}
    canvas_size: tuple[int, int] | None = None
    for name in DRAW_ORDER:
        path = PARTS_DIR / f"{name}.psd"
        psd = PSDImage.open(path)
        if canvas_size is None:
            canvas_size = psd.size
        elif psd.size != canvas_size:
            raise ValueError(f"Canvas mismatch: {path.name} is {psd.size}, expected {canvas_size}")
        images[name] = read_part(path)

    assert canvas_size is not None
    master = PSDImage.new("RGBA", canvas_size, color=(0, 0, 0, 0))
    for name in DRAW_ORDER:
        add_cropped_layer(master, images[name], name)
    master.save(STAGING)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    PSDImage.open(STAGING).composite().convert("RGBA").save(PREVIEW)

    print(f"staging={STAGING}")
    print(f"preview={PREVIEW}")

    if args.apply:
        backup_dir = PROJECT / "archive" / "master_backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        if MASTER.exists():
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(MASTER, backup_dir / f"包子_before_rebuild_{stamp}.psd")
        shutil.copy2(STAGING, MASTER)
        print(f"applied={MASTER}")


if __name__ == "__main__":
    main()
