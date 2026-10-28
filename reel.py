# -*- coding: utf-8 -*-
"""Ҳар кунлик постдан юқори сифатли Reels (1080x1920, 30fps) ясайди.
Элементлар навбатма-навбат чиқади. Ишлатиш:  python reel.py 3
Натижа: reels/dayNN.mp4
"""
import pathlib, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright
import render

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "reels"
OUT.mkdir(exist_ok=True)
W, H, FPS = 1080, 1920, 30

# Reels хавфсиз зонаси: тепада ~220px, пастда ~340px Instagram тугмалари ёпади
EXTRA_CSS = """
body{width:1080px!important;height:1920px!important}
.wrap{padding-top:230px!important}
.footer{bottom:330px!important;border-radius:0}
"""

ANIM_JS = """
(() => {
  const seq = [];
  const LEAF = '.m,.li,.op,.col,.kpi,.chart,.pt,.st';
  const wrap = document.querySelector('.wrap');
  for (const el of wrap.children) {
    const leaves = el.querySelectorAll(LEAF);
    if (leaves.length && !el.matches(LEAF)) {
      if (el.classList.contains('glass')) seq.push(el);
      leaves.forEach(l => seq.push(l));
    } else if (el.classList.contains('big') || el.classList.contains('vs') || el.classList.contains('opts') || el.classList.contains('pts')) {
      el.querySelectorAll(':scope > *').forEach(l => seq.push(l));
    } else seq.push(el);
  }
  seq.push(document.querySelector('.footer'));
  window.__seq = seq;
  const fol = document.querySelector('.fol');
  const ease = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
  window.__render = (t) => {
    seq.forEach((el, i) => {
      const start = 0.25 + i * 0.32, p = ease((t - start) / 0.55);
      el.style.opacity = p;
      el.style.transform = `translateY(${(1 - p) * 46}px)`;
    });
    const last = 0.25 + (seq.length - 1) * 0.32 + 0.55;
    if (t > last) { const s = 1 + 0.05 * Math.sin((t - last) * 5); fol.style.transform = `scale(${s})`; }
    return last;
  };
  return window.__render(0);
})()
"""


def make(day, hold=6.0):
    html = render.html_for(day).replace("</style>", EXTRA_CSS + "</style>", 1)
    mp4 = OUT / f"day{day:02d}.mp4"
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.set_content(html); pg.wait_for_timeout(300)
        last = pg.evaluate(ANIM_JS)
        total = last + hold
        n = int(total * FPS)
        for i in range(n):
            pg.evaluate(f"window.__render({i / FPS})")
            pg.screenshot(path=f"{tmp}/f{i:04d}.png")
        b.close()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.png",
                        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                        "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "14",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest",
                        "-movflags", "+faststart", str(mp4)], check=True)
    print("reel:", mp4, f"{total:.1f}s")
    return mp4


if __name__ == "__main__":
    for d in [int(x) for x in sys.argv[1:]]:
        make(d)
