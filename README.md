# SpeakUp clip tool

Turns talk links (YouTube, TED, direct .mp4) into mono 16 kHz WAV clips for
testing Whisper, Amazon Transcribe, and VAD. Everyone gets identical files, so
timestamps line up (0:00 = start of the clip).

## Setup (once)

1. Install FFmpeg: `brew install ffmpeg` (Mac), `winget install ffmpeg` (Windows), `sudo apt install ffmpeg` (Linux). Check with `ffmpeg -version`.
2. Create a venv and install:
   ```
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Use

1. Edit `clips.csv`: one row per clip with `name,url,start,end` (times like `1:03`; leave blank for the whole file).
2. Run `python make_clips.py` (or `python make_clips.py clip3_ted_gates` for one).
3. Clips appear in `data/clips/`. Downloads are cached in `data/raw/`, so re-runs are fast.

Share the WAVs with teammates privately (e.g., Drive). Do NOT commit them: `data/` and audio files are gitignored.

## Notes

- To change a clip's range, edit the CSV and delete the old WAV (it is rebuilt every run anyway, but the download stays cached).
- If a TED or YouTube download fails, update yt-dlp: `pip install -U yt-dlp`.
- Downloading may conflict with the sites' terms of service. Keep files internal and use them for testing only.
- `clip1` has no range in the plan; set start/end before annotating so you do not label a full-length video.