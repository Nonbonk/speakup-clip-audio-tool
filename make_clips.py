"""Download talks and cut them into mono 16 kHz WAV clips.

Usage:
    python make_clips.py                 # build every row in clips.csv
    python make_clips.py clip3_ted_gates # build only the named clip(s)

Reads clips.csv (name,url,start,end). Leave start/end blank to keep the whole file.
Downloads go to data/raw/ (cached), clips go to data/clips/.
"""
import csv
import glob
import shutil
import subprocess
import sys
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/clips")


def run(cmd):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def find_download(name):
    # yt-dlp picks the extension, so look for name.* (ignore partial files)
    hits = [p for p in glob.glob(str(RAW / f"{name}.*")) if not p.endswith((".part", ".ytdl"))]
    return Path(hits[0]) if hits else None


def download(name, url):
    existing = find_download(name)
    if existing:
        print(f"  using cached download: {existing}")
        return existing
    RAW.mkdir(parents=True, exist_ok=True)
    run([sys.executable, "-m", "yt_dlp", "-f", "bestaudio/best",
         "-o", str(RAW / f"{name}.%(ext)s"), url])
    path = find_download(name)
    if not path:
        raise RuntimeError(f"Download finished but no file found for {name}")
    return path


def cut(src, dst, start, end):
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", str(src)]
    # -ss/-to AFTER -i = accurate cut (matters for 0.25 s pauses)
    if start:
        cmd += ["-ss", start]
    if end:
        cmd += ["-to", end]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", str(dst)]
    run(cmd)


def main():
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found. Install it first (see README).")

    wanted = set(sys.argv[1:])
    with open("clips.csv", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["name"].strip()]

    failed = []
    for r in rows:
        name = r["name"].strip()
        if wanted and name not in wanted:
            continue
        print(f"\n== {name}")
        try:
            src = download(name, r["url"].strip())
            cut(src, OUT / f"{name}.wav", (r["start"] or "").strip(), (r["end"] or "").strip())
            print(f"  -> {OUT / (name + '.wav')}")
        except Exception as e:  # keep going so one bad link doesn't stop the batch
            print(f"  FAILED: {e}")
            failed.append(name)

    print("\nDone." if not failed else f"\nDone with failures: {', '.join(failed)}")


if __name__ == "__main__":
    main()