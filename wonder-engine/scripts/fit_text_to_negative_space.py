#!/usr/bin/env python3
"""Fit text rows to pale, low-detail negative space in generated artwork.

This is a proofing helper for Wonder Engine layouts. It reads a JSON manifest,
finds text blocks with "fit_to_negative_space", analyzes the block area in the
actual image, and writes line-by-line offsets/widths back to the manifest.

The result is intentionally gentle: it produces book-like shaped text blocks,
not extreme contour typography.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median
from typing import Iterable

from PIL import Image

from assemble_picture_book_pdf import (
    box_to_px,
    fit_fill,
    font_config,
    font_path,
    inch,
    line_height,
    load_font,
    load_manifest,
    page_inches,
    resolve_image,
)


def fit_options(value: object) -> dict:
    if value is True:
        return {}
    if isinstance(value, dict):
        return value
    return {}


def color_is_quiet(
    pixel: tuple[int, int, int],
    *,
    min_luma: float,
    max_chroma: float,
    white_luma: float,
) -> bool:
    red, green, blue = pixel
    luma = 0.299 * red + 0.587 * green + 0.114 * blue
    chroma = max(pixel) - min(pixel)
    return luma >= min_luma and (chroma <= max_chroma or luma >= white_luma)


def close_small_gaps(values: list[bool], max_gap: int) -> list[bool]:
    if max_gap <= 0:
        return values

    closed = values[:]
    index = 0
    while index < len(closed):
        if closed[index]:
            index += 1
            continue

        start = index
        while index < len(closed) and not closed[index]:
            index += 1
        end = index

        if (
            start > 0
            and end < len(closed)
            and closed[start - 1]
            and closed[end]
            and end - start <= max_gap
        ):
            for gap_index in range(start, end):
                closed[gap_index] = True
    return closed


def longest_run(values: list[bool]) -> tuple[int, int] | None:
    best: tuple[int, int] | None = None
    start: int | None = None

    for index, value in enumerate(values + [False]):
        if value and start is None:
            start = index
        elif not value and start is not None:
            run = (start, index)
            if best is None or run[1] - run[0] > best[1] - best[0]:
                best = run
            start = None
    return best


def quiet_columns_for_row(
    image: Image.Image,
    left: int,
    right: int,
    center_y: int,
    band_height: int,
    *,
    min_luma: float,
    max_chroma: float,
    white_luma: float,
    min_safe_ratio: float,
    gap_close_px: int,
) -> list[bool]:
    top = max(0, center_y - band_height // 2)
    bottom = min(image.height, center_y + max(1, band_height // 2))
    if bottom <= top:
        bottom = min(image.height, top + 1)

    pixels = image.load()
    safe_columns: list[bool] = []
    sample_step = max(1, (bottom - top) // 10)

    for x in range(left, right):
        safe = 0
        total = 0
        for y in range(top, bottom, sample_step):
            total += 1
            if color_is_quiet(
                pixels[x, y],
                min_luma=min_luma,
                max_chroma=max_chroma,
                white_luma=white_luma,
            ):
                safe += 1
        safe_columns.append(total > 0 and safe / total >= min_safe_ratio)

    return close_small_gaps(safe_columns, gap_close_px)


def smooth_segments(
    segments: list[tuple[float, float]],
    *,
    max_shift_in: float,
) -> list[tuple[float, float]]:
    if not segments:
        return []

    smoothed: list[tuple[float, float]] = []
    for index, _segment in enumerate(segments):
        window = segments[max(0, index - 1) : min(len(segments), index + 2)]
        left = float(median(item[0] for item in window))
        right = float(median(item[1] for item in window))
        if smoothed:
            prev_left, prev_right = smoothed[-1]
            left = max(prev_left - max_shift_in, min(prev_left + max_shift_in, left))
            right = max(prev_right - max_shift_in, min(prev_right + max_shift_in, right))
        if right <= left:
            right = left + 0.5
        smoothed.append((left, right))
    return smoothed


def constrain_segment_width(
    left: float,
    right: float,
    *,
    max_width_in: float | None,
    center_x_in: float | None,
) -> tuple[float, float]:
    if max_width_in is None or max_width_in <= 0:
        return left, right

    current_width = right - left
    if current_width <= max_width_in:
        return left, right

    target_width = max_width_in
    desired_center = center_x_in if center_x_in is not None else (left + right) / 2
    new_left = desired_center - target_width / 2
    new_left = max(left, min(right - target_width, new_left))
    return new_left, new_left + target_width


def scan_text_block(
    page_image: Image.Image,
    manifest: dict,
    block: dict,
    page_dpi: int,
) -> tuple[list[dict], dict]:
    options = fit_options(block.get("fit_to_negative_space"))
    scan_box = options.get("scan_box", block.get("box", [0.75, 2.0, 5.8, 5.8]))
    block_box = block.get("box", scan_box)

    scan_x, scan_y, scan_w, scan_h = box_to_px(scan_box, page_dpi)
    block_x, _block_y, block_w, _block_h = box_to_px(block_box, page_dpi)

    size_pt = int(block.get("size_pt", font_config(manifest, "body_size_pt", 17)))
    font_key = "heading" if block.get("bold") or block.get("role") == "heading" else "body"
    font = load_font(font_path(manifest, font_key), inch(size_pt / 72, page_dpi))
    row_height = line_height(font)

    row_count = int(options.get("rows", max(1, scan_h // max(1, row_height))))
    min_luma = float(options.get("min_luma", 214))
    max_chroma = float(options.get("max_chroma", 62))
    white_luma = float(options.get("white_luma", 232))
    min_safe_ratio = float(options.get("min_safe_ratio", 0.74))
    min_width_in = float(options.get("min_width_in", 2.6))
    max_width_in = options.get("max_width_in")
    max_width_in = float(max_width_in) if max_width_in is not None else None
    center_x_in = options.get("center_x_in")
    center_x_in = float(center_x_in) if center_x_in is not None else None
    padding_in = float(options.get("padding_in", 0.08))
    max_shift_in = float(options.get("max_shift_in", 0.22))
    band_ratio = float(options.get("band_ratio", 0.75))
    gap_close_in = float(options.get("gap_close_in", 0.1))

    sample_scale = float(options.get("sample_scale", 0.28))
    sample_scale = min(1.0, max(0.08, sample_scale))
    sample_size = (
        max(1, int(round(page_image.width * sample_scale))),
        max(1, int(round(page_image.height * sample_scale))),
    )
    sample = page_image.resize(sample_size, Image.Resampling.BOX).convert("RGB")

    s_left = max(0, int(round(scan_x * sample_scale)))
    s_right = min(sample.width, int(round((scan_x + scan_w) * sample_scale)))
    s_top = max(0, int(round(scan_y * sample_scale)))
    s_height = max(1, int(round(scan_h * sample_scale)))
    s_row_height = max(1, int(round(row_height * sample_scale)))
    s_band_height = max(1, int(round(s_row_height * band_ratio)))
    s_gap_close = max(0, int(round(inch(gap_close_in, page_dpi) * sample_scale)))
    s_min_width = max(1, int(round(inch(min_width_in, page_dpi) * sample_scale)))

    fallback_left = scan_x / page_dpi
    fallback_right = (scan_x + min(scan_w, block_w)) / page_dpi
    raw_segments: list[tuple[float, float]] = []
    warnings = 0

    previous: tuple[float, float] | None = None
    for row in range(row_count):
        center_y = s_top + int(round((row + 0.5) * s_row_height))
        if center_y >= sample.height:
            center_y = sample.height - 1

        columns = quiet_columns_for_row(
            sample,
            s_left,
            s_right,
            center_y,
            s_band_height,
            min_luma=min_luma,
            max_chroma=max_chroma,
            white_luma=white_luma,
            min_safe_ratio=min_safe_ratio,
            gap_close_px=s_gap_close,
        )
        run = longest_run(columns)
        if run and run[1] - run[0] >= s_min_width:
            left = (s_left + run[0]) / sample_scale / page_dpi
            right = (s_left + run[1]) / sample_scale / page_dpi
            previous = (left, right)
        elif previous:
            left, right = previous
            warnings += 1
        else:
            left, right = fallback_left, fallback_right
            previous = (left, right)
            warnings += 1
        raw_segments.append((left, right))

    segments = smooth_segments(raw_segments, max_shift_in=max_shift_in)

    rows: list[dict] = []
    for left, right in segments:
        left, right = constrain_segment_width(
            left,
            right,
            max_width_in=max_width_in,
            center_x_in=center_x_in,
        )
        padded_left = max(left + padding_in, block_x / page_dpi)
        padded_right = min(right - padding_in, (block_x + block_w) / page_dpi)
        if padded_right - padded_left < min_width_in:
            center = (left + right) / 2
            half = min_width_in / 2
            padded_left = max(block_x / page_dpi, center - half)
            padded_right = min((block_x + block_w) / page_dpi, center + half)
        rows.append(
            {
                "x": round(padded_left - block_x / page_dpi, 3),
                "width": round(max(0.5, padded_right - padded_left), 3),
            }
        )

    metadata = {
        "method": "negative-space-mask",
        "rows": len(rows),
        "fallback_rows": warnings,
        "min_luma": min_luma,
        "max_chroma": max_chroma,
        "white_luma": white_luma,
        "min_safe_ratio": min_safe_ratio,
    }
    return rows, metadata


def iter_fit_blocks(manifest: dict) -> Iterable[tuple[int, dict, dict]]:
    for page_index, page in enumerate(manifest.get("pages", [])):
        for block in page.get("text_blocks", []) or []:
            if block.get("fit_to_negative_space"):
                yield page_index, page, block


def fit_manifest(manifest_path: Path) -> dict:
    manifest = load_manifest(manifest_path)
    dpi = int(manifest.get("dpi", 300))
    base_dir = manifest_path.parent
    page_cache: dict[int, Image.Image] = {}

    for page_index, page, block in iter_fit_blocks(manifest):
        if page_index not in page_cache:
            page_w_in, page_h_in = page_inches(manifest, page)
            size_px = (inch(page_w_in, dpi), inch(page_h_in, dpi))
            source = Image.open(resolve_image(page["image"], base_dir)).convert("RGB")
            page_cache[page_index] = fit_fill(source, size_px)
        rows, metadata = scan_text_block(page_cache[page_index], manifest, block, dpi)
        block["line_shape"] = rows
        block["negative_space_fit"] = metadata

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add mask-derived line_shape rows to Wonder Engine text blocks."
    )
    parser.add_argument("manifest", help="Input manifest JSON.")
    parser.add_argument("--output", required=True, help="Path for fitted manifest JSON.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    fitted = fit_manifest(manifest_path)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(fitted, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
