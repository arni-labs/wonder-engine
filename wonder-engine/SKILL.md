---
name: wonder-engine
description: Create whimsical, coherent, science-flavored illustrated picture books from serious source material such as scientific papers, research directions, school topics, cultural themes, technical trends, or nonfiction ideas. Use when the workflow should creatively interview the human to surface original ideas and preferences, extract source concepts, pitch a story world, plan chapters and spreads, write a show-dont-tell manuscript, create per-spread image prompts, generate and approve images one by one, and assemble a polished PDF.
---

# Wonder Engine

## Overview

Use this skill to turn dense source material into a strange, clever, visually rich illustrated picture book. Preserve the source's conceptual structure, but teach through scenes, dialogue, visible systems, comic failures, emotional stakes, and a coherent adventure.

Do not imitate or name any existing book, character, author, illustrator, or exact style. Use broad functional ingredients only: dense picture-book worlds, invented machines, odd science, warm adventure, clear characters, and layouts that can become a clean PDF.

## Core Rules

- Make the final deliverable a PDF unless the user asks for manuscript, prompts, or images only.
- Interview naturally and editorially. The interview is a creative extraction process: draw out the human's source material, taste, odd associations, memories, ambitions, anxieties, and original metaphors. Use options, provocations, and suggestions as sparks when they help the human think, but do not open with an ABC checklist unless the user explicitly asks for shorthand.
- Preserve the human's imagination as the center of gravity. Suggest possibilities to unlock taste and invention, then ask what attracts, irritates, or surprises them. Do not replace missing answers with the agent's favorite defaults.
- Make book titles unique, imaginative, and slightly odd. Present each title as a package with a main title and a subtitle/tagline. Avoid short generic titles unless the user asks for simplicity.
- Ask about cultural flavor, language, and things to avoid before designing the world. Do not declare or label a cultural inspiration in the book unless the user asks for that.
- Do not assume a single human child protagonist. Before pitching, establish the lead structure and cast ecology: one lead, two leads, ensemble, animal, human, machine/tool, sentient object, place-as-character, adult-centered, child-centered, or another shape.
- Ask about typography after the story concept and world direction are clear, usually before illustration blueprint or PDF assembly. Choose fonts for readability, language support, and book personality; avoid generic fallback fonts when better local or supplied fonts are available.
- Convert abstract ideas into places, machines, creatures, tools, games, rituals, hazards, maps, visible rules, or civic systems.
- Keep source terminology out of reader-facing titles, subtitles, cast names, world names, and major object names unless the user explicitly asks for technical language. The source concepts are internal scaffolding; the story should reveal them through events.
- Keep the story coherent. Each spread must follow from the prior spread and change what can happen next.
- Keep character and world continuity explicit. Maintain a continuity bible for stable character appearance, props, scale, speech, relationships, map logic, world rules, recurring machines, materials, and no-go changes.
- Write real story scenes, not captions. Main story spreads should usually carry enough text, dialogue, action, and emotional turn to feel like a page from a book, not a two-sentence storyboard panel.
- Show, do not tell. Prefer characters in situations, making choices, talking, testing, misunderstanding, repairing, escaping, or discovering.
- Avoid static encyclopedia spreads. Every spread needs a visible event, a character reaction, and a reason the image exists.
- Keep whimsy causally meaningful. Strange details should reveal character, world rules, source concepts, or consequences.
- Use the image generation available in the current environment. In Codex, use the native image generation tool; in another setup, use that setup's image generator while preserving the prompt, review, and approval loop.
- Generate images one at a time unless the user explicitly requests a batch.
- Use concept images as visual probes, not canon. Generate a simple exploratory image only after the source, world direction, cultural/language handling, lead/cast ecology, key motifs, and avoidances are known or tentatively pitched. Treat feedback from the probe as durable, but do not let the probe lock the final story, character designs, page layout, or illustration system.
- Use a hybrid text policy: allow native image text for short signs, labels, maps, tiny jokes, and designed front-matter label pages; typeset final story body text separately by default.
- Design text space before image generation. The blank or pale areas must be part of the illustrated composition, sized to the actual text, not a generic white side panel pasted over art.
- Prefer broad natural negative space for body text when it fits the scene: open sky, mist, water, snow, pale wall, blank paper-white, or calm watercolor wash. Object-shaped text areas are useful but optional.
- Fit typeset text to the shape of the negative space. Use gentle line-length changes, offsets, centered titles, or multiple text blocks when the quiet area is curved, tapered, or interrupted.
- Fit the whole text composition, not only the body paragraph. Chapter label, scene heading, body, speech bubbles, and image quiet space should feel deliberately placed together.
- Treat the first assembled PDF as a layout proof, not the final book. Do a page-by-page correction pass against the actual generated images before calling a PDF finished.
- Keep the human oriented. At every stage, clearly state what just happened, what decision or artifact comes next, and what kind of feedback would be most useful, without rushing them.

