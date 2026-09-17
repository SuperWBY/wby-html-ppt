import importlib.util,tempfile,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('builder',str(Path(__file__).resolve().parents[1]/'scripts/build.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'assets').mkdir();(p/'slides').mkdir();(p/'css').mkdir()
 (p/'assets/a.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
 (p/'css/a.css').write_text('body{background:url(../assets/a.svg)}')
 f=p/'slides/a.html';f.write_text('<html><head><title>A</title><link rel="stylesheet" href="../css/a.css"></head><body><a href="https://example.com">go</a><img src="../assets/a.svg"><img src="../assets/a.svg"></body></html>')
 manifest=p/'deck.json';manifest.write_text(json.dumps({'title':'Test <title>','slides':['slides/a.html']}))
 r=m.build(p,manifest,p/'out.html');assert r['assets']==1
 assert 'https://example.com' in (p/'out.html').read_text()
 for bad in ['<img src="../assets/missing.png">','<img src="../../outside.png">','<img src="https://example.com/a.png">','<script type="module">import x from "x"</script>']:
  f.write_text(bad)
  try:m.build(p,manifest,p/'out.html')
  except ValueError:pass
  else:raise AssertionError(bad)
 print('PASS: asset deduplication, external hyperlink preservation, missing file / escape / remote asset / module rejection')
