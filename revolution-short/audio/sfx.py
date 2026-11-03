# Every sound effect and ambience bed of the Bastille short as a cue list timed to the picture (timeline.py, SHOTPLAN.md
# section 4), rendered into one stereo SFX stem. Level convention (skill standard mix): each EVENT has a "naive" level
# (LU relative to the voice stem, as the event's max momentary loudness) and is placed SFX_DB = -6 dB under it; ambience
# BEDS (integrated loudness) are not reduced. No gore: musket shots are cartoon pops at a distance, nobody is hurt.
import numpy as np
from dsp import (SR, ns, tt, rng, dbg, lp, hp, bp, peq, shelf, pan, st, place, fades, widen, make_ir, convolve_st,
                 momentary_max, integrated, colored, smooth_noise, modal, phase, reson)
import sfx_gen as G
import timeline as T

N = ns(T.DUR)
SFX_DB = -6.0


class Cue:
    def __init__(self, t, name, desc, gen, naive, kind="event", p=0.0, extra=0.0, lpf=None, send=0.12, group=None, cut=None, room="square"):
        self.t, self.name, self.desc, self.gen, self.naive = t, name, desc, gen, naive
        self.kind, self.p, self.extra, self.lpf, self.send, self.cut, self.room = kind, p, extra, lpf, send, cut, room
        self.group = group or name
        self.applied = naive + (SFX_DB if kind == "event" else 0.0) + extra
        self.measured = None


# ================================================================ generators
def _murmur(dur, r, voices, early=False):
    n = ns(dur)
    out = np.zeros((2, n))
    for v in range(voices):
        kind = r.uniform()
        base, scale = ((r.uniform(95, 140), r.uniform(0.95, 1.05)) if kind < 0.45 else
                       (r.uniform(175, 235), r.uniform(1.12, 1.2)) if kind < 0.85 else (r.uniform(260, 330), r.uniform(1.25, 1.35)))
        y = G.babble(dur, r, base, scale, r.uniform(3.6, 4.8), r.uniform(0.55, 0.8), fmax=3400)
        y = lp(y, r.uniform(2200, 3600), 1) * r.uniform(0.3, 1.0)
        out += pan(y, r.uniform(-0.85, 0.85))
    if early:
        for k in range(4):
            h = G.hurrah(r, r.uniform(110, 230), r.uniform(1.0, 1.18))
            place(out, pan(lp(h, 3000, 1) * 0.5, r.uniform(-0.8, 0.8)), r.uniform(0.2, max(0.3, dur - 0.9)))
    return fades(out, 0.2, 0.4)


def _cheer(dur, r, voices=26, env_pts=None, applause=0.6):
    n = ns(dur)
    t = np.arange(n) / SR
    out = np.zeros((2, n))
    for v in range(voices):
        kid = v % 7 == 6
        base = r.uniform(270, 340) if kid else (r.uniform(105, 160) if v % 2 else r.uniform(180, 250))
        scale = 1.3 if kid else (1.0 if v % 2 else 1.15)
        tm = r.uniform(0.0, 0.35)
        while tm < dur - 0.5:
            h = G.hurrah(r, base * r.uniform(0.97, 1.05), scale, kid)
            place(out, pan(lp(h, 4000, 1) * r.uniform(0.35, 1.0), r.uniform(-0.9, 0.9)), tm)
            tm += r.uniform(0.7, 1.3)
    out += _roar(dur, r) * 0.5
    if applause:
        out += G.applause(dur, r, 30) * applause
    pts = env_pts or [(0, 0.0), (0.25, 0.8), (dur * 0.5, 1.0), (dur, 0.6)]
    env = np.interp(t, [p[0] for p in pts], [p[1] for p in pts])
    return fades(out * env[None, :], 0.03, 0.3)


def _roar(dur, r):
    """broadband crowd roar body (many voices blended): formant-coloured noise with slow surges"""
    n = ns(dur)
    x = colored(n, r, 0.4)
    y = reson(x, 650, 1.2) + 0.7 * reson(x, 1150, 1.5) + 0.4 * reson(x, 2500, 2.0) + 0.3 * reson(x, 320, 1.0)
    y = bp(y, 180, 4200, 1)
    y = y / (np.abs(y).max() + 1e-9)
    l = y * (0.8 + 0.25 * smooth_noise(n, r, 1.3))
    rr = np.roll(y, ns(0.011)) * (0.8 + 0.25 * smooth_noise(n, r, 1.1))
    return np.vstack([l, rr])


def _plank_steps(dur, r, rate=7.0, scuff=0.6, plank=True):
    """a loose crowd walking over planks/cobbles: irregular footsteps"""
    out = np.zeros((2, ns(dur)))
    tm = r.uniform(0, 0.1)
    while tm < dur - 0.3:
        s = G.boot(r, 0.6) * 0.6 if plank else G.stroll_step(r, scuff)
        if plank:
            s2 = G.stroll_step(r, scuff) * 0.5
            s = np.pad(s, (0, len(s2) - len(s))) + s2
        place(out, pan(s * r.uniform(0.35, 1.0), r.uniform(-0.8, 0.8)), tm)
        tm += r.exponential(1 / rate)
    return out


