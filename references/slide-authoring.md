# Slide authoring

English | [中文](slide-authoring.zh-CN.md)

## Source and narrative

Use `deck.json` as the single ordered list, `slides/*.html` as editable page sources, and project-local assets. An outline describes intentions, not proof that a page is finished. Generated previews are disposable outputs; edit source pages.

For each slide identify its subject, what the audience should understand, and the evidence or visual that supports that understanding. Keep missing facts explicit. For product demonstrations show where an action happens and where its result appears. Show implementation names only when teaching implementation.

Keep one main point per page. Split overloaded pages at a meaningful topic or process boundary; retain necessary causes, consequences, conditions, and actions. Merge neighboring pages when they repeat the same idea. Keep approved content stable during scoped revisions. Do not require a new approval after every slide when the user has authorized the deck.

## Composition and implementation

Select composition from the relationship: focus, comparison, sequence, convergence, evidence, or change. These are options, not a quota. Avoid repeatedly using equal-weight cards when the content has hierarchy.

Use a consistent project baseline for type, colors, spacing, and illustration medium. Exact sizes follow the viewing context. Check the page at the intended projection scale; shrinking all text is not a fix for too much content. Let screenshots or diagrams carry information instead of repeating it in the title, caption, and paragraph.

Keep page styles isolated. For the supplied player, use 1920×1080 source canvases or deliberately adapt the player's sizing with the source. Preserve image proportions and meaningful screenshot context. Use code for exact labels and relationships, image generation for scenes. Distinguish evidence from teaching mockups.

## Built-in commands

Resolve `scripts/studio.py` relative to this Skill. Python 3.9+ is sufficient.

```sh
python3 scripts/studio.py init /path/to/deck --title "My talk"
python3 scripts/studio.py add /path/to/deck opening --title "Opening"
python3 scripts/studio.py add /path/to/deck evidence --title "Evidence" --after opening
python3 scripts/studio.py move /path/to/deck evidence --to 1
python3 scripts/studio.py remove /path/to/deck evidence
python3 scripts/studio.py status /path/to/deck
python3 scripts/studio.py check /path/to/deck
python3 scripts/studio.py build /path/to/deck --output /path/to/deck/dist/talk.html
python3 scripts/studio.py preview /path/to/deck --port 4173
```

`add` creates an unfinished canvas, not a designed slide. Author it and remove `data-wby-draft` when it is ready to inspect. Check/build/preview reject marked drafts. IDs use lowercase letters, digits, and hyphens. `--to` is one-based. `remove` only removes the manifest entry; it preserves source files and assets. The previous manifest is stored as `deck.json.bak`. To restore a removed page, reinsert its path into the manifest rather than overwriting its source.

`status` reports files, titles, and draft markers. `check` runs the static packaging checks in a temporary directory; it does not prove visual quality. `preview` builds the artifact and serves its output directory on loopback until Ctrl+C. Use a dedicated output directory. There is no automatic reload; rebuild after changes. A port conflict is reported as an error; choose another port.

## Review

Read [copywriting.md](copywriting.md) for audience text and [visual-method.en.md](visual-method.en.md) for visuals. Inspect actual pages in a browser for clipping, scrolling, overlap, contrast, projection readability, broken assets, and unexpected repetition across adjacent slides. Check the final packed artifact using [interaction-delivery.en.md](interaction-delivery.en.md). Static validation is not browser validation.
