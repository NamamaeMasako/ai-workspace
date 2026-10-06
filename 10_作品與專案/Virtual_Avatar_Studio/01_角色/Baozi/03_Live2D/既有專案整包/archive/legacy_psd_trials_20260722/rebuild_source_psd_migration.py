from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "source" / "包子.psd"
STAGING = PROJECT / "source" / "包子_restructured.psd"
PARTS_DIR = PROJECT / "source" / "parts"
PREVIEW_DIR = PROJECT / "preview" / "source_restructure"


def alpha_of(image: Image.Image) -> Image.Image:
    return image.getchannel("A")


def mask_union(*masks: Image.Image) -> Image.Image:
    result = Image.new("L", masks[0].size, 0)
    for mask in masks:
        result = ImageChops.lighter(result, mask)
    return result


def masked(image: Image.Image, mask: Image.Image) -> Image.Image:
    result = image.copy()
    result.putalpha(ImageChops.multiply(alpha_of(image), mask))
    return result


def add_cropped_layer(canvas: PSDImage, image: Image.Image, name: str) -> None:
    bbox = alpha_of(image).getbbox()
    if bbox is None:
        PixelLayer.frompil(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), canvas, name=name)
        return
    PixelLayer.frompil(image.crop(bbox), canvas, name=name, left=bbox[0], top=bbox[1])


def save_single_layer_psd(image: Image.Image, name: str, path: Path) -> None:
    canvas = PSDImage.new("RGBA", image.size, color=(0, 0, 0, 0))
    add_cropped_layer(canvas, image, name)
    canvas.save(path)


def polygon_lid_mask(size: tuple[int, int], points: list[tuple[int, int]]) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


def pupil_with_hidden_ellipse(
    full: Image.Image,
    visible_mask: Image.Image,
    center: tuple[int, int],
    radius: tuple[int, int],
    seam_y: int,
) -> Image.Image:
    result = masked(full, visible_mask)
    px = result.load()
    src = full.load()
    cx, cy = center
    rx, ry = radius
    for y in range(cy - ry, seam_y):
        mirrored_y = min(full.height - 1, 2 * cy - y)
        for x in range(cx - rx, cx + rx + 1):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1:
                continue
            r, g, b, a = src[x, mirrored_y]
            if a:
                px[x, y] = (r, g, b, a)
    return result


