#!/usr/bin/env python3
"""Simpler screenshot — viewport-only at fixed dimensions, scrolled to a section."""
import sys, os, json, subprocess, time, base64, socket, http.client, websocket

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temporary screenshots')
os.makedirs(OUT_DIR, exist_ok=True)

def free_port() -> int:
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def capture(url: str, label: str, scroll_y: int = 0) -> str:
    port = free_port()
    proc = subprocess.Popen([
        CHROME, f'--remote-debugging-port={port}',
        '--headless=new', '--disable-gpu',
        '--no-first-run', '--no-default-browser-check',
        '--remote-allow-origins=*', '--hide-scrollbars',
        '--window-size=1440,900', 'about:blank',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(40):
        try:
            c = http.client.HTTPConnection('127.0.0.1', port, timeout=1)
            c.request('GET', '/json/list')
            ws_url = json.loads(c.getresponse().read())[0]['webSocketDebuggerUrl']
            c.close()
            break
        except Exception:
            time.sleep(0.25)
    if not ws_url:
        proc.kill()
        raise RuntimeError('Chrome failed to start')
    ws = websocket.create_connection(ws_url, timeout=15)

    def cmd(method, params=None, mid=1):
        ws.send(json.dumps({'id': mid, 'method': method, 'params': params or {}}))
        ws.settimeout(15)
        while True:
            msg = json.loads(ws.recv())
            if msg.get('id') == mid:
                return msg.get('result', {})

    cmd('Page.enable', mid=1)
    cmd('Page.navigate', {'url': url}, mid=2)
    time.sleep(3.5)  # let fonts + images settle
    if scroll_y:
        cmd('Runtime.evaluate', {'expression': f'window.scrollTo(0, {scroll_y})'}, mid=3)
        time.sleep(0.6)
    res = cmd('Page.captureScreenshot', {'format': 'png'}, mid=4)
    ws.close()
    proc.kill()

    out = os.path.join(OUT_DIR, f'_shot-{label}.png')
    with open(out, 'wb') as f:
        f.write(base64.b64decode(res['data']))
    return out

if __name__ == '__main__':
    url = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else 'page'
    scroll = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    print(capture(url, label, scroll))
