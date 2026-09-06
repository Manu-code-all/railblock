"""
Repair pass on the MVP draft — everything fixable without re-shooting.

  1. Re-frames each talking-head shot to crop the phone out of frame
     (works on five of the seven; see NOTE below).
  2. Lifts the voiceover section, which was recorded ~10 dB quieter than
     the pieces to camera, then normalises the whole track.
  3. Corrects the underexposed, orange-cast indoor shots.
  4. Exports 720p H.264 under the portal's 10 MB cap.

NOTE: in the last two shots (136 s onward) the phone is held level with
the chin, so no crop can remove it without cutting the face. Those are
re-framed tighter to make it less prominent, and that is the limit of
what post can do.

Run:  python fix_draft.py
"""
import os
import shutil
import subprocess
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "edit", "draft one .mov")
WORK = os.path.join(HERE, "_work")
OUT = os.path.join(HERE, "final", "railblock_mvp.mp4")
END = 172.13

# Warm indoor shots: lift exposure and pull the orange back toward neutral.
WARM = ("eq=brightness=0.055:contrast=1.07:saturation=0.94,"
        "colorbalance=rm=-0.07:gm=-0.02:bm=0.09")

# (start, end, crop or None, extra filter)
#   crop = w:h:x:y  chosen so the phone falls below the frame
SEGMENTS = [
    (0.00,   12.20, "1056:594:374:0",   None),   # atrium      1.21x
    (12.20,  20.80, "1066:600:426:0",   None),   # sofa        1.20x
    (20.80,  33.00, "1066:600:312:0",   WARM),   # warm, wide  1.20x
    (33.00,  41.50, "1152:648:518:0",   WARM),   # warm, mid   1.11x
    (41.50,  45.70, "1382:778:192:0",   WARM),   # warm, close 0.93x
    (45.70, 136.10, None,               None),   # screen capture — untouched
    (136.10, 160.90, "1066:600:426:100", None),  # bench       1.20x
    (160.90, END,    "1066:600:426:130", None),  # glass       1.20x
]

# The voiceover ran about 10 dB under the pieces to camera.
VO_START, VO_END, VO_GAIN = 45.70, 136.10, 8

TARGET_MB = 9.8
AUDIO_KBPS = 96


def run(cmd):
    subprocess.run(cmd, check=True, cwd=HERE)


def render_segments():
    """Each shot rendered on its own — far more robust than one big graph."""
    paths = []
    for i, (a, b, crop, extra) in enumerate(SEGMENTS):
        chain = []
        if crop:
            chain.append(f"crop={crop}")
        if extra:
            chain.append(extra)
        chain += ["scale=1280:720:flags=lanczos", "setsar=1", "fps=30"]
        dst = os.path.join(WORK, f"seg{i:02d}.mp4")
        print(f"  segment {i}  {a:6.1f}-{b:6.1f}s"
              f"  {'crop ' + crop if crop else 'no crop'}")
        run([FF, "-y", "-loglevel", "error", "-i", SRC,
             "-ss", str(a), "-to", str(b),
             "-vf", ",".join(chain), "-an",
             "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
             "-pix_fmt", "yuv420p", dst])
        paths.append(dst)
    return paths


def join(paths):
    lst = os.path.join(WORK, "list.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for p in paths:
            f.write(f"file '{p.replace(chr(92), '/')}'\n")
    dst = os.path.join(WORK, "video.mp4")
    run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", dst])
    return dst


def audio():
    dst = os.path.join(WORK, "audio.wav")
    run([FF, "-y", "-loglevel", "error", "-i", SRC, "-vn",
         "-af", f"highpass=f=80,"
                f"volume=enable='between(t,{VO_START},{VO_END})':"
                f"volume={VO_GAIN}dB,"
                f"loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:a", "pcm_s16le", "-ar", "48000", dst])
    return dst


def video_bitrate():
    total = TARGET_MB * 1024 * 1024 * 8
    return int((total - AUDIO_KBPS * 1000 * END) / END / 1000 * 0.94)


def encode(vid, aud):
    vb = video_bitrate()
    print(f"  encoding at {vb} kbps video + {AUDIO_KBPS} kbps audio")
    base = [FF, "-y", "-loglevel", "error", "-i", vid, "-i", aud,
            "-map", "0:v", "-c:v", "libx264", "-b:v", f"{vb}k",
            "-preset", "slow", "-pix_fmt", "yuv420p"]
    run(base + ["-pass", "1", "-an", "-f", "mp4", os.devnull])
    run(base + ["-pass", "2", "-map", "1:a",
                "-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k",
                "-shortest", "-movflags", "+faststart", OUT])


def main():
    os.makedirs(os.path.join(HERE, "final"), exist_ok=True)
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)

    segs = render_segments()
    print("  joining ...")
    vid = join(segs)
    print("  processing audio ...")
    aud = audio()
    encode(vid, aud)

    for f in os.listdir(HERE):
        if f.startswith("ffmpeg2pass"):
            os.remove(os.path.join(HERE, f))
    shutil.rmtree(WORK, ignore_errors=True)

    mb = os.path.getsize(OUT) / 1048576
    print(f"\n  {OUT}")
    print(f"  {mb:.2f} MB  (limit 10 MB)")
    if mb > 10:
        print("  OVER — lower TARGET_MB and re-run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
