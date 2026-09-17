#!/usr/bin/env python3
"""Manage static HTML slides without external Skills (Python 3.9+)."""
import argparse
import functools
import html
import http.server
import json
import re
import tempfile
from pathlib import Path
from build import build


def read_deck(project):
    manifest = project / 'deck.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    slides = data.get('slides')
    if not isinstance(slides, list) or not all(isinstance(x, str) for x in slides):
        raise ValueError('deck.json slides must be an array of relative paths')
    if len(slides) != len(set(slides)):
        raise ValueError('Duplicate slide paths in deck.json')
    for ref in slides:
        path = (project / ref).resolve()
        if Path(ref).is_absolute() or not path.is_relative_to(project):
            raise ValueError(f'Slide path escapes project: {ref}')
    return manifest, data


def save(manifest, data):
    # Preserve the previous manifest so ordering changes are recoverable.
    if manifest.exists():
        manifest.with_suffix('.json.bak').write_bytes(manifest.read_bytes())
    staged = manifest.with_suffix('.json.tmp')
    staged.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    staged.replace(manifest)


def slide_ref(slides, key):
    matches = [s for s in slides if s == key or Path(s).stem == key]
    if len(matches) != 1:
        raise ValueError(f'Expected one slide matching {key!r}; found {len(matches)}')
    return matches[0]


def run(a):
    project = a.project.resolve()
    if a.action == 'init':
        project.mkdir(parents=True, exist_ok=True)
        if (project / 'deck.json').exists():
            raise ValueError('deck.json already exists; use status to inspect it')
        for name in ('slides', 'assets'):
            (project / name).mkdir(exist_ok=True)
        save(project / 'deck.json', {'title': a.title, 'slides': []})
        return {'project': str(project), 'pages': 0}
    manifest, data = read_deck(project)
    slides = data['slides']
    if a.action == 'add':
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', a.id):
            raise ValueError('Use lowercase letters, digits and hyphens for the slide ID')
        ref = f'slides/{a.id}.html'
        target = (project / ref).resolve()
        if not target.is_relative_to(project):
            raise ValueError('Slide directory escapes project')
        if target.exists() or ref in slides:
            raise ValueError('Slide already exists; edit its source instead')
        index = slides.index(slide_ref(slides, a.after)) + 1 if a.after else len(slides)
        title = html.escape(a.title)
        target.parent.mkdir(parents=True, exist_ok=True)
        # Only a canvas scaffold: no illustrative example facts or prescribed layout.
        target.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<style>*{{box-sizing:border-box}}body{{margin:0;width:1920px;height:1080px;overflow:hidden;font-family:Arial,sans-serif}}main{{padding:80px}}h1{{font-size:64px}}</style>
</head><body><main data-wby-draft><h1>{title}</h1>
<!-- Author this slide for its speaking goal, then remove data-wby-draft. -->
</main></body></html>''', encoding='utf-8')
        slides.insert(index, ref)
        save(manifest, data)
        return {'path': str(target), 'position': index + 1, 'draft': True}
    if a.action in ('move', 'remove'):
        ref = slide_ref(slides, a.id)
        if a.action == 'move':
            if not 1 <= a.to <= len(slides):
                raise ValueError('Position must be between 1 and the slide count')
            slides.remove(ref)
            slides.insert(a.to - 1, ref)
        else:
            slides.remove(ref)  # Intentionally keep source and assets on disk.
        save(manifest, data)
        return {'slides': slides, 'source_files_preserved': True}
    if a.action == 'status':
        records = []
        for i, ref in enumerate(slides, 1):
            p = project / ref
            text = p.read_text(encoding='utf-8') if p.is_file() else ''
            title = re.search(r'<title[^>]*>(.*?)</title>', text, re.I | re.S)
            records.append({'page': i, 'path': ref, 'exists': p.is_file(),
                            'draft': 'data-wby-draft' in text,
                            'title': html.unescape(title.group(1)) if title else ''})
        return {'title': data.get('title', ''), 'pages': records,
                'visual_review': 'Not determined by static status; inspect in a browser.'}
    for ref in slides:
        p = project / ref
        if p.exists() and 'data-wby-draft' in p.read_text(encoding='utf-8'):
            raise ValueError(f'Unfinished scaffold: {ref}')
    if a.action == 'check':
        with tempfile.TemporaryDirectory() as temp:
            result = build(project, manifest, Path(temp) / 'check.html')
        return {'pages': result['pages'], 'assets': result['assets'], 'static_packaging': 'passed',
                'browser_review': 'Required: overflow, readability, interactions, reduced motion.'}
    output = a.output.resolve() if a.output else project / 'dist/presentation.html'
    result = build(project, manifest, output)
    if a.action == 'build':
        return result
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(output.parent))
    with http.server.ThreadingHTTPServer(('127.0.0.1', a.port), handler) as server:
        from urllib.parse import quote
        print(json.dumps({'preview': f'http://127.0.0.1:{server.server_port}/{quote(output.name)}',
                          'note': 'Local preview only; Ctrl+C to stop. Rebuild after editing.'}), flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    return {'preview': 'stopped'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    for name in ('init', 'add', 'move', 'remove', 'status', 'check', 'build', 'preview'):
        p = sub.add_parser(name)
        p.add_argument('project', type=Path)
        if name == 'init':
            p.add_argument('--title', default='Untitled presentation')
        if name == 'add':
            p.add_argument('id'); p.add_argument('--title', required=True); p.add_argument('--after')
        if name in ('move', 'remove'):
            p.add_argument('id')
        if name == 'move':
            p.add_argument('--to', type=int, required=True)
        if name in ('build', 'preview'):
            p.add_argument('--output', type=Path)
        if name == 'preview':
            p.add_argument('--port', type=int, default=4173)
    try:
        print(json.dumps(run(parser.parse_args()), ensure_ascii=False))
    except (ValueError, OSError, KeyError) as e:
        parser.exit(1, f'Failed: {e}\n')


if __name__ == '__main__':
    main()
