"""
Record the three screen segments for the MVP video.

Drives the real RailBlock app in a real browser and records what happens,
so the footage is genuine capture of the working software — not a mockup.
A cursor is drawn into the page so it reads as a normal screencast.

Produces, in video/raw/screen/ :
    b04_screen.mp4   the plan          ~30 s
    b05_screen.mp4   the slider        ~24 s
    b06_screen.mp4   the conflict      ~30 s

Run:
    python capture_screen.py

Needs the app dependencies plus:  pip install playwright imageio-ffmpeg
and one-time:                     python -m playwright install chromium
"""
from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
APP = HERE.parent / "prototype" / "app.py"
OUT = HERE / "raw" / "screen"
TMP = HERE / "raw" / "_capture_tmp"

W, H = 1600, 900          # 16:9, downscales cleanly to 1280x720
PORT = 8531
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


# ══════════════════════════════════════════════════════════════════
#  Cursor drawn into the page (headless browsers record no pointer)
# ══════════════════════════════════════════════════════════════════
CURSOR_JS = r"""
() => {
  if (document.getElementById('__cur')) return;
  const d = document.createElement('div');
  d.id = '__cur';
  d.style.cssText = [
    'position:fixed','left:0','top:0','width:24px','height:24px',
    'z-index:2147483647','pointer-events:none',
    'transform:translate(60px,60px)',
    'filter:drop-shadow(0 2px 3px rgba(0,0,0,.35))'
  ].join(';');
  d.innerHTML =
    '<svg viewBox="0 0 24 24" width="24" height="24">' +
    '<path d="M5 2 L5 19 L9.5 14.5 L12.5 21 L15 19.8 L12 13.6 L18.5 13.2 Z"' +
    ' fill="#1a1a1a" stroke="#ffffff" stroke-width="1.5"' +
    ' stroke-linejoin="round"/></svg>';
  document.body.appendChild(d);

  const ring = document.createElement('div');
  ring.id = '__ring';
  ring.style.cssText = [
    'position:fixed','left:0','top:0','width:34px','height:34px',
    'margin:-17px 0 0 -17px','border-radius:50%','opacity:0',
    'border:2.5px solid #A63D28','z-index:2147483646','pointer-events:none'
  ].join(';');
  document.body.appendChild(ring);

  window.__moveCur = (x, y, ms) => {
    const c = document.getElementById('__cur');
    c.style.transition = `transform ${ms}ms cubic-bezier(.33,0,.2,1)`;
    c.style.transform = `translate(${x}px,${y}px)`;
  };
  window.__clickCur = (x, y) => {
    const r = document.getElementById('__ring');
    r.style.transition = 'none';
    r.style.left = x + 'px'; r.style.top = y + 'px';
    r.style.transform = 'scale(.35)'; r.style.opacity = '.95';
    requestAnimationFrame(() => {
      r.style.transition = 'transform .45s ease-out, opacity .45s ease-out';
      r.style.transform = 'scale(1.5)'; r.style.opacity = '0';
    });
  };
}
"""


class Screen:
    """Thin wrapper so each step reads like a shot description."""

    def __init__(self, page):
        self.page = page
        self.x, self.y = 60, 60

    def cursor(self):
        """(Re)draw the cursor and hide Streamlit's hover chrome.

        Called again after every interaction because a Streamlit rerun
        replaces the DOM and takes both of them with it.
        """
        self.page.evaluate(CURSOR_JS)
        self.page.evaluate(
            """(css) => {
                 if (document.getElementById('__clean')) return;
                 const s = document.createElement('style');
                 s.id = '__clean'; s.textContent = css;
                 document.head.appendChild(s);
               }""", CLEAN_CSS)

    def move(self, x, y, ms=650, settle=180):
        self.page.evaluate(f"window.__moveCur({x},{y},{ms})")
        self.page.wait_for_timeout(ms + settle)
        self.x, self.y = x, y

    def hold(self, ms):
        self.page.wait_for_timeout(ms)

    def click_at(self, x, y, ms=650):
        self.move(x, y, ms)
        self.page.evaluate(f"window.__clickCur({x},{y})")
        self.page.mouse.click(x, y)
        self.page.wait_for_timeout(250)

    def click(self, locator, ms=650, after=1600):
        box = locator.bounding_box()
        if box is None:
            raise RuntimeError("element not visible")
        cx = box["x"] + box["width"] / 2
        cy = box["y"] + box["height"] / 2
        self.click_at(cx, cy, ms)
        self.page.wait_for_timeout(after)
        self.cursor()          # survive Streamlit DOM swaps

    def sweep(self, points, ms=700):
        """Trace the cursor through a series of points."""
        for x, y in points:
            self.move(x, y, ms, settle=120)