def _creak_bed(dur, r, every=0.6):
    out = np.zeros((2, ns(dur)))
    tm = 0.05
    while tm < dur - 0.4:
        c = G.creak(r.uniform(0.25, 0.45), r, r.uniform(70, 110), r.uniform(130, 200), G.TIMBER, rough=0.2, noise=0.05)
        place(out, pan(c * r.uniform(0.4, 1.0), r.uniform(-0.5, 0.5)), tm)
        tm += every * r.uniform(0.6, 1.4)
    return out


def _grains(dur, r):
    """powder trickling: dry fine hiss + sparse grain ticks"""
    n = ns(dur)
    hiss = bp(r.standard_normal(n), 3500, 11000, 2) * 0.12 * (0.7 + 0.3 * smooth_noise(n, r, 6))
    y = hiss.copy()
    for tm in r.uniform(0, dur, int(dur * 60)):
        L = ns(0.003)
        a = ns(tm)
        if a + L < n:
            y[a:a + L] += hp(r.standard_normal(L), 4000) * np.exp(-np.arange(L) / (SR * 0.0005)) * r.uniform(0.05, 0.3)
    return widen(y, r, 7, 0.8)


def _barrel_thump(r, big=1.0):
    """full wooden powder barrel set on a shoulder / ground: hollow low thock"""
    d = 0.5
    t = tt(d)
    body = modal(d, [(r.uniform(95, 125), 1.0, 0.09), (r.uniform(210, 260), 0.7, 0.06), (r.uniform(420, 520), 0.45, 0.035),
                     (r.uniform(800, 1000), 0.2, 0.02)], r)
    knock = bp(r.standard_normal(len(t)), 300, 3000, 1) * np.exp(-t / 0.008) * 0.6
    thud = lp(r.standard_normal(len(t)), 200, 2) * np.exp(-t / 0.03) * 1.2 * big
    return fades((body + knock + thud) * big, 0.0, 0.05)


def _barrel_roll(dur, r, speed=1.0):
    """a barrel rolling on cobbles/planks: low rumble, hoop clicks once per turn, stave knocks"""
    n = ns(dur)
    t = np.arange(n) / SR
    rum = lp(colored(n, r, 1.0), 260, 2) * (0.6 + 0.4 * smooth_noise(n, r, 9)) * 0.9
    y = rum.copy()
    tm = 0.05
    while tm < dur - 0.1:
        k = _barrel_thump(r, 0.25)[: ns(0.2)]
        G._place_mono(y, k * r.uniform(0.4, 0.8), tm)
        G._place_mono(y, G.clink(r, r.uniform(900, 1400), 0.08) * 0.15, tm + 0.01)
        tm += r.uniform(0.17, 0.26) / speed
    env = np.clip(t / 0.08, 0, 1) * np.clip((dur - t) / 0.15, 0, 1)
    return y * env


def _wheels(dur, r):
    """cart wheels on quay cobbles: wooden rumble, cobble bumps, axle creaks, harness jingle"""
    n = ns(dur)
    y = lp(colored(n, r, 1.0), 380, 2) * (0.7 + 0.3 * smooth_noise(n, r, 7)) * 0.8
    tm = 0.0
    while tm < dur - 0.2:
        b = modal(0.18, [(r.uniform(80, 120), 1.0, 0.04), (r.uniform(220, 320), 0.5, 0.02)], r)
        G._place_mono(y, b * r.uniform(0.4, 1.0), tm)
        tm += r.uniform(0.09, 0.16)
    tm = 0.3
    while tm < dur - 0.6:
        G._place_mono(y, G.creak(0.35, r, 140, 220, G.WOOD, rough=0.15) * 0.25, tm)
        tm += r.uniform(0.7, 1.1)
    y += G.rattle(dur, r, 6, heavy=True) * 0.12
    return y


def _water_lap(dur, r, level=1.0):
    n = ns(dur)
    x = bp(colored(n, r, 0.8), 180, 1600, 1) * (0.6 + 0.4 * smooth_noise(n, r, 0.6)) * 0.5
    x += G.bubbles(dur, r, 6, 300, 1600, (0.01, 0.03)) * 0.15
    return x * level


def _bell(r, f0=392.0, dur=3.5):
    modes = [(f0 * 0.5, 0.5, 2.5), (f0, 1.0, 1.8), (f0 * 1.19, 0.6, 1.2), (f0 * 1.5, 0.45, 1.0), (f0 * 2.0, 0.5, 0.8),
             (f0 * 2.52, 0.3, 0.5), (f0 * 3.0, 0.2, 0.4)]
    return fades(modal(dur, modes, r), 0.0005, 0.3)


def _town(dur, r):
    n = ns(dur)
    x = G.breeze(dur, r, 0.8, 0.1, 900)
    x = x + pan(G.bird_chirps(dur, r, 0.5, "sparrow") * 0.08, 0.5) + pan(G.bird_chirps(dur, r, 0.35, "sparrow") * 0.05, -0.6)
    x = x + st(_water_lap(dur, r, 0.6))
    for k, tm in enumerate([0.25, 1.15, 2.05]):            # distant church bell, 3 strokes
        b = lp(_bell(r, 392.0, 1.6), 2500, 1) * 0.12
        place(x, pan(b, 0.55), tm)
    return fades(x, 0.15, 0.3)


def _quiet_square(dur, r):
    n = ns(dur)
    x = G.breeze(dur, r, 0.5, 0.08, 700)
    x = x + pan(G.bird_chirps(dur, r, 0.4, "sparrow") * 0.07, -0.4) + pan(G.bird_chirps(dur, r, 0.25, "blackbird") * 0.05, 0.6)
    return fades(x, 0.3, 0.3)


