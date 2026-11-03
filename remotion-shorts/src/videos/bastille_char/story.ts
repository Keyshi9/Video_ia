// Timeline of the Bastille short (SHOTPLAN.md v2): shots timed to the guide words (public/bastille/words.json),
// story cues, world locations, fortress state and the camera grammar from the skill: continuous slow push-ins;
// symmetric smootherstep glides 18-40 f; big reframes are hard cuts; impacts are 7-frame flip kicks; no hand-held float.
// Every visual reaction lands 0-3 f before its word (LEAD = 2 f).
export const FPS = 30;
export const TOTAL = 900;
export const D0 = 6.0; // bank top / ground height (m)
export const LEAD = 2 / 30;
export type V3 = [number, number, number];

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));
export const smooth = (x: number) => { const u = clamp01(x); return u * u * (3 - 2 * u); };
export const easeOut = (u: number) => 1 - (1 - clamp01(u)) ** 4;

// ---------------- story cues (FRAMES; cast/world schedule from these, never from literal numbers) ----------------
export const CUE = {
  STORMED: 39, TOWN_CHEER: [99, 130], MUSKETS_UP: 198, HORN_TIP: 246, HORN_PUFF: 250, ARMS_DOWN: [254, 268], DOORS: [349, 355],
  HEADS_TURN: [372, 376], IDEA: 382, POPS: [405, 413, 426, 431, 436], CLOTH_UP: 457, DRAW: [468, 479], SURGE: 483, CAPS: 514,
  SEVEN_OUT: [530, 555], COINS: 571, MADMEN: 592, CUFFS: [610, 630], PORTRAIT: 640, HOIST: 669, SETDOWN: 692, CHAIN: 690,
  SADE_BLINK: 752, SHOUT: 773, STARTLE: 782, MASSACRE: 824, WALKOUT: [840, 864],
} as const;

// ---------------- world points (metres, y up; river along x between z -30..30; near bank z < 0 = Bastille side) ----------------
export const LOC = {
  BRIDGE: [0, D0, 0] as V3, BRIDGE_HALF_W: 4.6,
  SQUARE: [0, D0, -72] as V3, SQUARE_BOX: [-46, -92, 46, -50], // x0, z0, x1, z1
  GATE: [0, D0, -100] as V3, GATE_W: 4.4, GATE_H: 6.5, WALL_FRONT_Z: -100, WALL_BACK_Z: -150, WALL_HALF_X: 32, WALL_T: 3, WALL_TOP: D0 + 22,
  TOWERS: [[-30, -101.5], [-10, -101.5], [10, -101.5], [30, -101.5], [-30, -148.5], [-10, -148.5], [10, -148.5], [30, -148.5]] as [number, number][],
  TOWER_R: 5.5, TOWER_TOP: D0 + 26,
  DRAW_HINGE: [0, D0, -100] as V3, DRAW_LEN: 8, DRAW_W: 4.8, MOAT: [-38, -100, 38, -92], MOAT_DEPTH: 4,
  COURT: [0, D0, -125] as V3, COURT_BOX: [-27, -147, 27, -103], DOOR: [0, D0, -147] as V3,
  SADE_WIN: [-30, D0 + 13.2, -96.0] as V3, SADE_FLOOR: D0 + 11.9, WINDOW_BOUNCE: [-30, D0 + 12.0, -94.6] as V3,
  GOVERNOR: [10, D0 + 26, -98.4] as V3,
  HOOK_PRISONERS: [-4.5, D0, -86.2] as V3, FORGERS_Z: -136.5, COUNT: [3.6, D0, -136.6] as V3,
  PARADE_C: [0, D0, -72] as V3, PARADE_R: 9, PARADE_W: 0.008 /* rad per frame */, BARREL_PILE: [6, D0, -84] as V3,
  CART_QUAY_Z: -33.6, CART_X0: 5.5, CART_V: 0.05 /* m per frame */,
  INVALIDES_FACADE_Z: 96, DOME: [0, D0, 108] as V3, ESPLANADE: [0, D0, 75] as V3, ESPLANADE_BOX: [-46, 37, 46, 92], HORN_MAN: [0.4, D0, 70] as V3,
} as const;

