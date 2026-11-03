"""Word timings for a voice file: python tools/words.py voice.wav words.json"""
import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel

src, dst = sys.argv[1], sys.argv[2]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio, word_timestamps=True, language="en")
words = [{"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s in segs for w in s.words]
json.dump(words, open(dst, "w"), indent=1)
print(len(words), "words;", " ".join(f"{w['word']}@{w['start']}" for w in words))