## Workflow

### 1. Interview

Start by asking only what is needed to make a strong first concept. The interview should feel like a thoughtful creative conversation, not a form. Its purpose is not only to collect requirements; it is to help the human discover what they mean.

Hard rule: the first interview turn must establish the source or seed idea unless the user has already supplied it. Ask what the book should be based on before asking accuracy, "what must stay true," story shape, world, character, or visual-style questions.

Hard rule: before producing a concept pitch, spread plan, manuscript, image prompts, images, or PDF, explicitly ask for book length and current output target unless the user already stated them. Do not silently assume the default full book. You may recommend "full book: front cover plus 20 spreads, optional back cover" after asking.

Hard rule: before producing a concept pitch, explicitly establish who or what carries the story and who else belongs in the world unless the user already stated it. Ask about the lead shape and cast mix before offering protagonist names. Do not default to one child, a family mentor, an animal companion, or a machine companion.

Do not ask about typography before the concept pitch unless the user brings up type, language/script, layout, PDF production, or visual design. Story first; typography is a later design decision.

Read `references/interview-options.md` when designing the intake. Use the question bank as hidden scaffolding. Cover these decisions over the conversation, but do not dump them all at once:

- source type and source material
- audience and reading level
- desired feeling
- story mode and world flavor
- cultural/language preferences
- lead structure and cast ecology
- required motifs or avoided motifs
- book length and output format
- author credit

If the user has already answered a category, do not ask again. State the assumption and move forward.

Before ending the pre-pitch interview, confirm any missing production choices in one compact question: length, output target, cover credit, and whether to include back matter/back cover. Do not include typography in this checkpoint unless it is already relevant from the user's answers.

Ask in small batches of 2 to 4 tailored questions. After each user answer, reflect the emerging intention in one or two sentences, then ask the next most useful follow-up. Offer choices in natural language only when a choice would speed them up, always leaving room for a custom answer.

Use creative nudges when the user is vague: offer a few sharply different interpretations, strange metaphor directions, possible emotional conflicts, or cast/world shapes, then invite the user to choose, reject, combine, or name what is missing. Treat rejection as useful signal.

Avoid repeated canned interview phrasing. Do not ask "Who is this for," "What feeling should the ending leave," or "Practical shape" as a stock bundle. Rephrase missing checkpoints around the actual source, world, and user language.

### 2. Digest the Source

For a paper or document, read it and extract the thesis, mechanism, vocabulary, evidence, stakes, limits, and future implications.

For a loose trend, research direction, school topic, or adult nonfiction theme, first synthesize the core idea, tensions, examples, and stakes. Then treat that synthesis as the source.

Read `references/source-processing.md` when mapping concepts. Produce a compact table with:

1. source concept
2. child-readable metaphor
3. visual object or place
4. character interaction
5. failure mode
6. resolution
7. likely spread

Do not flatten the source into a moral. The story should let the real idea survive inside a playful world.

### 3. Pitch the Book

Produce a concept pitch before writing the full manuscript:

