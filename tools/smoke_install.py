"""Exercise first-run setup from a clean source copy, using no preinstalled Python.

The test harness itself uses Python; the native launcher it starts downloads its
own uv, managed Python and runtime dependencies into isolated temporary folders.
"""
import http.cookiejar
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from multiprocessing.connection import Client


def main():
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='rfp-install-') as scratch:
        scratch = Path(scratch)
        folder = scratch/'Download with spaces'
        folder.mkdir()
        shutil.copytree(source/'app', folder/'app', ignore=shutil.ignore_patterns('__pycache__'))
        for name in ['pyproject.toml', 'uv.lock', '.python-version', 'Launch RFP Empire.command', 'Launch RFP Empire.cmd', 'Try Demo.command', 'Try Demo.cmd']:
            shutil.copy2(source/name, folder/name)
        directory = scratch/'data'/'demo'
        env = os.environ | {'UV_MANAGED_PYTHON':'1', 'UV_PYTHON_INSTALL_DIR':str(scratch/'python'), 'UV_CACHE_DIR':str(scratch/'cache'), 'CI':'1'}
        # No developer virtualenv or system uv may satisfy this first-run check.
        env.pop('VIRTUAL_ENV', None)
        env.pop('UV_PROJECT_ENVIRONMENT', None)
        command = [str(folder/'Try Demo.command')]
        if sys.platform == 'win32':
            command = ['cmd.exe', '/c', str(folder/'Try Demo.cmd')]
        command += ['--no-browser', '--data-dir', str(scratch/'data')]
        with (scratch/'install.log').open('w+') as log:
            process = subprocess.Popen(command, cwd=folder, env=env, stdout=log, stderr=subprocess.STDOUT)
            stopped = False
            try:
                deadline = time.monotonic()+240
                while not (directory/'runtime.json').exists():
                    if process.poll() is not None or time.monotonic()>deadline:
                        log.seek(0)
                        raise AssertionError('Clean installation did not start:\n'+log.read())
                    time.sleep(0.25)
                info = json.loads((directory/'runtime.json').read_text())
                with Client(info['address'], family=info['family'], authkey=bytes.fromhex(info['key'])) as conn:
                    conn.send_bytes(b'open')
                    assert conn.poll(5), 'Launcher IPC did not answer'
                    url = json.loads(conn.recv_bytes(4096))['url']
                parsed = urllib.parse.urlsplit(url)
                origin = parsed.scheme+'://'+parsed.netloc
                token = urllib.parse.parse_qs(parsed.fragment)['token'][0]
                client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
                req = urllib.request.Request(origin+'/api/bootstrap', data=json.dumps({'token':token}).encode(), headers={'Origin':origin, 'Content-Type':'application/json'})
                with client.open(req, timeout=10) as response:
                    assert response.status == 200
                with client.open(origin+'/search', timeout=10) as response:
                    html = response.read().decode()
                assert '4 local results' in html and 'DEMO WORKSPACE' in html
                for asset in ['/static/app.css', '/static/app.js']:
                    with client.open(origin+asset, timeout=10) as response:
                        assert response.status == 200 and len(response.read())>100
                # Reopening must reuse the same process without reinstalling anything.
                reopened = subprocess.run(command, cwd=folder, env=env, capture_output=True, text=True, timeout=30)
                assert reopened.returncode == 0 and 'already running' in reopened.stdout, reopened.stdout+reopened.stderr
                csrf = re.search(r'name="csrf" value="([^"]+)"', html)[1]
                workspace = re.search(r'name="workspace_id" value="([^"]+)"', html)[1]
                data = urllib.parse.urlencode({'csrf':csrf, 'workspace_id':workspace}).encode()
                with client.open(urllib.request.Request(origin+'/settings/stop', data=data, headers={'Origin':origin}), timeout=10) as response:
                    assert response.status == 200
                assert process.wait(timeout=15) == 0
                stopped = True
                assert not (directory/'runtime.json').exists()
                assert (directory/'rfp.sqlite3').exists()
                assert not (scratch/'data'/'rfp.sqlite3').exists()
                print('PASS: fresh setup downloaded uv/Python, served authenticated demo and assets, reopened the same service, and stopped cleanly.')
            finally:
                if not stopped and process.poll() is None:
                    if sys.platform == 'win32':
                        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
                    else:
                        process.terminate()
                    process.wait(timeout=15)


if __name__ == '__main__':
    main()