def inpaint_background(full: Image.Image, removal_mask: Image.Image) -> Image.Image:
    rgba = np.array(full)
    rgb = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2BGR)
    mask = np.array(removal_mask)
    repaired = cv2.inpaint(rgb, mask, 5, cv2.INPAINT_TELEA)
    repaired = cv2.cvtColor(repaired, cv2.COLOR_BGR2RGB)
    out = np.dstack((repaired, rgba[:, :, 3]))
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def main() -> None:
    psd = PSDImage.open(SOURCE)
    full = psd.composite().convert("RGBA")
    size = full.size
    layers = {layer.name: layer.composite().convert("RGBA") for layer in psd.descendants()}

    left_brow_mask = alpha_of(layers["left_brow"])
    right_brow_mask = alpha_of(layers["right_brow"])
    hands_book_mask = mask_union(
        alpha_of(layers["left_hand"]),
        alpha_of(layers["right_hand"]),
        alpha_of(layers["book"]),
    )

    # The legacy eye layers contain fragments of the glasses and face outline.
    # Restrict them to the actual pupil/lid areas before separating the parts.
    left_eye_source = alpha_of(layers["left_eye_open"])
    right_eye_source = alpha_of(layers["right_eye_open"])
    left_eye_box = Image.new("L", size, 0)
    right_eye_box = Image.new("L", size, 0)
    ImageDraw.Draw(left_eye_box).rectangle((372, 680, 516, 802), fill=255)
    ImageDraw.Draw(right_eye_box).rectangle((738, 680, 882, 802), fill=255)
    left_eye_raw = ImageChops.multiply(left_eye_source, left_eye_box)
    right_eye_raw = ImageChops.multiply(right_eye_source, right_eye_box)

    # Open-eye upper lids follow the original slanted horizontal strokes.
    left_upper_mask = polygon_lid_mask(size, [(360, 620), (525, 620), (510, 687), (381, 713), (360, 713)])
    right_upper_mask = polygon_lid_mask(size, [(730, 620), (895, 620), (895, 713), (869, 713), (744, 687)])
    left_lower_mask = polygon_lid_mask(size, [(360, 790), (520, 790), (520, 840), (360, 840)])
    right_lower_mask = polygon_lid_mask(size, [(735, 790), (895, 790), (895, 840), (735, 840)])

    # Keep the visible pupil pixels below the lid seam, then restore a hidden
    # full oval behind the lid so the pupil itself is no longer a cut-off shape.
    left_visible_pupil = left_eye_raw.copy()
    right_visible_pupil = right_eye_raw.copy()
    ld = ImageDraw.Draw(left_visible_pupil)
    rd = ImageDraw.Draw(right_visible_pupil)
    ld.rectangle((0, 0, size[0], 701), fill=0)
    rd.rectangle((0, 0, size[0], 701), fill=0)
    left_pupil = pupil_with_hidden_ellipse(full, left_visible_pupil, (449, 738), (54, 56), 702)
    right_pupil = pupil_with_hidden_ellipse(full, right_visible_pupil, (812, 738), (54, 56), 702)

    # Cover every newly restored upper-ellipse pixel with the source face at
    # the default pose. This keeps the open-eye composite pixel-identical while
    # leaving the completed oval safely behind the upper lid.
    hidden_top = Image.new("L", size, 0)
    ImageDraw.Draw(hidden_top).rectangle((0, 0, size[0], 701), fill=255)
    left_hidden_shape = ImageChops.multiply(alpha_of(left_pupil), hidden_top).point(
        lambda value: 255 if value else 0
    )
    right_hidden_shape = ImageChops.multiply(alpha_of(right_pupil), hidden_top).point(
        lambda value: 255 if value else 0
    )
    left_source_stroke = ImageChops.multiply(left_eye_raw, hidden_top)
    right_source_stroke = ImageChops.multiply(right_eye_raw, hidden_top)
    left_upper_mask = mask_union(
        left_upper_mask,
        left_hidden_shape,
        left_source_stroke,
    )
    right_upper_mask = mask_union(
        right_upper_mask,
        right_hidden_shape,
        right_source_stroke,
    )

    # Use the current face pixels for the lids. At the open pose these are
    # visually identical to the source; their ArtMeshes can later move over
    # the pupil. Glasses remain a separate higher layer.
    left_upper_lid = masked(full, left_upper_mask)
    right_upper_lid = masked(full, right_upper_mask)
    left_lower_lid = masked(full, left_lower_mask)
    right_lower_lid = masked(full, right_lower_mask)

    # Isolate only the dark glasses frame inside known frame geometry, avoiding
    # the pupils that were baked into the old "glasses" source layer.
    frame_geo = Image.new("L", size, 0)
    gd = ImageDraw.Draw(frame_geo)
    for outer, inner in [((292, 560, 590, 862), (311, 579, 571, 843)), ((662, 560, 960, 862), (681, 579, 941, 843))]:
        gd.ellipse(outer, fill=255)
        gd.ellipse(inner, fill=0)
    gd.rounded_rectangle((563, 680, 690, 746), radius=28, fill=255)
    gd.rounded_rectangle((252, 680, 322, 735), radius=18, fill=255)
    gd.rounded_rectangle((930, 680, 1000, 735), radius=18, fill=255)
    old_glasses_alpha = alpha_of(layers["glasses"])
    glasses_mask = ImageChops.multiply(old_glasses_alpha, frame_geo)
    glasses = masked(full, glasses_mask)

    mouth_mask = alpha_of(layers["mouth_open"])
    mouth_binary = mouth_mask.point(lambda value: 255 if value else 0)
    mouth_inner_binary = mouth_binary.filter(ImageFilter.MinFilter(9))
    lip_edge = ImageChops.subtract(mouth_binary, mouth_inner_binary)
    upper_half = Image.new("L", size, 0)
    lower_half = Image.new("L", size, 0)
    ImageDraw.Draw(upper_half).rectangle((0, 0, size[0], 838), fill=255)
    ImageDraw.Draw(lower_half).rectangle((0, 839, size[0], size[1]), fill=255)
    upper_lip_mask = ImageChops.multiply(lip_edge, upper_half)
    lower_lip_mask = ImageChops.multiply(lip_edge, lower_half)
    mouth_interior_mask = ImageChops.subtract(mouth_mask, mask_union(upper_lip_mask, lower_lip_mask))

    parts = {
        "body_base": None,
        "hands_book": masked(full, hands_book_mask),
        "left_brow": masked(full, left_brow_mask),
        "right_brow": masked(full, right_brow_mask),
        "left_pupil": left_pupil,
        "right_pupil": right_pupil,
        "left_upper_lid": left_upper_lid,
        "left_lower_lid": left_lower_lid,
        "right_upper_lid": right_upper_lid,
        "right_lower_lid": right_lower_lid,
        "glasses": glasses,
        "mouth_interior": masked(full, mouth_interior_mask),
        "upper_lip": masked(full, upper_lip_mask),
        "lower_lip": masked(full, lower_lip_mask),
    }

    visible_removal = mask_union(
        hands_book_mask,
        left_brow_mask,
        right_brow_mask,
        left_eye_raw,
        right_eye_raw,
        glasses_mask,
        mouth_mask,
    )
    parts["body_base"] = inpaint_background(full, visible_removal)

    PARTS_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for name, image in parts.items():
        save_single_layer_psd(image, name, PARTS_DIR / f"{name}.psd")
        image.save(PREVIEW_DIR / f"{name}.png")

    # PSD children are serialized background-to-foreground in this builder.
    # Always reopen the saved PSD before previewing or validating it.
    draw_order = [
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
    master = PSDImage.new("RGBA", size, color=(0, 0, 0, 0))
    for name in draw_order:
        add_cropped_layer(master, parts[name], name)
    master.save(STAGING)

    rebuilt = PSDImage.open(STAGING).composite().convert("RGBA")
    rebuilt.save(PREVIEW_DIR / "restructured_composite.png")
    full.save(PREVIEW_DIR / "original_composite.png")
    diff = ImageChops.difference(full, rebuilt)
    diff.save(PREVIEW_DIR / "pixel_difference.png")

    full_np = np.array(full, dtype=np.int16)
    rebuilt_np = np.array(rebuilt, dtype=np.int16)
    delta = np.abs(full_np - rebuilt_np)
    print(f"staging={STAGING}")
    print(f"parts={PARTS_DIR}")
    print(f"mean_abs_error={delta.mean():.4f}")
    print(f"max_abs_error={delta.max()}")
    print(f"changed_pixels={np.count_nonzero(np.any(delta > 0, axis=2))}")


if __name__ == "__main__":
    main()
