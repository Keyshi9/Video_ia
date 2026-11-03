# Mix of the Bastille short (adapted from the skill's mix.py). The guide voice (public/bastille/voice.wav, Piper TTS) is
# the level reference and is NOT changed (unity gain, no EQ/compression). Music = original fife-and-drum march, ducked
# under the speech spans of words.json and set per section relative to the voice (standard mix: music +3 dB = bed
# -10 LU under the voice instead of -13); SFX = event cues at naive - 6 dB (standard mix), beds at their own level.
# Outputs (48 kHz, stereo, 24-bit, exactly 30.000 s = 1,440,000 samples):
#   music_sfx.wav  music + SFX, no voice (for the user's own voice later; same gains as guide_mix)
#   guide_mix.wav  music + SFX + guide voice
#   stem_voice.wav / stem_music.wav / stem_sfx.wav (pre-limiter, at mix gain)
#   cues.md        cue sheet + loudness report
import os
import sys
import time
import json
import subprocess
import numpy as np
from scipy import ndimage, signal
from dsp import (SR, ns, st, dbg, read_wav, write_wav, integrated, momentary, short_term, lra, true_peak, fades)
import timeline as T

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = r"C:/Users/pu99cle/remotion-shorts/public/bastille"
FFMPEG = r"C:/Users/pu99cle/AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe"
CACHE = os.path.join(HERE, "_cache")
N = ns(T.DUR)                    # 1,440,000 samples = 30.000 s
CEIL_DBTP = -1.0
TARGET_LUFS = -15.0
DUCK_DB = -3.0                   # music dip while the voice speaks (keyed from words.json)

# music level per section, LU relative to the voice in that section (after ducking). Standard: bed -10 (music +3 dB).
MUSIC_TARGET = {"hook": -9.5, "town": -10.5, "muskets": -10.0, "flashback1": -11.0, "siege": -9.5, "courtyard": -13.0,
                "parade": -9.5, "flashback2": -11.0, "finale": -9.0}
REPORT = [(f"{name}", a, b) for name, a, b in [
    ("1 hook", *T.shot_t(1)), ("2 town", *T.shot_t(2)), ("3 muskets", *T.shot_t(3)), ("4 cart (sepia)", *T.shot_t(4)),
    ("5 turn", *T.shot_t(5)), ("6 siege", *T.shot_t(6)), ("7 surrender", *T.shot_t(7)), ("8 seven", *T.shot_t(8)),
    ("9 parade", *T.shot_t(9)), ("10 Sade (sepia)", *T.shot_t(10)), ("11 window", *T.shot_t(11))]]


def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)


def lufs(x):
    v = integrated(x)
    return v if np.isfinite(v) else -99.0


def load_voice():
    x, sr = read_wav(os.path.join(PUB, "voice.wav"))
    assert sr == SR, sr
    v = x[0] if x.shape[0] == 1 else x.mean(0)
    out = np.zeros(N)
    out[: min(N, len(v))] = v[:N]
    return st(out)


def speech_spans(words, merge=0.3):
    sp = []
    for w in words:
        s, e = w["s"], w["e"]
        if sp and s - sp[-1][1] < merge:
            sp[-1][1] = max(sp[-1][1], e)
        else:
            sp.append([s, e])
    return sp


def duck_db(spans, depth=DUCK_DB, pre=0.08, post=0.12, att=0.07, rel=0.45):
    ctrl = 1000
    nc = int(T.DUR * ctrl) + 2
    va = np.zeros(nc)
    for s, e in spans:
        va[max(0, int((s - pre) * ctrl)): int((e + post) * ctrl)] = 1.0
    ka, kr = 1 - np.exp(-1 / (att * ctrl)), 1 - np.exp(-1 / (rel * ctrl))
    env = np.zeros(nc)
    e = 0.0
    for i in range(nc):
        tgt = va[i]
        e += (tgt - e) * (ka if tgt > e else kr)
        env[i] = e
    return np.interp(np.arange(N) / SR, np.arange(nc) / ctrl, depth * env)