/** the one powder barrel used everywhere (world pile/cart/barrels3 FG and char carried barrels) */
export const BARREL = { h: 0.7, rMid: 0.29, rEnd: 0.24, hoops: 2, bungR: 0.03, trickle: { grains: 10, fallS: 0.5, color: "#2b2533" } } as const;

// ---------------- shots ----------------
export type Light = "day" | "golden";
export type Scene = "hook" | "town" | "muskets" | "cart" | "turn" | "siege" | "surrender" | "seven" | "parade" | "sade" | "window";
/** degrees, camera-relative like LIGHTS; lerped f0..f1 then frozen (optional, lowest priority) */
export type SunSweep = { f0: number; f1: number; az0: number; az1: number; el0: number; el1: number };
/** legacy bridge-era crowd modes (cast.ts still switches on them until the char owner moves to `scene`) */
export type Crowd = "march" | "fall" | "water" | "bank" | "tourists" | "none";
export type ShotDef = {
  id: number; a: number; b: number; light: Light; scene: Scene; flashback?: boolean; towns?: boolean; sun?: SunSweep;
  /** legacy: kept "none" so the bridge column never spawns */ crowd: Crowd;
  /** legacy: story time = shot time */ tau: (t: number) => number;
};
const id_ = (t: number) => t;
export const SHOTS: ShotDef[] = [
  { id: 1, a: 0, b: 98, light: "golden", scene: "hook", crowd: "none", tau: id_ },
  { id: 2, a: 98, b: 174, light: "day", scene: "town", towns: true, crowd: "none", tau: id_ },
  { id: 3, a: 174, b: 270, light: "day", scene: "muskets", crowd: "none", tau: id_ },
  { id: 4, a: 270, b: 370, light: "day", scene: "cart", flashback: true, crowd: "none", tau: id_ },
  { id: 5, a: 370, b: 404, light: "day", scene: "turn", crowd: "none", tau: id_ },
  { id: 6, a: 404, b: 446, light: "day", scene: "siege", sun: { f0: 404, f1: 430, az0: 35, az1: 110, el0: 62, el1: 42 }, crowd: "none", tau: id_ },
  { id: 7, a: 446, b: 530, light: "golden", scene: "surrender", crowd: "none", tau: id_ },
  { id: 8, a: 530, b: 658, light: "golden", scene: "seven", crowd: "none", tau: id_ },
  { id: 9, a: 658, b: 728, light: "golden", scene: "parade", crowd: "none", tau: id_ },
  { id: 10, a: 728, b: 864, light: "day", scene: "sade", flashback: true, crowd: "none", tau: id_ },
  { id: 11, a: 864, b: TOTAL, light: "golden", scene: "window", crowd: "none", tau: id_ },
];
/** crossfades (frames) at a shot start. Kept EMPTY: a crossfade means two WebGL canvases at once (crashed the GPU).
 *  The plan's wish list was {3: 6, 4: 8, 6: 6, 7: 8, 9: 6, 10: 8, 11: 8}; all of them are hard cuts now. */
export const XFADE: Record<number, number> = {};
/** white 4-frame flash after the hook; the cut to shot 2 happens under it at 98 */
export const FLASH_AT = 96;

export const shotAt = (f: number) => SHOTS.find((s) => f >= s.a && f < s.b) ?? SHOTS[SHOTS.length - 1];
/** layers to draw at frame f: base shot, plus the next shot fading in during a crossfade */
export const layersAt = (f: number): { id: number; alpha: number }[] => {
  for (const s of SHOTS) {
    const x = XFADE[s.id];
    if (x && f >= s.a - x / 2 && f < s.a + x / 2) return [{ id: s.id - 1, alpha: 1 }, { id: s.id, alpha: (f - (s.a - x / 2) + 1) / (x + 1) }];
  }
  return [{ id: shotAt(f).id, alpha: 1 }];
};

