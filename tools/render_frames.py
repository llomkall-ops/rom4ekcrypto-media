#!/usr/bin/env python3
"""Render an HTML animation (window.render(t)) to PNG frames.
Usage: render_frames.py page.html out_dir duration_s [fps] [t1,t2,... for stills only]"""
import sys, asyncio, pathlib
from playwright.async_api import async_playwright

async def main(page_path, out, dur, fps=30, stills=None):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.goto(pathlib.Path(page_path).resolve().as_uri())
        await pg.wait_for_timeout(400)
        times = stills if stills else [i / fps for i in range(int(round(dur * fps)))]
        for i, t in enumerate(times):
            await pg.evaluate(f"render({t})")
            name = f"still_{t:05.2f}.png" if stills else f"f_{i:05d}.png"
            await pg.screenshot(path=str(out / name))
        await b.close()

if __name__ == "__main__":
    a = sys.argv
    stills = [float(x) for x in a[5].split(",")] if len(a) > 5 else None
    asyncio.run(main(a[1], a[2], float(a[3]), int(a[4]) if len(a) > 4 else 30, stills))
