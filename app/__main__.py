"""Local desktop launcher. Reopening authenticates to the existing local process."""
import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import sys
import tempfile
import threading
import time
import webbrowser
from multiprocessing.connection import Client, Listener
from multiprocessing import AuthenticationError

import uvicorn

from .web import create_app


def default_directory():
    if sys.platform == 'win32':
        return Path(os.environ['LOCALAPPDATA']) / 'RFP Empire'
    if sys.platform == 'darwin':
        return Path.home() / 'Library/Application Support/RFP Empire'
    return Path.home() / '.local/share/rfp-empire'


def acquire_lock(path):
    handle = path.open('a+b')
    handle.seek(0)
    if sys.platform == 'win32':
        import msvcrt
        if path.stat().st_size == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            handle.close()
            return None
    else:
        import fcntl
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            handle.close()
            return None
    return handle


def request_launch(directory):
    """Mutual IPC authentication precedes any URL exchange; never trust a stale port."""
    info = json.loads((Path(directory) / 'runtime.json').read_text())
    with Client(info['address'], family=info['family'], authkey=bytes.fromhex(info['key'])) as conn:
        conn.send_bytes(b'open')
        if not conn.poll(5):
            raise RuntimeError('The running app did not respond. Stop it before restarting.')
        result = json.loads(conn.recv_bytes(4096))
    if result.get('directory') != str(Path(directory).resolve()):
        raise RuntimeError('The running app uses a different data directory.')
    return result['url']


def main():
    parser = argparse.ArgumentParser(description='RFP Empire local browser application')
    parser.add_argument('--demo', action='store_true', help='Use a separate synthetic demonstration database')
    parser.add_argument('--data-dir', type=Path, help='Private application data directory')
    parser.add_argument('--port', type=int, default=0, help='Loopback port; default selects an available port')
    parser.add_argument('--no-browser', action='store_true', help='Start without opening the browser (development/testing)')
    args = parser.parse_args()
    if args.port and not 1024 <= args.port <= 65535:
        parser.error('--port must be 0 or between 1024 and 65535')
    os.umask(0o077)
    directory = (args.data_dir or default_directory()).expanduser().resolve()
    if args.demo:
        directory = directory / 'demo'
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    handle = acquire_lock(directory / 'instance.lock')
    if handle is None:
        for attempt in range(20):
            try:
                url = request_launch(directory)
                if not args.no_browser:
                    webbrowser.open(url)
                print('RFP Empire is already running. Opened a new local session.' if not args.no_browser else 'RFP Empire is already running.')
                return
            except (OSError, ValueError, EOFError, AuthenticationError):
                time.sleep(0.25)
        raise SystemExit('The existing app is not responding. Stop its process before restarting; your saved data remains on disk.')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ipc_directory = None
    listener = None
    runtime = directory / 'runtime.json'
    try:
        sock.bind(('127.0.0.1', args.port))
        origin = f'http://127.0.0.1:{sock.getsockname()[1]}'
        app = create_app(directory, origin, demo=args.demo)
        server = uvicorn.Server(uvicorn.Config(app, log_level='warning', access_log=False))
        app.state.stop = lambda: setattr(server, 'should_exit', True)
        key = secrets.token_bytes(32)
        if sys.platform == 'win32':
            family, address = 'AF_PIPE', r'\\.\pipe\rfp-empire-' + secrets.token_hex(16)
        else:
            ipc_directory = tempfile.mkdtemp(prefix='rfp-')
            family, address = 'AF_UNIX', str(Path(ipc_directory) / 'launcher.sock')
        listener = Listener(address, family=family, authkey=key)

        def serve_launcher():
            while not server.should_exit:
                try:
                    with listener.accept() as conn:
                        if not conn.poll(2) or conn.recv_bytes(32) != b'open':
                            continue
                        url = origin + '/?launch=1#token=' + app.state.new_bootstrap()
                        conn.send_bytes(json.dumps(dict(url=url, directory=str(directory))).encode())
                except (OSError, EOFError, ValueError, AuthenticationError):
                    continue

        def ready():
            while not server.started and not server.should_exit:
                time.sleep(0.05)
            if not server.started:
                return
            runtime.write_text(json.dumps(dict(address=address, family=family, key=key.hex())))
            threading.Thread(target=serve_launcher, daemon=True).start()
            print(f'RFP Empire is running at {origin}. Data: {directory}', flush=True)
            if not args.no_browser:
                webbrowser.open(origin + '/?launch=1#token=' + app.state.new_bootstrap())

        threading.Thread(target=ready, daemon=True).start()
        try:
            server.run(sockets=[sock])
        except KeyboardInterrupt:
            pass
    finally:
        runtime.unlink(missing_ok=True)
        if listener:
            listener.close()
        if ipc_directory:
            shutil.rmtree(ipc_directory, ignore_errors=True)
        sock.close()
        handle.close()


if __name__ == '__main__':
    main()