// ---------------- fortress + props state (pure function of shot id + frame) ----------------
export type FortState = { draw: number /*0 up..1 down*/; doors: number /*0 open..1 shut*/; cart: V3 | null; cloth: number /*0 hidden..1 waving*/ };
/** shot 4 powder cart: along the near quay heading -x until 325 (the turn is off-screen), then rolling into the gate */
export const cartAt = (f: number): V3 =>
  f < 325 ? [LOC.CART_X0 - LOC.CART_V * (f - 270), D0, LOC.CART_QUAY_Z] : [0, D0, Math.max(-104, -100.6 - LOC.CART_V * (f - 325))];
export const fortState = (id: number, f: number): FortState => {
  const s = SHOTS[id - 1];
  // drawbridge: up during the morning, the turn and the siege; drops (quadratic ease-in, slam at 479) in shot 7
  let draw = 1;
  if (s.scene === "town" || s.scene === "muskets" || s.scene === "turn" || s.scene === "siege") draw = 0;
  if (s.scene === "surrender") draw = clamp01((f - CUE.DRAW[0]) / (CUE.DRAW[1] - CUE.DRAW[0])) ** 2;
  // gate doors (flashback cart only): shut 349..355, slam at the end (ease-in)
  const doors = s.scene === "cart" ? clamp01((f - CUE.DOORS[0]) / (CUE.DOORS[1] - CUE.DOORS[0])) ** 2 : 0;
  const cart = s.scene === "cart" ? cartAt(f) : null;
  const cloth = s.scene === "surrender" ? clamp01((f - CUE.CLOTH_UP + 2) / 3) : 0;
  return { draw, doors, cart, cloth };
};

/** shot 6 smoke puffs: tower embrasures every 9-15 f alternating towers, plus the crowd muzzle pops (muzzles up at the towers) */
export const SMOKE: { f: number; at: V3; s: number }[] = (() => {
  const out: { f: number; at: V3; s: number }[] = [];
  const towers: [number, number][] = [[-10, -101.5], [10, -101.5], [-30, -101.5], [30, -101.5]];
  const steps = [0, 11, 20, 33, 42, 54, 63, 75, 86];
  steps.forEach((d, i) => {
    const f = 400 + d; if (f >= 446) return;
    const [x, z] = towers[i % towers.length];
    out.push({ f, at: [x + ((i * 37) % 5) - 2, D0 + 23.5 + (i % 3) * 0.8, z + 5.8], s: 1.4 + (i % 2) * 0.4 });
  });
  CUE.POPS.forEach((f, i) => out.push({ f: f - 1, at: [-3 + ((i * 2.3) % 7), D0 + 2.7, -87.2], s: 0.9 }));
  return out.sort((a, b) => a.f - b.f);
})();

// ---------------- legacy bridge-era exports (other owners will drop these; calm, intact, harmless) ----------------
export const HALF = 27;
export const FILES = [-1.65, -0.55, 0.55, 1.65];
export const ROW_GAP = 1.3;
export const COUNT = 0;
export const PARK: V3 = [70, D0, -75];
export const ANCHOR: V3 = [-2.7, D0 + 0.62, -37];
export const SNAP = 1e4, DROP0 = 1e4, DROP1 = 1e4, DROP_H = 0;
export const front = (tau: number) => 26 - 1.6 * tau;
export const marchPhase = (tau: number) => ((tau % 1) + 1) % 1;
export const amp = (_tau: number) => 0;
export const stomp = (_tau: number) => 1;
export const shapeZ = (z: number) => (Math.abs(z) < HALF ? Math.cos((Math.PI * z) / (2 * HALF)) : 0);
export const dropW = (_z: number) => 0;
export const dropU = (_tau: number) => 0;
export type BridgeState = { bounce: number; drop: number; snap: number; collapsed: boolean };
export const deckY = (_z: number, _b?: BridgeState) => D0;
export const bridgeState = (_id: number, _t: number): BridgeState => ({ bounce: 0, drop: 0, snap: 0, collapsed: false });
export const snapEnd = (_snap: number): V3 => ANCHOR;

