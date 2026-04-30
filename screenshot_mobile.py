#!/usr/bin/env python3
"""Mobile screenshot tool — iPhone 14 Pro viewport (393x852, DPR=3)."""
import sys, os, json, subprocess, time, base64, glob, socket, http.client, websocket

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temporary screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

VIEWPORT_W = 393
VIEWPORT_H = 852
DPR = 3
USER_AGENT = ('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
              'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')


def next_num():
    nums = []
    for f in glob.glob(os.path.join(SCREENSHOTS_DIR, 'screenshot-*.png')):
        base = os.path.basename(f).replace('screenshot-', '').replace('.png', '')
        try:
            nums.append(int(base.split('-')[0]))
        except Exception:
            pass
    return max(nums, default=0) + 1


def free_port():
    with socket.socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def send(ws, mid, method, params=None):
    cmd = {'id': mid, 'method': method}
    if params is not None:
        cmd['params'] = params
    ws.send(json.dumps(cmd))


def recv_until(ws, target_id=None, event=None, timeout=15):
    ws.settimeout(timeout)
    try:
        while True:
            msg = json.loads(ws.recv())
            if target_id is not None and msg.get('id') == target_id:
                return msg.get('result', {})
            if event and msg.get('method') == event:
                return msg
    except websocket.WebSocketTimeoutException:
        return {}


def main(url, label='mobile'):
    port = free_port()
    proc = subprocess.Popen([
        CHROME,
        f'--remote-debugging-port={port}',
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--remote-allow-origins=*',
        '--hide-scrollbars',
        f'--window-size={VIEWPORT_W},{VIEWPORT_H}',
        'about:blank',
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    ws_url = None
    for _ in range(40):
        try:
            conn = http.client.HTTPConnection('127.0.0.1', port, timeout=1)
            conn.request('GET', '/json/list')
            tabs = json.loads(conn.getresponse().read())
            conn.close()
            ws_url = tabs[0]['webSocketDebuggerUrl']
            break
        except Exception:
            time.sleep(0.2)

    if not ws_url:
        proc.kill()
        print('Error: Chrome failed to start')
        sys.exit(1)

    ws = websocket.create_connection(ws_url, timeout=15)

    # Mobile emulation
    send(ws, 1, 'Emulation.setDeviceMetricsOverride', {
        'width': VIEWPORT_W, 'height': VIEWPORT_H,
        'deviceScaleFactor': DPR, 'mobile': True,
    })
    recv_until(ws, target_id=1)
    send(ws, 2, 'Emulation.setUserAgentOverride', {'userAgent': USER_AGENT})
    recv_until(ws, target_id=2)
    send(ws, 3, 'Emulation.setTouchEmulationEnabled', {'enabled': True, 'maxTouchPoints': 5})
    recv_until(ws, target_id=3)

    send(ws, 4, 'Page.enable')
    recv_until(ws, target_id=4)

    send(ws, 5, 'Page.navigate', {'url': url})
    recv_until(ws, target_id=5)
    recv_until(ws, event='Page.loadEventFired', timeout=12)

    time.sleep(2.5)  # fonts + lazy renders

    # Capture full page (beyond the visible viewport)
    send(ws, 6, 'Page.captureScreenshot', {
        'format': 'png',
        'captureBeyondViewport': True,
    })
    result = recv_until(ws, target_id=6, timeout=25)

    ws.close()
    proc.kill()

    if not result or 'data' not in result:
        print('Error: screenshot capture failed')
        sys.exit(1)

    n = next_num()
    suffix = f'-{label}' if label else ''
    path = os.path.join(SCREENSHOTS_DIR, f'screenshot-{n}{suffix}.png')
    with open(path, 'wb') as f:
        f.write(base64.b64decode(result['data']))
    print(f'Screenshot saved: {path}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 screenshot_mobile.py <url> [label]')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'mobile')