- 5 creative title packages, each with a main title and subtitle/tagline
- 6 to 10 lead, duo, or ensemble name options if needed
- recommended title and lead or ensemble structure
- one-sentence thesis
- one-paragraph premise
- core concept-to-world metaphor table
- proposed world
- proposed cast ecology with roles, wants, speech patterns, relationships, and props
- proposed chapter count and story arc
- assumptions about culture, language, typography, trim size, and PDF output

Titles should feel specific to this book, not interchangeable with a generic adventure. The main title may be poetic, strange, place-based, object-based, or character-based. The subtitle/tagline should add mischief, promise, stakes, or comic specificity without explaining the source concept too literally.

Names should be easy to read aloud and easy to typeset. Avoid diacritics unless the user wants them.

Before presenting title options, perform the scaffolding-leak check in `references/source-processing.md`. Titles should sound like adventure titles, not paper abstracts or internal concept maps.

### 4. Optional Concept Visual Probe

Use this stage when the user asks to see the concept, when the world is hard to imagine, or when early visual feedback would prevent wasted story work.

Do not generate the probe before the idea has enough anchors. Minimum anchors:

- source or seed idea
- audience and emotional direction
- rough world direction
- cultural/language handling
- lead shape and cast ecology
- several visual motifs or no-go zones
- current title or working title, if available

If the user asks for an image too early, give a brief reason and ask for the smallest missing anchor needed to avoid a misleading image. If the user insists, make the image explicitly provisional.

The probe should be one simple concept image, not a final spread:

- no final body text
- no final cover typography
- no exact character model sheet unless character design is the point
- no source jargon or internal metaphor labels
- no final page layout commitments
- no over-specific scene that forces the later plot

Prompt it as an exploratory mood-and-world frame: the place, social mix, machinery/nature balance, material texture, density, lighting, and one small visible incident. Ask for feedback on what feels right, wrong, too literal, too generic, too culturally thin, too crowded, or worth carrying forward.

After the probe, summarize durable visual preferences separately from the image's accidental details. Carry forward the preferences, not the whole image.

### 5. Build The Continuity Bible And Opening Anchor Spreads

After the pitch and any visual probe, create a compact continuity bible before generating final story images. Read `references/continuity.md`.

The continuity bible is internal production scaffolding. It should include:

- character anchors: stable visual identity, silhouette, proportions, colors, clothing, props, gestures, speech pattern, role, want, arc, relationships, do-not-change notes, and reusable prompt snippet
- world anchors: map/geography, routes, scale, material palette, light/weather, recurring objects, machines, rules, civic systems, source-metaphor logic, language/signage handling, do-not-change notes, and reusable prompt snippet
- approved reference image paths when available, especially the character-introduction and world-introduction spreads
- continuity risks, such as easy-to-confuse characters, similar props, repeated machines, or rules the image model may literalize incorrectly

The opening character-introduction spread and world-introduction spread should be built from this bible. They serve the reader, but they also become visual anchors for the rest of the book. Generate and approve them before the main story images whenever possible.

If a later user change alters a character design, map, object, or world rule, update the continuity bible first, then revise affected prompts, images, and text.

### 6. Plan Chapters And Spreads

Default structure, after the user confirms or accepts it:

- front cover
- opening character-introduction spread
- opening world-introduction spread, such as a map, object atlas, concept diagram, or labeled civic system
- 5 chapters
- 4 spreads per chapter
- 20 main story spreads
- optional back matter explaining the real idea under the adventure
- optional portrait back cover with a short blurb, source note, or production credit

For each spread, include:

- spread number
- scene title
- story purpose
- what visibly happens
- who wants what
- what changes or goes wrong
- characters present
- source concept, if any
- substantial draft text, not just a caption or summary

The opening character spread should introduce the cast through portraits, avatars, small vignettes, object props, or another format that fits the book's world. The opening world spread should introduce the place and its key story objects through a map, cutaway, diagram, artifact table, route chart, machine atlas, or other world-native form. These front-matter spreads should orient the reader visually without becoming static encyclopedia pages, and they should match the internal continuity bible.

The chapter title appears only on the first spread of that chapter. Later spreads use a small scene heading or no heading.