// ---------------- camera ----------------
// Grammar (skill motion.md): every move is a symmetric smootherstep glide of 18-40 f; a reframe bigger than about half
// a frame width or 40 % zoom is a hard cut on its key frame. Holds push in (dolly toward the look point, or a fov zoom
// next to walls/towers): 0.2-0.3 %/f, ~0.6 %/f on the punch words. Rolls 4-4.6 deg on emphasis beats only (1 B, 7 A, 8 D).
export type Cam = { pos: V3; look: V3; fov: number; roll: number };
type Shot = Partial<Cam> & { pos: V3; look: V3 };
/** cut keys may carry `dur` too: then keyEnd waits for their own internal move (the whip) */
type Key = { f: number; dur?: number; cut?: boolean; s: (f: number) => Shot };
/** reference camera ease: symmetric smootherstep */
export const glide = (u: number) => { const x = clamp01(u); return x * x * x * (x * (6 * x - 15) + 10); };
const mix = (a: Cam, b: Cam, k: number): Cam => ({
  pos: a.pos.map((v, i) => v + (b.pos[i] - v) * k) as V3, look: a.look.map((v, i) => v + (b.look[i] - v) * k) as V3,
  fov: a.fov + (b.fov - a.fov) * k, roll: a.roll + (b.roll - a.roll) * k,
});
const full = (c: Shot): Cam => ({ fov: 40, roll: 0, ...c });
const run = (keys: Key[], f: number) => {
  let cur = full(keys[0].s(f));
  for (let i = 1; i < keys.length; i++) {
    const k = keys[i];
    if (f < k.f) break;
    cur = k.cut ? full(k.s(f)) : mix(cur, full(k.s(f)), glide((f - k.f) / (k.dur ?? 24)));
  }
  return cur;
};
const T = (f: number) => f / FPS;
/** push-in factor since f0: the subject grows ~rate per frame; `punch` raises it (with 8 f soft edges) for the first n frames */
const pushK = (f: number, f0: number, rate: number, punch = 0, n = 35) => {
  const x = Math.max(0, f - f0);
  let s = rate * x;
  if (punch > rate) for (let i = 0; i < Math.min(x, n); i++) s += (punch - rate) * Math.max(0, Math.min(1, (i + 0.5) / 8, (n - i - 0.5) / 8));
  return Math.exp(-s);
};
/** an extra punch on top of a running push: total rate becomes `total` for n frames from f0 */
const punchK = (f: number, f0: number, base: number, total: number, n: number) => pushK(f, f0, 0, total - base, n);
/** dolly push: camera slides toward the look point by factor k */
const dolly = (pos: V3, look: V3, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos: [look[0] + (pos[0] - look[0]) * k, look[1] + (pos[1] - look[1]) * k, look[2] + (pos[2] - look[2]) * k], look, ...rest });
/** zoom push (camera stays put): tan(fov/2) shrinks by k */
const zoom = (pos: V3, look: V3, fov: number, k: number, rest: Partial<Cam> = {}): Shot =>
  ({ pos, look, fov: (360 / Math.PI) * Math.atan(Math.tan((fov * Math.PI) / 360) * k), ...rest });
const rolled = (s: (f: number) => Shot, roll: number) => (f: number): Shot => ({ ...s(f), roll });
const Y = (h: number) => D0 + h;

