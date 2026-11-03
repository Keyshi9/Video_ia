# Original 18th-century style fife-and-drum march for the Bastille short, composed and synthesized here
# (D major, 112 bpm, 4/4). Not based on La Marseillaise, Ca ira or any other existing tune.
# Band: fife 1 (melody), fife 2 (diatonic third below), field snare, rope bass drum, a soft low reed/bassoon bass.
# Sepia flashbacks (shots 4 and 10) switch to a solo music-box version of the same tune with vinyl crackle.
import numpy as np
from dsp import SR, ns, tt, rng, pan, place, fades, dbg, make_ir, convolve_st, integrated, lp, hp, bp, phase, smooth_noise
import instruments as I
import timeline as T

N = ns(T.DUR)
BPM = 112.0
Q = 60.0 / BPM            # 0.5357 s
BAR = 4 * Q               # 2.143 s
F = I.m2f

# theme: (bar, beat, length in quarters, midi) - fife register (D5 = 74)
THEME = [
    (1, 0, 1, 74), (1, 1, .75, 78), (1, 1.75, .25, 76), (1, 2, 1, 78), (1, 3, 1, 81),
    (2, 0, .5, 83), (2, .5, .5, 81), (2, 1, .5, 78), (2, 1.5, .5, 74), (2, 2, 2, 76),
    (3, 0, 1, 78), (3, 1, .75, 81), (3, 1.75, .25, 83), (3, 2, 1, 86), (3, 3, .5, 85), (3, 3.5, .5, 83),
    (4, 0, 1, 81), (4, 1, .5, 79), (4, 1.5, .5, 78), (4, 2, 1, 76), (4, 3, 1, 73),
    (5, 0, 1, 81), (5, 1, .75, 86), (5, 1.75, .25, 85), (5, 2, 1, 83), (5, 3, 1, 81),
    (6, 0, .5, 79), (6, .5, .5, 78), (6, 1, .5, 76), (6, 1.5, .5, 79), (6, 2, 1, 78), (6, 3, 1, 74),
    (7, 0, .75, 76), (7, .75, .25, 78), (7, 1, .5, 79), (7, 1.5, .5, 76), (7, 2, 1, 73), (7, 3, .5, 76), (7, 3.5, .5, 73),
    (8, 0, 2, 74),
]
CHB = {1: "DDDD", 2: "GGAA", 3: "DDGG", 4: "AAAA", 5: "DDGG", 6: "GGDD", 7: "AAAA", 8: "DDDD"}
ROOT = {"D": 38, "G": 43, "A": 45}
SCALE = [2, 4, 6, 7, 9, 11, 13]   # D major pitch classes (13 = C# of the next octave)

SECTIONS = [  # (name, start, end) - used by mix.py for level automation and by the cue sheet
    ("hook", 0.0, T.FLASH_AT), ("town", T.FLASH_AT, 5.8), ("muskets", 5.8, 8.87), ("flashback1", 8.87, T.COLOUR1),
    ("siege", T.COLOUR1, T.COURTYARD), ("courtyard", T.COURTYARD, T.CHEER_BACK), ("parade", T.CHEER_BACK, T.FLASHBACK2[0]),
    ("flashback2", T.FLASHBACK2[0], T.COLOUR2), ("finale", T.COLOUR2, T.DUR),
]


def third_below(m):
    pc = m % 12
    pcs = [p % 12 for p in SCALE]
    if pc not in pcs:
        return m - 3
    i = pcs.index(pc)
    j = i - 2
    oct_ = 0
    if j < 0:
        j += 7
        oct_ = -12
    d = (pcs[j] - pc) % 12 - 12
    return m + d


def theme(t_bar1, bars, transpose=0):
    ev = []
    for (b, beat, d, m) in THEME:
        if b in bars:
            k = list(bars).index(b)
            ev.append((t_bar1 + k * BAR + beat * Q, d * Q, m + transpose))
    return sorted(ev)