def _musket_pop(r, close=False):
    """cartoon musket shot: dry 'pok' crack + low boom (+ powder-puff whoomph when close); no ricochets"""
    d = 0.9
    t = tt(d)
    nz = r.standard_normal(len(t))
    crack = bp(nz, 700, 6000 if close else 3500, 2) * np.exp(-t / (0.006 if close else 0.012)) * 1.3
    pok = np.exp(-t / 0.02) * np.sin(phase(r.uniform(320, 420) * (1 + 0.5 * np.exp(-t / 0.004)))) * 0.6
    boom = np.exp(-t / (0.12 if close else 0.22)) * np.sin(phase(r.uniform(55, 75) * (1 + 0.4 * np.exp(-t / 0.02)))) * (1.2 if close else 0.8)
    y = crack + pok + boom
    if close:
        puff = lp(nz, 500, 2) * np.clip(t / 0.03, 0, 1) * np.exp(-t / 0.14) * 0.9
        y += puff
    else:
        y = lp(y, 2600, 2)
    return fades(y, 0.0, 0.1)


def _siege(dur, r):
    """crowd roar under the towers + distant pops every 0.3-0.5 s"""
    x = _roar(dur, r) * 0.9
    tm = 0.1
    while tm < dur - 0.2:
        p = _musket_pop(r, False) * r.uniform(0.25, 0.5)
        place(x, pan(p, r.uniform(-0.7, 0.7)), tm)
        tm += r.uniform(0.3, 0.5)
    for k in range(5):
        h = G.hurrah(r, r.uniform(110, 230), r.uniform(1.0, 1.18))
        place(x, pan(lp(h, 3200, 1) * 0.4, r.uniform(-0.8, 0.8)), r.uniform(0.0, dur - 0.8))
    return fades(x, 0.1, 0.25)


def _chain_run(r, dur=0.37):
    """drawbridge chain running out: dense heavy rattle + ratchet pawl clicks accelerating + windlass creak"""
    n = ns(dur + 0.25)
    t = np.arange(n) / SR
    env = np.interp(t, [0, 0.05, dur, dur + 0.25], [0.4, 0.9, 1.0, 0.0])
    y = G.rattle(dur + 0.25, r, 140, env, heavy=True)
    tm, gap = 0.0, 0.06
    while tm < dur:
        c = modal(0.06, [(r.uniform(1300, 1700), 1.0, 0.01), (r.uniform(2900, 3400), 0.5, 0.006)], r)
        G._place_mono(y, c * 0.7, tm)
        tm += gap
        gap = max(0.022, gap * 0.85)
    G._place_mono(y, G.creak(dur, r, 60, 150, G.TIMBER, rough=0.25) * 0.5, 0.0)
    return y


def _slam(r):
    """drawbridge deck slams down on the stone: huge timber boom, chain jolt, dust whoomph"""
    d = 2.2
    t = tt(d)
    boom = np.exp(-t / 0.35) * np.sin(phase(42 * (1 + 0.5 * np.exp(-t / 0.03)))) * 2.0
    timber = modal(d, [(70, 1.0, 0.25), (140, 0.8, 0.18), (260, 0.6, 0.12), (450, 0.4, 0.07), (800, 0.25, 0.04)], r)
    nz = r.standard_normal(len(t))
    hit = bp(nz, 200, 4000, 1) * np.exp(-t / 0.015) * 1.5
    dust = lp(nz, 900, 2) * np.clip(t / 0.06, 0, 1) * np.exp(-t / 0.4) * 0.5
    y = boom + timber * 1.3 + hit + dust
    G._place_mono(y, G.rattle(0.6, r, 60, np.exp(-np.linspace(0, 4, ns(0.6))), heavy=True) * 0.5, 0.01)
    return widen(fades(y, 0.0, 0.3), r, 12, 0.6)


def _gate_slam(r):
    d = 2.0
    t = tt(d)
    boom = np.exp(-t / 0.25) * np.sin(phase(55 * (1 + 0.4 * np.exp(-t / 0.02)))) * 1.6
    doors = modal(d, [(90, 1.0, 0.2), (180, 0.7, 0.14), (330, 0.5, 0.08), (610, 0.3, 0.05)], r)
    nz = r.standard_normal(len(t))
    hit = bp(nz, 250, 4500, 1) * np.exp(-t / 0.012) * 1.3
    y = boom + doors * 1.2 + hit
    bolt = modal(0.5, [(620, 1.0, 0.08), (1460, 0.7, 0.05), (2650, 0.4, 0.03)], r) + bp(r.standard_normal(ns(0.5)), 1000, 6000, 1) * np.exp(-tt(0.5) / 0.01) * 0.5
    G._place_mono(y, bolt * 0.9, 0.38)
    G._place_mono(y, bolt * 0.6, 0.48)
    return fades(y, 0.0, 0.3)


def _swish(r, dur=0.35, lo=600, hi=3500):
    """cloth swish"""
    n = ns(dur)
    t = np.arange(n) / SR
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return bp(r.standard_normal(n), lo, hi, 1) * env * (0.7 + 0.3 * smooth_noise(n, r, 30))


def _crowd_swish(r):
    out = np.zeros((2, ns(0.7)))
    for k in range(16):
        place(out, pan(_swish(r, r.uniform(0.18, 0.35)) * r.uniform(0.3, 1.0), r.uniform(-0.9, 0.9)), r.uniform(0, 0.2))
    return out