// ---- shot 1 HOOK (golden square, column of barrel carriers coming out of the gate toward the lens) ----
/** z of the barrel column's front row (-90 at f0 -> -86 at f98) */
export const hookFrontZ = (f: number) => -90 + (4 * f) / 98;
const S1a = (f: number) => dolly([3.5, Y(1.2), -72], [0, Y(5.0), -100], pushK(f, 0, 0.0025), { fov: 44 });
const S1b = (f: number) => dolly([1.8, Y(1.6), -80.5], [0.4, Y(1.5), -86.5], pushK(f, 60, 0.0025, 0.006, 30), { fov: 38, roll: 0.04 });
// ---- shot 2 SETTING (aerial over the far bank, crane toward the eight towers) ----
const S2a = (f: number) => dolly([40, 34, 70], [0, 9, -40], pushK(f, 98, 0.002), { fov: 44 });
const S2b = (f: number) => dolly([24, 27, 18], [0, 14, -112], pushK(f, 119, 0.002), { fov: 40 });
// ---- shot 3 MUSKETS (Invalides esplanade, crowd facing -z toward the lens, dome behind) ----
const S3a = (f: number) => dolly([0, Y(3.2), 48], [0, Y(6), 90], pushK(f, 174, 0.002), { fov: 44 });
const S3b = (f: number) => dolly([0, Y(9), 40], [0, Y(4.5), 82], pushK(f, 204, 0.002), { fov: 46 });
const S3c = (f: number) => dolly([0.75, Y(1.85), 67.9], [0.35, Y(1.75), 70], pushK(f, 246, 0.0025, 0.006, 20), { fov: 32 }); // horn CU
// ---- shot 4 FLASHBACK powder cart (near quay -> gate) ----
const S4a = (f: number) => dolly([1, Y(2.4), -14], [2, Y(3.2), -60], pushK(f, 270, 0.0025), { fov: 42 }); // on the bridge deck, up the street gap
const S4b = (f: number) => {
  const [cx, , cz] = cartAt(Math.min(f, 324));
  return dolly([cx - 1.6, Y(1.9), cz + 2.6], [cx, Y(1.3), cz - 0.4], pushK(f, 292, 0.0025, 0.006, 30), { fov: 36 });
};
const S4c = (f: number) => dolly([-6, Y(3), -70], [0, Y(4), -100], pushK(f, 325, 0.002), { fov: 42 });
// ---- shot 5 HEADS TURN: hard cut, then the short's only whip pan (camera fixed, ~105 deg yaw over 26 f) ----
const S5POS: V3 = [-14, Y(1.8), 64], S5L0: V3 = [6, Y(1.6), 70], S5L1: V3 = [-10, Y(16), -125];
const S5a = (f: number) => zoom(S5POS, S5L0, 40, pushK(f, 370, 0.0025));
const polar = (l: V3) => { const d = [l[0] - S5POS[0], l[1] - S5POS[1], l[2] - S5POS[2]], h = Math.hypot(d[0], d[2]); return { yaw: Math.atan2(d[0], d[2]), pit: Math.atan2(d[1], h), r: Math.hypot(h, d[1]) }; };
const S5P0 = polar(S5L0), S5P1 = polar(S5L1);
const S5b = (f: number): Shot => {
  const u = glide((f - 372) / 26), a = S5a(372);
  let dy = S5P1.yaw - S5P0.yaw; if (dy > Math.PI) dy -= 2 * Math.PI; if (dy < -Math.PI) dy += 2 * Math.PI;
  const yaw = S5P0.yaw + dy * u, pit = S5P0.pit + (S5P1.pit - S5P0.pit) * u, r = S5P0.r * (S5P1.r / S5P0.r) ** u;
  const look: V3 = [S5POS[0] + r * Math.cos(pit) * Math.sin(yaw), S5POS[1] + r * Math.sin(pit), S5POS[2] + r * Math.cos(pit) * Math.cos(yaw)];
  return zoom(S5POS, look, (a.fov ?? 40) + (34 - (a.fov ?? 40)) * u, pushK(f, 398, 0.006));
};
// ---- shot 6 SIEGE (crowd in profile aiming up at the towers) ----
const S6a = (f: number) => dolly([30, Y(14), -86], [0, Y(9), -97], pushK(f, 404, 0.002), { fov: 44 });
const S6b = (f: number) => dolly([6.0, Y(1.4), -84.5], [0, Y(3.0), -86.5], pushK(f, 426, 0.003), { fov: 38 });
// ---- shot 7 SURRENDER (governor on the front-right tower, drawbridge drop, reverse from inside the gate) ----
const S7a = (f: number) => dolly([12.5, Y(27.4), -92.5], [10, Y(27.6), -98.3], pushK(f, 446, 0.0025), { fov: 38 });
const S7b = (f: number) => dolly([12, Y(1.8), -88], [-1, Y(3.2), -97], pushK(f, 468, 0.0025), { fov: 42 });
const S7c = (f: number) => dolly([0.8, Y(1.6), -106.5], [0, Y(2.6), -88], pushK(f, 492, 0.0025), { fov: 44 });
// ---- shot 8 THE SEVEN (courtyard) ----
const S8a = (f: number) => dolly([0, Y(4.5), -106], [0, Y(1.5), -140], pushK(f, 530, 0.002) * punchK(f, 555, 0.002, 0.006, 30), { fov: 44 });
const S8b = (f: number) => dolly([-1.6, Y(1.7), -131.4], [-1.9, Y(1.5), -136.5], pushK(f, 571, 0.0025), { fov: 38 });
const S8c = (f: number) => dolly([1.8, Y(1.8), -131], [1.6, Y(1.5), -137.5], pushK(f, 584, 0.0025), { fov: 40 });
const S8d = (f: number) => dolly([3.4, Y(1.75), -132.2], [3.6, Y(1.65), -136.6], pushK(f, 606, 0.0025) * punchK(f, 633, 0.0025, 0.006, 25), { fov: 36 });
// ---- shot 9 PARADE + barrel chain (square) ----
const S9a = (f: number) => dolly([16, Y(3.0), -58], [0, Y(2.2), -76], pushK(f, 658, 0.0025), { fov: 44 });
const S9b = (f: number) => dolly([7, Y(2.0), -80], [0, Y(1.6), -95], pushK(f, 689, 0.0025) * punchK(f, 710, 0.0025, 0.006, 18), { fov: 40 });
// ---- shot 10 FLASHBACK Sade (through the bars, passers-by below, walk-out) ----
const S10a = (f: number) => dolly([-29.2, Y(13.6), -90.5], [-30, Y(13.1), -96.2], pushK(f, 728, 0.0025), { fov: 38 });
const S10b = (f: number) => dolly([-26.5, Y(1.4), -78], [-30, Y(9), -96], pushK(f, 781, 0.003), { fov: 42 });
const S10c = (f: number) => dolly([8, Y(2.2), -76], [0, Y(2.0), -95], pushK(f, 840, 0.002), { fov: 42 });
// ---- shot 11 EMPTY WINDOW ----
const S11a = (f: number) => dolly([-27, Y(1.9), -84], [-30, Y(11), -96], pushK(f, 864, 0.0025), { fov: 42 });