class Band:
    def __init__(self):
        self.tr, self.send, self.cues = {}, {}, []

    def track(self, name, send):
        if name not in self.tr:
            self.tr[name] = np.zeros((2, N))
            self.send[name] = send
        return self.tr[name]

    def add(self, name, x, t, p=0.0, g=1.0):
        place(self.track(name, 0.15), pan(x, p) if np.ndim(x) == 1 else x, t, g)

    def gate(self, names, t_off, fade=0.02, t_on=None):
        """silence the given tracks from t_off (short fade) until t_on (or the end)"""
        g = np.ones(N)
        a, z = ns(t_off), ns(t_off + fade)
        g[a:z] = np.linspace(1, 0, z - a)
        e = N if t_on is None else ns(t_on)
        g[z:e] = 0
        for k in names:
            if k in self.tr:
                self.tr[k] *= g[None, :]


R = rng(1789)


def _r():
    return rng(int(R.integers(1 << 30)))


def bassdrum(vel=0.8, r=None):
    r = r or rng(0)
    d = 0.7
    t = tt(d)
    body = np.exp(-t / 0.16) * np.sin(phase(58 * (1 + 0.35 * np.exp(-t / 0.018))))
    skin = np.exp(-t / 0.07) * np.sin(phase(96 * (1 + 0.2 * np.exp(-t / 0.01)))) * 0.45
    beat = lp(r.standard_normal(len(t)), 900, 2) * np.exp(-t / 0.012) * 0.8
    return fades((body + skin + beat) * vel, 0.0005, 0.08)


def fifes(b, notes, vel, harm=True, gate=0.88, p1=0.18, p2=-0.22):
    for (t, d, m) in notes:
        b.add("fife", I.fife(F(m), d * gate, vel * R.uniform(0.94, 1.04), _r()), t + R.normal(0, 0.003), p1)
        if harm:
            b.add("fife2", I.fife(F(third_below(m)), d * gate, vel * 0.8 * R.uniform(0.94, 1.04), _r()), t + 0.008 + R.normal(0, 0.004), p2)


SN = {  # 16th steps per bar: 0 rest, 1 ghost, 2 normal, 3 flam accent
    "light": [3, 0, 0, 0, 2, 0, 1, 0, 2, 0, 0, 0, 2, 0, 1, 1],
    "march": [3, 0, 1, 1, 2, 0, 1, 0, 3, 0, 1, 1, 2, 1, 2, 1],
    "drive": [3, 1, 2, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2, 1, 2, 1],
}


def snare_bar(b, t_bar, pat, vel, steps=range(16), cres=0.0, t_min=-1.0):
    for s in steps:
        v = SN[pat][s]
        t = t_bar + s * Q / 4
        if not v or t < t_min:
            continue
        vv = vel * (1 + cres * s / 16) * {1: 0.42, 2: 0.85, 3: 1.0}[v] * R.uniform(0.93, 1.05)
        if v == 3:
            b.add("snare", I.snare(vv * 0.4, _r()), t - 0.024, 0.06)
        b.add("snare", I.snare(vv, _r()), t + R.normal(0, 0.002), 0.06)


def roll(b, t0, t1, v0, v1, accent=None):
    for t, v in I.snare_roll(t0, t1, v0, v1, _r()):
        b.add("snare", I.snare(v, _r(), dur=0.14, buzz=True), t, 0.06)
    if accent:
        b.add("snare", I.snare(accent * 0.4, _r()), t1 - 0.024, 0.06)
        b.add("snare", I.snare(accent, _r()), t1, 0.06)


def drums_bar(b, t_bar, pat, vel, bd=0.8, steps=range(16), cres=0.0, t_min=-1.0):
    snare_bar(b, t_bar, pat, vel, steps, cres, t_min)
    for beat in (0, 2):
        t = t_bar + beat * Q
        if t >= t_min and beat * 4 in steps:
            b.add("bassdrum", bassdrum(bd * (1.0 if beat == 0 else 0.85), _r()), t, 0.0)


def bass_bar(b, t_bar, bar, vel=0.5, beats=(0, 1, 2, 3)):
    ch = CHB[bar]
    for beat in beats:
        m = ROOT[ch[beat]] + (7 if beat % 2 else 0)        # root on 1/3, fifth on 2/4
        b.add("bassoon", I.brass(F(m), Q * 0.55, vel * (1.0 if beat % 2 == 0 else 0.8), _r(), "soft", scoop=-10), t_bar + beat * Q, -0.08)


