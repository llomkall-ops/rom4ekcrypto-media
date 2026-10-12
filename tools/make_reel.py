"""Turn a carousel folder (slide_N.jpg, 1080x1350) into a vertical 9:16 Reel/Short (silent MP4).

Usage: python3 tools/make_reel.py posts/<folder> videos/<folder>.mp4 ["first,others" seconds, default 3.2,4.5] [hook.mp4]
If hook.mp4 (from tools/make_hook.py) is given, it is prepended with a quick 0.3 s fade into the slides.

Layout: dark #1b1b1b canvas 1080x1920, slide centered (y=285), static header "@romchekcrypto"
and a red "Telegram: @romchekcrypto" pill at the bottom; slides change with a slide-left transition.
Music is NOT embedded: Instagram adds it at publication via Metricool audioConfiguration.
"""
import glob, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
DS = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "3.2,4.5"  # first slide, other slides (seconds)
D1, D = (float(x) for x in (DS.split(',') + DS.split(','))[:2])
T = 0.4  # transition
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

slides = sorted(glob.glob(os.path.join(src, "slide_*.jpg")), key=lambda p: int(p.rsplit("_", 1)[1].split(".")[0]))
assert slides, "no slides found"
tmp = tempfile.mkdtemp()
frames = []
for i, p in enumerate(slides, 1):
    bg = Image.new("RGB", (1080, 1920), (27, 27, 27))
    bg.paste(Image.open(p).convert("RGB").resize((1080, 1350)), (0, 285))
    f = os.path.join(tmp, f"f{i}.png"); bg.save(f); frames.append(f)

ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
d.rectangle([0, 0, 1080, 284], fill=(27, 27, 27, 255)); d.rectangle([0, 1636, 1080, 1920], fill=(27, 27, 27, 255))
d.text((540, 150), "@romchekcrypto", font=ImageFont.truetype(FONT, 46), fill=(244, 239, 232), anchor="mm")
d.rounded_rectangle([140, 1715, 940, 1815], radius=50, fill=(208, 58, 62))
d.text((540, 1765), "Telegram: @romchekcrypto", font=ImageFont.truetype(FONT, 40), fill="white", anchor="mm")
ovp = os.path.join(tmp, "overlay.png"); ov.save(ovp)

args, filt = [], ""
for i, f in enumerate(frames):
    args += ["-loop", "1", "-framerate", "30", "-t", str(D1 if i == 0 else D), "-i", f]
    filt += f"[{i}:v]setsar=1,format=yuv420p[v{i}];"
prev = "v0"
for i in range(1, len(frames)):
    off = round(D1 + (i - 1) * D - i * T, 3)
    filt += f"[{prev}][v{i}]xfade=transition=slideleft:duration={T}:offset={off}[x{i}];"
    prev = f"x{i}"
n = len(frames)
args += ["-loop", "1", "-i", ovp]
filt += f"[{prev}][{n}:v]overlay=0:0,format=yuv420p[out]"
total = round(D1 + (n - 1) * D - (n - 1) * T, 2)
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
hook = sys.argv[4] if len(sys.argv) > 4 else None
body = os.path.join(tmp, "body.mp4") if hook else out
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", filt, "-map", "[out]",
                "-t", str(total), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", "30",
                "-movflags", "+faststart", body], check=True)
if hook:
    hd = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                        "-of", "csv=p=0", hook]).strip())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", hook, "-i", body, "-filter_complex",
                    f"[0:v]fps=30,format=yuv420p,setsar=1[h];[1:v]fps=30,format=yuv420p,setsar=1[b];"
                    f"[h][b]xfade=transition=fade:duration=0.3:offset={hd-0.3:.2f}[out]",
                    "-map", "[out]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
                    "-movflags", "+faststart", out], check=True)
    total = round(total + hd - 0.3, 2)
print(out, total, "s")
