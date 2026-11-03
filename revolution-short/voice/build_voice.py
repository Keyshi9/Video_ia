"""voice.wav from script.txt: Piper per line, short pauses inside a line, GAP between lines."""
import subprocess, sys, wave, numpy as np
MODEL = "C:/Users/pu99cle/remotion-shorts/voices/en_US-ryan-high.onnx"
LS, INNER, GAP, HEAD, TAIL = float(sys.argv[1]), 0.12, 0.3, 0.25, 0.6
lines = [l.strip() for l in open("script.txt", encoding="utf-8") if l.strip()]
out, sr, starts = [], 22050, []
def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    return x[max(0, idx[0] - 220): idx[-1] + 880] if len(idx) else x
out.append(np.zeros(int(HEAD * sr)))
for i, l in enumerate(lines):
    subprocess.run([sys.executable, "-m", "piper", "-m", MODEL, "--length-scale", str(LS), "--sentence-silence", str(INNER), "-f", f"line{i}.wav"], input=l.encode(), check=True, capture_output=True)
    w = wave.open(f"line{i}.wav"); sr = w.getframerate()
    x = trim(np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768)
    starts.append(round(sum(len(a) for a in out) / sr, 3))
    out.append(x); out.append(np.zeros(int((GAP if i < len(lines) - 1 else TAIL) * sr)))
y = np.concatenate(out)
w = wave.open("voice.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
print("duration", round(len(y) / sr, 2), "line starts", starts)