def section_db(m_ducked, v):
    import music
    gains = {}
    for name, a, b in music.SECTIONS:
        seg = slice(ns(a), ns(b))
        Lm, Lv = lufs(m_ducked[:, seg]), lufs(v[:, seg])
        gains[name] = (Lv + MUSIC_TARGET[name] - Lm) if Lm > -90 and Lv > -60 else None
    # finale: the voice stops at 29.0, so the finale rides on the parade gain (+1 dB for the button)
    gains["finale"] = (gains.get("parade") or 0.0) + 1.0
    for k in gains:
        if gains[k] is None:
            gains[k] = 0.0
    curve = np.zeros(N)
    t = np.arange(N) / SR
    for name, a, b in music.SECTIONS:
        curve[t >= a] = gains[name]
    # the section switches all sit on hard cuts where the band changes, so keep them short (60 ms)
    curve = ndimage.uniform_filter1d(curve, ns(0.06), mode="nearest")
    return curve, gains


def limiter(x, ceil_db=CEIL_DBTP, look=0.003, rel=0.08):
    """4x-oversampled peak detection, look-ahead min filter, one-pole release, centred smoothing"""
    c = dbg(ceil_db)
    n = x.shape[1]
    up = np.abs(signal.resample_poly(x, 4, 1, axis=-1)).max(0)
    pk = np.pad(up, (0, max(0, 4 * n - len(up))))[: 4 * n].reshape(n, 4).max(1)
    gr = np.minimum(1.0, c / np.maximum(pk, 1e-12))
    La = max(1, ns(look))
    g1 = ndimage.minimum_filter1d(gr, 2 * La + 1, mode="nearest")
    g2 = g1.copy()
    idx = np.flatnonzero(g1 < 1.0)
    if len(idx):
        kr = 1 - np.exp(-1 / (rel * SR))
        gap = ns(rel * 8)
        brk = np.flatnonzero(np.diff(idx) > gap)
        starts = np.concatenate([[idx[0]], idx[brk + 1]])
        ends = np.concatenate([idx[brk], [idx[-1]]])
        for a, b_ in zip(starts, ends):
            e = min(n, b_ + gap)
            seg = g1[a:e]
            out = np.empty(len(seg))
            g = 1.0
            for k in range(len(seg)):
                g = min(seg[k], g + (1 - g) * kr)
                out[k] = g
            g2[a:e] = out
    g3 = np.minimum(ndimage.uniform_filter1d(g2, 2 * La + 1, mode="nearest"), 1.0)
    return x * g3[None, :], g3


def ffmpeg_ebur(path):
    try:
        r = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True, timeout=300)
        txt = r.stderr
        i = txt.rfind("Summary:")
        if i < 0:
            return txt[-1500:]
        out = []
        for line in txt[i:].splitlines():
            if line.strip():
                out.append(line.rstrip())
            if line.strip().startswith("Peak:"):
                break
        return "\n".join(out)
    except Exception as e:  # noqa
        return f"ffmpeg check failed: {e}"


def section_table(v, m, s, words):
    Mv, Mb = momentary(v), momentary(m + s)
    tc = np.arange(len(Mv)) * 0.01 + 0.2
    speak = np.zeros(len(tc), bool)
    for w in words:
        speak |= (tc >= w["s"] + 0.03) & (tc <= w["e"] - 0.03)
    speak &= Mv > lufs(v) - 10
    rows = []
    for name, a, b in REPORT:
        seg = slice(ns(a), ns(b))
        Lv, Lm, Ls, Lb = lufs(v[:, seg]), lufs(m[:, seg]), lufs(s[:, seg]), lufs(m[:, seg] + s[:, seg])
        k = speak & (tc >= a) & (tc < b) & np.isfinite(Mb) & (Mb > -70)
        med = float(np.median(Mv[k] - Mb[k])) if k.sum() > 5 else float("nan")
        p10 = float(np.percentile(Mv[k] - Mb[k], 10)) if k.sum() > 5 else float("nan")
        rows.append((name, a, b, Lv, Lm, Ls, Lb, Lv - Lb, p10, med))
    return rows


