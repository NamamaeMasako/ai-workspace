from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer


PROJECT = Path(__file__).resolve().parents[1]
LEGACY = PROJECT / "source_backup_20260722_1532" / "包子_original.psd"
PARTS = PROJECT / "source" / "parts"
PREVIEW = PROJECT / "preview" / "source_restructure_v2"
PAGE_REFERENCE = PROJECT / "archive" / "master_backups" / "包子_before_rebuild_20260722_174738.psd"
SCALE = 4


def manual_composite(psd: PSDImage) -> Image.Image:
    result = Image.new("RGBA", psd.size, (0, 0, 0, 0))
    for layer in psd:
        result.alpha_composite(layer.composite().convert("RGBA"), (layer.left, layer.top))
    return result


def place_layer(layer, size: tuple[int, int]) -> Image.Image:
    result = Image.new("RGBA", size, (0, 0, 0, 0))
    result.alpha_composite(layer.composite().convert("RGBA"), (layer.left, layer.top))
    return result


def aa_mask(size: tuple[int, int], draw_fn) -> Image.Image:
    large = Image.new("L", (size[0] * SCALE, size[1] * SCALE), 0)
    draw_fn(ImageDraw.Draw(large), SCALE)
    return large.resize(size, Image.Resampling.LANCZOS)


def aa_ellipse(size: tuple[int, int], bbox: tuple[int, int, int, int]) -> Image.Image:
    return aa_mask(size, lambda draw, s: draw.ellipse(tuple(v * s for v in bbox), fill=255))


def aa_polygon(size: tuple[int, int], points: list[tuple[int, int]]) -> Image.Image:
    return aa_mask(size, lambda draw, s: draw.polygon([(x * s, y * s) for x, y in points], fill=255))


def bezier(p0, p1, p2, p3, count=80) -> list[tuple[float, float]]:
    points = []
    for t in np.linspace(0.0, 1.0, count):
        u = 1.0 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points


def masked(image: Image.Image, mask: Image.Image) -> Image.Image:
    result = image.copy()
    result.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
    return result


def composite(*images: Image.Image) -> Image.Image:
    result = Image.new("RGBA", images[0].size, (0, 0, 0, 0))
    for image in images:
        result.alpha_composite(image)
    return result


def add_layer(canvas: PSDImage, image: Image.Image, name: str) -> None:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        PixelLayer.frompil(Image.new("RGBA", (1, 1), (0, 0, 0, 0)), canvas, name=name)
        return
    PixelLayer.frompil(image.crop(bbox), canvas, name=name, left=bbox[0], top=bbox[1])


def save_part(image: Image.Image, name: str) -> None:
    psd = PSDImage.new("RGBA", image.size, color=(0, 0, 0, 0))
    add_layer(psd, image, name)
    psd.save(PARTS / f"{name}.psd")
    image.save(PREVIEW / f"{name}.png")


def draw_stroke(size: tuple[int, int], points: list[tuple[float, float]], colour, width: int) -> Image.Image:
    large = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(large)
    scaled = [(round(x * SCALE), round(y * SCALE)) for x, y in points]
    d.line(scaled, fill=colour, width=width * SCALE, joint="curve")
    radius = width * SCALE // 2
    for x, y in (scaled[0], scaled[-1]):
        d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=colour)
    return large.resize(size, Image.Resampling.LANCZOS)


def outline_from_mask(mask: Image.Image, colour, width: int) -> Image.Image:
    kernel = width * 2 + 1
    outer = mask.filter(ImageFilter.MaxFilter(kernel))
    inner = mask.filter(ImageFilter.MinFilter(kernel))
    ring = ImageChops.subtract(outer, inner)
    result = Image.new("RGBA", mask.size, colour)
    result.putalpha(ImageChops.multiply(result.getchannel("A"), ring))
    return result