def _coins(r, n=12):
    out = np.zeros(ns(1.0))
    tm = 0.0
    for k in range(n):
        c = G.clink(r, r.uniform(3200, 5200), 0.15, 1.2) * (0.9 ** k)
        G._place_mono(out, c, tm)
        tm += 0.09 * (0.88 ** k) + 0.015
    return out


def _ohh(r, voices=14, dur=0.6):
    """disappointed crowd 'ohhh' (descending)"""
    n = ns(dur)
    t = np.arange(n) / SR
    out = np.zeros((2, n))
    for v in range(voices):
        base = r.uniform(110, 150) if v % 2 else r.uniform(190, 240)
        f0 = base * np.interp(t, [0, dur * 0.3, dur], [1.15, 1.05, 0.78]) * r.uniform(0.97, 1.03)
        forms = np.tile(np.array(G.VOW["o"], float), (n, 1))
        amp = np.clip(t / 0.06, 0, 1) * np.clip((dur - t) / 0.2, 0, 1)
        y = G.vox(f0, forms, amp, r, 1.0 if v % 2 else 1.15, breath=0.2)
        place(out, pan(lp(y, 3500, 1) * r.uniform(0.4, 1.0), r.uniform(-0.8, 0.8)), r.uniform(0, 0.06))
    return out


def _gasp(r, voices=6):
    out = np.zeros((2, ns(0.5)))
    for v in range(voices):
        d = r.uniform(0.18, 0.3)
        n = ns(d)
        t = np.arange(n) / SR
        y = bp(r.standard_normal(n), r.uniform(700, 1100), r.uniform(2500, 4000), 1) * np.clip(t / 0.03, 0, 1) * np.clip((d - t) / 0.08, 0, 1)
        place(out, pan(y * r.uniform(0.4, 1.0), r.uniform(-0.7, 0.7)), r.uniform(0, 0.08))
    return out


def _shouting(dur, r):
    """non-verbal muffled yelling from a high barred window: one voice, babble, high pitch, lowpassed, stony echo"""
    y = G.babble(dur, r, 175, 1.05, 4.5, 0.85, fmax=3000) * 1.0
    y = lp(y, 1300, 2) * (0.7 + 0.3 * smooth_noise(ns(dur), r, 2))
    t = tt(dur)
    y *= np.clip(t / 0.15, 0, 1) * np.clip((dur - t) / 0.3, 0, 1)
    return y


def _basket(r):
    """basket drops: wicker crunch + soft thump, a hat hops (two light taps)"""
    d = 0.8
    t = tt(d)
    nz = r.standard_normal(len(t))
    crunch = bp(nz, 1500, 7000, 1) * np.exp(-t / 0.04) * 0.6
    thump = lp(nz, 250, 2) * np.exp(-t / 0.03) * 1.2
    y = crunch + thump
    for tm, a in [(0.22, 0.5), (0.36, 0.3)]:
        tap = modal(0.15, [(r.uniform(300, 420), 1.0, 0.02), (r.uniform(800, 1100), 0.4, 0.01)], r) * a
        G._place_mono(y, tap, tm)
    return y


def _hup(r, voices=16):
    out = np.zeros((2, ns(1.0)))
    for v in range(voices):
        base = r.uniform(105, 160) if v % 3 else r.uniform(180, 240)
        h = G.oof(r, "oof", base=base, scale=r.uniform(0.95, 1.1))
        place(out, pan(h * r.uniform(0.4, 1.0), r.uniform(-0.8, 0.8)), abs(r.normal(0, 0.03)))
    return out


def _flash(r):
    dur = 0.75
    y = G.whoosh(dur, r, 0.33, 500, 4200, 0.9, 0.09, 0.4)
    t = tt(dur)
    shim = sum(np.sin(2 * np.pi * f * t) * r.uniform(0.3, 0.6) for f in (2093, 2637, 3136, 4186)) * np.clip(t / 0.33, 0, 1) ** 2 * np.exp(-np.maximum(t - 0.33, 0) / 0.08) * 0.08
    boom = np.where(t > 0.33, np.exp(-(t - 0.33) / 0.12) * np.sin(2 * np.pi * 62 * (t - 0.33)), 0) * 0.8
    return widen(y + shim + boom, r, 12, 0.9), 0.33


def _cut(fn, fin, fout):
    def g():
        x, a = fn()
        return fades(x, fin, fout), a
    return g


