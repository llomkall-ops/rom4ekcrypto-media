"""Mix a background track into a silent Reel to make a YouTube Short.

Usage: python3 tools/add_music.py videos/<folder>.mp4 <track.mp3> shorts/<folder>.mp4
Music: trimmed to video length, loudness-normalised to about -20 LUFS, 1 s fade-in, 2 s fade-out.
"""
import subprocess, sys
vid, track, out = sys.argv[1:4]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", vid]).strip())
import os; os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
af = (f"[1:a]atrim=0:{dur},asetpts=N/SR/TB,loudnorm=I=-20:TP=-2:LRA=11,"
      f"afade=t=in:st=0:d=1,afade=t=out:st={max(dur-2,0):.2f}:d=2[a]")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vid, "-i", track, "-filter_complex", af,
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
print(out, dur, "s")