def main():
    t0 = time.time()
    fresh = "--fresh" in sys.argv
    words = T.words(os.path.join(PUB, "words.json"))
    spans = speech_spans(words)
    v = load_voice()
    v_ref = lufs(v)
    log(f"voice: {v_ref:.2f} LUFS (as stereo), TP {true_peak(v):.2f} dBTP")

    import music
    b = music.build()
    m_raw, levels = music.render(b)
    log("music rendered", f"{lufs(m_raw):.2f} LUFS raw", levels)
    dk = duck_db(spans)
    m_d = m_raw * dbg(dk)[None, :]
    sec_curve, sec_gains = section_db(m_d, v)
    m = m_d * dbg(sec_curve)[None, :]

    import sfx
    s, C = sfx.render(v_ref)
    log("sfx rendered", f"{lufs(s):.2f} LUFS")

    # ---- master gain (one common gain on every stem, as in the skill template) so guide_mix sits at -15 LUFS and the
    # hot TTS peaks (+0.1 dBTP raw) barely touch the limiter; the voice gets this gain only (no EQ, no compression)
    G = TARGET_LUFS - lufs(v + m + s)
    for it in range(5):
        y_g, g_g = limiter((v + m + s) * dbg(G))
        L = lufs(y_g)
        if abs(L - TARGET_LUFS) < 0.02:
            break
        G += TARGET_LUFS - L
    log(f"master gain {G:+.2f} dB")
    v, m, s = v * dbg(G), m * dbg(G), s * dbg(G)
    y_g = fades(y_g, 0.0, 0.02)
    # ---- music + sfx only, same gains
    y_b, g_b = limiter(m + s)
    y_b = fades(y_b, 0.0, 0.02)
    for x in (y_g, y_b):
        assert x.shape == (2, N)
    write_wav(os.path.join(HERE, "guide_mix.wav"), y_g)
    write_wav(os.path.join(HERE, "music_sfx.wav"), y_b)
    write_wav(os.path.join(HERE, "stem_voice.wav"), v)
    write_wav(os.path.join(HERE, "stem_music.wav"), m)
    write_wav(os.path.join(HERE, "stem_sfx.wav"), s)
    log("wrote mixes + stems")

    st_ = {}
    for key, y, g in (("guide", y_g, g_g), ("bed", y_b, g_b)):
        grdb = -20 * np.log10(g)
        st_[key] = dict(I=lufs(y), TP=true_peak(y), LRA=lra(y), Mmax=float(np.max(momentary(y))), Smax=float(np.max(short_term(y))),
                        grmax=float(grdb.max()), gr01=float((grdb > 0.1).mean() * 100))
        log(key, {k: round(v_, 2) for k, v_ in st_[key].items()})
    st_["stems"] = dict(voice=lufs(v), music=lufs(m), sfx=lufs(s))
    rows = section_table(v, m, s, words)
    for r in rows:
        log(f"{r[0]:<16} voice {r[3]:6.1f}  music {r[4]:6.1f}  sfx {r[5]:6.1f}  bed {r[6]:6.1f}  margin {r[7]:5.1f}  speech med {r[9]:5.1f} p10 {r[8]:5.1f}")
    eb = {k: ffmpeg_ebur(os.path.join(HERE, f)) for k, f in (("guide_mix.wav", "guide_mix.wav"), ("music_sfx.wav", "music_sfx.wav"))}
    for k, e in eb.items():
        print(k)
        print(e)
    write_cues(C, b, st_, rows, eb, v_ref + G, sec_gains, levels, G)
    log(f"done in {time.time() - t0:.0f} s")