const CAMS: Record<number, Key[]> = {
  1: [
    { f: 0, s: S1a }, // low on the gate, both front towers
    { f: 60, dur: 26, s: S1b }, // fastest at 73 ("gunpowder"), MS of the front carriers + prisoners left, roll 0 -> 0.04
  ],
  2: [
    { f: 98, s: S2a }, // cut under the flash
    { f: 119, dur: 40, s: S2b }, // slow crane toward the towers, fastest 139 ("1789"), lands 159
  ],
  3: [
    { f: 174, s: S3a },
    { f: 204, dur: 30, s: S3b }, // fastest 219 ("30,000"): forest of muskets under the dome
    { f: 246, cut: true, s: S3c }, // HORN_TIP: CU of the upturned horn
  ],
  4: [
    { f: 270, s: S4a }, // cart crosses the street mouth in profile
    { f: 292, dur: 24, s: S4b }, // fastest 304 ("barrels"): front 3/4 on the barrel stack
    { f: 325, cut: true, s: S4c }, // cart into the gate, doors slam 355
  ],
  5: [
    { f: 370, s: S5a }, // hard cut back to colour
    { f: 372, dur: 26, cut: true, s: S5b }, // whip ~105 deg, fastest 385 ("-keeping"), lands 398, push 0.6 %/f to 404
  ],
  6: [
    { f: 404, s: S6a }, // high wide from the square's east side, crowd in profile
    { f: 426, cut: true, s: S6b }, // low along the front row, muzzles up
  ],
  7: [
    { f: 446, s: S7a }, // governor MS, merlons across his legs
    { f: 456, dur: 18, s: rolled(S7a, 0.035) }, // roll 0 -> 4 deg
    { f: 468, cut: true, s: S7b }, // drawbridge drops in profile, slam 479
    { f: 492, cut: true, s: S7c }, // reverse from inside the gate, crowd toward the lens
  ],
  8: [
    { f: 530, s: S8a }, // vast courtyard, punch from 555 ("seven")
    { f: 571, cut: true, s: S8b }, // forgers
    { f: 584, dur: 20, s: S8c }, // fastest 594 ("madmen")
    { f: 606, cut: true, s: S8d }, // the count
    { f: 633, dur: 18, s: rolled(S8d, 0.04) }, // "family": punch + roll
  ],
  9: [
    { f: 658, s: S9a }, // parade in profile on the arc
    { f: 689, dur: 28, s: S9b }, // fastest 703 ("back"), punch from 710 ("barrels")
  ],
  10: [
    { f: 728, s: S10a }, // through the bars
    { f: 781, cut: true, s: S10b }, // low under the window, passers-by
    { f: 840, cut: true, s: S10c }, // walk-out over the drawbridge
  ],
  11: [{ f: 864, s: S11a }],
};

