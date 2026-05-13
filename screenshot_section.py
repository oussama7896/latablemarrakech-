#!/usr/bin/env python3
"""Viewport-only screenshot scrolled to a section id. Avoids the full-page
height blowup that the original screenshot.py hits on tall pages."""
from __future__ import annotations
import sys, os, json, subprocess, time, base64, glob, socket, http.client, websocket
from typing import Optional

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temporary screenshots")
os.makedirs(OUT_DIR, exist_ok=True)


def next_num() -> int:
    nums = []
    for f in glob.glob(os.path.join(OUT_DIR, "screenshot-*.png")):
        try:
            nums.append(int(os.path.basename(f).split("-")[1].split(".")[0]))
        except (IndexError, ValueError):
            pass
    return max(nums, default=0) + 1


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def send(ws, method: str, params: Optional[dict] = None, *, id: int) -> None:
    msg = {"id": id, "method": method}
    if params:
        msg["params"] = params
    ws.send(json.dumps(msg))


def wait(ws, *, target_id: Optional[int] = None, event: Optional[str] = None, timeout: float = 10) -> dict:
    ws.settimeout(timeout)
    try:
        while True:
            msg = json.loads(ws.recv())
            if target_id is not None and msg.get("id") == target_id:
                return msg.get("result", {})
            if event is not None and msg.get("method") == event:
                return msg
    except websocket.WebSocketTimeoutException:
        return {}


def capture(url: str, label: str, section_id: Optional[str]) -> None:
    port = free_port()
    proc = subprocess.Popen(
        [
            CHROME,
            f"--remote-debugging-port={port}",
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--remote-allow-origins=*",
            "--hide-scrollbars",
            "--window-size=1440,900",
            "about:blank",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    ws_url: Optional[str] = None
    for _ in range(50):
        try:
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
            conn.request("GET", "/json/list")
            tabs = json.loads(conn.getresponse().read())
            conn.close()
            ws_url = tabs[0]["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(0.2)
    if not ws_url:
        proc.kill()
        sys.exit("Chrome failed to start")

    ws = websocket.create_connection(ws_url, timeout=10)

    send(ws, "Page.enable", id=1)
    wait(ws, target_id=1)
    send(ws, "Runtime.enable", id=2)
    wait(ws, target_id=2)

    # Force a fixed viewport — no full-page emulation, no scale blowup.
    send(
        ws,
        "Emulation.setDeviceMetricsOverride",
        {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False},
        id=3,
    )
    wait(ws, target_id=3)

    send(ws, "Page.navigate", {"url": url}, id=4)
    wait(ws, target_id=4)
    wait(ws, event="Page.loadEventFired", timeout=8)
    time.sleep(2.0)  # fonts + images

    if section_id:
        send(
            ws,
            "Runtime.evaluate",
            {
                "expression": (
                    f"document.getElementById({section_id!r})?.scrollIntoView("
                    "{block:'start', behavior:'instant'})"
                ),
                "awaitPromise": False,
            },
            id=5,
        )
        wait(ws, target_id=5)
        time.sleep(0.8)

    send(ws, "Page.captureScreenshot", {"format": "png"}, id=6)
    result = wait(ws, target_id=6, timeout=60)

    ws.close()
    proc.kill()

    if not result or "data" not in result:
        sys.exit(f"Error: screenshot capture failed; raw_result={result!r}")

    suffix = f"-{label}" if label else ""
    path = os.path.join(OUT_DIR, f"screenshot-{next_num()}{suffix}.png")
    with open(path, "wb") as f:
        f.write(base64.b64decode(result["data"]))
    print(f"Screenshot saved: {path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: screenshot_section.py <url> [label] [section_id]")
    capture(
        sys.argv[1],
        sys.argv[2] if len(sys.argv) > 2 else "",
        sys.argv[3] if len(sys.argv) > 3 else None,
    )
