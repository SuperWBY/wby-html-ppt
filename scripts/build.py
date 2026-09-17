#!/usr/bin/env python3
"""Build a self-contained presentation from a project-local slide manifest."""
import argparse, base64, html, json, mimetypes, re
from pathlib import Path


def build(project, manifest, output):
    project = project.resolve()
    def resolve(ref, base):
        p = (base / ref).resolve()
        if not p.is_relative_to(project):
            raise ValueError(f'Resource escapes project: {ref}')
        if not p.is_file():
            raise ValueError(f'Missing resource: {p}')
        return p
    def external(ref):
        return bool(re.match(r'^(?:[a-z][a-z0-9+.-]*:|//|#)', ref, re.I))
    assets = {}
    def asset(ref, base):
        if ref.startswith('data:'):
            return ref
        if external(ref):
            raise ValueError(f'External embedded resource: {ref}')
        p = resolve(ref, base)
        if p.suffix.lower() in ('.html', '.htm'):
            raise ValueError(f'Use player navigation instead of local HTML links: {ref}')
        if p not in assets:
            assets[p] = f'__PRESENTATION_ASSET_{len(assets)}__'
        return assets[p]
    def css_inline(css, base):
        if re.search(r'@import\b', css):
            raise ValueError('CSS @import must be flattened before packing')
        def sub(m):
            ref = m.group(2).strip()
            if ref.startswith('#'):
                return m.group(0)
            return 'url("' + asset(ref, base) + '")'
        return re.sub(r'url\(\s*([\"\']?)([^\)\"\']+)\1\s*\)', sub, css)
    data = json.loads(manifest.read_text())
    paths = data.get('slides', [])
    if not paths or not all(isinstance(p, str) for p in paths):
        raise ValueError('slides must be a non-empty array of paths')
    docs = []
    for ref in paths:
        p = resolve(ref, project)
        s = p.read_text()
        if re.search(r'\bsrcset\s*=|type=["\']module["\']|\bfetch\s*\(|\bimport\s*\(', s):
            raise ValueError(f'Unsupported dynamic resource/module/srcset in {ref}')
        # Inline original styles before adding scripts, so JS strings are not parsed as CSS.
        s = re.sub(r'<style\b[^>]*>(.*?)</style>', lambda m:'<style>'+css_inline(m.group(1),p.parent)+'</style>', s, flags=re.S|re.I)
        def link(m):
            tag=m.group(0)
            href=re.search(r'href=["\']([^"\']+)["\']',tag)
            if not href: return tag
            if not re.search(r'rel=["\']stylesheet["\']',tag,re.I):
                raise ValueError(f'Unsupported link resource: {tag}')
            path=resolve(href.group(1),p.parent)
            return '<style>'+css_inline(path.read_text(),path.parent)+'</style>'
        s=re.sub(r'<link\b[^>]*>',link,s,flags=re.I)
        def attrs(m):
            tag=m.group(0)
            name=re.match(r'<([\w-]+)',tag).group(1).lower()
            if name=='script': return tag
            def attr(a):
                key,ref=a.group(1),html.unescape(a.group(3))
                if key.lower()=='href' and name=='a' and external(ref): return a.group(0)
                return key+'="'+asset(ref,p.parent)+'"'
            return re.sub(r'\b(src|href|poster)=("|\')([^"\']+)\2',attr,tag,flags=re.I)
        s=re.sub(r'<[a-zA-Z][^>]*>',attrs,s)
        def script(m):
            path=resolve(m.group(1),p.parent)
            code=path.read_text()
            if re.search(r'\bfetch\s*\(|\bimport\s*(?:\(|["\'{*])',code):
                raise ValueError(f'Dynamic fetch/import in {path}')
            return '<script>'+code+'</script>'
        s=re.sub(r'<script\b[^>]*src=["\']([^"\']+)["\'][^>]*>\s*</script>',script,s,flags=re.S|re.I)
        s=s.replace('</head>','<style>@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}</style></head>')
        docs.append(s)
    packed={token:{'mime':mimetypes.guess_type(str(p))[0] or 'application/octet-stream','base64':base64.b64encode(p.read_bytes()).decode()} for p,token in assets.items()}
    def js(value): return json.dumps(value,ensure_ascii=False).replace('<','\\u003c')
    payload='const embeddedAssets = '+js(packed)+''';
const assetUrls = Object.fromEntries(Object.entries(embeddedAssets).map(([key, value]) => [key, URL.createObjectURL(new Blob([Uint8Array.from(atob(value.base64), c => c.charCodeAt(0))], {type:value.mime}))]));
const slideDocuments = '''+js(docs)+''';
slideDocuments.forEach((doc, i) => { slideDocuments[i] = doc.replace(/__PRESENTATION_ASSET_\\d+__/g, key => assetUrls[key]); });'''
    template=Path(__file__).resolve().parent.parent/'assets/player.html'
    result=template.read_text().replace('__TITLE__',html.escape(data.get('title','演示文稿'))).replace('/* EMBEDDED_DECK */',payload)
    if output.resolve() in [resolve(ref,project) for ref in paths] or output.resolve()==manifest.resolve():
        raise ValueError('Output cannot overwrite input')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(result)
    return {'file':str(output),'pages':len(docs),'assets':len(assets),'bytes':output.stat().st_size}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('project',type=Path);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try: print(json.dumps(build(a.project,a.manifest,a.output),ensure_ascii=False))
    except (ValueError,OSError,KeyError) as e: p.exit(1,f'Build failed: {e}\n')