def make_blush(size: tuple[int, int]) -> Image.Image:
    blush_mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(blush_mask)
    d.ellipse((205, 752, 350, 858), fill=82)
    d.ellipse((904, 752, 1049, 858), fill=82)
    blush_mask = blush_mask.filter(ImageFilter.GaussianBlur(22))
    blush = Image.new("RGBA", size, (255, 129, 119, 255))
    blush.putalpha(blush_mask)

    slashes = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(slashes)
    for x in (274, 297, 320):
        sd.line((x * SCALE, 832 * SCALE, (x + 11) * SCALE, 812 * SCALE), fill=(139, 62, 52, 255), width=2 * SCALE)
    for x in (927, 950, 973):
        sd.line((x * SCALE, 812 * SCALE, (x + 11) * SCALE, 832 * SCALE), fill=(139, 62, 52, 255), width=2 * SCALE)
    return composite(blush, slashes.resize(size, Image.Resampling.LANCZOS))


def make_clean_hand(size: tuple[int, int], bbox: tuple[int, int, int, int]) -> Image.Image:
    """Draw one complete hand with a single antialiased perimeter."""
    mask = aa_ellipse(size, bbox)
    h, w = size[1], size[0]
    y0, y1 = bbox[1], bbox[3]
    yy, _ = np.mgrid[0:h, 0:w]
    t = np.clip((yy - y0) / max(1, y1 - y0), 0, 1)[:, :, None]
    top = np.array([255, 254, 249], dtype=float)
    bottom = np.array([249, 225, 199], dtype=float)
    rgb = top[None, None, :] * (1 - t) + bottom[None, None, :] * t
    fill = Image.fromarray(
        np.dstack((rgb.clip(0, 255).astype(np.uint8), np.array(mask))), "RGBA"
    )

    large = Image.new("RGBA", (w * SCALE, h * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(large)
    d.ellipse(
        tuple(v * SCALE for v in bbox),
        outline=(111, 77, 52, 255),
        width=3 * SCALE,
    )
    return composite(fill, large.resize(size, Image.Resampling.LANCZOS))


def make_body(size: tuple[int, int], legacy_body: Image.Image, top_creases: Image.Image) -> Image.Image:
    w, h = size
    # Build one clean closed bun contour. The previous scanline-filled legacy
    # silhouette inherited stray edge fragments, so no old contour pixels are
    # used here.
    segments = [
        ((627, 136), (604, 134), (590, 142), (578, 151)),
        ((578, 151), (560, 151), (544, 147), (526, 151)),
        ((526, 151), (487, 163), (461, 207), (396, 243)),
        ((396, 243), (302, 301), (220, 366), (178, 460)),
        ((178, 460), (132, 552), (106, 648), (108, 720)),
        ((108, 720), (105, 812), (125, 878), (160, 932)),
        ((160, 932), (222, 1032), (300, 1091), (390, 1116)),
        ((390, 1116), (480, 1142), (560, 1155), (627, 1155)),
    ]
    left_path: list[tuple[float, float]] = []
    for i, segment in enumerate(segments):
        points = bezier(*segment, count=45)
        left_path.extend(points if i == 0 else points[1:])
    right_path = [(w - x, y) for x, y in reversed(left_path[:-1])]
    silhouette = aa_polygon(size, [(round(x), round(y)) for x, y in left_path + right_path])

    yy, xx = np.mgrid[0:h, 0:w]
    dx = np.abs((xx - 627) / 520).clip(0, 1)
    lower = np.clip((yy - 650) / 520, 0, 1)
    shade = 22 * dx**3 + 8 * lower
    rgb = np.empty((h, w, 3), dtype=np.float32)
    rgb[:, :, 0] = 255 - shade * 0.42
    rgb[:, :, 1] = 253 - shade * 0.70
    rgb[:, :, 2] = 247 - shade
    alpha = np.array(silhouette)
    rgba = np.dstack((rgb.clip(0, 255).astype(np.uint8), alpha))
    body = Image.fromarray(rgba, "RGBA")

    # Use one continuous procedural outline instead of the incomplete legacy
    # contour fragments. Crown creases and fixed blush remain baked into base.
    outline = outline_from_mask(silhouette, (71, 43, 28, 255), 2)
    return composite(body, top_creases, make_blush(size), outline)


def make_hands_book(
    size: tuple[int, int],
    full: Image.Image,
    body: Image.Image,
    clean_page_reference: Image.Image,
) -> Image.Image:
    book_points = [
        (312, 906), (337, 882), (421, 885), (505, 909), (563, 938), (623, 970),
        (682, 936), (758, 906), (906, 881), (933, 908), (925, 1103),
        (655, 1182), (590, 1182), (324, 1106),
    ]
    book_mask = aa_polygon(size, book_points)
    # Keep the artwork's single existing cover/hand outline.  The earlier
    # cleanup drew a second outline around it, which caused the visible echo.
    book_part = masked(full, book_mask)
    # Rebuild the simple hands instead of tracing over the legacy hands.  A
    # slightly fuller silhouette hides the body contour behind them, while a
    # single new outline avoids the previous echo/double-edge problem.
    hand_part = composite(
        make_clean_hand(size, (244, 942, 367, 1091)),
        make_clean_hand(size, (887, 942, 1010, 1091)),
    )

    # Replace only the messy stacked-page zone with the already approved
    # clean page treatment from the previous revision.  This preserves the
    # current single book/hand outline while removing the pale offset lines.
    page_zone = Image.new("L", size, 0)
    ImageDraw.Draw(page_zone).polygon(
        [(300, 845), (954, 845), (954, 982), (627, 995), (300, 982)], fill=255
    )
    clean_pages = masked(clean_page_reference, page_zone)

    result = composite(book_part, clean_pages, hand_part)
    # The legacy export contains a thin magenta fringe around the book. It is
    # not part of the artwork; normalize those pixels to the new brown outline.
    rgba = np.array(result)
    hsv = cv2.cvtColor(rgba[:, :, :3], cv2.COLOR_RGB2HSV)
    fringe = (hsv[:, :, 0] > 135) & (hsv[:, :, 0] < 179) & (hsv[:, :, 1] > 60) & (rgba[:, :, 3] > 0)
    rgba[fringe, :3] = (91, 57, 38)
    return Image.fromarray(rgba, "RGBA")


def make_brow(size, full, source_alpha, box) -> Image.Image:
    crop = Image.new("L", size, 0)
    ImageDraw.Draw(crop).rectangle(box, fill=255)
    return masked(full, ImageChops.multiply(source_alpha, crop))


def make_pupil(size: tuple[int, int], center: tuple[int, int], highlight_x: int, mirror_shine: bool) -> Image.Image:
    w, h = size
    cx, cy = center
    rx, ry = 52, 57
    yy, xx = np.mgrid[0:h, 0:w]
    t = np.clip((yy - (cy - ry)) / (2 * ry), 0, 1)
    top = np.array([55, 34, 17], dtype=float)
    bottom = np.array([210, 145, 73], dtype=float)
    colour = top[None, None, :] * (1 - t[:, :, None]) + bottom[None, None, :] * t[:, :, None]
    dark = np.exp(-(((xx - cx) / 38) ** 2 + ((yy - (cy - 9)) / 33) ** 2))[:, :, None]
    colour *= 1 - 0.74 * dark
    ellipse = aa_ellipse(size, (cx - rx, cy - ry, cx + rx, cy + ry))
    rgba = np.dstack((colour.clip(0, 255).astype(np.uint8), np.array(ellipse)))
    pupil = Image.fromarray(rgba, "RGBA")

    outline = Image.new("RGBA", (w * SCALE, h * SCALE), (0, 0, 0, 0))
    od = ImageDraw.Draw(outline)
    od.ellipse(tuple(v * SCALE for v in (cx - rx, cy - ry, cx + rx, cy + ry)), outline=(41, 25, 12, 255), width=4 * SCALE)
    od.ellipse(tuple(v * SCALE for v in (highlight_x - 13, cy - 40, highlight_x + 13, cy - 14)), fill=(255, 255, 250, 255))
    shine_y = cy + 34
    if mirror_shine:
        od.line(((cx + 24) * SCALE, (shine_y - 7) * SCALE, (cx + 34) * SCALE, (shine_y + 5) * SCALE), fill=(255, 248, 231, 255), width=2 * SCALE)
        od.line(((cx - 29) * SCALE, (shine_y + 2) * SCALE, (cx - 20) * SCALE, (shine_y - 8) * SCALE), fill=(255, 248, 231, 255), width=2 * SCALE)
    else:
        od.line(((cx - 24) * SCALE, (shine_y - 7) * SCALE, (cx - 34) * SCALE, (shine_y + 5) * SCALE), fill=(255, 248, 231, 255), width=2 * SCALE)
        od.line(((cx + 29) * SCALE, (shine_y + 2) * SCALE, (cx + 20) * SCALE, (shine_y - 8) * SCALE), fill=(255, 248, 231, 255), width=2 * SCALE)
    return composite(pupil, outline.resize(size, Image.Resampling.LANCZOS))


def make_upper_lid(size, body, curve: list[tuple[float, float]], left: bool) -> Image.Image:
    if left:
        top = [(358, 610), (525, 610), curve[-1]]
        polygon = top + list(reversed(curve)) + [(358, curve[0][1])]
    else:
        top = [(729, 610), (896, 610), (896, curve[-1][1])]
        polygon = top + list(reversed(curve)) + [(729, 610)]
    skin = masked(body, aa_polygon(size, [(round(x), round(y)) for x, y in polygon]))
    lash = draw_stroke(size, curve, (48, 31, 15, 255), 8)
    return composite(skin, lash)


def make_lower_lid(size, body, points: list[tuple[float, float]], left: bool) -> Image.Image:
    if left:
        polygon = points + [(520, 850), (360, 850)]
    else:
        polygon = points + [(895, 850), (735, 850)]
    return masked(body, aa_polygon(size, [(round(x), round(y)) for x, y in polygon]))


def make_glasses(size) -> Image.Image:
    large = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), (0, 0, 0, 0))
    d = ImageDraw.Draw(large)
    dark = (30, 27, 24, 255)
    mid = (67, 60, 53, 255)
    rings = ((294, 562, 589, 860), (664, 562, 959, 860))
    for bbox in rings:
        scaled = tuple(v * SCALE for v in bbox)
        d.ellipse(scaled, outline=dark, width=17 * SCALE)
        d.ellipse(scaled, outline=mid, width=10 * SCALE)

    for bbox in ((258, 691, 317, 725), (936, 691, 995, 725)):
        scaled = tuple(v * SCALE for v in bbox)
        d.rounded_rectangle(scaled, radius=15 * SCALE, fill=dark)
        inset = tuple((v + (4 if i < 2 else -4)) * SCALE for i, v in enumerate(bbox))
        d.rounded_rectangle(inset, radius=11 * SCALE, fill=mid)

    result = large.resize(size, Image.Resampling.LANCZOS)
    bridge = bezier((579, 714), (601, 685), (649, 685), (674, 714))
    return composite(
        result,
        draw_stroke(size, bridge, dark, 17),
        draw_stroke(size, bridge, mid, 10),
    )