def write_cues(C, b, st_, rows, eb, v_ref, sec_gains, levels, G):
    import music
    L = []
    w = L.append
    w("# The Bastille: Stormed for Gunpowder, Not Prisoners - sound cue sheet")
    w("")
    w("All music and SFX are original, synthesized in numpy/scipy (`music.py` + `instruments.py`, `sfx.py` + `sfx_gen.py`), mixed by `mix.py`.")
    w("The march is an original tune composed for this short (D major, 112 bpm, fife and drum) - not La Marseillaise, not Ca ira, no quoted melody.")
    w(f"Guide voice = `remotion-shorts/public/bastille/voice.wav` (Piper TTS) with no processing: only the common master gain {G:+.2f} dB that every stem gets (mix at -15 LUFS). Timeline: 900 frames @ 30 fps = 30.000 s.")
    w("")
    w("## Files")
    w("| file | content |")
    w("|---|---|")
    w("| `music_sfx.wav` | music + SFX, **no voice**, music already ducked under the guide-voice word spans; same gains as guide_mix |")
    w("| `guide_mix.wav` | music + SFX + guide voice (unprocessed, common master gain only) |")
    w("| `stem_voice.wav` / `stem_music.wav` / `stem_sfx.wav` | stems at mix gain, pre-limiter (they sum to guide_mix before the true-peak limiter) |")
    w("")
    w("All files: 48 kHz, stereo, 24-bit PCM, 1,440,000 samples = 30.000 s.")
    w("")
    w("When the user records the real voice: keep the same rhythm as words.json; lay it at about the guide's level in this mix "
      f"({v_ref:.1f} LUFS integrated, = stem_voice.wav) on top of `music_sfx.wav`. If its timing moves by more than ~0.15 s, re-run `python mix.py` with the new words.json so the duck follows it.")
    w("")
    w("## Loudness")
    for key, name in (("guide", "guide_mix.wav"), ("bed", "music_sfx.wav")):
        s = st_[key]
        w(f"- **{name}**: integrated {s['I']:.1f} LUFS, true peak {s['TP']:.1f} dBTP, LRA {s['LRA']:.1f} LU, max momentary {s['Mmax']:.1f}, "
          f"max short-term {s['Smax']:.1f}. Limiter (ceiling {CEIL_DBTP} dBTP): max GR {s['grmax']:.2f} dB, active on {s['gr01']:.2f} % of samples.")
    S = st_["stems"]
    w(f"- Stems: voice {S['voice']:.1f}, music {S['music']:.1f}, sfx {S['sfx']:.1f} LUFS.")
    w("")
    for k, e in eb.items():
        w(f"ffmpeg ebur128, `{k}`:")
        w("```")
        w(e)
        w("```")
    w("")
    w("## Voice on top: per-shot loudness (LUFS, at mix gain)")
    w("bed = music + sfx; margin = voice - bed; speech median / p10 = 400 ms momentary margin over windows centred on spoken words.")
    w("")
    w("| shot | time s | voice | music | sfx | bed | margin LU | speech median | speech p10 |")
    w("|---|---|---|---|---|---|---|---|---|")
    f = lambda x: "-" if (not np.isfinite(x) or x <= -98) else f"{x:.1f}"
    for r in rows:
        w(f"| {r[0]} | {r[1]:.2f}-{r[2]:.2f} | {f(r[3])} | {f(r[4])} | {f(r[5])} | {f(r[6])} | {f(r[7])} | {f(r[9])} | {f(r[8])} |")
    w("")
    w("## Music map")
    w(f"Original march, D major, 112 bpm (quarter = {music.Q:.4f} s): fife 1, fife 2 (a third below), field snare, rope bass drum, soft low reed. "
      "Sepia flashbacks = solo music box of the same tune + vinyl crackle.")
    w(f"Speech duck {DUCK_DB:+.0f} dB keyed from words.json. Section targets (LU under the voice): " +
      ", ".join(f"{k} {v:+.1f}" for k, v in MUSIC_TARGET.items()) + ". Applied section gains (dB): " +
      ", ".join(f"{k} {v:+.1f}" for k, v in sec_gains.items()) + ".")
    w("")
    w("| time s | frame | music |")
    w("|---|---|---|")
    for t, d in sorted(b.cues):
        w(f"| {t:.2f} | {t * T.FPS:.0f} | {d} |")
    w("")
    w("## SFX events")
    w("Level convention: EVENT naive level = LU vs the voice (event max momentary); applied = naive - 6 dB (standard mix). "
      "BEDs are integrated loudness vs the voice and are not reduced. Reverb: 'square' (open, 1.0 s) or 'stone' (gate arch / courtyard, 1.8 s).")
    w("")
    w("| # | time s | frame | cue | what | naive LU | applied LU | room | pan |")
    w("|---|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(sorted(C, key=lambda c: (c.t, c.name))):
        kind = " (bed)" if c.kind == "bed" else ""
        w(f"| {i + 1} | {c.t:.2f} | {c.t * T.FPS:.0f} | {c.name}{kind} | {c.desc} | {c.naive:+.0f} | {c.applied:+.1f} | {c.room} | {c.p:+.2f} |")
    w("")
    open(os.path.join(HERE, "cues.md"), "w", encoding="utf-8").write("\n".join(L))


if __name__ == "__main__":
    main()