def musicbox_theme(b, notes, vel=0.6, bass_bars=None):
    for (t, d, m) in notes:
        b.add("musicbox", I.musicbox(F(m + 12), vel * R.uniform(0.9, 1.05), _r()), t, 0.15)
    for (t_bar, bar) in (bass_bars or []):
        for beat in (0, 2):
            m = ROOT[CHB[bar][beat]] + 24
            b.add("musicbox", I.musicbox(F(m), vel * 0.55, _r(), dur=1.2), t_bar + beat * Q, -0.15)
            b.add("musicbox", I.musicbox(F(m + 7 + 12), vel * 0.3, _r(), dur=0.8), t_bar + (beat + 1) * Q, -0.1)


def crackle(dur, r):
    n = ns(dur)
    out = np.zeros(n)
    hiss = bp(r.standard_normal(n), 1500, 7000, 1) * 0.012 * (0.8 + 0.2 * smooth_noise(n, r, 1.5))
    out += hiss
    k = int(dur * 14)
    for tm in r.uniform(0, dur, k):
        L = ns(0.004)
        a = ns(tm)
        if a + L >= n:
            continue
        out[a:a + L] += hp(r.standard_normal(L), 1200) * np.exp(-np.arange(L) / (SR * 0.0006)) * r.uniform(0.05, 0.35)
    # 33 rpm thump (0.55 Hz) - barely there
    t = np.arange(n) / SR
    out += lp(r.standard_normal(n), 120) * 0.02 * np.exp(-((t % 1.8) / 0.02))
    return fades(out, 0.15, 0.25)