// impact kicks: the image offset flips sign every frame (~3 px at 720p per unit), decays to 0 in 7 f, roll +-0.23 deg per unit.
// [seconds, gain]: doors slam, close musket pops, drawbridge slam, "massacred".
const KICKS: [number, number][] = [[355 / 30, 0.8], [426 / 30, 0.3], [431 / 30, 0.3], [436 / 30, 0.3], [479 / 30, 1.2], [824 / 30, 0.5]];
export const kickAt = (t: number) => {
  let a = 0;
  for (const [t0, g] of KICKS) {
    const n = Math.floor((t - t0) * FPS + 1e-6);
    if (n >= 0 && n < 7) a += g * (n % 2 ? -1 : 1) * (1 - n / 7) ** 1.5;
  }
  return a;
};
export const camAt = (id: number, f: number): Cam => {
  const c = run(CAMS[id], f), a = kickAt(T(f));
  if (!a) return c;
  const d: V3 = [c.look[0] - c.pos[0], c.look[1] - c.pos[1], c.look[2] - c.pos[2]];
  const L = Math.hypot(...d), h = Math.hypot(d[0], d[2]) || 1;
  const m = (3 / 640) * Math.tan((c.fov * Math.PI) / 360) * L * a; // metres at the look distance for 3 px x a
  return { ...c, look: [c.look[0] - (d[2] / h) * m, c.look[1] + 0.6 * m, c.look[2] + (d[0] / h) * m], roll: c.roll + a * 0.004 };
};
/** frame at which the current key's move has finished (for picking billboard views per key, not per frame) */
export const keyEnd = (id: number, f: number) => {
  let e = 0;
  for (const k of CAMS[id]) if (f >= k.f) e = k.f + (k.cut && !k.dur ? 0 : k.dur ?? 24);
  return Math.max(f, e);
};

// ---------------- lens: depth of field + foreground framing ----------------
/** Lens blur per shot (thin lens). cInf = blur-disc radius in px at 1080x1920 for things at infinity; 0 = all sharp.
 *  Entries switch on cuts (no dur) or ramp with the camera glide they share f/dur with. focus = world point (else the
 *  camera look point). */