def make_mouth_interior(size, upper_curve, lower_curve) -> Image.Image:
    # Complete closed shape, independent from both lip strokes. The darker
    # upper area is the mouth cavity; the warmer lower area reads as tongue.
    points = upper_curve + list(reversed(lower_curve))
    mask = aa_polygon(size, [(round(x), round(y)) for x, y in points])
    h, w = size[1], size[0]
    yy, _ = np.mgrid[0:h, 0:w]
    t = np.clip((yy - 809) / 58, 0, 1)[:, :, None]
    top = np.array([201, 91, 78], dtype=float)
    bottom = np.array([255, 154, 143], dtype=float)
    rgb = top[None, None, :] * (1 - t) + bottom[None, None, :] * t
    rgba = np.dstack((rgb.clip(0, 255).astype(np.uint8), np.array(mask)))
    return Image.fromarray(rgba, "RGBA")


def main() -> None:
    PARTS.mkdir(parents=True, exist_ok=True)
    PREVIEW.mkdir(parents=True, exist_ok=True)
    psd = PSDImage.open(LEGACY)
    size = psd.size
    legacy = {layer.name: place_layer(layer, size) for layer in psd}
    full = manual_composite(psd)
    full.save(PREVIEW / "reference.png")

    page_psd = PSDImage.open(PAGE_REFERENCE)
    page_layer = next(layer for layer in page_psd if layer.name == "hands_book")
    clean_page_reference = place_layer(page_layer, size)

    body = make_body(size, legacy["body_base_holes"], legacy["top_creases"])
    hands_book = make_hands_book(size, full, body, clean_page_reference)
    left_brow = make_brow(size, full, legacy["left_brow"].getchannel("A"), (385, 500, 485, 565))
    right_brow = make_brow(size, full, legacy["right_brow"].getchannel("A"), (770, 500, 870, 565))
    left_pupil = make_pupil(size, (449, 738), 478, True)
    right_pupil = make_pupil(size, (805, 738), 826, False)

    left_curve = bezier((380, 711), (420, 703), (468, 692), (505, 688))
    right_curve = bezier((744, 688), (785, 692), (834, 703), (870, 711))
    left_upper = make_upper_lid(size, body, left_curve, True)
    right_upper = make_upper_lid(size, body, right_curve, False)
    left_lower_curve = bezier((392, 791), (425, 801), (474, 801), (508, 791))
    right_lower_curve = bezier((746, 791), (780, 801), (829, 801), (862, 791))
    left_lower = make_lower_lid(size, body, left_lower_curve, True)
    right_lower = make_lower_lid(size, body, right_lower_curve, False)

    glasses = make_glasses(size)
    upper_curve = bezier((588, 831), (590, 807), (657, 805), (661, 831))
    lower_curve = bezier((588, 831), (595, 858), (650, 875), (661, 831))
    mouth_interior = make_mouth_interior(size, upper_curve, lower_curve)
    upper_lip = draw_stroke(size, upper_curve, (119, 65, 51, 255), 5)
    lower_lip = draw_stroke(size, lower_curve, (100, 54, 43, 255), 5)

    parts = {
        "body_base": body,
        "hands_book": hands_book,
        "left_brow": left_brow,
        "right_brow": right_brow,
        "left_pupil": left_pupil,
        "right_pupil": right_pupil,
        "left_upper_lid": left_upper,
        "left_lower_lid": left_lower,
        "right_upper_lid": right_upper,
        "right_lower_lid": right_lower,
        "glasses": glasses,
        "mouth_interior": mouth_interior,
        "upper_lip": upper_lip,
        "lower_lip": lower_lip,
    }
    for name, image in parts.items():
        save_part(image, name)

    # Isolated-layer contact sheet for checking contamination and transparency.
    cells = []
    for name, image in parts.items():
        bbox = image.getchannel("A").getbbox()
        crop = image.crop(bbox) if bbox else Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        scale = min(280 / crop.width, 190 / crop.height, 1.5)
        crop = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.Resampling.LANCZOS)
        cell = Image.new("RGBA", (300, 230), (210, 210, 210, 255))
        d = ImageDraw.Draw(cell)
        for y in range(0, 200, 20):
            for x in range(0, 300, 20):
                if (x // 20 + y // 20) % 2:
                    d.rectangle((x, y, x + 19, y + 19), fill=(245, 245, 245, 255))
        cell.alpha_composite(crop, ((300 - crop.width) // 2, (200 - crop.height) // 2))
        d.rectangle((0, 200, 299, 229), fill=(32, 32, 32, 255))
        d.text((8, 207), name, fill=(255, 255, 255, 255))
        cells.append(cell.convert("RGB"))
    sheet = Image.new("RGB", (1200, 920), (255, 255, 255))
    for i, cell in enumerate(cells):
        sheet.paste(cell, ((i % 4) * 300, (i // 4) * 230))
    sheet.save(PREVIEW / "isolated_layers.png")

    print(f"parts={PARTS}")
    print(f"preview={PREVIEW}")


if __name__ == "__main__":
    main()