### 7. Write The Manuscript

Rewrite the full manuscript after the beat plan is approved or clearly good enough.

Requirements:

- Use scene-first prose.
- Default main story spread text should usually be about 120 to 220 words, unless the user requests a younger, sparser, or more poetic book. A spread under about 90 words should be a deliberate pacing choice, not the default.
- Include more dialogue and character action than narration.
- Give each spread a small scene shape: situation, action, friction or discovery, character response, and a final turn into the next spread.
- Give the lead character, duo, or ensemble real decisions.
- Make each spread readable aloud.
- Use short paragraphs and separate dialogue lines.
- Keep technical language concrete and earned by events.
- Let jokes come from situations, not random decoration.
- Make the ending emotionally warm and practically optimistic.
- Do not shorten the manuscript merely because layout is hard. Instead, plan enough native quiet space, split text into two islands, revise the image prompt, or adjust typography while preserving story substance.

Before moving on, run the manuscript against the quality checklist in `references/story-standards.md`.

### 8. Build The Illustration Blueprint

For every cover, spread, and back cover, create:

- final text
- image prompt
- composition notes
- text rendering mode: manual, native, or mixed
- text area placement and approximate word count
- native negative-space plan, such as open sky, mist, water, snow, pale wall, paper-white, calm watercolor wash, or an optional object-shaped area
- text-flow plan: rectangular, centered, tapered, stepped, two-island, stacked chapter-start group, or another gentle shape-aware layout
- typography plan: font mood, body/heading pairing, language coverage, and any user-supplied font files
- speech bubble text, if any
- important visual motifs
- characters to include
- characters to avoid or simplify
- continuity anchors to reuse from the continuity bible
- print safety notes

For character-introduction and world-introduction spreads, create a locked label sheet before image generation. These spreads may use native image text because their labels, arrows, badges, map marks, object names, and tiny explanations often need to be visually integrated into a complex diagram-like composition. Keep native text short and proofreadable: names, one-line role notes, labels, short rules, map marks, and brief callouts. Labels should be reader-helpful, not merely names: each main character needs a tiny "who they are" note, and fictional world objects or places need a brief function note unless the meaning is already obvious. Avoid long paragraphs as native image text. After generation, inspect every label and regenerate or manually correct anything misspelled, missing, or misleading before treating the spread as a continuity anchor.

When assembling the PDF, use `text_rendering_mode: native` for an anchor spread whose text is already accepted inside the image, `mixed` when only corrections or extra labels are overlaid, and `manual` when all readable text is typeset afterward. Remove placeholder `text_blocks` for any text that is already native in the approved image so labels are not duplicated.

Interior spreads should usually be double-page landscape compositions with clean native white or pale negative space for text. Often the best layout is not a text object, but an airy part of the painting where the illustrated world gathers around the edges and action points. The text area may be one broad quiet zone or several smaller zones, but it must match the amount of final text. Avoid a repeated left-page rectangle unless the scene calls for it. Do not request parchment, old paper texture, a visible center fold, or long generated body text.

For each spread, create a layout contract before image generation:

- text load and target word count
- text zone coordinates, in spread-relative terms or manifest inches
- text-zone shape: rectangle, oval/cloud, tapered wedge, stepped shape, or two islands
- text flow: centered title, left body, tapered body, stepped body, or split blocks
- image prompt language telling the model where the calm area must be and where action/detail must stop
- proof criteria: text sits on pale low-detail space, follows the quiet shape, remains readable, and does not collide with figures, machinery, buildings, or color

Read `references/story-standards.md` for the visual and layout standards.

### 9. Generate Images

Generate the cover and spreads one at a time unless the user asks for a batch. After each image:

- show the image or provide its path
- ask for targeted feedback if needed
- treat feedback as durable for future spreads unless it is clearly local
- update the prompt language before generating the next image

Generate and approve the character-introduction and world-introduction spreads before the main story spreads when possible. Use them as reference images in later prompts if the image generation environment supports references. If not, reuse the concise character/world prompt snippets from the continuity bible. Do not rely on memory alone.

