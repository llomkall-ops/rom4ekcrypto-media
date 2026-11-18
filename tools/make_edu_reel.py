#!/usr/bin/env python3
"""Build an educational Reel: animated HTML page + cloned voice + subtitles + SFX + music + standard outro.

usage: python3 tools/make_edu_reel.py <lesson_dir> <out.mp4> [--stills t1,t2,...]

<lesson_dir> must contain:
  page.html     – animation page with window.render(t) (copy reels/lessons/2026-11-18-liquidity-hunt/page.html,
                  keep the engine, change scenes). Placeholders /*W*/ and /*G*/ are filled by this script
                  (or W/GROUPS already filled).
  voice.mp3     – ElevenLabs voice (romchek, eleven_v4)
  words.json    – ElevenLabs Scribe words.json ({"words":[{text,type,start,end}]})
  phrases.json  – subtitle groups: list of strings, words in order, 2–4 words each (must cover all words)
  sfx.json      – [[time_s_in_reel, "whoosh/whoosh_short", volume 0.08–0.15], ...] (times = word start + 0.25)
--stills renders only still PNGs to <lesson_dir>/stills for checking (no video).
"""
import json, re, subprocess, sys, pathlib, os

REPO = pathlib.Path(__file__).resolve().parent.parent
SFX = REPO / "reels/sfx"
MUSIC = REPO / "reels/music/edu_bg_01.mp3"
OUTRO = REPO / "reels/outro/romchek_outro.mp4"
VO = 0.25


def run(a):
    subprocess.run(a, check=True)


def fill(lesson):
    h = (lesson / "page.html").read_text()
    w = json.loads((lesson / "words.json").read_text())["words"]
    W = []
    for x in w:
        t = x["text"]
        if x.get("type") != "word" or t.startswith("[") or t.endswith("]") or t in ("—", "-", "–"):
            continue
        W.append([t.rstrip(".,:;"), round(x["start"], 3), round(x["end"], 3)])
    phr = json.loads((lesson / "phrases.json").read_text())
    G, a = [], 0
    for p in phr:
        n = len(p.split()); G.append([a, a + n]); a += n
    if a != len(W):
        sys.exit(f"phrases cover {a} words, transcript has {len(W)}: {[x[0] for x in W]}")
    Wj = json.dumps(W, ensure_ascii=False)
    if "/*W*/" in h:
        h = h.replace("/*W*/[]", Wj).replace("/*G*/[]", json.dumps(G))
    else:
        h = re.sub(r"const W=\[\[.*?\]\]\.map", "const W=" + Wj + ".map", h, flags=re.S)
        h = re.sub(r"const GROUPS=\[\[.*?\]\];", "const GROUPS=" + json.dumps(G) + ";", h)
    out = lesson / "_page_filled.html"
    out.write_text(h)
    return out, round(W[-1][2] + VO + 0.6, 2)


def main():
    lesson = pathlib.Path(sys.argv[1]).resolve()
    page, D = fill(lesson)
    rf = str(REPO / "tools/render_frames.py")
    if "--stills" in sys.argv:
        st = sys.argv[sys.argv.index("--stills") + 1]
        run(["python3", rf, str(page), str(lesson / "stills"), str(D), "30", st])
        print("stills in", lesson / "stills"); return
    out = pathlib.Path(sys.argv[2]).resolve()
    tmp = lesson / "_build"; tmp.mkdir(exist_ok=True)
    frames = tmp / "frames"
    subprocess.run(["rm", "-rf", str(frames)])
    run(["python3", rf, str(page), str(frames), str(D), "30"])
    run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", str(frames / "f_%05d.png"), "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp / "v.mp4")])
    sfx = json.loads((lesson / "sfx.json").read_text())
    a = ["ffmpeg", "-y", "-v", "error", "-i", str(lesson / "voice.mp3")]
    for t, f, v in sfx:
        a += ["-i", str(SFX / f"{f}.wav")]
    fc = f"[0:a]aresample=48000,aformat=channel_layouts=stereo,loudnorm=I=-15:TP=-1.5:LRA=7,adelay=250|250,apad=whole_dur={D}[v];"
    for i, (t, f, v) in enumerate(sfx, 1):
        ms = int(t * 1000)
        fc += f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{i}];"
    fc += "[v]" + "".join(f"[s{i}]" for i in range(1, len(sfx) + 1)) + \
          f"amix=inputs={len(sfx)+1}:normalize=0:duration=first,atrim=0:{D}[out]"
    run(a + ["-filter_complex", fc, "-map", "[out]", "-c:a", "pcm_s16le", str(tmp / "a.wav")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp / "v.mp4"), "-i", str(tmp / "a.wav"), "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-shortest", str(tmp / "main.mp4")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp / "main.mp4"), "-i", str(OUTRO), "-filter_complex",
         "[0:v]fps=30,setsar=1[v0];[1:v]fps=30,scale=1080:1920,setsar=1[v1];"
         "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];"
         "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264",
         "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", str(tmp / "joined.mkv")])
    run(["ffmpeg", "-y", "-v", "error", "-i", str(MUSIC), "-i", str(MUSIC), "-filter_complex",
         "[0:a][1:a]acrossfade=d=3[m]", "-map", "[m]", str(tmp / "music_long.wav")])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                         "csv=p=0", str(tmp / "joined.mkv")]).decode())
    run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp / "joined.mkv"), "-i", str(tmp / "music_long.wav"),
         "-filter_complex",
         f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dur},volume=0.13,afade=t=in:d=0.5,"
         f"afade=t=out:st={dur-1.5}:d=1.5[m];[0:a][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])
    subprocess.run(["rm", "-rf", str(tmp), str(page)])
    print(f"OK {out} {dur:.1f}s (lesson {D}s + outro)")
    if dur < 61:
        print("WARNING: reel is shorter than 61 s — owner's rule: reels must be longer than 1 minute. Extend the script.")


if __name__ == "__main__":
    main()
