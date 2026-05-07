#!/usr/bin/env python3
"""Assemble generated picture-book images and exact text into a PDF.

The manifest is JSON. See assets/layout-manifest-template.json for the shape.
This script rasterizes final pages with Pillow, which is useful for proofs and
many print workflows. Inspect the result before delivery.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


BLUE = (23, 61, 92)
INK = (24, 28, 32)
WHITE = (255, 255, 255)
COLORS = {
    "blue": BLUE,
    "ink": INK,
    "white": WHITE,
}

PLACEHOLDER_MARKERS = (
    "Replace with",
    "Working Title",
    "A Quirky Tagline",
    "by Author Name",
    "Scene Heading",
    "Character Name -",
    "World Label -",
)

REGULAR_FONTS = [
    "/System/Library/Fonts/Supplemental/Iowan Old Style.ttc",
    "/System/Library/Fonts/Supplemental/Charter.ttc",
    "/System/Library/Fonts/Palatino.ttc",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "DejaVuSerif.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/Library/Fonts/Georgia.ttf",
]

BOLD_FONTS = [
    "/System/Library/Fonts/Supplemental/Cochin.ttc",
    "/System/Library/Fonts/Supplemental/Baskerville.ttc",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "DejaVuSerif-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def inch(value: float, dpi: int) -> int:
    return int(round(float(value) * dpi))


def box_to_px(box: Iterable[float], dpi: int) -> tuple[int, int, int, int]:
    x, y, w, h = box
    return inch(x, dpi), inch(y, dpi), inch(w, dpi), inch(h, dpi)


def load_manifest(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON manifest: {exc}") from exc


def resolve_image(path: str, base_dir: Path) -> Path:
    image_path = Path(path)
    if not image_path.is_absolute():
        image_path = base_dir / image_path
    if not image_path.exists():
        raise SystemExit(f"Missing image: {image_path}")
    return image_path


def page_inches(manifest: dict, page: dict) -> tuple[float, float]:
    trim = manifest.get("trim", {})
    if page.get("type") in {"cover", "back_cover"}:
        size = trim.get("cover", [8.5, 11.0])
    else:
        size = trim.get("spread", [17.0, 11.0])
    return float(size[0]), float(size[1])


def fit_fill(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (int(round(image.width * scale)), int(round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - target_w) // 2)
    top = max(0, (resized.height - target_h) // 2)
    return resized.crop((left, top, left + target_w, top + target_h))


def load_font(preferred: str | None, size_px: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = []
    if preferred:
        candidates.append(preferred)
    candidates.extend(BOLD_FONTS if bold else REGULAR_FONTS)

    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size_px)
        except OSError:
            continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    if not text:
        return 0, 0
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def split_long_word(
    draw: ImageDraw.ImageDraw, word: str, font: ImageFont.ImageFont, max_width: int
) -> list[str]:
    chunks: list[str] = []
    current = ""
    for char in word:
        trial = current + char
        if current and text_size(draw, trial, font)[0] > max_width:
            chunks.append(current)
            current = char
        else:
            current = trial
    if current:
        chunks.append(current)
    return chunks


def wrap_paragraph(
    draw: ImageDraw.ImageDraw, paragraph: str, font: ImageFont.ImageFont, max_width: int
) -> list[str]:
    words = paragraph.split()
    if not words:
        return [""]

    lines: list[str] = []
    current = ""
    for word in words:
        pieces = [word]
        if text_size(draw, word, font)[0] > max_width:
            pieces = split_long_word(draw, word, font, max_width)
        for piece in pieces:
            trial = piece if not current else f"{current} {piece}"
            if current and text_size(draw, trial, font)[0] > max_width:
                lines.append(current)
                current = piece
            else:
                current = trial
    if current:
        lines.append(current)
    return lines


def line_height(font: ImageFont.ImageFont, multiplier: float = 1.45) -> int:
    left, top, right, bottom = font.getbbox("Ag")
    return max(1, int((bottom - top) * multiplier))


def layout_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(wrap_paragraph(draw, paragraph.strip(), font, max_width))
    return lines


def line_shape_rows(
    block: dict, default_width: int, dpi: int
) -> list[tuple[int, int]]:
    rows = block.get("line_shape") or []
    shaped_rows: list[tuple[int, int]] = []
    for row in rows:
        if isinstance(row, dict):
            offset = inch(float(row.get("x", 0)), dpi)
            width = inch(float(row.get("width", default_width / dpi)), dpi)
        elif isinstance(row, (list, tuple)) and len(row) >= 2:
            offset = inch(float(row[0]), dpi)
            width = inch(float(row[1]), dpi)
        else:
            continue
        shaped_rows.append((offset, max(1, width)))
    return shaped_rows


def row_shape_at(
    rows: list[tuple[int, int]], index: int, default_width: int
) -> tuple[int, int]:
    if not rows:
        return 0, default_width
    if index < len(rows):
        return rows[index]
    return rows[-1]


def layout_text_shaped(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    rows: list[tuple[int, int]],
    default_width: int,
) -> list[str]:
    lines: list[str] = []
    line_index = 0
    for paragraph in text.splitlines():
        if not paragraph.strip():
            lines.append("")
            line_index += 1
            continue

        current = ""
        for word in paragraph.split():
            _, row_width = row_shape_at(rows, line_index, default_width)
            pieces = [word]
            if text_size(draw, word, font)[0] > row_width:
                pieces = split_long_word(draw, word, font, row_width)
            for piece in pieces:
                _, row_width = row_shape_at(rows, line_index, default_width)
                trial = piece if not current else f"{current} {piece}"
                if current and text_size(draw, trial, font)[0] > row_width:
                    lines.append(current)
                    line_index += 1
                    current = piece
                else:
                    current = trial
        if current:
            lines.append(current)
            line_index += 1
    return lines


def block_height(
    lines: list[str], font: ImageFont.ImageFont, multiplier: float = 1.45
) -> int:
    lh = line_height(font, multiplier)
    height = 0
    for line in lines:
        height += lh if line else int(lh * 0.55)
    return height


def fit_body_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_height: int,
    font_path: str | None,
    start_pt: int,
    min_pt: int,
    dpi: int,
    line_height_mult: float = 1.45,
) -> tuple[ImageFont.ImageFont, list[str], bool]:
    for pt in range(start_pt, min_pt - 1, -1):
        font = load_font(font_path, inch(pt / 72, dpi), bold=False)
        lines = layout_text(draw, text, font, max_width)
        if block_height(lines, font, line_height_mult) <= max_height:
            return font, lines, True

    font = load_font(font_path, inch(min_pt / 72, dpi), bold=False)
    return font, layout_text(draw, text, font, max_width), False


def fit_shaped_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    rows: list[tuple[int, int]],
    max_width: int,
    max_height: int,
    font_path: str | None,
    start_pt: int,
    min_pt: int,
    dpi: int,
    bold: bool = False,
    line_height_mult: float = 1.45,
) -> tuple[ImageFont.ImageFont, list[str], bool]:
    for pt in range(start_pt, min_pt - 1, -1):
        font = load_font(font_path, inch(pt / 72, dpi), bold=bold)
        lines = layout_text_shaped(draw, text, font, rows, max_width)
        if block_height(lines, font, line_height_mult) <= max_height:
            return font, lines, True

    font = load_font(font_path, inch(min_pt / 72, dpi), bold=bold)
    return font, layout_text_shaped(draw, text, font, rows, max_width), False


def draw_fade_panel(canvas: Image.Image, page: dict, dpi: int) -> None:
    panel_side = page.get("text_panel")
    if panel_side not in {"left", "right"}:
        return

    width, height = canvas.size
    panel_width = inch(float(page.get("text_panel_width", 6.8)), dpi)
    fade_width = inch(float(page.get("fade_width", 0.65)), dpi)
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    if panel_side == "left":
        draw.rectangle((0, 0, panel_width, height), fill=WHITE + (255,))
        for offset in range(fade_width):
            alpha = int(255 * (1 - offset / max(1, fade_width)))
            x = panel_width + offset
            if x < width:
                draw.line((x, 0, x, height), fill=WHITE + (alpha,))
    else:
        draw.rectangle((width - panel_width, 0, width, height), fill=WHITE + (255,))
        for offset in range(fade_width):
            alpha = int(255 * (1 - offset / max(1, fade_width)))
            x = width - panel_width - offset
            if x >= 0:
                draw.line((x, 0, x, height), fill=WHITE + (alpha,))

    canvas.alpha_composite(overlay)


def font_config(manifest: dict, key: str, default: int) -> int:
    return int(manifest.get("font", {}).get(key, default))


def font_path(manifest: dict, key: str) -> str | None:
    value = manifest.get("font", {}).get(key)
    return str(value) if value else None


def parse_color(value: str | list[int] | tuple[int, int, int] | None) -> tuple[int, int, int]:
    if value is None:
        return INK
    if isinstance(value, str):
        lower = value.lower()
        if lower in COLORS:
            return COLORS[lower]
        if lower.startswith("#") and len(lower) == 7:
            return tuple(int(lower[index : index + 2], 16) for index in (1, 3, 5))
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return tuple(int(channel) for channel in value)
    return INK


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    font: ImageFont.ImageFont,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int],
    shadow: tuple[int, int, int] | None = None,
    shadow_offset: int = 0,
) -> None:
    x, y, w, h = box
    lh = line_height(font)
    total_h = block_height(lines, font)
    cursor = y + max(0, (h - total_h) // 2)
    for line in lines:
        if line:
            tw, _ = text_size(draw, line, font)
            line_x = x + max(0, (w - tw) // 2)
            if shadow and shadow_offset:
                draw.text(
                    (line_x + shadow_offset, cursor + shadow_offset),
                    line,
                    font=font,
                    fill=shadow,
                )
            draw.text((line_x, cursor), line, font=font, fill=fill)
            cursor += lh
        else:
            cursor += int(lh * 0.55)


def draw_cover_text(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    manifest: dict,
    page: dict,
    dpi: int,
) -> None:
    title = page.get("title", manifest.get("title", ""))
    subtitle = page.get("subtitle", manifest.get("subtitle", ""))
    author = page.get("author", manifest.get("author", ""))
    title_box = box_to_px(page.get("title_box", [0.7, 0.6, 7.1, 2.2]), dpi)
    subtitle_box = box_to_px(page.get("subtitle_box", [0.85, 2.65, 6.8, 0.8]), dpi)
    author_box = box_to_px(page.get("author_box", [0.7, 9.7, 7.1, 0.6]), dpi)
    title_fill = parse_color(page.get("title_color", "blue"))
    subtitle_fill = parse_color(page.get("subtitle_color", "ink"))
    author_fill = parse_color(page.get("author_color", "ink"))
    shadow_fill = page.get("cover_shadow_color")
    shadow = parse_color(shadow_fill) if shadow_fill else None
    shadow_offset = inch(float(page.get("cover_shadow_offset_in", 0.0)), dpi)

    title_start = int(page.get("title_size_pt", font_config(manifest, "title_size_pt", 46)))
    title_font_path = font_path(manifest, "title")
    for pt in range(title_start, 22, -2):
        font = load_font(title_font_path, inch(pt / 72, dpi), bold=True)
        lines = layout_text(draw, title, font, title_box[2])
        if block_height(lines, font) <= title_box[3]:
            draw_centered_lines(
                draw, lines, font, title_box, title_fill, shadow, shadow_offset
            )
            break

    if subtitle:
        subtitle_start = int(
            page.get("subtitle_size_pt", font_config(manifest, "subtitle_size_pt", 20))
        )
        subtitle_font_path = font_path(manifest, "heading")
        for pt in range(subtitle_start, 11, -1):
            font = load_font(subtitle_font_path, inch(pt / 72, dpi), bold=False)
            lines = layout_text(draw, subtitle, font, subtitle_box[2])
            if block_height(lines, font) <= subtitle_box[3]:
                draw_centered_lines(
                    draw, lines, font, subtitle_box, subtitle_fill, shadow, shadow_offset
                )
                break

    author_font = load_font(
        font_path(manifest, "author"),
        inch(font_config(manifest, "author_size_pt", 18) / 72, dpi),
        bold=False,
    )
    author_lines = layout_text(draw, author, author_font, author_box[2])
    draw_centered_lines(
        draw, author_lines, author_font, author_box, author_fill, shadow, shadow_offset
    )


def draw_spread_text(
    draw: ImageDraw.ImageDraw,
    manifest: dict,
    page: dict,
    dpi: int,
) -> list[str]:
    warnings: list[str] = []
    text = page.get("text", "")
    if not text:
        return warnings

    box = box_to_px(page.get("text_box", [0.7, 0.75, 5.7, 9.5]), dpi)
    x, y, w, h = box
    cursor = y

    heading_font = load_font(
        font_path(manifest, "heading"),
        inch(int(page.get("heading_size_pt", font_config(manifest, "heading_size_pt", 22))) / 72, dpi),
        bold=True,
    )
    small_heading_font = load_font(
        font_path(manifest, "heading"),
        inch(13 / 72, dpi),
        bold=True,
    )

    chapter_label = page.get("chapter_label")
    if chapter_label:
        draw.text((x, cursor), str(chapter_label).upper(), font=small_heading_font, fill=BLUE)
        cursor += line_height(small_heading_font)

    heading = page.get("heading")
    if heading:
        heading_lines = layout_text(draw, str(heading), heading_font, w)
        for line in heading_lines:
            draw.text((x, cursor), line, font=heading_font, fill=BLUE)
            cursor += line_height(heading_font)
        cursor += inch(0.12, dpi)

    body_start = int(page.get("body_size_pt", font_config(manifest, "body_size_pt", 17)))
    body_min = int(page.get("min_body_size_pt", 11))
    body_font, lines, fits = fit_body_font(
        draw=draw,
        text=text,
        max_width=w,
        max_height=max(1, y + h - cursor),
        font_path=font_path(manifest, "body"),
        start_pt=body_start,
        min_pt=body_min,
        dpi=dpi,
    )
    if not fits:
        warnings.append(
            f"Spread {page.get('spread_number', '?')} text overflowed at {body_min} pt"
        )

    lh = line_height(body_font)
    bottom = y + h
    for line in lines:
        step = lh if line else int(lh * 0.55)
        if cursor + step > bottom:
            break
        if line:
            draw.text((x, cursor), line, font=body_font, fill=INK)
        cursor += step
    return warnings


def draw_text_block(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    manifest: dict,
    page: dict,
    block: dict,
    dpi: int,
) -> list[str]:
    warnings: list[str] = []
    text = str(block.get("text", ""))
    if not text:
        return warnings

    x, y, w, h = box_to_px(block.get("box", [0.75, 1.0, 5.8, 5.8]), dpi)
    role = str(block.get("role", "body"))
    size_pt = int(block.get("size_pt", font_config(manifest, "body_size_pt", 17)))
    min_size_pt = int(block.get("min_size_pt", block.get("min_body_size_pt", 11)))
    bold = bool(block.get("bold", role in {"chapter_label", "heading"}))
    fill = parse_color(block.get("color", "blue" if bold else "ink"))
    stroke_fill = parse_color(block.get("stroke_fill")) if block.get("stroke_fill") else None
    stroke_width_px = int(block.get("stroke_width_px", 0))
    if block.get("stroke_width_in") is not None:
        stroke_width_px = max(0, inch(float(block.get("stroke_width_in", 0.0)), dpi))
    align = str(block.get("align", "left"))
    font_key = "heading" if bold or role in {"chapter_label", "heading"} else "body"
    rows = line_shape_rows(block, w, dpi)
    line_height_mult = float(block.get("line_height_mult", block.get("leading", 1.45)))

    if rows:
        font, lines, fits = fit_shaped_font(
            draw=draw,
            text=text,
            rows=rows,
            max_width=w,
            max_height=h,
            font_path=font_path(manifest, font_key),
            start_pt=size_pt,
            min_pt=min_size_pt,
            dpi=dpi,
            bold=bold,
            line_height_mult=line_height_mult,
        )
        if not fits:
            warnings.append(
                f"Spread {page.get('spread_number', '?')} block '{role}' overflowed"
            )
    elif role == "body" or block.get("fit", True):
        font, lines, fits = fit_body_font(
            draw=draw,
            text=text,
            max_width=w,
            max_height=h,
            font_path=font_path(manifest, font_key),
            start_pt=size_pt,
            min_pt=min_size_pt,
            dpi=dpi,
            line_height_mult=line_height_mult,
        )
        if bold:
            font = load_font(font_path(manifest, font_key), inch(size_pt / 72, dpi), bold=True)
            lines = layout_text(draw, text, font, w)
            if block_height(lines, font, line_height_mult) > h:
                for pt in range(size_pt - 1, min_size_pt - 1, -1):
                    font = load_font(font_path(manifest, font_key), inch(pt / 72, dpi), bold=True)
                    lines = layout_text(draw, text, font, w)
                    if block_height(lines, font, line_height_mult) <= h:
                        fits = True
                        break
                else:
                    fits = False
            else:
                fits = True
        if not fits:
            warnings.append(
                f"Spread {page.get('spread_number', '?')} block '{role}' overflowed"
            )
    else:
        font = load_font(font_path(manifest, font_key), inch(size_pt / 72, dpi), bold=bold)
        lines = layout_text(draw, text, font, w)

    cursor = y
    if str(block.get("vertical_align", "top")) == "center":
        cursor = y + max(0, (h - block_height(lines, font, line_height_mult)) // 2)

    background_fill = block.get("background_fill")
    if background_fill:
        if not bool(manifest.get("_allow_text_backgrounds")):
            warnings.append(
                f"Spread {page.get('spread_number', '?')} block '{role}' has "
                "background_fill; ignored because story text must sit on native "
                "image space. Use --allow-text-backgrounds only for an explicitly "
                "requested graphic-card treatment."
            )
        else:
            pad = inch(float(block.get("background_padding_in", 0.08)), dpi)
            radius = inch(float(block.get("background_radius_in", 0.08)), dpi)
            background_h = h
            if bool(block.get("background_auto_height", True)):
                background_h = min(h, block_height(lines, font, line_height_mult))
            bg_box = (x - pad, cursor - pad, x + w + pad, cursor + background_h + pad)
            outline = block.get("background_outline")
            alpha_value = block.get("background_alpha", 1.0)
            alpha = int(255 * float(alpha_value))
            background_color = parse_color(background_fill)
            outline_fill = parse_color(outline) if outline else None
            width = (
                max(1, inch(float(block.get("background_outline_width_in", 0.01)), dpi))
                if outline
                else 1
            )
            if alpha < 255:
                overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rounded_rectangle(
                    bg_box,
                    radius=max(0, radius),
                    fill=background_color + (max(0, min(255, alpha)),),
                    outline=outline_fill + (max(0, min(255, alpha)),) if outline_fill else None,
                    width=width,
                )
                canvas.alpha_composite(overlay)
                draw = ImageDraw.Draw(canvas)
            else:
                draw.rounded_rectangle(
                    bg_box,
                    radius=max(0, radius),
                    fill=background_color,
                    outline=outline_fill,
                    width=width,
                )

    lh = line_height(font, line_height_mult)
    bottom = y + h
    for line_index, line in enumerate(lines):
        row_offset, row_width = row_shape_at(rows, line_index, w)
        step = lh if line else int(lh * 0.55)
        if cursor + step > bottom:
            break
        if line:
            draw_x = x + row_offset
            active_width = row_width
            if align == "center":
                draw_x += max(0, (active_width - text_size(draw, line, font)[0]) // 2)
            elif align == "right":
                draw_x += max(0, active_width - text_size(draw, line, font)[0])
            draw.text(
                (draw_x, cursor),
                line,
                font=font,
                fill=fill,
                stroke_width=stroke_width_px,
                stroke_fill=stroke_fill,
            )
        cursor += step

    return warnings


def block_box_px(block: dict, dpi: int) -> tuple[int, int, int, int] | None:
    if not block.get("text") or not block.get("box"):
        return None
    return box_to_px(block["box"], dpi)


def boxes_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int], padding: int = 0) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (
        ax + aw + padding <= bx
        or bx + bw + padding <= ax
        or ay + ah + padding <= by
        or by + bh + padding <= ay
    )


def text_block_layout_warnings(page: dict, blocks: list[dict], dpi: int) -> list[str]:
    warnings: list[str] = []
    measured: list[tuple[str, tuple[int, int, int, int]]] = []
    for block in blocks:
        box = block_box_px(block, dpi)
        if box:
            measured.append((str(block.get("role", "body")), box))

    for i, (role_a, box_a) in enumerate(measured):
        for role_b, box_b in measured[i + 1 :]:
            if boxes_overlap(box_a, box_b):
                warnings.append(
                    f"Spread {page.get('spread_number', '?')} text blocks "
                    f"'{role_a}' and '{role_b}' have overlapping boxes"
                )

    roles = {str(block.get("role", "")): block for block in blocks}
    heading = roles.get("heading")
    body = roles.get("body")
    if page.get("chapter_label") and heading and body and heading.get("box") and body.get("box"):
        heading_bottom = float(heading["box"][1]) + float(heading["box"][3])
        body_top = float(body["box"][1])
        min_gap_in = 0.12
        if body_top < heading_bottom + min_gap_in:
            warnings.append(
                f"Spread {page.get('spread_number', '?')} chapter heading/body "
                "need more vertical breathing room"
            )
    return warnings


def draw_text_blocks(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    manifest: dict,
    page: dict,
    dpi: int,
) -> list[str]:
    blocks = page.get("text_blocks") or []
    warnings: list[str] = text_block_layout_warnings(page, blocks, dpi)
    for block in blocks:
        warnings.extend(draw_text_block(canvas, draw, manifest, page, block, dpi))
    return warnings


def page_label(page: dict, index: int | None = None) -> str:
    prefix = f"Page {index}: " if index is not None else ""
    if page.get("spread_number"):
        return f"{prefix}spread {page['spread_number']}"
    if page.get("front_matter_kind"):
        return f"{prefix}{page['front_matter_kind']} front matter"
    return f"{prefix}{page.get('type', 'page')}"


def iter_strings(value: object, path: str = "$"):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield from iter_strings(nested, f"{path}.{key}")
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            yield from iter_strings(nested, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def is_starter_scene_heading(value: str) -> bool:
    stripped = value.strip()
    if not stripped.startswith("Scene "):
        return False
    return stripped.removeprefix("Scene ").isdigit()


def preflight_manifest(
    manifest: dict,
    manifest_path: Path,
    dpi: int,
    allow_text_backgrounds: bool,
    allow_text_panels: bool,
) -> list[str]:
    warnings: list[str] = []
    base_dir = manifest_path.parent

    for path, value in iter_strings(manifest):
        if any(marker in value for marker in PLACEHOLDER_MARKERS) or is_starter_scene_heading(value):
            warnings.append(f"Placeholder starter text remains at {path}: {value[:90]}")

    for index, page in enumerate(manifest.get("pages", []), start=1):
        label = page_label(page, index)
        image = page.get("image")
        if not image:
            warnings.append(f"{label} has no image path.")
        else:
            image_path = Path(str(image))
            if not image_path.is_absolute():
                image_path = base_dir / image_path
            if not image_path.exists():
                warnings.append(f"{label} image is missing: {image_path}")

        if (page.get("render_panel") or page.get("text_panel")) and not allow_text_panels:
            warnings.append(
                f"{label} asks for a rendered text panel; it will be ignored unless "
                "--allow-text-panels is used. Regenerate art with native quiet space instead."
            )

        blocks = page.get("text_blocks") or []
        if page.get("type") in {"spread", "back_cover"} and page.get("text_rendering_mode") != "native":
            if not blocks:
                warnings.append(
                    f"{label} has no text_blocks; generic fallback text layout is not "
                    "acceptable for a final Wonder Engine PDF."
                )
            for block in blocks:
                role = str(block.get("role", "body"))
                if block.get("background_fill") and not allow_text_backgrounds:
                    warnings.append(
                        f"{label} block '{role}' uses background_fill; final story text "
                        "should be fitted to native image space, not pasted on a card."
                    )
                if (
                    role == "body"
                    and block.get("text")
                    and not (
                        block.get("fit_to_negative_space")
                        or block.get("line_shape")
                        or block.get("shape_verified")
                    )
                ):
                    warnings.append(
                        f"{label} body text has no fit_to_negative_space, line_shape, "
                        "or shape_verified marker."
                    )

        if page.get("type") == "front_matter" and page.get("text_rendering_mode") != "native":
            for block in blocks:
                if block.get("background_fill") and not allow_text_backgrounds:
                    warnings.append(
                        f"{label} block '{block.get('role', 'body')}' uses background_fill; "
                        "use native/mixed labels or world-native surfaces instead."
                    )

    return warnings


def render_page(manifest: dict, page: dict, base_dir: Path, dpi: int) -> tuple[Image.Image, list[str]]:
    page_w_in, page_h_in = page_inches(manifest, page)
    size_px = (inch(page_w_in, dpi), inch(page_h_in, dpi))
    source_image = Image.open(resolve_image(page["image"], base_dir)).convert("RGB")
    canvas = fit_fill(source_image, size_px).convert("RGBA")
    warnings: list[str] = []

    should_draw_panel = page.get("render_panel") or (
        page.get("type") == "spread" and not page.get("text_blocks") and page.get("text_panel")
    )
    if should_draw_panel:
        if bool(manifest.get("_allow_text_panels")):
            draw_fade_panel(canvas, page, dpi)
        else:
            warnings.append(
                f"{page_label(page)} requested a text panel; ignored because final "
                "story text should sit on native image space. Use --allow-text-panels "
                "only for an explicitly requested panel treatment."
            )

    draw = ImageDraw.Draw(canvas)
    if page.get("type") == "cover":
        draw_cover_text(canvas, draw, manifest, page, dpi)
    elif page.get("text_rendering_mode") == "native":
        pass
    elif page.get("text_blocks"):
        warnings.extend(draw_text_blocks(canvas, draw, manifest, page, dpi))
    else:
        warnings.extend(draw_spread_text(draw, manifest, page, dpi))

    return canvas.convert("RGB"), warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assemble a picture-book PDF from a Wonder Engine JSON manifest."
    )
    parser.add_argument("manifest", help="Path to JSON layout manifest.")
    parser.add_argument("--output", required=True, help="Path to write PDF.")
    parser.add_argument(
        "--preview-dir",
        help="Optional directory for rendered PNG previews of each PDF page.",
    )
    parser.add_argument("--dpi", type=int, help="Override manifest DPI.")
    parser.add_argument(
        "--strict-final",
        action="store_true",
        help=(
            "Fail if starter text, missing images, generic fallback spread text, "
            "card backgrounds, or unverified body text blocks remain."
        ),
    )
    parser.add_argument(
        "--allow-text-backgrounds",
        action="store_true",
        help="Permit block background_fill rendering for explicitly requested card treatments.",
    )
    parser.add_argument(
        "--allow-text-panels",
        action="store_true",
        help="Permit page-level rendered text panels for explicitly requested panel treatments.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = load_manifest(manifest_path)
    pages = manifest.get("pages", [])
    if not pages:
        raise SystemExit("Manifest has no pages.")

    dpi = int(args.dpi or manifest.get("dpi", 300))
    if dpi < 72:
        raise SystemExit("DPI must be at least 72.")

    allow_text_backgrounds = bool(
        args.allow_text_backgrounds or manifest.get("allow_text_backgrounds")
    )
    allow_text_panels = bool(args.allow_text_panels or manifest.get("allow_text_panels"))
    manifest["_allow_text_backgrounds"] = allow_text_backgrounds
    manifest["_allow_text_panels"] = allow_text_panels

    rendered: list[Image.Image] = []
    warnings: list[str] = preflight_manifest(
        manifest,
        manifest_path,
        dpi,
        allow_text_backgrounds=allow_text_backgrounds,
        allow_text_panels=allow_text_panels,
    )
    if args.strict_final and warnings:
        for warning in warnings:
            print(f"Warning: {warning}")
        raise SystemExit("Strict final validation failed; fix the manifest, images, or layout.")

    preview_dir = Path(args.preview_dir) if args.preview_dir else None
    if preview_dir:
        preview_dir.mkdir(parents=True, exist_ok=True)

    for index, page in enumerate(pages, start=1):
        image, page_warnings = render_page(manifest, page, manifest_path.parent, dpi)
        rendered.append(image)
        warnings.extend(page_warnings)
        if preview_dir:
            slug = page.get("type", "page")
            if page.get("spread_number"):
                slug = f"spread-{int(page['spread_number']):02d}"
            image.save(preview_dir / f"{index:02d}-{slug}.png")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    first, rest = rendered[0], rendered[1:]
    first.save(output, "PDF", save_all=True, append_images=rest, resolution=dpi)

    print(f"Wrote {output}")
    for warning in warnings:
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()
