# Interaction and delivery contract

## Standard controls

- Left/right: previous/next slide, with disabled boundary buttons. PageUp/PageDown/Space may also be supported.
- Fullscreen button/F: use the Fullscreen API; explain failure or lack of support instead of pretending success.
- O: toggle overview with thumbnails, numbers, titles, and active-page indication. Click to jump. Keep thumbnail proportions and scrolling on small screens.
- Esc: close the top dialog; the browser handles fullscreen exit. Do not turn slides while an image overlay is open.
- Zoomable screenshots: `<a class="image-link" href="assets/example.png"><img ...></a>`.
- External links: actual `<a href="https://..." target="_blank" rel="noopener">` or `button[data-url]`. Do not download private linked pages for offline packaging.
- Optional copy button: `data-copy-target="#prompt-id"`; provide manual selection guidance on failure.
- Preserve editable-element input and modifier shortcuts. Holding O/F must not repeatedly toggle.
- Shortcuts work inside the main iframe. Thumbnail iframes do not capture pointer or keyboard input.

## Animation

The player provides lightweight page and overview transitions with reduced-motion support. Slides may implement local CSS/SVG animation, but essential text must not depend on it. The builder adds reduced-motion CSS to embedded slides.

No autoplay audio, automatic slide advance, or hidden gestures by default. Step reveals must not commandeer arrow navigation or O/F; provide a clear step button.

## Packaging inputs and scope

When migrating existing slides, convert player-specific hardcoded link mappings into real anchors or data-url buttons. Convert copy actions into data-copy-target. Do not put case-specific links into the generic player.

build.py reads title and slides from JSON. Input pages are trusted, reviewed project code; do not execute arbitrary third-party HTML.

Supports local stylesheets, classic scripts, img/src, local image href, and CSS url() within style tags and stylesheets. Resources stay inside the project, are deduplicated, and embedded. CSS paths resolve relative to the CSS file.

Unsupported: ES modules/import, dynamic fetch, CSS @import, srcset, remote embedded resources, and relative HTML navigation. Convert these to static inputs or use an appropriate build tool. Do not simply disable checks. Remote hyperlinks can remain.

Deliver source plus standalone HTML, optionally an archive. Public publishing is a separate action requiring user authorization. Report page count, size, usage, and tested limitations. Share the file, not a localhost URL. Recipients download and open it in a modern desktop browser; chat previews may disable scripts.

## Meaningful verification

1. Verify manifest order and count; missing assets and paths escaping the project fail.
2. Preview representative and changed slides at different viewport shapes. Check projected readability and complete images.
3. Test arrows, iframe focus, boundaries, O, thumbnail jumps, Esc, zoom, and entering/exiting fullscreen.
4. Confirm required resources are embedded with no original-project runtime dependency; preserve external hyperlinks.
5. Prefer testing the final file offline. If local-file access is blocked, respect the restriction. Test the packed file over HTTP and report offline opening as untested.
6. Check readability with reduced motion. Do not describe static checks as cross-browser verification.