# ================================================================ cue list
def cues():
    C = []
    R = rng(1789)
    rr = lambda: rng(int(R.integers(1 << 30)))
    add = C.append
    FL = T.FLASH_AT + 0.03                     # the hook ends on the white flash

    # ------------------------------------------------ SHOT 1 hook (golden square, drawbridge down) 0 - 3.2
    add(Cue(0.0, "cheer_bed", "crowd cheering on the golden square (column + 20 extras)", _cut(lambda: (_cheer(3.35, rng(1), 22), 0.0), 0.0, 0.05),
            -18, "bed", lpf=5000, send=0.2, cut=FL))
    add(Cue(0.0, "plank_creak", "drawbridge planks creaking under the barrel column", lambda: (_creak_bed(3.3, rng(2), 0.45), 0.0), -28, "bed",
            send=0.12, cut=FL))
    add(Cue(0.0, "plank_steps", "loose column footsteps on the drawbridge planks", lambda: (_plank_steps(3.3, rng(3), 8.0), 0.0), -24, "bed",
            send=0.12, cut=FL))
    add(Cue(0.0, "grain_hiss", "faint gunpowder trickling from the barrel bungs", lambda: (_grains(3.3, rng(4)), 0.0), -34, "bed", send=0.0, cut=FL))
    add(Cue(T.CHEER_STORMED, "cheer_swell", "cheer swell, barrels hoisted ('stormed' 1.38)",
            lambda: (_cheer(1.9, rng(5), 18, [(0, 0), (0.12, 1.0), (1.0, 0.8), (1.9, 0.4)], 0.4), 0.0), -6, lpf=5500, send=0.2, cut=FL))
    for k, tm in enumerate([2.0, 2.27, 2.52, 2.78, 3.0]):
        add(Cue(tm, "barrel_thump", "barrel bumped on a shoulder", (lambda r=rr(): (_barrel_thump(r, 0.8), 0.0)), -12, p=[-0.3, 0.25, -0.1, 0.4, 0.0][k],
                send=0.12, group="barrel_thumps", cut=FL))
    add(Cue(T.FLASH_AT, "flash_whoosh", "reverse swell + shimmer into the white flash (f96) + soft low whoomp", lambda: _flash(rng(96)), -6, send=0.2))

    # ------------------------------------------------ SHOT 2 town 3.27 - 5.8
    add(Cue(3.27, "amb_town", "Paris morning: breeze, sparrows, river lapping, three distant church-bell strokes", lambda: (_town(2.75, rng(10)), 0.0),
            -24, "bed", send=0.0))
    add(Cue(3.30, "town_cheer", "small cheer from the townsfolk waving (f99-130)",
            lambda: (_cheer(1.1, rng(11), 10, [(0, 0), (0.15, 1), (0.6, 0.8), (1.1, 0)], 0.5), 0.0), -14, lpf=3500, send=0.35))
    add(Cue(T.fr(119), "whoosh_crane", "long soft crane whoosh toward the eight towers", lambda: (G.whoosh(1.4, rng(12), 0.6, 250, 1400, 0.9, 0.35, 0.1), 0.0),
            -14, send=0.1))

    # ------------------------------------------------ SHOT 3 muskets (Invalides) 5.8 - 8.87
    add(Cue(5.75, "murmur_esplanade", "crowd of 70 murmuring on the esplanade", lambda: (_murmur(2.5, rng(20), 22), 0.0), -20, "bed", lpf=3600, send=0.3))
    add(Cue(T.MUSKETS_UP - 0.03, "musket_rattle", "70 muskets lifted overhead: wood and metal rattle in a ripple",
            lambda: (_musket_lift(rng(21)), 0.0), -8, send=0.2))
    add(Cue(T.MUSKETS_UP, "big_cheer", "big cheer as the muskets go up",
            lambda: (_cheer(1.6, rng(22), 26, [(0, 0), (0.1, 1), (1.0, 0.85), (1.6, 0.0)], 0.3), 0.0), -6, lpf=5000, send=0.3))
    add(Cue(T.fr(204), "whoosh_crane", "crane up over the forest of muskets", lambda: (G.whoosh(1.0, rng(23), 0.5, 300, 1800, 0.8, 0.25, 0.12), 0.0),
            -14, send=0.1))
    add(Cue(T.HORN_TIP, "murmur_low", "murmur drops, held breath (behind the horn close-up)", lambda: (_murmur(0.7, rng(24), 12), 0.0), -30, "bed",
            lpf=2500, send=0.3))
    add(Cue(T.HORN_TIP, "horn_creak", "leather strap creak: horn flipped upside down", lambda: (G.creak(0.22, rng(25), 160, 260, G.WOOD, rough=0.25) * 0.6, 0.0),
            -16, p=0.15, send=0.05))
    for k, tm in enumerate([T.HORN_PUFF, T.HORN_PUFF + 0.12]):
        add(Cue(tm, "horn_tap", f"hollow tap on the empty powder horn {k + 1}/2",
                (lambda r=rr(): (modal(0.25, [(r.uniform(520, 600), 1.0, 0.05), (r.uniform(1300, 1500), 0.5, 0.03), (2600, 0.2, 0.015)], r), 0.0)),
                -12, p=0.15, send=0.05, group="horn_tap"))
    add(Cue(T.HORN_PUFF + 0.27, "grain_tick", "one single grain ticks out - then the comic empty pause", lambda: (G.clink(rng(26), 5200, 0.06, 0.6) * 0.5, 0.0),
            -22, p=0.15, send=0.05))
    add(Cue(T.ARMS_DOWN, "musket_lower", "muskets lowering in a wave: wood clunks", lambda: (_musket_lower(rng(27)), 0.0), -12, send=0.2))
    add(Cue(T.ARMS_DOWN + 0.05, "ohh", "disappointed crowd 'ohhh' (non-verbal)", lambda: (_ohh(rng(28)), 0.0), -10, lpf=3500, send=0.3))

    # ------------------------------------------------ SHOT 4 flashback (sepia): the powder cart 8.87 - 12.33
    add(Cue(8.87, "cart_wheels", "flashback: cart wheels on the quay cobbles, axle creaks, harness jingle", lambda: (st(_wheels(2.0, rng(30))), 0.0),
            -22, "bed", lpf=6000, send=0.15))
    add(Cue(8.87, "cart_steps", "carters walking beside the cart", lambda: (_plank_steps(2.0, rng(31), 3.0, plank=False), 0.0), -30, "bed", send=0.1))
    add(Cue(8.87, "river_lap", "river lapping along the quay", lambda: (fades(st(_water_lap(2.0, rng(32))), 0.3, 0.3), 0.0), -32, "bed", send=0.0))
    add(Cue(T.BARREL_KNOCK, "barrel_knock", "barrels knock together on the cart", lambda: (_barrel_thump(rng(33), 0.7) + np.pad(_barrel_thump(rng(34), 0.5), (ns(0.09), 0))[: ns(0.5)], 0.0),
            -10, p=-0.2, send=0.15))
    add(Cue(10.45, "barrel_roll", "powder barrels rolled off the cart into the fortress", lambda: (_barrel_roll(1.2, rng(35)), 0.0), -14, p=0.25, send=0.25))
    add(Cue(10.83, "gate_amb", "inside the gate: stone echo ambience, a few steps", lambda: (_plank_steps(1.5, rng(36), 2.0, plank=False) * 0.6, 0.0),
            -30, "bed", send=0.6, room="stone"))
    add(Cue(T.GATE_SLAM, "gate_slam", "HEAVY GATE DOORS SLAM + bolt clank (f355)", lambda: (_gate_slam(rng(37)), 0.0), -4, send=0.35, room="stone"))

    # ------------------------------------------------ SHOT 5 back to colour, heads turn 12.33 - 13.47
    add(Cue(T.COLOUR1, "murmur_back", "crowd murmur back in colour (Invalides)", lambda: (_murmur(1.3, rng(40), 20), 0.0), -20, "bed", lpf=3600, send=0.3))
    add(Cue(T.fr(372), "heads_swish", "heads turn: collective clothing swish", lambda: (_crowd_swish(rng(41)), 0.0), -12, send=0.15))
    add(Cue(T.WHIP, "whip_whoosh", "whip-pan whoosh", lambda: (G.whoosh(0.45, rng(42), 0.12, 400, 3200, 0.7, 0.12, 0.2), 0.12), -9, send=0.1))

    # ------------------------------------------------ SHOT 6 siege 13.47 - 14.87
    add(Cue(13.45, "siege_bed", "siege: crowd roar + distant cartoon musket pops from the towers every 0.3-0.5 s", lambda: (_siege(1.6, rng(50)), 0.0),
            -16, "bed", send=0.3))
    for k, tm in enumerate([13.50, 13.77]):
        add(Cue(tm, "musket_pop", "crowd musket pop (mid distance)", (lambda r=rr(): (_musket_pop(r, False), 0.0)), -12, p=[-0.4, 0.35][k], send=0.35,
                group="musket_pops"))
    for k, tm in enumerate([14.20, 14.37, 14.53]):
        add(Cue(tm, "musket_pop_close", "close musket pop + powder-puff whoomph (cartoon, nobody hit)", (lambda r=rr(): (_musket_pop(r, True), 0.0)),
                -8, p=[0.3, -0.2, 0.1][k], send=0.25, group="musket_pops"))

    # ------------------------------------------------ SHOT 7 surrender 14.87 - 17.67
    add(Cue(14.85, "tower_wind", "wind on the tower top (roar fades under it)", lambda: (fades(_as_st(G.breeze(1.25, rng(60), 1.2, 0.25, 1100)), 0.2, 0.15), 0.0),
            -26, "bed", send=0.0))
    add(Cue(T.fr(457), "cloth_flutter", "white cloth flutters", lambda: (G.flag_flutter(0.7, rng(61)) * np.interp(tt(0.7), [0, 0.1, 0.5, 0.7], [0, 1, 1, 0]), 0.0),
            -14, p=0.2, send=0.1))
    add(Cue(T.CHAIN_RUN[0], "chain_run", "DRAWBRIDGE CHAIN RUN: heavy ratchet rattle accelerating (f468-479)", lambda: (_chain_run(rng(62)), 0.0),
            -5, p=-0.2, send=0.2))
    add(Cue(T.DB_SLAM, "drawbridge_slam", "DRAWBRIDGE SLAMS DOWN + dust whoomph (f479)", lambda: (_slam(rng(63)), 0.0), 0, send=0.3))
    add(Cue(T.SURGE, "surge_roar", "crowd surge roar", lambda: (_cheer(1.7, rng(64), 26, [(0, 0), (0.15, 1.0), (1.2, 1.0), (1.7, 0.5)], 0.0), 0.0),
            -8, lpf=5500, send=0.3))
    add(Cue(T.SURGE + 0.05, "running_feet", "running feet over the drawbridge", lambda: (_plank_steps(1.55, rng(65), 16.0), 0.0), -18, "bed", send=0.2))
    add(Cue(T.fr(492), "arch_rush", "inside the gate: the crowd rushes past the lens left and right (stone arch)",
            lambda: (_rush(rng(66), 1.1), 0.0), -8, send=0.45, room="stone"))
    add(Cue(T.fr(514), "caps_cheer", "caps thrown: whoosh + cheer peak", lambda: (_caps(rng(67)), 0.0), -6, lpf=6000, send=0.45, room="stone"))

    # ------------------------------------------------ SHOT 8 the seven (courtyard) 17.67 - 21.93
    add(Cue(T.COURTYARD, "awkward_murmur", "courtyard: the roar drops to an awkward murmur, then hush (18.33)",
            lambda: (_murmur(0.85, rng(70), 14) * np.interp(tt(0.85), [0, 0.5, 0.85], [1, 0.8, 0])[None, :], 0.0), -20, "bed", lpf=3000, send=0.4,
            room="stone"))
    add(Cue(T.HUSH[0], "shuffle", "hush: shuffling feet on the courtyard stones", lambda: (_plank_steps(0.6, rng(71), 14.0, plank=False) * 0.6, 0.0),
            -16, send=0.35, room="stone"))
    add(Cue(T.HUSH[0], "court_air", "empty courtyard air, soft stone room tone", lambda: (fades(_as_st(G.breeze(3.6, rng(72), 0.4, 0.05, 600)), 0.3, 0.3), 0.0),
            -36, "bed", send=0.0))
    add(Cue(T.COINS[0], "coins", "a forger's coins tinkle out: 12 small bounces", lambda: (_coins(rng(73)), 0.0), -12, p=0.2, send=0.3, room="stone"))
    for k, tm in enumerate([T.BLIP, T.BLIP + 0.3]):
        add(Cue(tm, "wander_step", f"a 'madman' wanders: footstep {k + 1}/2", (lambda r=rr(): (G.stroll_step(r, 0.8), 0.0)), -16, p=-0.25 + 0.2 * k,
                send=0.3, group="wander", room="stone"))
    for k, tm in enumerate([20.33, 20.6, 20.85]):
        add(Cue(tm, "cuff_tug", "fabric tug at a cuff", (lambda r=rr(): (_swish(r, 0.15, 900, 4500), 0.0)), -18, p=0.1, send=0.2, group="cuff",
                room="stone"))
    add(Cue(T.fr(640), "portrait_tap", "small wood tap (portrait)", lambda: (modal(0.2, [(640, 1.0, 0.03), (1500, 0.5, 0.015)], rng(74)), 0.0),
            -16, send=0.25, room="stone"))

    # ------------------------------------------------ SHOT 9 parade, back to the barrels 21.93 - 24.13
    add(Cue(T.CHEER_BACK, "cheer_back", "crowd cheer back up on the square", lambda: (_cheer(2.25, rng(80), 24, [(0, 0), (0.2, 1), (1.6, 0.9), (2.25, 0.5)], 0.3), 0.0),
            -16, "bed", lpf=5000, send=0.25, cut=T.FLASHBACK2[0] + 0.02))
    add(Cue(T.CHEER_BACK, "march_steps", "brisk march of the barrel carriers", lambda: (_plank_steps(2.2, rng(81), 9.0, plank=False), 0.0), -24, "bed",
            send=0.15, cut=T.FLASHBACK2[0] + 0.02))
    add(Cue(T.HUP - 0.02, "hup", "'hup!' as the barrels are hoisted (non-verbal grunt) + cheer", lambda: (_hup(rng(82)), 0.0), -8, lpf=4500, send=0.25))
    for k in range(7):
        tm = T.SETDOWN + k * 0.05 + (0.01 if k % 2 else 0)
        add(Cue(tm, "setdown", f"barrel set-down thud {k + 1}/7", (lambda r=rr(): (_barrel_thump(r, 1.0), 0.0)), -10 - k * 0.5, p=-0.6 + 0.2 * k,
                send=0.15, group="setdown"))
    for k, tm in enumerate([23.25, 23.55, 23.82, 24.05]):
        add(Cue(tm, "chain_thump", "barrel swung down the human chain: hollow thump", (lambda r=rr(): (_barrel_thump(r, 0.7), 0.0)), -14,
                p=0.5 - 0.3 * k, send=0.15, group="chain_thumps", cut=T.FLASHBACK2[0] + 0.02))
    add(Cue(23.2, "barrel_roll2", "a barrel rolled across the cobbles", lambda: (_barrel_roll(0.9, rng(83), 1.2), 0.0), -14, p=0.35, send=0.2,
            cut=T.FLASHBACK2[0] + 0.02))
    add(Cue(T.fr(703), "whoosh_cam", "camera whoosh", lambda: (G.whoosh(0.5, rng(84), 0.12, 350, 2600, 0.8, 0.14, 0.15), 0.12), -12, send=0.1))

    # ------------------------------------------------ SHOT 10 flashback (sepia): Sade 24.13 - 28.8
    add(Cue(T.FLASHBACK2[0], "quiet_square", "flashback: quiet square, birds", lambda: (_quiet_square(4.7, rng(90)), 0.0), -30, "bed", send=0.0))
    add(Cue(25.77, "shouting", "muffled non-verbal yelling from the high barred window (stone echo)", lambda: (_shouting(2.13, rng(91)), 0.0),
            -14, p=-0.35, lpf=1600, send=0.6, room="stone"))
    add(Cue(T.fr(782), "gasp", "passers-by gasp", lambda: (_gasp(rng(92)), 0.0), -14, p=0.2, send=0.15))
    add(Cue(T.fr(824), "basket_drop", "basket drops, a hat hops", lambda: (_basket(rng(93)), 0.0), -10, p=0.3, send=0.15))
    add(Cue(28.0, "guard_steps", "guards' footsteps on the drawbridge planks", lambda: (_guard_steps(rng(94)), 0.0), -14, send=0.2))

    # ------------------------------------------------ SHOT 11 back to colour 28.8 - 30.0
    add(Cue(T.COLOUR2, "final_roar", "huge crowd roar, back to colour", lambda: (_cheer(1.2, rng(100), 30, [(0, 0), (0.08, 1.0), (0.9, 1.0), (1.2, 0.7)], 0.5), 0.0),
            -4, lpf=6000, send=0.3))
    for k, tm in enumerate([28.85, 29.12, 29.38, 29.62]):
        add(Cue(tm, "final_thump", "barrel thumps on shoulders", (lambda r=rr(): (_barrel_thump(r, 0.8), 0.0)), -12, p=[-0.5, 0.4, -0.2, 0.2][k],
                send=0.15, group="final_thumps"))
    add(Cue(T.COLOUR2, "final_steps", "marching carriers", lambda: (_plank_steps(1.15, rng(101), 9.0, plank=False), 0.0), -22, "bed", send=0.15))
    return C


