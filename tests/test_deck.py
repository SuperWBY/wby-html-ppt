"""Exercise real CLI state changes, packaging, and local preview."""
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / 'scripts/deck.py'
with tempfile.TemporaryDirectory() as folder:
    project = Path(folder) / 'deck'
    def call(action, *args, ok=True):
        result = subprocess.run([sys.executable, str(CLI), action, str(project), *args], capture_output=True, text=True)
        assert (result.returncode == 0) == ok, result.stderr
        return json.loads(result.stdout) if ok else result.stderr
    call('init', '--title', 'Test')
    call('init', ok=False)
    call('add', 'one', '--title', 'One')
    call('add', 'two', '--title', 'Two', '--after', 'one')
    assert call('status')['pages'][0]['draft']
    call('check', ok=False)
    call('add', '../escape', '--title', 'Invalid', ok=False)
    call('move', 'two', '--to', '1')
    assert call('status')['pages'][0]['path'] == 'slides/two.html'
    call('move', 'two', '--to', '0', ok=False)
    call('remove', 'one')
    assert (project / 'slides/one.html').exists()
    assert len(json.loads((project / 'deck.json.bak').read_text())['slides']) == 2
    p = project / 'slides/two.html'
    p.write_text(p.read_text().replace('data-wby-draft', 'data-authored'))
    assert call('check')['static_packaging'] == 'passed'
    output = Path(call('build')['file'])
    assert output.exists()
    proc = subprocess.Popen([sys.executable, str(CLI), 'preview', str(project), '--port', '0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        info = json.loads(proc.stdout.readline())
        with urllib.request.urlopen(info['preview'], timeout=5) as response:
            assert response.status == 200
            assert b'slideDocuments' in response.read()
    finally:
        proc.terminate(); proc.wait(timeout=5)
    print('PASS: init, draft gate, safe add, ordering, source-preserving removal, backup, status, check, build, HTTP preview')