export type Dof = { f: number; dur?: number; cInf: number; focus?: (f: number) => V3 };
const at = (p: V3) => () => p;
export const DOF: Dof[] = [
  { f: 0, cInf: 0 }, // hook establishing
  { f: 60, dur: 26, cInf: 12, focus: (f) => [0.4, Y(1.6), hookFrontZ(f)] }, // front-row eyes
  { f: 98, cInf: 0 }, // town aerial
  { f: 246, cInf: 14, focus: at([0.35, Y(1.75), 69.9]) }, // horn mouth
  { f: 270, cInf: 8, focus: (f) => { const c = cartAt(f); return [c[0], Y(1.3), c[2]]; } }, // the cart
  { f: 292, dur: 24, cInf: 13, focus: (f) => { const c = cartAt(Math.min(f, 324)); return [c[0], Y(1.2), c[2] + 0.4]; } }, // the barrels
  { f: 325, cInf: 0 }, // gate, turn, siege wide
  { f: 426, cInf: 10, focus: at([1.5, Y(1.6), -86]) }, // front-row musketeers
  { f: 446, cInf: 12, focus: at([10, Y(27.6), -98.4]) }, // de Launay's eyes
  { f: 468, cInf: 0 }, // drawbridge side-on
  { f: 492, cInf: 6, focus: at([0, Y(1.7), -100]) }, // front runners through the gate
  { f: 530, cInf: 0 }, // vast courtyard
  { f: 571, cInf: 12, focus: at([-2.0, Y(1.5), -136.5]) }, // forgers
  { f: 584, dur: 20, cInf: 12, focus: at([1.6, Y(1.5), -137.5]) }, // madmen
  { f: 606, cInf: 13, focus: at([3.6, Y(1.6), -136.6]) }, // the count's eyes
  { f: 658, cInf: 0 }, // parade
  { f: 689, dur: 28, cInf: 10, focus: at([2, Y(1.6), -90]) }, // barrel chain
  { f: 728, cInf: 12, focus: at([-30, Y(13.3), -96.55]) }, // Sade's eyes
  { f: 781, cInf: 6, focus: at([-28.5, Y(1.5), -84]) }, // passers-by
  { f: 840, cInf: 0 }, // walk-out
  { f: 864, cInf: 8, focus: at(LOC.SADE_WIN) }, // empty window, near crowd soft
];
export const dofAt = (f: number) => {
  let i = 0; while (i + 1 < DOF.length && f >= DOF[i + 1].f) i++;
  const d = DOF[i], p = DOF[Math.max(0, i - 1)];
  const k = d.dur ? Math.min(1, (f - d.f) / d.dur) : 1;
  return { cInf: p.cInf + (d.cInf - p.cInf) * k, focus: d.focus };
};
/** what the lens focuses on (DOF): the DOF table's focus point, else the camera look point */
export const focusAt = (id: number, f: number): V3 => {
  const d = dofAt(f);
  return d.focus ? d.focus(f) : camAt(id, f).look;
};

/** near framing objects: visible while a <= f < b. kit in "musket_crate" | "lamppost" | "cannon" | "barrels3" | "cart"
 *  (procedural builders, world owner). pos = base point, s = height in metres, yaw in radians. Ranges stay inside one shot. */
export type FgKit = "musket_crate" | "lamppost" | "cannon" | "barrels3" | "cart";
export type Fg = { a: number; b: number; kit: FgKit; pos: V3; s?: number; yaw?: number };
export const FOREGROUND: Fg[] = [
  { a: 174, b: 246, kit: "musket_crate", pos: [-3.2, D0, 55], s: 1.0 }, // shot 3 A/B, bottom-left, muzzles out
  { a: 325, b: 370, kit: "lamppost", pos: [-4.8, D0, -76], s: 3.2 }, // shot 4 C, left edge
  { a: 468, b: 492, kit: "cannon", pos: [9.1, D0, -90.9], s: 1.0 }, // shot 7 B, bottom-right, barrel toward the gate
  { a: 689, b: 728, kit: "barrels3", pos: [5.2, D0, -82.2], s: 1.2 }, // shot 9 B, right edge, bungs toward the lens
  { a: 781, b: 840, kit: "cart", pos: [-24.8, D0, -82.6], s: 0.9 }, // shot 10 B, bottom-left
];