# Streamlit's hover chrome would otherwise drift into the footage.
CLEAN_CSS = """
[data-testid="stElementToolbar"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stStatusWidget"],
[data-testid="stToolbar"],
header [data-testid="stHeader"] { display:none !important; }
[data-testid="stHeader"] { background:transparent !important; }
"""


def wait_ready(page, timeout=45000):
    """Wait until Streamlit has finished its rerun.

    Waits on the metric row rather than the chart: scenario C is
    infeasible, so it stops before drawing any chart at all and an
    image-based wait would hang there forever.
    """
    page.wait_for_selector('[data-testid="stMetric"]', timeout=timeout)
    for _ in range(60):
        if page.locator('[data-testid="stStatusWidget"]').count() == 0:
            break
        page.wait_for_timeout(250)
    page.wait_for_timeout(900)


# ══════════════════════════════════════════════════════════════════
#  Server
# ══════════════════════════════════════════════════════════════════
def port_open(port):
    with socket.socket() as s:
        s.settimeout(0.4)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_app():
    if port_open(PORT):
        print(f"  app already up on {PORT}")
        return None
    print(f"  starting streamlit on {PORT} ...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", str(APP),
         "--server.port", str(PORT), "--server.headless", "true"],
        cwd=str(APP.parent),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(90):
        if port_open(PORT):
            time.sleep(3)
            print("  app ready")
            return proc
        time.sleep(1)
    proc.terminate()
    raise RuntimeError("streamlit did not start")


# ══════════════════════════════════════════════════════════════════
#  The three shots
# ══════════════════════════════════════════════════════════════════
def shot_plan(page):
    """BEAT 4 — pick the full corridor, show the plan and the verification."""
    s = Screen(page)
    s.cursor()
    s.hold(1200)

    # Choose scenario B; the corridor re-solves on screen.
    s.click(page.get_by_text("B — Full corridor", exact=False), ms=900)
    wait_ready(page)
    s.cursor()
    s.hold(2600)

    # The metric row: proven optimal, blocks, solve time, violations.
    s.move(560, 300, 800); s.hold(1900)      # Result
    s.move(900, 300, 700); s.hold(1400)      # Blocks scheduled
    s.move(1230, 300, 700); s.hold(1700)     # Solved in
    s.move(1520, 300, 700); s.hold(2000)     # Rule violations

    # Trace across the Gantt: a window band, then blocks inside it.
    s.sweep([(620, 430), (760, 470), (980, 520), (1240, 560)], ms=760)
    s.hold(1600)

    # Settle on the green verification banner.
    s.move(820, 690, 800)
    s.hold(3200)


def shot_slider(page):
    """BEAT 5 — the priority trade-off, both extremes.

    Each shot gets a fresh browser context, which resets the app to
    scenario A, so select the full corridor first: the script talks about
    "the same 18 jobs", and the 7-day / 2-day contrast only reads on B.
    """
    s = Screen(page)
    s.cursor()
    s.hold(700)

    s.click(page.get_by_text("B — Full corridor", exact=False), ms=800)
    wait_ready(page)
    s.cursor()
    s.hold(1600)

    track = page.locator('[data-testid="stSlider"]').first
    box = track.bounding_box()
    y = box["y"] + box["height"] / 2
    left = box["x"] + 6
    right = box["x"] + box["width"] - 6
    mid = box["x"] + box["width"] / 2

    # Grab the handle.
    s.move(mid, y, 800)
    s.hold(700)

    # Drag to "protect service".
    page.evaluate(f"window.__clickCur({mid},{y})")
    page.mouse.move(mid, y)
    page.mouse.down()
    for i in range(1, 13):
        x = mid + (left - mid) * i / 12
        page.mouse.move(x, y)
        page.evaluate(f"window.__moveCur({x},{y},90)")
        page.wait_for_timeout(70)
    page.mouse.up()
    wait_ready(page)
    s.cursor()
    page.evaluate(f"window.__moveCur({left},{y},0)")
    s.hold(3600)                       # let the 7-day spread be read

    # Drag to "clear urgent work".
    page.mouse.move(left, y)
    page.mouse.down()
    for i in range(1, 19):
        x = left + (right - left) * i / 18
        page.mouse.move(x, y)
        page.evaluate(f"window.__moveCur({x},{y},90)")
        page.wait_for_timeout(70)
    page.mouse.up()
    wait_ready(page)
    s.cursor()
    page.evaluate(f"window.__moveCur({right},{y},0)")
    s.hold(4200)                       # and the 2-day compression


