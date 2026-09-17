# WBY HTML PPT

[中文](README.zh-CN.md) | **English**

An AI Skill for building HTML presentations from speaking goals. It brings together content decisions, concise copy, scene-specific illustrations, real screenshots, code-drawn diagrams, and presentation controls.

**Adapt the visual expression to the content. Keep the presentation controls consistent.** The green palette and watercolor characters in the examples belong to one deck, not a mandatory theme.

## The method

Speaking goal → content relationships → visual direction → composition and assets → implementation → slide-by-slide feedback → delivery.

- Use character illustrations for confusion, discussion, and realization; match expressions and gestures to the scene.
- Use tool illustrations to explain computers, cloud services, code, documents, and applications.
- Use HTML/CSS/SVG for precise diagrams, comparisons, cards, icons, speech bubbles, and timelines.
- Use real screenshots as evidence. Clearly identify teaching mockups.
- Use short copy and a focused visual for chapter transitions.
- Continue the existing deck and preserve approved work when making revisions.

## Consistent controls and motion

| Input | Action |
|---|---|
| ← / → | Previous / next slide |
| Fullscreen button / F | Toggle fullscreen, subject to browser support and permissions |
| Overview button / O | View thumbnails and click to jump |
| Esc | Close overlays; the browser handles exiting fullscreen |
| Click a marked screenshot | Enlarge the image |
| Document / application link | Open the actual external resource |

Includes page numbers, first/last-page boundaries, input-focus protection, and shortcuts inside the slide iframe. Prompt-copy buttons are optional. Lightweight transitions are included; add CSS/SVG content animation when it explains a relationship. Respect reduced-motion preferences and do not auto-advance by default.

## Install and use

Requires an AI tool that supports local Skills. For Codex's default skill directory, use the following. Inspect an existing installation before replacing it.

```sh
git clone https://github.com/SuperWBY/wby-html-ppt.git ~/.codex/skills/wby-html-ppt
```

Start a new session and ask:

```text
Use $wby-html-ppt to make a presentation from my materials.
Choose copy, illustrations, and composition based on each slide's speaking goal.
Keep the deck visually coherent, include the standard presentation controls,
and deliver editable source files plus a shareable standalone HTML file.
```

For revisions: “Use $wby-html-ppt to revise slide 6 of this deck and preserve the other approved slides.”

The Skill includes slide-authoring and copywriting guidance plus its own page-management and packaging tools. No installation or invocation of oil-ppt or oil-tone is required. Image generation, browser access, and Python are supplied by your environment. This repository does not include model services or API keys. See [sources and licenses](third_party/README.md).

## Manage slides

See [the built-in CLI guide](references/slide-authoring.md) for init, add, move, remove, status, check, build, and preview commands. Page removal preserves source files. Static checks do not replace browser review.

## Build a standalone file

The builder requires Python 3.9+ and no third-party Python packages. Create static HTML slides and maintain a single ordered manifest:

```json
{"title":"My presentation","slides":["slides/intro.html","slides/example.html"]}
```

```sh
python3 scripts/build.py /path/to/project   --manifest /path/to/project/deck.json   --output /path/to/project/dist/presentation.html
```

Supports local stylesheets, classic scripts, images, and CSS url() resources in style tags and stylesheets. Assets must stay inside the project; they are deduplicated and embedded. The player defaults to 16:9 and can be adapted. Slide language is determined by source content; the bundled player UI is currently Chinese.

Convert ES modules, dynamic fetch, CSS @import, srcset, and remote embedded resources to static assets first. This is not a general-purpose website archiver. External document links still require network access and permission. Recipients should download the HTML and open it in a modern desktop browser; chat previews may disable scripts. Verify layout and controls before delivery, not just build success.

## Showcase

These author-provided screenshots show a Chinese-language deck and different ways to communicate. They are examples, not fixed layouts. The repository contains only these showcase screenshots, not the full business deck, internal documents, or data.

### Tool checklist and scene illustration
![Tool preparation](docs/images/tool-preparation.png)

### Character illustration, review checklist, and flow
![Requirements alignment](docs/images/requirements-alignment.png)

### Chapter transition and emotional expression
![Chapter transition](docs/images/chapter-transition.png)

### Tool diagrams and side-by-side comparison
![Environment comparison](docs/images/environment-comparison.png)

### Parallel timelines and version changes
![Release timeline](docs/images/release-timeline.png)

## Repository map

- [SKILL.md](SKILL.md): English agent instructions; [中文版](SKILL.zh-CN.md).
- `references/`: visual decisions, interactions, and delivery guidance in both languages.
- `assets/player.html`: reusable controls, independent of slide visual design.
- `scripts/build.py`: standalone HTML builder.
- `docs/images/`: showcase screenshots.

The output is an HTML presentation. It does not directly generate editable PowerPoint `.pptx` files. Use a separate export workflow and check editability when PPTX is required.