For anchor spreads that use native image text, perform a label audit before approval: compare the generated labels against the locked label sheet, check spelling of names, check that roles and world rules are accurate, and decide whether to accept, regenerate, or manually correct. Do not approve an anchor spread with wrong text just because the artwork is attractive.

Keep small background characters simple. Use clean silhouettes, animals, boats, tools, signs, plants, buildings, or machines instead of many tiny detailed faces.

### 10. Layout Correction And PDF Assembly

When images and text are approved, assemble a proof PDF, then correct layout against the actual generated art before producing the final PDF.

- place approved images as page backgrounds
- typeset exact manuscript text manually into native blank or pale image areas
- use the chosen font pairing; if the requested language or glyph set is not covered, choose a supported alternative and note it
- do not rely on starter manifest boxes as final placement
- inspect the real usable pale/low-detail area on each generated image
- update each page's text zones, split text islands, or regenerate art when the quiet space does not match the text
- shape text blocks to the actual quiet area rather than defaulting to a rectangle when the whitespace is curved, tapered, or broken by illustration
- when available, run the negative-space fitting helper before final assembly so `line_shape` rows are derived from the actual art, then inspect the proof visually
- preserve safe margins
- avoid busy art behind text
- include front cover, story spreads, optional front/back matter, and optional back cover
- check page order, title, author credit, chapter title placement, readability, character continuity, and world-rule continuity
- on chapter-start spreads, check the chapter label, chapter title/heading, and body as a single group: they must share the same quiet area, align intentionally, keep enough vertical spacing, and never overlap

Use `scripts/new_manifest.py` to create a layout manifest and `scripts/assemble_picture_book_pdf.py` for proof and final raster PDFs:

```bash
python3 scripts/new_manifest.py --title "Working Title" --subtitle "A Quirky Tagline" --author "by Name" --spreads 20 --back-cover --output build/book-manifest.json
python3 scripts/fit_text_to_negative_space.py build/book-manifest.json --output build/book-manifest-fitted.json
python3 scripts/assemble_picture_book_pdf.py build/book-manifest-fitted.json --output build/book-layout-proof.pdf --preview-dir build/previews
```

The assembly script is a practical helper, not a substitute for visual judgment. Inspect the rendered preview PNGs and PDF page by page. Revise text boxes, line shapes, font sizes, text islands, or images until it reads cleanly. Only then export or name the final PDF.

Use `text_blocks[].fit_to_negative_space` when the body block should be measured against the generated image. The helper will write `text_blocks[].line_shape` with gentle line-by-line offsets and widths. If the image does not honor the layout contract, regenerate or revise the art rather than forcing text over busy detail.

Do not call a PDF production-ready until every page passes the layout gate: text sits on calm native space, line shape follows the visible quiet area, headings are aligned with the natural opening, no text crosses into busy art or saturated color, no faces/machinery/ropes/windows interfere with reading, large blank areas are intentional, and the result looks designed rather than placed by coordinates.

After every major stage, end with a forward-guidance note: the recommended next step, why it comes next, and the specific feedback the human can give now. Examples of feedback prompts: choose a title package, reject/merge concept directions, approve character/world anchors, mark visual details to keep/change, approve manuscript tone, approve layout proof, or identify pages that need regeneration.

## Resource Guide

- `references/interview-options.md`: option-based intake templates and defaults.
- `references/source-processing.md`: source extraction and concept-to-world mapping.
- `references/continuity.md`: continuity bible, character/world anchors, and prompt reuse rules.
- `references/story-standards.md`: manuscript, spread, image prompt, and PDF quality rules.
- `assets/layout-manifest-template.json`: starter manifest format for PDF assembly.
- `scripts/new_manifest.py`: create a blank manifest for cover plus spreads.
- `scripts/fit_text_to_negative_space.py`: derive shaped text rows from pale low-detail areas in the generated art.
- `scripts/assemble_picture_book_pdf.py`: combine generated images and manually typeset text into a PDF.
