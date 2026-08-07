"""Build uniform thigh-shot game sprites from the formal character mirrors.

The source PNGs in game/images/characters stay untouched. Derived sprites are
written to game/images/characters/thigh and are the files referenced by Ren'Py.
"""

from pathlib import Path

from PIL import Image


PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_DIR / "game" / "images" / "characters"
OUTPUT_DIR = SOURCE_DIR / "thigh"
OUTPUT_SIZE = (1024, 1536)


def framing_factor(filename: str) -> float:
    """Return the retained share of the visible subject's vertical extent."""
    if "_thigh_" in filename:
        return 1.0
    if filename.startswith(("jorogumo_", "tsuchigumo_")):
        return 0.82
    return 0.72


def build_sprite(source_path: Path, output_path: Path) -> tuple[int, int, int, int]:
    image = Image.open(source_path).convert("RGBA")
    alpha_box = image.getchannel("A").getbbox()
    if alpha_box is None:
        raise ValueError(f"Sprite has no visible pixels: {source_path.name}")

    factor = framing_factor(source_path.name)
    visible_height = alpha_box[3] - alpha_box[1]
    crop_height = min(image.height, round(visible_height * factor))
    crop_width = min(image.width, round(crop_height * 2 / 3))

    crop_top = max(0, min(image.height - crop_height, alpha_box[1] - 20))
    visible_slice = image.crop(
        (0, crop_top, image.width, crop_top + crop_height)
    ).getchannel("A").getbbox()
    if visible_slice is None:
        center_x = (alpha_box[0] + alpha_box[2]) / 2
    else:
        center_x = (visible_slice[0] + visible_slice[2]) / 2

    crop_left = max(0, min(image.width - crop_width, round(center_x - crop_width / 2)))
    crop_box = (
        crop_left,
        crop_top,
        crop_left + crop_width,
        crop_top + crop_height,
    )

    framed = image.crop(crop_box).resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    framed.save(output_path, optimize=True)
    return crop_box


def main() -> None:
    sources = sorted(SOURCE_DIR.glob("*.png"))
    if not sources:
        raise SystemExit(f"No source sprites found in {SOURCE_DIR}")

    for source_path in sources:
        crop_box = build_sprite(source_path, OUTPUT_DIR / source_path.name)
        print(f"{source_path.name}: crop={crop_box}")

    print(f"Built {len(sources)} thigh-shot sprites in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