def shot_conflict(page):
    """BEAT 6 — the overloaded night and the minimal conflict set."""
    s = Screen(page)
    s.cursor()
    s.hold(1000)

    s.click(page.get_by_text("C — Overloaded", exact=False), ms=900)
    wait_ready(page)
    s.cursor()
    s.hold(2400)

    # The conflict panel is already on screen for scenario C, because the
    # app defaults "every request is mandatory" on for this scenario.
    s.move(700, 300, 800); s.hold(1800)       # "No valid plan"
    s.move(1050, 300, 700); s.hold(1600)      # requests in conflict
    s.move(1380, 300, 700); s.hold(1500)      # proved in

    # The explanation, then each culprit in turn.
    s.move(700, 400, 800); s.hold(3000)
    s.move(520, 500, 700); s.hold(1500)       # R01
    s.move(520, 545, 500); s.hold(1500)       # R02
    s.move(520, 590, 500); s.hold(1900)       # R03
    s.move(760, 680, 800); s.hold(3400)       # the takeaway note


SHOTS = [
    ("b04_screen", "the plan",     shot_plan),
    ("b05_screen", "the slider",   shot_slider),
    ("b06_screen", "the conflict", shot_conflict),
]


# ══════════════════════════════════════════════════════════════════
def transcode(src: Path, dst: Path):
    """webm -> mp4 h264, the format every editor accepts."""
    subprocess.run(
        [FFMPEG, "-y", "-loglevel", "error", "-i", str(src),
         "-c:v", "libx264", "-preset", "slow", "-crf", "20",
         "-pix_fmt", "yuv420p", "-r", "30",
         "-vf", "scale=1280:720:flags=lanczos", "-an", str(dst)],
        check=True)


def main() -> int:
    # Optional shot names on the command line, e.g.  python capture_screen.py b05
    wanted = [a.lower() for a in sys.argv[1:]]
    shots = [s for s in SHOTS
             if not wanted or any(w in s[0] for w in wanted)]
    if not shots:
        print("  no shot matched", wanted)
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)

    proc = start_app()
    made = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=["--force-color-profile=srgb"])
            for name, label, shot in shots:
                print(f"  recording {name} — {label} ...")
                ctx = browser.new_context(
                    viewport={"width": W, "height": H},
                    device_scale_factor=1,
                    record_video_dir=str(TMP / name),
                    record_video_size={"width": W, "height": H},
                    color_scheme="light",
                )
                page = ctx.new_page()
                page.goto(f"http://127.0.0.1:{PORT}", wait_until="load")
                wait_ready(page)
                shot(page)
                page.wait_for_timeout(600)
                ctx.close()          # flushes the video file

                webm = next((TMP / name).glob("*.webm"))
                mp4 = OUT / f"{name}.mp4"
                transcode(webm, mp4)
                size = mp4.stat().st_size / 1024
                made.append((mp4, size))
                print(f"    -> {mp4.name}  ({size:.0f} KB)")
            browser.close()
    finally:
        if proc:
            proc.terminate()
        shutil.rmtree(TMP, ignore_errors=True)

    print()
    print("  Done. Screen footage in:", OUT)
    for p, s in made:
        print(f"    {p.name:18} {s:7.0f} KB")
    print()
    print("  ffmpeg for your final export:")
    print("   ", FFMPEG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
