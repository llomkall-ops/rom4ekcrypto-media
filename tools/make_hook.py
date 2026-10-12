"""Render the animated 9:16 cover (~3.8 s) that opens every Reel/Short. Use the SAME text as carousel slide 1
(tag, headline line 1 white, line 2 red, subtitle) so the video does not repeat the cover twice.

Usage:
  python3 tools/make_hook.py out.mp4 --tag "₿ BTC" --l1 "МИНУС" --l2 "$1,25 МЛРД" --sub "Кто сливает крипту?" [--trend down|up]

Look: dark #1b1b1b, candle chart drawing in from the left behind the text, line 1 (white) and
line 2 (red) slam in with a scale-down + shake, sub-line slides up, a pulsing "СМОТРИ ДО КОНЦА 👀" badge.
Frames are rendered with Playwright (Chromium) by seeking CSS animations, then encoded with ffmpeg.
"""
import argparse, asyncio, os, random, subprocess, tempfile, html
from playwright.async_api import async_playwright

ap = argparse.ArgumentParser()
ap.add_argument("out"); ap.add_argument("--tag", default="₿ Крипта")
ap.add_argument("--l1", required=True); ap.add_argument("--l2", required=True)
ap.add_argument("--sub", default=""); ap.add_argument("--trend", default="down", choices=["down", "up"])
ap.add_argument("--dur", type=float, default=3.8)
a = ap.parse_args()
FPS = 30

def candles(trend, seed=3):
    random.seed(seed); w, h = 1080, 700; n = 26; step = (w - 80) / (n - 1)
    p = h * (0.16 if trend == "down" else 0.92); s = []
    for i in range(n):
        o = p; p += random.uniform(6, 34) * (1 if trend == "down" else -1) + random.uniform(-14, 14)
        c = p; x = 40 + i * step; col = "#26a17b" if c < o else "#e0575b"
        hi = min(o, c) - random.uniform(8, 28); lo = max(o, c) + random.uniform(8, 28)
        s.append(f"<line x1='{x}' y1='{hi}' x2='{x}' y2='{lo}' stroke='{col}' stroke-width='5'/>"
                 f"<rect x='{x-16}' y='{min(o,c)}' width='32' height='{max(abs(o-c),5)}' fill='{col}'/>")
    return f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}'>{''.join(s)}</svg>"

esc = html.escape
page = f"""<html><head><meta charset='utf-8'><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1920px;background:#1b1b1b;overflow:hidden;font-family:'Inter Display','Inter',sans-serif;position:relative}}
.chart{{position:absolute;left:0;bottom:250px;opacity:.85;clip-path:inset(0 70% 0 0);animation:draw 2.5s ease-out forwards}}
@keyframes draw{{to{{clip-path:inset(0 0 0 0)}}}}
.fade{{position:absolute;inset:0;background:linear-gradient(#1b1b1b 0%,rgba(27,27,27,.2) 45%,rgba(27,27,27,.85) 100%)}}
.tag{{position:absolute;top:150px;left:50%;transform:translateX(-50%);background:#2a2a2a;border:2px solid #3a3a3a;color:#f4efe8;
  border-radius:50px;padding:16px 38px;font-weight:800;font-size:40px;font-family:Inter;white-space:nowrap}}
.row{{position:absolute;left:0;right:0;display:flex;justify-content:center}}
.big{{font-weight:900;text-transform:uppercase;letter-spacing:-4px;line-height:.9;white-space:nowrap;transform:scaleX(.8)}}
.l1{{color:#f4efe8;font-size:210px;animation:slam .4s cubic-bezier(.2,1.4,.4,1) 0s both}}
.l2{{color:#d03a3e;font-size:230px;animation:slam .4s cubic-bezier(.2,1.4,.4,1) 0s both, shake .3s linear .5s 2}}
.sub{{color:#f4efe8;font-family:Inter;font-weight:800;font-size:64px;line-height:1.15;text-align:center;animation:up .4s ease-out 0s both;max-width:940px}}
.badge{{background:#d03a3e;color:#fff;font-family:Inter;font-weight:900;font-size:46px;border-radius:60px;padding:24px 52px;white-space:nowrap;
  animation:pulse .5s ease-in-out .4s 6 alternate}}
@keyframes slam{{0%{{opacity:1;transform:scaleX(.8) scale(1.06)}}100%{{opacity:1;transform:scaleX(.8) scale(1)}}}}
@keyframes shake{{0%,100%{{transform:scaleX(.8) translateX(0)}}25%{{transform:scaleX(.8) translateX(-14px)}}75%{{transform:scaleX(.8) translateX(14px)}}}}
@keyframes up{{from{{opacity:1;transform:translateY(30px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{from{{opacity:0;transform:translateX(-50%) scale(.6)}}to{{opacity:1;transform:translateX(-50%) scale(1)}}}}
.badge{{position:relative}}
@keyframes pulse{{from{{transform:scale(1)}}to{{transform:scale(1.08)}}}}
</style></head><body>
<div class='chart'>{candles(a.trend)}</div><div class='fade'></div>
<div class='tag'>{esc(a.tag)}</div>
<div class='row' style='top:400px'><div class='big l1'>{esc(a.l1)}</div></div>
<div class='row' style='top:620px'><div class='big l2'>{esc(a.l2)}</div></div>
<div class='row' style='top:880px'><div class='sub'>{esc(a.sub)}</div></div>
<div class='row' style='bottom:190px'><div class='badge'>СМОТРИ ДО КОНЦА 👀</div></div>
</body></html>"""

async def main():
    tmp = tempfile.mkdtemp()
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(page); await pg.wait_for_timeout(300)
        # auto-shrink lines that are too wide
        await pg.evaluate("""() => { document.querySelectorAll('.big').forEach(el => {
            let fs = parseFloat(getComputedStyle(el).fontSize);
            const lim = 1180;  /* big lines are scaleX(.8) */
            while (el.scrollWidth > lim && fs > 40) { fs -= 4; el.style.fontSize = fs + 'px'; } }); }""")
        await pg.evaluate("() => document.getAnimations().forEach(x => x.pause())")
        n = int(a.dur * FPS)
        for i in range(n):
            t = i * 1000 / FPS
            await pg.evaluate(f"() => document.getAnimations().forEach(x => x.currentTime = {t})")
            await pg.screenshot(path=f"{tmp}/h{i:03d}.png")
        await b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/h%03d.png",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", a.out], check=True)
    print(a.out)
asyncio.run(main())
