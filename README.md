# SpeakUp clip tool

Turns talk links into mono 16 kHz WAV clips for testing Whisper, Transcribe, and VAD.

Setup (Mac):
  brew install ffmpeg
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt

Use:
  1. Edit clips.csv (name,url,start,end)
  2. python make_clips.py
  3. Clips appear in data/clips/

Do not commit audio. Share WAVs privately (e.g., Drive).