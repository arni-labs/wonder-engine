#!/usr/bin/env python3
"""Create a starter layout manifest for a picture-book PDF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def front_matter_spread(kind: str, image_dir: str) -> dict:
    if kind == "characters":
        return {
            "type": "front_matter",
            "front_matter_kind": "characters",
            "image": f"{image_dir}/characters.png",
            "heading": "Meet The Cast",
            "text": (
                "Replace with short character descriptions and a locked label sheet. "
                "Use clean portraits, avatars, prop cards, or small world-native vignettes."
            ),
            "text_rendering_mode": "mixed",
            "native_text_policy": (
                "Native image text is allowed for short integrated character names, badges, "
                "and one-line role notes after a label audit. Manually correct or regenerate "
                "any misspelled critical labels."
            ),
            "label_sheet": [
                {
                    "id": "C1",
                    "text": "Character Name - brief who-they-are note",
                    "target": "Replace with character or prop target.",
                    "reader_purpose": "Explain who this character is, not only their name.",
                    "brief_explanation": "Replace with a tiny role, want, job, or story function.",
                    "importance": "critical",
                    "rendering_mode": "native_or_manual",
                    "max_length": "1 name plus 1 short who-they-are note",
                    "fallback": "Overlay manually if native text is wrong.",
                }
            ],
            "native_text_space": (
                "Use a clean world-native layout for portraits or avatars with calm "
                "areas for short names, labels, badges, and descriptions."
            ),
            "text_blocks": [
                {
                    "role": "heading",
                    "text": "Meet The Cast",
                    "box": [0.75, 0.65, 15.5, 0.75],
                    "size_pt": 24,
                    "min_size_pt": 18,
                    "bold": True,
                    "color": "blue",
                    "align": "center",
                },
                    {
                        "role": "body",
                        "text": (
                            "Replace with manual corrections or extra short labels only. "
                            "Remove this block if all labels are accepted as native image text."
                        ),
                    "box": [1.0, 8.9, 15.0, 1.35],
                    "size_pt": 13,
                    "min_size_pt": 10,
                    "color": "ink",
                    "align": "center",
                },
            ],
        }
    if kind == "world":
        return {
            "type": "front_matter",
            "front_matter_kind": "world",
            "image": f"{image_dir}/world.png",
            "heading": "A Map Of The World",
            "text": (
                "Replace with a locked label sheet for map, object, machine, or concept labels."
            ),
            "text_rendering_mode": "mixed",
            "native_text_policy": (
                "Native image text is allowed for short integrated map marks, object labels, "
                "badges, arrows, route names, and tiny rules after a label audit. Manually "
                "correct or regenerate any misspelled critical labels."
            ),
            "label_sheet": [
                {
                    "id": "W1",
                    "text": "World Label - brief what-it-does note",
                    "target": "Replace with map place, object, machine, or rule target.",
                    "reader_purpose": "Explain what this fictional world element is when the name is not obvious.",
                    "brief_explanation": "Replace with a tiny function, rule, or why-it-matters note.",
                    "importance": "critical",
                    "rendering_mode": "native_or_manual",
                    "max_length": "1 short label plus 1 brief function note",
                    "fallback": "Overlay manually if native text is wrong.",
                }
            ],
            "native_text_space": (
                "Use a map, cutaway, object atlas, route chart, machine diagram, "
                "or another world-native format with calm label areas."
            ),
            "text_blocks": [
                {
                    "role": "heading",
                    "text": "A Map Of The World",
                    "box": [0.75, 0.65, 15.5, 0.75],
                    "size_pt": 24,
                    "min_size_pt": 18,
                    "bold": True,
                    "color": "blue",
                    "align": "center",
                },
                {
                    "role": "body",
                    "text": (
                        "Replace with manual corrections or extra short explanatory labels only. "
                        "Remove this block if all labels are accepted as native image text."
                    ),
                    "box": [1.0, 8.9, 15.0, 1.35],
                    "size_pt": 13,
                    "min_size_pt": 10,
                    "color": "ink",
                    "align": "center",
                },
            ],
        }
    raise ValueError(f"Unknown front matter kind: {kind}")


def spread_page(number: int, image_dir: str) -> dict:
    chapter = ((number - 1) // 4) + 1
    is_chapter_start = (number - 1) % 4 == 0
    heading_box = [0.75, 1.12, 5.8, 1.0] if is_chapter_start else [0.75, 1.05, 5.8, 0.75]
    body_box = [0.75, 2.45, 5.8, 5.35] if is_chapter_start else [0.75, 2.0, 5.8, 5.8]
    page = {
        "type": "spread",
        "spread_number": number,
        "image": f"{image_dir}/spread-{number:02d}.png",
        "native_text_space": (
            "Generate or choose art with native blank/pale text space sized to "
            "the final text; do not rely on a generic side panel."
        ),
        "heading": f"Scene {number}",
        "text": "Replace with final manuscript text for this spread.",
        "text_blocks": [
            {
                "role": "heading",
                "text": f"Scene {number}",
                "box": heading_box,
                "size_pt": 22,
                "min_size_pt": 16,
                "bold": True,
                "color": "blue",
            },
            {
                "role": "body",
                "text": "Replace with final manuscript text for this spread.",
                "box": body_box,
                "size_pt": 17,
                "min_size_pt": 11,
                "color": "ink",
                "fit_to_negative_space": {
                    "min_width_in": 2.7,
                    "max_width_in": 5.8,
                    "center_x_in": 3.7,
                    "padding_in": 0.12,
                    "min_luma": 214,
                    "max_chroma": 64,
                },
            },
        ],
    }
    if is_chapter_start:
        page["chapter_label"] = f"CHAPTER {chapter}"
        page["text_blocks"].insert(
            0,
            {
                "role": "chapter_label",
                "text": f"CHAPTER {chapter}",
                "box": [0.75, 0.68, 5.6, 0.35],
                "size_pt": 13,
                "bold": True,
                "color": "blue",
            },
        )
    return page


def build_manifest(
    title: str,
    subtitle: str,
    author: str,
    spreads: int,
    image_dir: str,
    include_front_matter: bool,
    include_back_matter: bool,
    include_back_cover: bool,
    dpi: int,
) -> dict:
    pages = [
        {
            "type": "cover",
            "image": f"{image_dir}/cover.png",
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "title_box": [0.7, 0.55, 7.1, 2.1],
            "subtitle_box": [0.85, 2.65, 6.8, 0.8],
            "author_box": [0.7, 9.7, 7.1, 0.6],
        }
    ]
    if include_front_matter:
        pages.append(front_matter_spread("characters", image_dir))
        pages.append(front_matter_spread("world", image_dir))
    pages.extend(spread_page(number, image_dir) for number in range(1, spreads + 1))
    if include_back_matter:
        pages.append(
            {
                "type": "spread",
                "spread_number": spreads + 1,
                "image": f"{image_dir}/back-matter.png",
                "heading": "The Real Idea Under The Adventure",
                "text": "Replace with concise back matter explaining the source idea.",
                "native_text_space": (
                    "Use a deliberately calm diagram, notebook, wall, or map margin "
                    "as the native text area."
                ),
                "text_blocks": [
                    {
                        "role": "heading",
                        "text": "The Real Idea Under The Adventure",
                        "box": [0.75, 0.9, 6.5, 0.85],
                        "size_pt": 22,
                        "min_size_pt": 16,
                        "bold": True,
                        "color": "blue",
                    },
                    {
                        "role": "body",
                        "text": "Replace with concise back matter explaining the source idea.",
                        "box": [0.75, 1.95, 6.4, 7.8],
                        "size_pt": 16,
                        "min_size_pt": 11,
                        "color": "ink",
                        "fit_to_negative_space": {
                            "min_width_in": 2.7,
                            "max_width_in": 5.8,
                            "center_x_in": 3.7,
                            "padding_in": 0.12,
                            "min_luma": 214,
                            "max_chroma": 64,
                        },
                    },
                ],
            }
        )
    if include_back_cover:
        pages.append(
            {
                "type": "back_cover",
                "image": f"{image_dir}/back-cover.png",
                "native_text_space": (
                    "Use portrait back-cover art with a calm text area for a short "
                    "book blurb, source note, or production credit."
                ),
                "text_blocks": [
                    {
                        "role": "heading",
                        "text": "About This Adventure",
                        "box": [0.8, 1.1, 6.9, 0.85],
                        "size_pt": 22,
                        "min_size_pt": 16,
                        "bold": True,
                        "color": "blue",
                        "align": "center",
                    },
                    {
                        "role": "body",
                        "text": "Replace with a short back-cover blurb, source note, or reader invitation.",
                        "box": [1.05, 2.25, 6.4, 5.2],
                        "size_pt": 15,
                        "min_size_pt": 10,
                        "color": "ink",
                        "fit_to_negative_space": {
                            "min_width_in": 2.7,
                            "max_width_in": 5.6,
                            "center_x_in": 4.25,
                            "padding_in": 0.12,
                            "min_luma": 214,
                            "max_chroma": 64,
                        },
                    },
                    {
                        "role": "credit",
                        "text": author,
                        "box": [1.05, 9.35, 6.4, 0.5],
                        "size_pt": 13,
                        "min_size_pt": 10,
                        "color": "blue",
                        "align": "center",
                    },
                ],
            }
        )
    return {
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "dpi": dpi,
        "trim": {"cover": [8.5, 11.0], "spread": [17.0, 11.0]},
        "continuity": {
            "source_thesis": "Replace with the source idea that must stay true.",
            "world_rules": [
                "Replace with a stable rule of how this world works.",
                "Replace with what important machines, creatures, or systems can and cannot do.",
            ],
            "map_anchors": [
                "Replace with stable places, routes, thresholds, or districts."
            ],
            "material_palette": [
                "Replace with recurring materials, colors, weather, light, and textures."
            ],
            "characters": [
                {
                    "name": "Character Name",
                    "role": "Story role and source-metaphor function.",
                    "visual_anchor": (
                        "Stable silhouette, age/scale, colors, clothing/casing, "
                        "distinctive marks, and recurring prop."
                    ),
                    "speech_anchor": "Speech pattern or recurring phrase.",
                    "do_not_change": [
                        "Replace with details that must not drift across images."
                    ],
                    "prompt_snippet": "Concise reusable prompt snippet for this character.",
                    "reference_image": f"{image_dir}/characters.png",
                }
            ],
            "world_prompt_snippet": "Concise reusable prompt snippet for the world.",
            "reference_images": {
                "characters": f"{image_dir}/characters.png",
                "world": f"{image_dir}/world.png",
            },
            "continuity_risks": [
                "Replace with details likely to drift or be confused by image generation."
            ],
        },
        "font": {
            "body": "",
            "heading": "",
            "title": "",
            "author": "",
            "body_size_pt": 17,
            "heading_size_pt": 22,
            "title_size_pt": 46,
            "subtitle_size_pt": 20,
            "author_size_pt": 18,
        },
        "pages": pages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a starter JSON manifest for Wonder Engine PDF assembly."
    )
    parser.add_argument("--title", required=True, help="Book title.")
    parser.add_argument("--subtitle", default="", help="Book subtitle or tagline.")
    parser.add_argument("--author", required=True, help="Cover author credit.")
    parser.add_argument(
        "--spreads", type=int, default=20, help="Number of main story spreads."
    )
    parser.add_argument(
        "--image-dir", default="images", help="Relative directory for generated images."
    )
    parser.add_argument(
        "--no-front-matter",
        action="store_true",
        help="Do not add the default character and world introduction spreads.",
    )
    parser.add_argument(
        "--back-matter",
        action="store_true",
        help="Add a final explanatory back-matter spread.",
    )
    parser.add_argument(
        "--back-cover",
        action="store_true",
        help="Add a portrait back-cover page after the story/back matter.",
    )
    parser.add_argument("--dpi", type=int, default=300, help="Output PDF resolution.")
    parser.add_argument("--output", required=True, help="Path to write JSON manifest.")
    args = parser.parse_args()

    if args.spreads < 1:
        raise SystemExit("--spreads must be at least 1")
    if args.dpi < 72:
        raise SystemExit("--dpi must be at least 72")

    manifest = build_manifest(
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        spreads=args.spreads,
        image_dir=args.image_dir.strip("/"),
        include_front_matter=not args.no_front_matter,
        include_back_matter=args.back_matter,
        include_back_cover=args.back_cover,
        dpi=args.dpi,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