def build():
    b = Band()
    for name, send in [("fife", 0.18), ("fife2", 0.18), ("snare", 0.14), ("bassdrum", 0.12), ("bassoon", 0.12),
                       ("musicbox", 0.3), ("crackle", 0.0), ("cymbal", 0.18), ("pluck", 0.2)]:
        b.track(name, send)

    # ============ HOOK 0 - 3.2: tutti from the first frame; cut by the white flash, button ON the flash
    h = theme(0.0, [1, 2])
    fifes(b, h, 0.75)
    for k, bar in enumerate((1, 2)):
        tb = k * BAR
        drums_bar(b, tb, "march", 0.7, 0.85)
        bass_bar(b, tb, bar, 0.5)
    b.add("bassdrum", bassdrum(0.9, _r()), T.CHEER_STORMED + 0.06, 0.0)       # "stormed" (1.38) lift
    b.add("cymbal", I.cymbal(0.3, _r(), dur=1.4), T.CHEER_STORMED + 0.06, 0.0)
    roll(b, 2.55, T.FLASH_AT, 0.25, 0.7)
    b.gate(list(b.tr), T.FLASH_AT - 0.02, 0.02)
    b.add("snare", I.snare(0.4, _r()), T.FLASH_AT - 0.024, 0.06)
    b.add("snare", I.snare(1.0, _r()), T.FLASH_AT, 0.06)
    b.add("bassdrum", bassdrum(1.0, _r()), T.FLASH_AT, 0.0)
    b.add("fife", I.fife(F(86), 0.32, 0.8, _r()), T.FLASH_AT, 0.18)
    b.add("fife2", I.fife(F(81), 0.32, 0.65, _r()), T.FLASH_AT, -0.22)
    b.add("bassoon", I.brass(F(38), 0.35, 0.6, _r(), "soft"), T.FLASH_AT, -0.08)
    b.cues.append((0.0, "hook: theme bars 1-2, two fifes + snare + bass drum + low reed; bass-drum lift on 'stormed'"))
    b.cues.append((2.55, "snare roll into the white flash"))
    b.cues.append((T.FLASH_AT, "D button (fifes D6/A5, drum accent) exactly on the flash (f96); band cut"))

    # ============ TOWN 3.4 - 5.8 drum-only tap-in, fife enters with the theme at 4.457 so muskets-up (6.6) is a downbeat
    g0 = T.MUSKETS_UP - BAR                     # 4.457 = bar 1, 6.6 = bar 2, 8.743 = bar 3
    for s in range(16):                          # light drum tap-in from 3.5 (ghosts on the grid of g0)
        t = g0 - BAR + s * Q / 4
        if t >= 3.5 and SN["light"][s]:
            b.add("snare", I.snare(0.32 * {1: 0.42, 2: 0.85, 3: 1.0}[SN["light"][s]], _r()), t, 0.06)
    fifes(b, theme(g0, [1]), 0.55, harm=False)
    drums_bar(b, g0, "light", 0.45, 0.5)
    bass_bar(b, g0, 1, 0.35, beats=(0, 2))
    b.cues.append((3.5, "town: light drum tap-in (shot 2, 'Paris, July 14, 1789.')"))
    b.cues.append((g0, "fife 1 alone, theme bar 1, light drum"))

    # ============ MUSKETS: tutti downbeat on 6.6, bar 2-3; the horn cut (8.2) stops the band, comic fife droop
    b.add("cymbal", I.cymbal(0.45, _r()), T.MUSKETS_UP, 0.0)
    b.add("bassdrum", bassdrum(1.0, _r()), T.MUSKETS_UP, 0.0)
    fifes(b, theme(T.MUSKETS_UP, [2, 3]), 0.72)
    for k, bar in enumerate((2, 3)):
        tb = T.MUSKETS_UP + k * BAR
        drums_bar(b, tb, "march", 0.66, 0.85)
        bass_bar(b, tb, bar, 0.5)
    b.gate(list(b.tr), T.HORN_TIP - 0.03, 0.04, t_on=T.HORN_TIP + 0.7)
    # "No powder." -> deflating fife droop under the muskets lowering (8.47), then the bassoon "womp" (after "powder" ends 8.66)
    x = I.fife(F(81), 0.42, 0.55, _r())
    tx = np.arange(len(x)) / SR
    # pitch droop: re-synthesize a sliding fife tone
    f_sl = F(81) * 2 ** (-np.clip((tx - 0.08) / 0.34, 0, 1) * 7 / 12)
    droop = np.sin(phase(f_sl)) * np.interp(tx, [0, 0.02, 0.35, len(x) / SR], [0, 1, 0.8, 0]) * 0.5
    b.add("fife", droop, T.ARMS_DOWN, 0.18)
    b.add("bassoon", I.brass(F(40), 0.3, 0.55, _r(), "soft", scoop=-30, fall=-2), 8.70, -0.08)
    b.cues.append((T.MUSKETS_UP, "TUTTI on muskets-up (f198): cymbal + bass drum downbeat, both fifes, theme bars 2-3"))
    b.cues.append((T.HORN_TIP, "band cut on the horn close-up (f246): empty comic pause"))
    b.cues.append((T.ARMS_DOWN, "fife droops a fifth (muskets lowering, f254); bassoon 'womp' at 8.70 after 'powder.'"))

    # ============ FLASHBACK 1 (sepia) 8.87 - 11.83: music-box solo + crackle, stops dead on the gate slam
    f1 = 8.87
    mb = [n for n in theme(f1, [1, 2]) if n[0] < T.GATE_SLAM - 0.1]
    musicbox_theme(b, mb, 0.6, [(f1, 1), (f1 + BAR, 2)])
    b.gate(["musicbox"], T.GATE_SLAM - 0.01, 0.03, t_on=T.GATE_SLAM + 1.0)
    b.add("crackle", st_(crackle(T.COLOUR1 - f1 + 0.05, _r())), f1, 0.0)
    b.cues.append((f1, "sepia flashback: music-box version of the theme (bars 1-2) + vinyl crackle"))
    b.cues.append((T.GATE_SLAM, "music box stops dead on the gate slam (f355); crackle only to the cut"))

    # ============ COLOUR 12.33: drums back in (grid anchored so the drawbridge slam 15.97 is a downbeat)
    s0 = T.DB_SLAM - BAR                          # 13.827: fife enters; 15.97 slam = downbeat
    drums_bar(b, s0 - BAR, "march", 0.6, 0.8, t_min=T.COLOUR1)
    b.add("bassdrum", bassdrum(0.9, _r()), T.COLOUR1, 0.0)
    fifes(b, theme(s0, [3]), 0.7)
    drums_bar(b, s0, "drive", 0.62, 0.85, steps=range(12))
    bass_bar(b, s0 - BAR, 1, 0.45, beats=(1, 2, 3))
    bass_bar(b, s0, 3, 0.5)
    roll(b, T.CHAIN_RUN[0] - 0.05, T.DB_SLAM, 0.3, 0.85)
    b.add("bassdrum", bassdrum(1.0, _r()), T.DB_SLAM, 0.0)
    b.add("cymbal", I.cymbal(0.55, _r()), T.DB_SLAM, 0.0)
    fifes(b, [n for n in theme(T.DB_SLAM, [5, 6]) if n[0] < T.COURTYARD - 0.12], 0.8)
    for k, bar in enumerate((5,)):
        drums_bar(b, T.DB_SLAM, "march", 0.72, 0.95)
    bass_bar(b, T.DB_SLAM, 5, 0.55)
    b.gate(["fife", "fife2", "snare", "bassdrum", "bassoon", "cymbal"], T.COURTYARD - 0.03, 0.05, t_on=T.COURTYARD + 0.6)
    b.cues.append((T.COLOUR1, "hard cut to colour (f370): drums snap back in, bass-drum hit on the cut"))
    b.cues.append((s0, "siege: fifes theme bar 3, driving snare"))
    b.cues.append((T.CHAIN_RUN[0] - 0.05, "snare roll under the drawbridge chain run"))
    b.cues.append((T.DB_SLAM, "TUTTI on the drawbridge slam (f479): bass drum + cymbal, theme bars 5-6 loud"))
    b.cues.append((T.COURTYARD, "cut to the courtyard (f530): band stops - awkward"))

    # ============ COURTYARD 17.67 - 21.93: awkward tiptoe pizzicato + one bassoon blip
    for k in range(9):
        t = 18.75 + k * Q
        if T.BLIP - 0.2 < t < T.BLIP + 0.3:
            continue
        m = [50, 57, 50, 57, 52, 57, 50, 45, 50][k]
        b.add("pluck", I.pluck(F(m), 0.55, _r(), dur=0.5, bright=0.35), t, -0.1)
    b.add("bassoon", I.brass(F(36), 0.16, 0.6, _r(), "soft", scoop=-60), T.BLIP, -0.05)
    b.add("bassoon", I.brass(F(43), 0.14, 0.5, _r(), "soft", scoop=-40), T.BLIP + 0.18, -0.05)
    b.cues.append((18.75, "courtyard: tiptoe pizzicato on the beat, sparse"))
    b.cues.append((T.BLIP, "silly bassoon blip (two notes, low-high) on the wandering footsteps (f592)"))

    # ============ PARADE 21.93 - 24.13: full march returns, set-down hit, cut into the flashback
    p0 = T.CHEER_BACK
    roll(b, p0 - 0.4, p0, 0.15, 0.6)
    b.add("bassdrum", bassdrum(1.0, _r()), p0, 0.0)
    b.add("cymbal", I.cymbal(0.45, _r()), p0, 0.0)
    fifes(b, [n for n in theme(p0, [7, 8]) if n[0] < T.FLASHBACK2[0] - 0.1], 0.8)
    drums_bar(b, p0, "march", 0.72, 0.95)
    bass_bar(b, p0, 7, 0.55)
    b.add("bassdrum", bassdrum(0.95, _r()), T.SETDOWN, 0.0)
    b.add("snare", I.snare(0.9, _r()), BAR + p0, 0.06)
    b.add("bassdrum", bassdrum(0.9, _r()), BAR + p0, 0.0)
    b.add("bassoon", I.brass(F(38), 0.18, 0.55, _r(), "soft"), BAR + p0, -0.08)
    b.gate(["fife", "fife2", "snare", "bassdrum", "bassoon", "cymbal"], T.FLASHBACK2[0] - 0.02, 0.05, t_on=T.COLOUR2 - 0.6)
    b.cues.append((p0, "march back full on the cheer (f658): theme bars 7-8, roll-in, cymbal"))
    b.cues.append((T.SETDOWN, "bass-drum hit on the barrel set-down (f692)"))

    # ============ FLASHBACK 2 (sepia) 24.13 - 28.8: music box, a little slower and sadder (bars 5-6), crackle
    f2 = T.FLASHBACK2[0] + 0.05
    mb2 = theme(f2, [5, 6]) + [(f2 + 2 * BAR + 0.0, 1.5 * Q, 74)]
    musicbox_theme(b, [n for n in mb2 if n[0] < T.COLOUR2 - 0.3], 0.55, [(f2, 5), (f2 + BAR, 6)])
    b.add("crackle", st_(crackle(T.COLOUR2 - T.FLASHBACK2[0] + 0.05, _r())), T.FLASHBACK2[0], 0.0)
    b.cues.append((f2, "sepia flashback 2 (Sade): music-box theme bars 5-6, crackle"))

    # ============ FINALE 28.8 - 30.0: tutti back to colour, roll, final hit 29.83, ring out
    b.add("bassdrum", bassdrum(1.0, _r()), T.COLOUR2, 0.0)
    b.add("cymbal", I.cymbal(0.5, _r()), T.COLOUR2, 0.0)
    fin = [(T.COLOUR2, Q, 81), (T.COLOUR2 + Q, 0.5 * Q, 79), (T.COLOUR2 + 1.5 * Q, 0.5 * Q, 76)]
    fifes(b, fin, 0.85)
    roll(b, T.COLOUR2 + Q, T.FINAL_HIT, 0.3, 0.9)
    bass_bar(b, T.COLOUR2, 7, 0.55, beats=(0,))
    b.add("bassoon", I.brass(F(45), Q * 0.9, 0.55, _r(), "soft"), T.COLOUR2 + Q, -0.08)
    b.add("snare", I.snare(0.45, _r()), T.FINAL_HIT - 0.024, 0.06)
    b.add("snare", I.snare(1.05, _r()), T.FINAL_HIT, 0.06)
    b.add("bassdrum", bassdrum(1.1, _r()), T.FINAL_HIT, 0.0)
    b.add("cymbal", I.cymbal(0.6, _r()), T.FINAL_HIT, 0.0)
    b.add("fife", I.fife(F(86), 0.2, 0.85, _r(), rel=0.12), T.FINAL_HIT, 0.18)
    b.add("fife2", I.fife(F(78), 0.2, 0.7, _r(), rel=0.12), T.FINAL_HIT, -0.22)
    b.add("bassoon", I.brass(F(38), 0.2, 0.6, _r(), "soft", rel=0.1), T.FINAL_HIT, -0.08)
    b.cues.append((T.COLOUR2, "back to colour (f864): tutti hit + cymbal, fife cadence A-G-E, snare roll"))
    b.cues.append((T.FINAL_HIT, "final D hit (f895): drum + cymbal + fifes, ring-out faded to silence at 30.000"))
    end = np.ones(N)
    a = ns(T.DUR - 0.12)
    end[a:] = np.linspace(1, 0, N - a) ** 1.5
    for k in b.tr:
        b.tr[k] *= end[None, :]
    return b


def st_(x):
    return np.vstack([x, x])


TARGET = {  # relative balance inside the band (LU, each track's integrated loudness over its own render)
    "fife": 0.0, "fife2": -4.5, "snare": -3.5, "bassdrum": -5.0, "bassoon": -7.5, "musicbox": -1.0,
    "crackle": -17.0, "cymbal": -12.0, "pluck": -7.0,
}


def render(b, ref=-20.0):
    hall = make_ir(1.3, 7, pre=0.016, hf=1.5, early=[(0.07, 0.4, -0.4), (0.13, 0.3, 0.5)])
    dry = np.zeros((2, N))
    wet = np.zeros((2, N))
    levels = {}
    for k, x in b.tr.items():
        if not np.any(x):
            continue
        L = integrated(x)
        g = dbg(ref + TARGET.get(k, -6) - L)
        levels[k] = (round(L, 1), round(ref + TARGET.get(k, -6), 1))
        x = x * g
        b.tr[k] = x
        dry += x
        wet += b.send[k] * x
    out = dry + 0.7 * convolve_st(wet.mean(0), hall)
    out = hp(out, 30, 2)
    return out, levels