def _as_st(x):
    return x if np.ndim(x) == 2 else st(x)


def _musket_lift(r):
    out = np.zeros((2, ns(0.8)))
    for k in range(40):
        tm = abs(r.normal(0.0, 0.07)) + abs(r.uniform(-1, 1)) * 0.2          # centre outward over 6 f
        knock = modal(0.15, [(r.uniform(300, 520), 1.0, 0.02), (r.uniform(900, 1500), 0.5, 0.01)], r)
        clk = G.clink(r, r.uniform(1800, 3500), 0.08) * 0.4
        place(out, pan(knock * r.uniform(0.3, 1.0), r.uniform(-0.9, 0.9)), tm)
        place(out, pan(clk, r.uniform(-0.9, 0.9)), tm)
    return out


def _musket_lower(r):
    out = np.zeros((2, ns(0.8)))
    for k in range(24):
        tm = (k / 24) * 0.45 + abs(r.normal(0, 0.02))
        knock = modal(0.15, [(r.uniform(220, 380), 1.0, 0.025), (r.uniform(700, 1100), 0.4, 0.012)], r)
        place(out, pan(knock * r.uniform(0.3, 0.9), -0.9 + 1.8 * (k / 24) + r.normal(0, 0.15)), tm)
    return out


def _rush(r, dur):
    out = np.zeros((2, ns(dur + 0.5)))
    for k in range(9):
        w = G.whoosh(0.45, r, 0.18, 300, 1800, 0.8, 0.12, 0.1) * r.uniform(0.5, 1.0)
        place(out, pan(w, (-1) ** k * r.uniform(0.5, 0.95)), k * dur / 9 + r.uniform(0, 0.05))
    out += _plank_steps(dur + 0.5, r, 18.0, plank=False) * 0.7
    out += _roar(dur + 0.5, r) * 0.25
    return fades(out, 0.03, 0.2)


