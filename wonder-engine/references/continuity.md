# Continuity Guide

Use this guide after the concept pitch and before final story image generation. The goal is to keep the book's people, beings, objects, places, and rules stable across many spreads.

## Continuity Bible

Create a compact internal continuity bible. It is production scaffolding, not reader-facing prose.

Include:

- title package and working subtitle/tagline
- source thesis in one sentence
- world logic in three to seven rules
- map/geography anchors
- material and color palette
- recurring machines, instruments, tools, creatures, buildings, rituals, and civic systems
- character anchors
- approved reference images, if available
- prompt snippets to reuse
- do-not-change notes
- known risks: characters who may be confused, objects that may drift, rules that may be literalized, and visual details that must stay simple

## Character Anchors

Each recurring character needs a stable anchor:

- name and pronunciation if needed
- role in the story and function in the source metaphor
- what they want
- visual category: human, animal, machine, object, place, hybrid, or other
- age or scale, if relevant
- body shape and silhouette
- face, hair/fur/skin/material, colors, and distinctive marks
- clothing or casing
- recurring prop
- gesture, posture, or expression habit
- speech pattern or recurring phrase
- relationship to other characters
- arc across the book
- do-not-change details
- reusable prompt snippet
- approved reference image path, if available

Keep snippets short enough to paste into every relevant image prompt. Example shape:

```text
Amina Kadal: twelve-year-old harbor tinkerer, compact silhouette, warm brown skin, black braid tied with blue cord, saffron work tunic over rolled trousers, brass measuring bracelet, always carries a shell-handled screwdriver; alert, practical, impatient with vague answers.
```

## World Anchors

The world needs stable logic, not just atmosphere.

Track:

- what kind of place it is
- map structure: districts, routes, thresholds, important rooms, coastlines, tunnels, streets, towers, labs, markets, or other places
- what powers the world
- what machines, creatures, institutions, rituals, or natural forces can and cannot do
- what happens when a rule is broken
- what the reader should understand visually before the story starts
- material palette: woods, metals, fabrics, stone, paper, water, smoke, light, plants, weather
- recurring labels, signs, map marks, or callouts and whether they should be native image text, manual overlay text, or mixed
- background population rules
- cultural/language handling
- do-not-change details
- reusable prompt snippet

World rules should be specific enough to prevent contradictions. Bad: "The harbor has machines." Better: "Machines must receive stamped brass plates before touching public docks; unapproved machines can hum, calculate, and complain, but cannot move cranes, gates, bridges, or boats."

## Opening Anchor Spreads

The character-introduction spread and world-introduction spread serve two purposes:

- Reader purpose: invite the reader into the cast and world.
- Production purpose: establish approved visual continuity for later image prompts.

Character spread:

- show large, clean recurring characters with readable silhouettes
- include key props and scale cues
- use a locked label sheet for names and short descriptions
- native image text is allowed for integrated labels and role notes if the page is proofread carefully
- avoid tiny crowded faces
- avoid finalizing too many background extras
- use this spread as the approved reference for appearance when possible

World spread:

- show the map, object atlas, machine diagram, route chart, civic board, cutaway, or other world-native explanation
- identify where the main story can happen
- show the rules through visible systems, not long explanation
- use a locked label sheet for exact labels, short rules, route names, object names, and map marks
- native image text is allowed for integrated map labels and callouts if the page is proofread carefully
- include recurring objects/machines in their canonical form
- use this spread as the approved reference for geography and world logic when possible

## Anchor Label Sheet

Before generating the character-introduction or world-introduction spread, write a short label sheet.

For each label:

- id
- exact text
- target object or character
- reader purpose: what the label helps the reader understand
- brief explanation, if the name is not self-explanatory
- importance: critical, useful, or decorative
- rendering mode: native, manual, or either
- maximum length
- fallback if the image model misspells it

Use native image text mainly for short, visually integrated pieces:

- character names
- one-line role notes
- object labels
- map marks
- badges, signs, route names, and tiny rules
- short diagram callouts

Use reader-helpful label text. For characters, include a compact role, want, job, or story function, not only the name. For fictional machines, places, creatures, tools, or rituals, include a short function note unless the picture and name make it obvious. Good shape: "No-Bell / means not yet, not failure" or "Ledger Crabs / file shell receipts after machines act."

Avoid native text for long explanations, dense back matter, precise source definitions, cover title/credit, and story body copy.

After generation, audit each label. Critical labels must be correct before the image becomes a continuity anchor. If a beautiful image has a wrong critical label, regenerate, manually correct, or remove that label from the image and overlay it later.

For PDF assembly:

- `text_rendering_mode: native` means the approved image already contains the accepted labels; remove duplicate overlay text blocks.
- `text_rendering_mode: mixed` means the image contains some native labels and the manifest overlays corrections or extra labels.
- `text_rendering_mode: manual` means the image leaves room for all readable text to be typeset afterward.

## Prompt Reuse

Before generating each image:

1. Identify which recurring characters, objects, places, and rules appear.
2. Pull only the relevant anchor snippets into the prompt.
3. Mention any approved reference image if the environment supports image references.
4. State what must remain consistent and what can vary for the scene.
5. Keep background beings simple unless they are part of the cast bible.

Do not paste the whole continuity bible into every prompt. Use concise anchor snippets for the elements on that spread.

## Continuity Review

Before approving a generated image, check:

- Does each recurring character match the anchor?
- Did clothing, colors, props, species, age, or scale drift?
- Did a machine or object change function?
- Did the map/geography contradict the world spread?
- Did the image introduce unplanned labels, cultures, scripts, symbols, or background characters?
- Did it make a source metaphor too literal?
- Did it add details that would force later story changes?

If an image contains a happy accident, decide explicitly:

- adopt it into the continuity bible, or
- treat it as non-canonical and avoid repeating it.

If a user changes a continuity anchor, update the bible first. Then revise all affected prompts, story beats, image prompts, and final text.
