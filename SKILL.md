---
name: wby-html-ppt
description: Create and refine HTML presentations from speaking goals, combining scene-specific illustrations, real screenshots, and code-drawn diagrams with consistent controls, optional animation, and standalone HTML delivery. Use for slide creation, revision, and packaging.
---

# WBY HTML PPT

[中文](SKILL.zh-CN.md) | English

Teach a method, not the layout of one example. Controls, verification, and delivery are consistent; style, composition, assets, and motion follow the content. Explicit user preferences take priority.

## Working approach

Distinguish requests for a proposal from requests to execute. For proposals, show copy and visual intent. For “make, edit, or add,” work in the existing project. Do not repeatedly ask for information or authorization already supplied. Clarify only consequential missing information while progressing independent work.

1. Read the source project, slide order, materials, and approved visual direction. Continue from maintainable source rather than rebuilding from a packed artifact.
2. Identify the audience, speaking goal, narrative role, and transition. Distinguish verified facts, user judgments, teaching examples, and unknowns.
3. Use [visual-method.en.md](references/visual-method.en.md) to choose expression. Internally identify the subject, relationship, evidence, composition, and implementation for each slide.
4. Build and preview slides within scope. Preserve approved pages; update related pages only where consistency requires it. Do not turn iteration into repeated approval requests.
5. Revise content, order, pacing, and expression based on feedback. Maintain a single ordered manifest when adding, removing, or reordering slides.
6. Follow [interaction-delivery.en.md](references/interaction-delivery.en.md). Deliver maintainable source and standalone HTML. Report actual checks and environmental limitations.

## Internal authoring and writing guidance

Use [slide-authoring.md](references/slide-authoring.md) for source organization, page creation, ordering, review, and the bundled CLI. Use [copywriting.md](references/copywriting.md) when writing audience-facing text.

Use the available image-generation tool for new scene-specific illustrations; persist assets in the project. Use HTML/CSS/SVG for precise text and diagrams. Use permitted browser tools for visual and interaction verification. The environment still supplies image generation, browser access, and Python. Read relevant tool instructions when required by the environment; do not claim missing capabilities or install tools automatically.

Default output is HTML. Use a separate appropriate export workflow if PPTX is requested and explain editability limits.

## Standard presentation capabilities

New deliveries include arrow navigation, fullscreen button/F, overview/O with thumbnail navigation, Esc to dismiss overlays, screenshot enlargement, actual external links, page numbers and boundaries, and standalone HTML packaging. Do not intercept typing in editable elements. Shortcuts must work when focus enters the slide iframe. Never invent links to fill UI slots.

Support motion without requiring animation on every slide. Use light page/overlay transitions and selective content animation to explain sequence, change, or emphasis. No automatic advance or distracting loops unless requested. Respect `prefers-reduced-motion`.

## Reusable implementation

`assets/player.html` is a controls shell, not a slide design template. Use independent HTML pages with isolated styles. Adapt dimensions and appearance to the project; default aspect ratio is 16:9.

Maintain a UTF-8 manifest:

```json
{"title":"Presentation title","slides":["slides/intro.html","slides/example.html"]}
```

Paths are relative to the project. Include only slides intended for delivery. An existing compatible deck.json can be used after checking scope.

```sh
python3 <skill-directory>/scripts/build.py <project-directory> --manifest <manifest-path> --output <output-html-path>
```

The builder embeds and deduplicates supported local resources, preserving external hyperlinks. See the delivery reference for supported inputs and limitations. Customize controls styling without removing the standard capabilities.

## Completion criteria

- The example did not become a mandatory character, palette, card count, or layout.
- Illustrations support narration; real evidence stays faithful; mockups are labeled.
- Adjacent slides connect clearly; projected text and images are readable without clipping or overflow.
- Test the final standalone artifact. External documents still require network and permissions; packaging does not bypass them.