def _caps(r):
    out = np.zeros((2, ns(1.2)))
    for k in range(6):
        place(out, pan(G.whoosh(0.3, r, 0.08, 500, 3000, 0.7, 0.08, 0.2) * 0.6, r.uniform(-0.8, 0.8)), r.uniform(0, 0.12))
    out += _cheer(1.2, r, 22, [(0, 0.3), (0.1, 1.0), (0.8, 0.9), (1.2, 0.0)], 0.4)
    return out


def _guard_steps(r):
    out = np.zeros((2, ns(1.0)))
    for k in range(8):
        tm = k * 0.1 + (0.04 if k % 2 else 0) + r.normal(0, 0.01)
        s = G.boot(r, 0.8) * (0.7 + 0.3 * (k % 2))
        place(out, pan(s, -0.2 + 0.4 * (k % 2)), max(0, tm))
    return out


# ================================================================ render
def render(v_ref, on_event=None):
    C = cues()
    out = np.zeros((2, N))
    sends = {"square": np.zeros(N), "stone": np.zeros(N)}
    for c in C:
        x, anchor = c.gen()
        x = np.asarray(x, float)
        x = pan(x, c.p) if x.ndim == 1 else x
        if c.cut is not None:
            k = ns(c.cut - (c.t - anchor))
            if 0 < k < x.shape[1]:
                x = fades(x[:, :k], 0.0, 0.02)
        tgt = v_ref + c.applied
        cur = momentary_max(x) if c.kind == "event" else integrated(x)
        if np.isfinite(cur):
            x = x * dbg(tgt - cur)
        if c.lpf:
            x = lp(x, c.lpf, 1)
        c.measured = momentary_max(x) - v_ref if c.kind == "event" else integrated(x) - v_ref
        t0 = c.t - anchor
        place(out, x, t0)
        if c.send > 0:
            G._place_mono(sends[c.room], c.send * x.mean(0), t0)
    square = make_ir(1.0, 77, pre=0.012, hf=1.6, early=[(0.08, 0.4, -0.5), (0.15, 0.3, 0.6)])
    stone = make_ir(1.8, 78, pre=0.02, hf=1.2, early=[(0.05, 0.55, -0.4), (0.09, 0.45, 0.5), (0.16, 0.35, -0.2)])
    out += 0.5 * convolve_st(sends["square"], square) + 0.6 * convolve_st(sends["stone"], stone)
    out = hp(out, 25, 2)
    end = ns(T.DUR - 0.1)
    out[:, end:] *= np.linspace(1, 0, N - end)[None, :] ** 2
    return out, C
