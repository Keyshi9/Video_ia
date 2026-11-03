# BASTILLE - shot plan (v2, 2026-11-03)

Approved script: SCRIPT.md candidate 1. Guide voice: `public/bastille/voice.wav`, `words.json` (last word "out." ends 29.0 s = f870).
Composition "Bastille", 1080x1920, 30 fps, **TOTAL = 900 f**. The user will record their own voice to this rhythm. So the picture
follows the guide word onsets below, and every visual reaction lands **0-3 f before its word** (LEAD = 2 f).
The look values, camera grammar and readability rules come from the skill's SKILL.md. Anything not stated here keeps the bridge-template value.

v2 changes (from the critique): the cart comes along the near-bank quay (Arsenal side), not over the bridge from the Invalides; every powder barrel
shows a black-grain trickle at its bung and is the same model in shots 1, 4, 9, 11; parade speed 0.008 rad/f; **no `back` view** (every crowd is
staged facing the lens, in 3/4 or in profile; shot 6, 7 B/C, 8, 9 and 10 B were restaged for this); shot 5 opens on a hard cut at 370 with the head
turn at 372-376 and a 26 f whip over ~105 deg; HORN_TIP 246, puff 250, shot 3 C is a close-up of the horn; shot 2 crane glides over 40 f;
PORTRAIT 640, Sade blink 752; cast trimmed (veteran, baker, apples, `tricorne_lace`, `roll`, one shoe off cut; `pass` merged into `hug`);
lit sill + warm bounce on the empty window; the shot 6 sun sweep is optional. Not taken: a funnel for Sade (the approved script drops the
funnel as poorly sourced and asks for cupped hands).

## 0. Word onsets (frame = round(start x 30))
```
The@0 most@9 famous@16 jail@26 ever@33 stormed@41 was@50 really@56 a@65 gunpowder@71 run.@82(end 92)
Paris@101 July@113 14@117 1789@141(end 166)
That@176 morning@180 the crowd@194 grabbed@200 about@208 30@215 ,000@221 muskets@232 No@248 powder@252(end 260)
The@270 powder@275 250@287 barrels@307 moved@327 into@332 the Bastille@338/342 days@351 before@356 For@372 safe-@375 -keeping@383(end 387)
About@400 four@406 hours@415 of@421 shooting@428 later@433 the@450 governor@452 gave@459 up@466(end 473)
Luckily@481 the@497 prisoners@500 were@507 freed@516(end 523)
Unluckily@532 there@550 were@553 seven@557 Four@573 forgers@575 two@590 madmen@594 an@608 "account"(=a count)@612 locked@618 up@625 by@629 his@633 own@637 family@642(end 652)
The@659 crowd@664 paraded@671 them@680 then@691 went@695 back@700 to@705 the@709 barrels@712(end 719)
The@731 Marquis@734 de@743 Sade@748 missed@754 it@760 He'd@770 yelled@775 to@779 passers@784 -by@791 that@799 prisoners@803 were@811 being@818 massacred@826 so@842 they'd@847 moved@853 him@857 out@863(end 870)
```

## 1. World layout (metres, y up, ground/bank top y = D0 = 6.0)

The **river runs along x** in the bed between z = -30 and +30. It already exists in world.ts: bed, water shader, embankment walls, copings, and cobble quays at |z| 30-36.5. Keep all of it.
- **Near bank (z < 0)** = the Bastille quarter. The Arsenal lies off-frame to **+x** along this bank; the powder cart comes from there along the near quay.
- **Far bank (z > 0)** = the Invalides esplanade.
The bridge at x = 0 joins the two banks.

### 1.1 Keep / change / remove
| Item | Action |
|---|---|
| River, water shader, embankments, copings, quay cobbles, river bed | **keep** |
| Riverfront house rows (fronts at \|z\| 36.5, centres \|z\| 40.5) | keep, except **far bank \|x\| < 46** (esplanade reaches the quay) |
| Main-street rows (fronts \|x\| 6) | near bank: keep only z -36.5..-50 (the short street from the bridge to the square). Far bank: remove all |
| Back rows (zf 52..96) | keep only \|x\| > 52 on both banks (square, fortress and esplanade need the middle) |
| Chain bridge (towers, chains, hangers, backstays, anchorages, bolt, eye, bunting, St George flags, deck deformation) | **remove**. Replace with a static **stone arch bridge** (1.2) |
| Park swing, sand, park trees/hedge/flowers/bench, PARK constant | **remove** |
| Mill, both chimneys + smoke, church (nave, tower, spire, clock), windmill, canoes, lilies, stalls, sign | **remove** |
| Collapse physics (bridgeState, deckY, snapEnd, splash/creak fx, flotsam, sitters in water, tourists, officer/hammer) | **remove** |
| Hills | keep, lowered 30 % (Paris basin) |
| Trees | Kenney trees are absent, so build **procedural** rounded trees with the VEG shapes in build.ts. Use them as plane-tree rows along both quays (every 22 m, leaving the near quay clear at \|x\| < 8 for the cart shot) and as two rows along the esplanade (x = +-42, z 40..90, every 9 m) |
| Quay lanterns | procedural iron post + glass box (2.8 m), every 12 m |

### 1.2 Stone arch bridge (shots 2, 4)
- Deck: x -4.6..4.6, z -30..30, top at D0, cobble top (reuse M.cobble).
- Three arches: side faces are boxes with semicircular cut-outs (radius 7, springing at y 0.5, centres z -18, 0, +18), on piers 3 m thick. Use warm beige stone M.wall and M.cope on the arch rings.
- Parapets: 0.6 m thick, 1.0 m high, at x = +-4.3, with a cope.
- Two round lamp posts per side at z = +-12.
- The existing parapet gap at |x| < 4.6 already fits.

### 1.3 Square (near bank)
- Cobble plane x -46..46, z -92..-50.
- House rows face the square at x = +-50 (fronts facing +-x), z -52..-92. They are 3-4 storey (8.4/9.8 m), cream/ochre/brick.
- Behind the fortress (z -160..-200) a back row of roofs adds depth over the walls.
- The street from the bridge enters at x -6..6, z -36.5..-50.
- Dressing (procedural): 2 lamp posts at (-14, -60) and (14, -60), a 3-barrel pile at (6, -84) (the shared `BARREL` model, with trickle), two cannons at (7.2, -86.5) and (-9, -64) (aimed at the gate, never fired), and one vegetable handcart at (-24.8, -82.6).

### 1.4 The Bastille (all procedural; warm grey stone a touch darker than the town, never blue-grey)
| Part | Geometry |
|---|---|
| Curtain walls | rectangle outer x -32..32, z -150..-100, thickness 3, top D0+22, with a 0.8 m corbelled machicolation band at D0+20.5 and a crenellated parapet (merlons 1.0 x 1.1 m, gaps 0.8) |
| 8 round towers | radius 5.5, top D0+26, crenellated, a slight batter (radius 6 at the base). Front centres (+-10, -101.5) and (+-30, -101.5), back centres (+-10, -148.5) and (+-30, -148.5). Cylinder 32 segments with smooth normals, so the ink draws silhouettes only |
| Tower slits | 3 dark arrow slits per tower face toward the square (unlit dark material #2b2533, not black) |
| Gate | opening x -2.2..2.2, y D0..D0+6.5 (round-arched top) in the front wall (face z = -100, through to -103), plus a stone gatehouse frame 0.4 proud. The inner face (z -103) gets the same arch frame, since shot 7 C looks out through it |
| Gate doors (flashback only) | two oak leaves 2.2 x 6 m hinged at x = +-2.2, z -100.6. Open = swung 90 deg inward |
| Drawbridge | oak planks 4.8 wide x 8 long x 0.35, hinged at (0, D0, -100), lowered tip at z -92. Two iron chains run from the tip corners to slots at (+-2.0, D0+8.6, -100). Up = vertical, covering the gate. Angle from `draw` 0 (up) .. 1 (down) |
| Moat | dry ditch x -38..38, z -100..-92, floor D0-4, with stone revetment walls. **Dry, not water** |
| Courtyard | floor x -27..27, z -147..-103, flagstones. The inner walls are lighter stone with 3 arched dark doorways (2.2 x 3.2) in the back inner face z = -147 at x = -12, 0, 12 (dark interior #2b2533 + an emissive lantern by the middle door, HDR 2.5). Seen straight through the gate from the square |
| Sade's barred window | on the front-left tower, facing +z. Opening centre (-30, D0+13.2, -96.0), 1.2 w x 1.6 h, 0.5 m deep reveal, a dark inside back plate at z -96.6. 4 vertical iron bars + 1 cross bar, 5 cm square, at the outer face. The **sill is a lit cope stone** (pale warm stone, 0.15 m proud, catches the light in every shot) |
| Window bounce (shot 11) | a warm point light #ffcf9a at `LOC.WINDOW_BOUNCE` (in front of and just below the window), range 4 m, lighting the sill, the reveal and the bars, so the backlit window never goes to a black hole. On in scene `window` only (optional in `sade`) |
| Governor's spot | top of the front-right tower: floor D0+26, parapet 1.1 m. De Launay stands at (10, D0+26, -98.4) by the front merlon gap |
| No flag on the fortress | (a white royal flag would read as the surrender cloth) |

### 1.5 Invalides esplanade (far bank)
| Part | Geometry |
|---|---|
| Esplanade | grass x -46..46, z 37..92, with a gravel cross path (x -3..3 and z 70..74) |
| Facade | z = 96 facing -z, x -40..40, 14 m high (2 storeys + attic dormers), cream stone, slate roof, tall arched windows with blue-grey shutters |
| Centre pavilion | x -8..8 brought forward to z 93.5, 18 m high, triangular pediment, big arched door |
| Two short wings | at x = +-40 from z 96 to 78, facing inward |
| Dome behind the pavilion | centre (0, *, 108). Drum radius 8 (D0+18..D0+27) with paired columns as boxes. Dome: hemisphere radius 8.5 squashed 1.3 tall, dark lead-blue #3b4a6a with 12 gold ribs (#d9b44a, lit, never lemon). Lantern and spire to D0+46 |
| Gun racks (shot 3 dressing) | 3 open crates of muskets at (-12, 62), (12, 60), (-3.2, 55, FG) |

### 1.6 Sight lines that must stay open (the culler in build.ts must protect them)
- Esplanade (0, D0+2, 70) toward the Bastille (0, D0+16, -125). The towers must rise clearly above the near-bank riverfront roofs; this needs tower top D0+26.
- Bridge deck (1, D0+2.4, -14) up the bridge-head street to the front towers (shot 4 A): the street gap x -6..6 must show both front-centre towers.
- Square (-27, D0+1.9, -84) up to the Sade window.
- Courtyard (0.8, D0+1.6, -106.5) out through the gate to the square (shot 7 C).

### 1.7 The powder barrel (one model everywhere: shots 1, 4, 9, 11 and the square pile)
- Exported spec `BARREL` in story.ts; world (pile, cart load, `barrels3` FG) and char (carried barrels) both build from it, so it is the same barrel in every shot.
- 0.7 m tall, bellied staves (warm oak), 2 dark iron hoops, no text or marks. One **bung hole** on the belly (dark disc 6 cm).
- **Powder trickle:** a thin stream of 8-12 black grains (#241726 to #2b2533, never pure black, 1.5-3 cm specks) runs from the bung and falls to the ground, plus a small dark speck patch where it lands. Grains respawn on a loop (fall ~0.5 s). This is what makes it gunpowder, not wine, with the sound off.
- Rule: the bung faces the lens (within 60 deg) in every shot where a barrel is the subject (1 B, 4 B, 9 B, 11).

## 2. Shot list (11 shots, 900 f)

Legend:
- Cam keys: `f` start frame, `dur` glide length, `cut` = a hard cut.
- Positions are world metres.
- Every key pushes in with `pushK(f, f0, rate[, punch, n])`.
- Rolls are in radians: 0.04 = 4.6 deg, 0.035 = 4 deg.
- X = crossfade length in frames at the shot start; the crossfade is centred on `a`.
- Facing rule (no back view): every crowd member is seen from the front, in 3/4, or in profile. Nobody walks away from the lens.

### Shot 1 - HOOK, 0-98, golden, scene `hook` (Bastille square, drawbridge down)
- **Line:** "The most famous jail ever stormed was really a gunpowder run."
- **Cast:**
  - **Barrel column:** 18 sans-culottes, women and 2 Gardes. They come out of the gate over the drawbridge toward the camera in a loose column (x -1.5..2.5) at 1.1 m/s. The front row is at z -90 at f0 and -86 at f98.
    - Most hug a `BARREL` (pose `hug`, both arms, bung toward the lens, grains trickling onto the planks) with expression `laugh`/`grin`.
    - 2 carry a barrel overhead (pose `overhead`; their trickle falls past their shoulders).
    - On "stormed" (cue f39) everyone hoists their barrel 8 cm higher and cheers.
  - **Seven prisoners:** at the left edge, standing still in a ragged row at x -5.4..-3.6, z -87..-85.5. Expression `dazed` with blinks. Nobody in the crowd looks at them.
  - **Background:** about 20 cheering extras at the square edges, facing the column (3/4 to the lens). Caps waving 39-60.
- **Fx:** dust puffs at the carriers' feet on the drawbridge planks; the powder trickles leave a dotted dark trail on the planks.
- **Cam:**
  - A f0: pos [3.5, D0+1.2, -72], look [0, D0+5.0, -100], fov 44, push 0.0025. Low angle on the gate, both front towers in frame.
  - B f60 dur 26 (fastest at f73, "gunpowder"): pos [1.8, D0+1.6, -80.5], look [0.4, D0+1.5, -86.5], fov 38, roll 0.04, push 0.0025 with punch 0.006 for 30 f. A medium shot of the front carriers, the trickle from the front barrel clearly visible, with the prisoners in the left third, uncut.
- **DOF:**
  - f0: cInf 0 (establishing).
  - f60 dur 26: ramp to 12, focus on the front-row eyes (0.4, D0+1.6, front z).
- **FG:** none.
- **Flash:** white flash 4 f at **FLASH_AT = 96**. The cut to shot 2 happens under it at 98.

### Shot 2 - SETTING, 98-174, day (morning), scene `town`, towns extras on
- **Line:** "Paris, July 14, 1789."
- **Cast:** townsfolk on both quays and the bridge (about 30, small). They wave 99-130 (cue `TOWN_CHEER`). Their hats carry blue-and-red cockades.
- **Props:** blue/red split pennants on 6 poles along the quays. No tricolour (it came on 17 July) and no text.
- **Cam:**
  - A f98: pos [40, 34, 70], look [0, 9, -40], fov 44, push 0.002. Over the far bank: the river, the stone bridge, roofs, and the Bastille at the top edge of town.
  - B f119 **dur 40** (fastest f139, "1789"): pos [24, 27, 18], look [0, 14, -112], fov 40, push 0.002. A slow crane (~55 m over 40 f) toward the eight towers. Lands 159, push-hold to 174.
- **DOF:** 0.
- **FG:** none.

### Shot 3 - MUSKETS, 174-270, day, scene `muskets`, X 6 (Invalides esplanade)
- **Line:** "That morning, the crowd grabbed about 30,000 muskets. No powder."
- **Cast:** about 70 people in tiers on the esplanade, x -16..16, z 62..88, facing -z toward the camera, with the dome behind them. Mixed sans-culottes, women, Gardes françaises and bourgeois in tricornes.
  - Each holds a musket at the hip until **MUSKETS_UP f198**. Then all muskets go up overhead, muzzle up, in a ripple from the centre outward over 6 f. Expression `laugh`.
  - **Horn man** (sans-culotte in a red phrygian cap) stands at (0.4, D0, 70). At **HORN_TIP f246** (on the cut) he raises his powder horn to cheek height and tips it upside down (pose `tip`). At **HORN_PUFF f250** one tiny 3-grain dust puff appears and nothing falls. His expression changes `grin` → `nervous` at 251 (blink across the swap).
  - **ARMS_DOWN f254-268:** muskets lower in a wave across the crowd behind him. Expressions go to `nervous`/`stern`.
- **Props:** 2 open musket crates by the wings.
- **Cam:**
  - A f174: pos [0, D0+3.2, 48], look [0, D0+6, 90], fov 44, push 0.002.
  - B f204 dur 30 (fastest f219, "30,000"): pos [0, D0+9, 40], look [0, D0+4.5, 82], fov 46, push 0.002. A forest of muskets with the dome over it.
  - C f246 cut: pos [0.75, D0+1.85, 67.9], look [0.35, D0+1.75, 70], fov 32, push 0.0025 with punch 0.006 for 20 f. A **close-up of the horn**: the upturned horn fills the centre, his face beside it in the upper third. The lowering muskets show soft behind him.
- **DOF:**
  - f174: 0.
  - f246: 14, focus on the horn mouth (0.35, D0+1.75, 69.9).
- **FG:** musket crate `musket_crate` at [-3.2, D0, 55], h 1.0, from f174 to f246 (bottom-left corner, muzzles sticking out, recognisable).

### Shot 4 - FLASHBACK: the powder cart, 270-370, `flashback` (sepia), light day, scene `cart`, X 8
- **Line:** "The powder? 250 barrels, moved into the Bastille days before."
- **Route (history + script beat):** the cart comes from the Arsenal along the **near-bank quay** (from +x), past the near bridge head, and turns up the bridge-head street to the square. It never crosses the bridge and never comes from the domed building; the dome stays behind the camera / out of frame in all of shot 4.
- **Cast:**
  - 4 Swiss garrison soldiers (red coats, tricornes) push a two-wheeled handcart with the side `push` pose (seen in profile). 2 more walk alongside on the far side with shouldered muskets. Expression `stern`.
  - On the quay: 3 neutral passers-by in profile, no reaction.
- **Props:** the handcart (2.6 x 1.5 m, wheels 1.2 m, shafts at the back) with 9 `BARREL`s in a 4/3/2 pyramid and rope lashings; the front row's bungs face the lens and trickle onto the cobbles.
- **Path:**
  - Quay part: CART x = 5.5 - 0.05(f-270), z -33.6, heading -x (f270-325; x 5.5 → 2.75). The turn into the street happens off-screen.
  - At the gate: CART z = -100.6 - 0.05(f-325), x 0, clamped at -104.
- **Gate:** drawbridge down. The doors shut over **DOORS f349-355** (smooth, slam on 355). Kick 0.8 at f355, 1 f before "before".
- **Cam:**
  - A f270: pos [1, D0+2.4, -14] (on the bridge deck), look [2, D0+3.2, -60], fov 42, push 0.0025. The cart crosses the street mouth in profile, screen-right to screen-left, with the bridge parapets at the bottom edges and both front towers up the street gap above it. The dome is behind the camera.
  - B f292 dur 24 (fastest f304, "barrels"): pos [CX-1.6, D0+1.9, CZ+2.6], look [CX, D0+1.3, CZ-0.4], fov 36, push with punch 0.006 for 30 f. Front 3/4 on the cart: the barrel stack and its trickles fill the frame, the pushers beyond it.
  - C f325 cut: pos [-6, D0+3, -70], look [0, D0+4, -100], fov 42, push 0.002. The cart rolls into the gate and the doors slam.
- **DOF:**
  - f270: 8, focus on the cart.
  - f292 dur 24: 13, focus on the barrels.
  - f325: 0.
- **FG:** `lamppost` at [-4.8, D0, -76], h 3.2, from f325 to f370 (left edge).

### Shot 5 - HEADS TURN, 370-404, day, scene `turn`, **hard cut** (back in colour at the Invalides; the script says "Cut back to colour")
- **Line:** "For safekeeping."
- **Cast:** the musket crowd of shot 3 with muskets lowered and heads slightly down.
  - At **HEADS_TURN f372-376** every head turns as one to screen-left, toward the towers: FrontOpts look -1 plus headTilt, or the side view facing -z.
  - Expressions `stern`, then `grin` from 382 (they have an idea).
- **Cam:**
  - A f370 cut: pos [-14, D0+1.8, 64], look [6, D0+1.6, 70], fov 40, push 0.0025. Seen from this side, screen-left points to -z, toward the Bastille; the crowd is in 3/4 and profile.
  - B f372 **dur 26** (fastest f385, "-keeping"): a **whip pan** with the camera fixed, yaw about 105 deg. Look goes to [-10, D0+16, -125] and fov to 34. The river and bridge pass, and it lands on the towers far away above the roofs at 398.
  - Then push 0.006 to the end (398-404 is the clean landing before the dissolve). This is the short's only whip; the post owner may add the optional whip blur from motion.md 5.4.
- **DOF:** 0 (the towers must read through the 200 m of haze).
- **FG:** none.

### Shot 6 - SIEGE, 404-446, day, sun sweep **optional (lowest priority; drop it if time runs short)**, scene `siege`, X 6
- **Line:** "About four hours of shooting later,"
- **Cast:** about 140 people fill the square: Gardes françaises in the front rows (front row at z -86, by the moat edge) and sans-culottes behind, in tiers, all facing -z.
  - The front row aims muskets **up at the tower tops** (at least 35 deg up, never level at anyone).
  - Expressions `stern`/`grin`.
- **Fx:** cream cartoon smoke puffs (`fxPuff`). Nobody is ever shown hit.
  - From tower embrasures (schedule `SMOKE`, about every 9-15 f, alternating towers).
  - From crowd muzzles at **POPS f405, 413, 426, 431, 436** (on "four", "hours", "shooting", 2 more).
  - Puffs drift slowly up and fade over 40 f.
- **Sun (optional):** shot field `sun = {f0: 404, f1: 430, az0: 35, az1: 110, el0: 62, el1: 42}`. Shadows of the crowd and towers swing visibly during key A, then the sun freezes. If dropped, the shot keeps the plain day light and nothing else changes.
- **Cam (both keys see the crowd in profile, never from behind):**
  - A f404: pos [30, D0+14, -86], look [0, D0+9, -97], fov 44, push 0.002. High wide view from the square's east side: the crowd in profile aiming up-left, the towers and their smoke above.
  - B f426 cut: pos [6.0, D0+1.4, -84.5], look [0, D0+3.0, -86.5], fov 38, push 0.003. Low along the front row: musketeers in profile, muzzles up toward screen-right and the tower tops.
- **Kicks:** 0.3 at f426, 431 and 436.
- **DOF:**
  - f404: 0.
  - f426: 10, focus on the front row's eyes (1.5, D0+1.6, -86).
- **FG:** none.

### Shot 7 - SURRENDER and "Luckily", 446-530, golden, scene `surrender`, X 8 (time passes, day → golden)
- **Line:** "the governor gave up. Luckily, the prisoners were freed."
- **Cast A - de Launay** on the front-right tower top:
  - expression `nervous` at first;
  - at **CLOTH_UP f457** he raises the white cloth on a short stick and waves it 457-470 (a 2 Hz flutter);
  - expression `relief` at 462.
- **Cast B - the crowd** at the moat edge, x -8..4, z -90..-80:
  - first `stern`;
  - when the drawbridge slams they shout `laugh`;
  - **SURGE f483:** they pour across the drawbridge into the gate, holding lanterns up (emissive, bloom) and arms open (`arms_open`);
  - **CAPS f514:** 6 caps and tricornes fly up (thrown 2 f before "freed").
- **Drawbridge:** **DRAW f468-479** from up to down (quadratic ease-in), slamming at 479. Kick 1.2 at f479, 2 f before "Luckily". A dust puff line along z -92. Chains rattle.
- **Cam:**
  - A f446: pos [12.5, D0+27.4, -92.5], look [10, D0+27.6, -98.3], fov 38, push 0.0025, roll 0 → 0.035 from f456 dur 18. A medium shot of the governor. The parapet crosses his legs, not his torso (the lens is 1.4 m above the tower floor).
  - B f468 cut: pos [12, D0+1.8, -88], look [-1, D0+3.2, -97], fov 42, push 0.0025. Side-on to the gate: the drawbridge drops in clear profile, and the surge runs across the frame (3/4, never away from the lens).
  - C f492 cut: **reverse angle from inside the gate**. pos [0.8, D0+1.6, -106.5], look [0, D0+2.6, -88], fov 44, push 0.0025. The camera stands in the courtyard just behind the gate arch; the crowd pours over the drawbridge and through the gate **toward the lens**, lanterns up, faces lit gold from the square, and splits left and right past the camera at 2.5 m. The caps fly at 514 against the square behind them. Shot 8 cuts in at 530.
- **DOF:**
  - f446: 12, focus on de Launay's eyes (10, D0+27.6, -98.4).
  - f468: 0.
  - f492: 6, focus on the front runners (0, D0+1.7, -100).
- **FG:** `cannon` at [9.1, D0, -90.9], h 1.0, from f468 to f492 (bottom-right, barrel toward the gate).

### Shot 8 - THE SEVEN, 530-658, golden, scene `seven`, hard cut (courtyard)
- **Line:** "Unluckily, there were seven. Four forgers, two madmen, and a count locked up by his own family."
- **Cast:** about 40 crowd members line the side walls (x +-18..24), facing inward (3/4 to the lens), lanterns up and arms open. They drop to `nervous`/`confused` at 557.
- **The seven** come out of the middle doorway (0, D0, -147) toward the camera at 0.6 m/s from 530 to 555. They stop at:
  - forgers x -3.2, -2.4, -1.6, -0.8 at z -136.5;
  - madmen x 1.0, 2.2 at z -137.5;
  - the count at x 3.6, z -136.6.
- **COINS f571-590:** each forger drops 3 fake coins (gold discs with a plain dot, no text) that bounce once, with a little sparkle. Expression `nervous`, with a guilty sideways look.
- **MADMEN f592+:** the 2 madmen wander off sideways in opposite directions along x (one to +x, one to -x) at 0.5 m/s, in profile. Expressions `smile` and `dazed`.
- **The count:**
  - **CUFFS f610-630:** straightens his cuffs (expression `stern`, nose up);
  - **PORTRAIT f640:** lifts a small oval portrait of 3 tiny bean faces and glances at it (`nervous`), 2 f before "family".
- **Cam:**
  - A f530: pos [0, D0+4.5, -106], look [0, D0+1.5, -140], fov 44, push 0.002, with punch 0.006 from f555 for 30 f ("seven"). The vast courtyard, with the seven small in the middle of the frame.
  - B f571 cut: pos [-1.6, D0+1.7, -131.4], look [-1.9, D0+1.5, -136.5], fov 38, push 0.0025. Medium shot of the forgers.
  - C f584 dur 20 (fastest f594, "madmen"): pos [1.8, D0+1.8, -131], look [1.6, D0+1.5, -137.5], fov 40.
  - D f606 cut: pos [3.4, D0+1.75, -132.2], look [3.6, D0+1.65, -136.6], fov 36, push 0.0025. Then at f633 dur 18 add punch 0.006 for 25 f and roll 0.04 ("family").
- **DOF:**
  - f530: 0.
  - f571: 12, focus on the forgers' eyes.
  - f584 dur 20: 12, focus on the madmen.
  - f606: 13, focus on the count's eyes.
- **FG:** none (the courtyard has to look vast and empty).

### Shot 9 - PARADE and back to the barrels, 658-728, golden, scene `parade`, X 6 (square)
- **Line:** "The crowd paraded them, then went back to the barrels."
- **Parade (in profile):**
  - **HOIST f669:** the seven are lifted onto shoulders, one rider per pair of carriers.
  - The riders use the `carried` sit pose, soles 1.25 m above the carriers' soles, waving.
  - They move along the near (camera-side) arc of a circle with centre (0, D0, -72), radius 9, at **0.008 rad/f** (about 2.2 m/s, a brisk march; about 0.27 rad over the shot). Riders are spaced 1.6 m on the arc. The motion is tangential, so carriers and riders read in profile.
  - The crowd `laugh`s and caps wave.
- **SETDOWN f692:** they are set down gently at the hook spot (x -5.4..-3.6, z -87..-85.5), `dazed`.
- **Barrel chain from f690:** 10 people in a bucket-brigade line from the gate (0, -101) across the drawbridge to the pile at (6, -84). Each stands **in profile** (facing across the line, not along it) and swings a `BARREL` from one side to the other with the `hug` pose (the old `pass` pose is merged into it: hug + a sideways body swing). Each barrel moves 1 position per 6 f, trickling grains. Expression `grin`.
- **Cam:**
  - A f658: pos [16, D0+3.0, -58], look [0, D0+2.2, -76], fov 44, push 0.0025.
  - B f689 dur 28 (fastest f703, "back"): pos [7, D0+2.0, -80], look [0, D0+1.6, -95], fov 40, then punch 0.006 from 710 for 18 f ("barrels"). The prisoners are left at the left edge, exactly like the hook.
- **DOF:**
  - f658: 0.
  - f689 dur 28: 10, focus on the chain (2, D0+1.6, -90).
- **FG:** `barrels3` at [5.2, D0, -82.2], h 1.2, from f689 to f728 (right edge, bungs toward the lens).

### Shot 10 - FLASHBACK: Sade, 728-864, `flashback` (sepia), light day, scene `sade`, X 8
- **Line:** "The Marquis de Sade missed it. He'd yelled to passers-by that prisoners were being massacred, so they'd moved him out."
- **Sade** stands behind the bars: soles on the inner floor at D0+11.9, (-30, *, -96.55), card scaled so his head fills the window.
  - 728-770: `stern`/bored, with a **blink at 752** ("missed" 754).
  - **SHOUT f773:** hands cupped at his mouth (`cupped`, per the approved script; no funnel), expression `shout`. Shout fx (3 curved lines, no text) pulse until 838.
- **Passers-by** (3: woman with a basket, bourgeois in a tricorne, a kid) walk across the square in profile at z -86..-82, along x.
  - **STARTLE f782:** they stop, turn 3/4 to the lens and look up (head tilt up, eyes up toward the window, which sits high in the same frame), `shock`.
  - **MASSACRE f824:** bigger shock. The basket drops (bounces once), the tricorne hops off.
  - Kick 0.5 at f824.
- **WALKOUT f840-864:** 2 garrison guards walk Sade out of the gate (drawbridge down) toward the camera at 1.2 m/s. Sade keeps shouting back over his shoulder at the tower.
- **Cam:**
  - A f728: pos [-29.2, D0+13.6, -90.5], look [-30, D0+13.1, -96.2], fov 38, push 0.0025. Medium shot through the bars.
  - B f781 cut: pos [-26.5, D0+1.4, -78], look [-30, D0+9, -96], fov 42, push 0.003. Low view a few metres in front of the passers-by (they cross the lower frame, then turn 3/4), up to the tiny shouting window.
  - C f840 cut: pos [8, D0+2.2, -76], look [0, D0+2.0, -95], fov 42, push 0.002.
- **DOF:**
  - f728: 12, focus on Sade's eyes.
  - f781: 6, focus on the passers-by.
  - f840: 0.
- **FG:** handcart `cart` at [-24.8, D0, -82.6], h 0.9, from f781 to f840 (bottom-left corner).

### Shot 11 - EMPTY WINDOW, 864-900, golden, scene `window`, X 8
- **Line:** (end of "out." and the tail)
- **Cast:** the roaring crowd marches in profile across the bottom of the frame, right to left, with `BARREL`s on their shoulders (bungs toward the lens, trickling), `laugh`, plus 2 lanterns.
- **Window:** the window is empty, a dark recess, but it reads as a window: the **lit sill** and the **warm bounce light** (`LOC.WINDOW_BOUNCE`) keep the reveal, sill and bars clear against the backlit tower.
- **Cam:** A f864: pos [-27, D0+1.9, -84], look [-30, D0+11, -96], fov 42, push 0.0025 until f899, ending on the window. The window sits at y ≈ 0.35 of the frame and the crowd's heads fill the lower 25 %.
- **DOF:** 8, focus on the window (the near crowd soft).
- **FG:** none.

### Timeline constants (for story.ts)
- `FLASH_AT = 96`
- `XFADE = {3: 6, 4: 8, 6: 6, 7: 8, 9: 6, 10: 8, 11: 8}` (shots 2, 5 and 8 start on a cut)
- `KICKS` (seconds, gain): `[[355/30, 0.8], [426/30, 0.3], [431/30, 0.3], [436/30, 0.3], [479/30, 1.2], [824/30, 0.5]]`
- About 1/3 of shots carry a foreground prop, as listed above.
- Rolls: shot 1 B, shot 7 A and shot 8 D only.
- Priority if time runs short: drop the shot 6 sun sweep first.

## 3. Cast list (toon.ts outfits + cast.ts roles)
All characters keep the house style:
- bean heads with h/w .94;
- 3.5 head-heights tall;
- plum ink #241726;
- face brightness ~.93;
- no blush.

Cockade = a small blue/red rosette on the hat.

| Role | Outfit (new toon.ts entries) | Hand props / poses |
|---|---|---|
| Sans-culotte (x 6 variants) | red **phrygian cap** (`hat: "phrygian"`, soft cone flopping forward, cockade), short brown/blue jacket (carmagnole), **vertical blue-white striped trousers** (`stripes`), wooden-clog brown boots, open shirt | musket, `BARREL` (hug / overhead / shoulder), lantern, cap in hand (thrown), powder horn (horn man) |
| Bourgeois (x 3) | black **tricorne** (`"tricorne"`) + cockade, long coat (ochre/green/plum), knee breeches, white stockings | musket, cane |
| Woman (x 4) | **mob-cap bonnet** (`"bonnet"` exists), striped skirt, apron, shawl crossed over the chest | basket, lantern, fist up |
| Garde française (x 2 variants) | royal-blue coat, red cuffs and collar, white waistcoat and breeches, plain black `"tricorne"`, cockade | musket (aim up / shoulder) |
| Swiss garrison soldier | red coat, blue cuffs, white belts, black tricorne | cart push (the existing `push` side pose), shouldered musket, guard walk |
| De Launay (governor) | **white coat** with red sash, powdered **wig** under a black tricorne, stout | white cloth on a stick (`cloth`, waves) |
| 4 forgers | ragged brown shirts, patched breeches, stubble; **ink-black fingertips**: the hand dots drawn #1b1a2e | `coin` (falling fake coins) |
| 2 madmen | **wild hair** (`"wild"`, spiky, grey and ginger), mismatched clothes | none; they wander |
| The count | tall and thin, powdered **wig** with side curls and a black-ribbon queue, faded pale-blue silk coat, lace jabot | `portrait` (small oval frame), cuffs gesture |
| Marquis de Sade | stout, powdered **wig**, dark plum coat, round face | `cupped` hands (shout pose) |
| Passers-by (shot 10, x 3) | woman (bonnet + basket), bourgeois (tricorne), kid | basket drop, hat hop |

Cut in v2: the Invalides veteran, the baker, the apples, `tricorne_lace`, the one-shoe-off detail.

Telling the three wigs apart:
- De Launay: tricorne + white coat + sash.
- The count: thin, jabot, pale blue.
- Sade: stout, dark plum, seen only in sepia.

### New expressions
- `shout`: big oval mouth, brows down.
- `confused`: one brow up, small mouth.

All other expressions already exist.

### New poses / views
- **No `back` view.** Billboards always face the camera, so every crowd is staged facing the lens, in 3/4 or in profile (see the facing rule in section 2).
- `raise` (musket overhead, muzzle up)
- `aim_up`
- `hug` (barrel; also used for the barrel chain with a sideways body swing, replacing `pass`)
- `overhead` (barrel)
- `carried` (sitting rider) + `carrier` (arms up)
- `cupped`
- `arms_open`
- `tip` (horn upside down at cheek height)
- `wave_cloth`

Prisoners' shuffle: walk bob 3 %, stride 0.5.

### Expressions per beat
| Shot | Expressions |
|---|---|
| 1 | crowd `laugh`/`grin`; prisoners `dazed` |
| 2 | townsfolk `smile` |
| 3 | crowd `laugh`; horn man `grin` → `nervous` at 251; crowd `nervous` from 254 |
| 5 | `stern`, then `grin` from 382 |
| 6 | `stern`/`grin` |
| 7 | governor `nervous` → `relief`; crowd `stern` → `laugh` |
| 8 | crowd `nervous`/`confused`; forgers `nervous`; madmen `smile`/`dazed`; count `stern` → `nervous` |
| 9 | `laugh`, riders `smile`, then `dazed` when set down |
| 10 | Sade `stern` (blink 752) → `shout`; passers-by `neutral` → `shock` |
| 11 | `laugh` |

Expression swaps get a blink across the swap (`lidAt` swaps list).

### FX cards (cast.ts)
- `fxPuff` smoke, cream #f4ecdc with a lilac shade side.
- Dust puff (also the 3-grain horn puff at 250).
- **Powder trickle** at every barrel bung (spec in 1.7), plus the dark speck patches it leaves.
- Coin sparkle (`fxBurst` small, gold).
- Shout lines.
- Flying caps.
- Lantern glow: emissive HDR 2.5, so it blooms.

## 4. Sound event table (for audio/timeline.py)
- **Music:** an original fife-and-snare march at 112 bpm, ducked under the voice.
  - Sepia flashbacks (f266-370 and f724-868) cut the march to a solo music-box / harpsichord version of the same tune, with a soft vinyl crackle.
  - The march returns at the hard cut back to colour (370) and under the dissolve at 864.
- **Mix:** music +3 dB, SFX -6 dB, voice unchanged.

| t (s) | f | Event |
|---|---|---|
| 0.00 | 0 | crowd cheer bed (golden square), wood creak of the drawbridge under feet, faint grain hiss |
| 1.30 | 39 | cheer swell ("stormed") |
| 2.00-3.0 | 60-90 | barrel thumps on shoulders, footsteps on planks |
| 3.20 | 96 | flash whoosh / shimmer |
| 3.30-5.6 | 98-168 | town ambience: birds, distant bells, river lap, small cheer 3.3-4.3 |
| 3.97-5.30 | 119-159 | crane whoosh (soft, long) |
| 5.80 | 174 | crossfade, crowd murmur (esplanade) |
| 6.60 | 198 | 70 muskets lifted: wood/metal rattle + big cheer |
| 7.30 | 219 | crane whoosh |
| 8.20 | 246 | cut; murmur drops; horn flipped (leather creak) |
| 8.33 | 250 | powder horn shake: hollow tap-tap, single grain tick, comic "empty" pause |
| 8.47-8.93 | 254-268 | muskets lowering: wood clunks in a wave, disappointed "ohh" |
| 8.87-12.3 | 266-370 | flashback: cart wheels on quay cobbles, wood creak, footsteps, river lap |
| 10.13 | 304 | barrels knock together |
| 10.83 | 325 | cut; gate echo ambience |
| 11.83 | 355 | **heavy gate doors slam** + bolt clank |
| 12.33 | 370 | hard cut to colour: march back in, crowd murmur |
| 12.40 | 372 | heads turn: collective clothing swish |
| 12.83 | 385 | whip-pan whoosh |
| 13.47-14.9 | 404-446 | siege bed: crowd roar, distant musket pops from the towers every 0.3-0.5 s |
| 13.50, 13.77 | 405, 413 | musket pops (crowd) |
| 14.20, 14.37, 14.53 | 426, 431, 436 | close musket pops + puff whoomph |
| 14.87 | 446 | crossfade: the roar fades, wind on the tower top |
| 15.23 | 457 | cloth flutter |
| 15.60-15.97 | 468-479 | **drawbridge chain run** (ratchet rattle) |
| 15.97 | 479 | **drawbridge slam** + dust whoomph |
| 16.10 | 483 | crowd surge roar, running feet |
| 16.40-17.6 | 492-530 | cut inside the gate: stone-arch reverb, the crowd rushes past the lens left and right |
| 17.13 | 514 | caps whoosh + cheer peak |
| 17.67 | 530 | cut: courtyard reverb, the roar drops to an awkward murmur |
| 18.33-18.5 | 550-555 | hush; shuffling feet |
| 19.03-19.7 | 571-590 | coin tinkles (12 small bounces) |
| 19.73 | 592 | two wandering footsteps + a silly bassoon blip |
| 20.33-21.0 | 610-630 | cuff fabric tugs |
| 21.33 | 640 | portrait: small wood tap |
| 21.93 | 658 | crowd cheer back up, march returns full |
| 22.30 | 669 | "hup!" hoist + cheer |
| 23.07 | 692 | set-down thud x7 |
| 23.0-24.2 | 690-726 | barrels swung down the chain (hollow thumps) |
| 23.43 | 703 | whoosh |
| 24.13 | 724 | flashback in: music box, birds, quiet square |
| 25.77-27.9 | 773-838 | muffled shouting from the high window (non-verbal, reverb) |
| 26.07 | 782 | passers-by gasp |
| 27.47 | 824 | basket drop, hat hop |
| 28.00-28.8 | 840-864 | guards' footsteps on the drawbridge planks |
| 28.80 | 864 | back to colour: huge crowd roar + march tutti, barrel thumps |
| 29.80-30.0 | 894-900 | final drum hit at 29.83 (f895), ring out |

## 5. Contracts (exported names; story.ts is the source, other owners read only)

### story.ts (cam)
```ts
export const FPS = 30, TOTAL = 900, D0 = 6.0;
export type V3 = [number, number, number];
export type Light = "day" | "golden";
export type Scene = "hook" | "town" | "muskets" | "cart" | "turn" | "siege" | "surrender" | "seven" | "parade" | "sade" | "window";
export type SunSweep = { f0: number; f1: number; az0: number; az1: number; el0: number; el1: number }; // degrees, camera-relative like LIGHTS
export type ShotDef = { id: number; a: number; b: number; light: Light; scene: Scene; flashback?: boolean; towns?: boolean; sun?: SunSweep };
export const SHOTS: ShotDef[];      // 11 entries exactly as in section 2 (flashback: shots 4 and 10; towns: shot 2; sun: shot 6, optional)
// a/b: 1 [0,98] 2 [98,174] 3 [174,270] 4 [270,370] 5 [370,404] 6 [404,446] 7 [446,530] 8 [530,658] 9 [658,728] 10 [728,864] 11 [864,900]
export const XFADE: Record<number, number>; // {3:6, 4:8, 6:6, 7:8, 9:6, 10:8, 11:8}; shots 2, 5, 8 start on a cut
export const FLASH_AT = 96;
export const shotAt, layersAt, camAt, keyEnd, kickAt, dofAt, focusAt, glide, smooth, clamp01; // same signatures as the bridge
export const DOF: Dof[]; export const FOREGROUND: Fg[]; // Fg.kit in: "musket_crate" | "lamppost" | "cannon" | "barrels3" | "cart"
export const LEAD = 2 / 30;
/** named story cues in FRAMES (cast/world schedule from these, never from literal numbers) */
export const CUE = { STORMED: 39, TOWN_CHEER: [99, 130], MUSKETS_UP: 198, HORN_TIP: 246, HORN_PUFF: 250, ARMS_DOWN: [254, 268], DOORS: [349, 355],
  HEADS_TURN: [372, 376], IDEA: 382, POPS: [405, 413, 426, 431, 436], CLOTH_UP: 457, DRAW: [468, 479], SURGE: 483, CAPS: 514,
  SEVEN_OUT: [530, 555], COINS: 571, MADMEN: 592, CUFFS: [610, 630], PORTRAIT: 640, HOIST: 669, SETDOWN: 692, CHAIN: 690,
  SADE_BLINK: 752, SHOUT: 773, STARTLE: 782, MASSACRE: 824, WALKOUT: [840, 864] } as const;
/** world points (metres) */
export const LOC = {
  BRIDGE: [0, D0, 0], BRIDGE_HALF_W: 4.6,
  SQUARE: [0, D0, -72], SQUARE_BOX: [-46, -92, 46, -50],             // x0, z0, x1, z1
  GATE: [0, D0, -100], GATE_W: 4.4, GATE_H: 6.5, WALL_FRONT_Z: -100, WALL_BACK_Z: -150, WALL_HALF_X: 32, WALL_T: 3, WALL_TOP: D0 + 22,
  TOWERS: [[-30, -101.5], [-10, -101.5], [10, -101.5], [30, -101.5], [-30, -148.5], [-10, -148.5], [10, -148.5], [30, -148.5]],
  TOWER_R: 5.5, TOWER_TOP: D0 + 26,
  DRAW_HINGE: [0, D0, -100], DRAW_LEN: 8, DRAW_W: 4.8, MOAT: [-38, -100, 38, -92], MOAT_DEPTH: 4,
  COURT: [0, D0, -125], COURT_BOX: [-27, -147, 27, -103], DOOR: [0, D0, -147],
  SADE_WIN: [-30, D0 + 13.2, -96.0], SADE_FLOOR: D0 + 11.9, WINDOW_BOUNCE: [-30, D0 + 12.0, -94.6],
  GOVERNOR: [10, D0 + 26, -98.4],
  HOOK_PRISONERS: [-4.5, D0, -86.2], FORGERS_Z: -136.5, COUNT: [3.6, D0, -136.6],
  PARADE_C: [0, D0, -72], PARADE_R: 9, PARADE_W: 0.008 /* rad per frame */, BARREL_PILE: [6, D0, -84],
  CART_QUAY_Z: -33.6, CART_X0: 5.5, CART_V: 0.05 /* m per frame */,
  INVALIDES_FACADE_Z: 96, DOME: [0, D0, 108], ESPLANADE: [0, D0, 75], ESPLANADE_BOX: [-46, 37, 46, 92], HORN_MAN: [0.4, D0, 70],
} as const;
/** the one powder barrel used everywhere (world pile/cart/barrels3 FG and char carried barrels) */
export const BARREL = { h: 0.7, rMid: 0.29, rEnd: 0.24, hoops: 2, bungR: 0.03, trickle: { grains: 10, fallS: 0.5, color: "#2b2533" } } as const;
/** fortress + props state per shot/frame (pure function of id + f) */
export type FortState = { draw: number /*0 up..1 down*/; doors: number /*0 open..1 shut*/; cart: V3 | null; cloth: number /*0 hidden..1 waving*/ };
export const fortState: (id: number, f: number) => FortState; // shot 4: cart on the near quay (x = CART_X0 - CART_V(f-270), z CART_QUAY_Z) until 325, then at the gate
export const SMOKE: { f: number; at: V3; s: number }[]; // tower + muzzle puffs for shot 6
```

### Other owners
- **world (build.ts, paint.ts, world.ts, lights.ts, shade.ts):** builds sections 1.1-1.7 from `LOC` and `BARREL`. `update(id, f)` reads `fortState` and `SHOTS[id-1].sun`; the sun sweep (optional) lerps az/el between f0 and f1, then freezes. It drops `bridgeState`/`PARK`/`ANCHOR`. Adds the lit sill and the `WINDOW_BOUNCE` warm point light (scene `window`). The procedural FG builders take the `Fg.kit` names above. The Kenney loader stays harmless.
- **char (toon.ts, cast.ts, cardshade.ts):**
  - New signature: `stage(id, t, fs: FortState, cam)`. It switches on `SHOTS[id-1].scene` and times everything from `CUE` (seconds = frame / 30).
  - It provides the outfits, poses and expressions in section 3, carried barrels from `BARREL` with the trickle fx. No back view: it stages every crowd facing the lens, in 3/4 or in profile.
  - `HITS`/`SIGN_AT`/`swing*` are removed.
- **post (grade.ts, Bridge.tsx, ink.ts, lensblur.ts):**
  - Add `GRADES.sepia`: chroma about 15 %, mids toward #c9a678, shadows #4a3a2c (p5 ≥ .18, never crushed), highlights #f3e2c0, and an 18 % vignette.
  - `gradeFor(fx, s.flashback ? "sepia" : s.light)`, applied per crossfade layer, so the sepia fades in and out with the XFADE (and switches on the frame at the hard cut 370).
  - The flash stays at FLASH_AT. Whip blur is optional, on shot 5 B only.

## 6. Readability traps for this short (check every still)
1. **Billboards always face the lens and there is no back view:** never stage a crowd walking away from the camera or seen from behind. Crowds come toward the lens (1, 7 C, 8, 10 C), or move/stand in 3/4 or profile (4, 5, 6, 7 B, 9, 11).
2. **Muskets** at a distance read as rakes or sticks. Give them a dark walnut stock, a steel barrel with one highlight, and no bayonets. They are never pointed level at a person or the lens; when aiming, they point up at least 35 deg at the tower tops.
3. **No gore, no hits:** only cream cartoon smoke, nobody falls. The garrison is never shown shooting at faces.
4. **White cloth** against a peach golden sky vanishes. Frame it against dark stone or blue upper sky (shot 7 A looks slightly down-and-across, so the stone is behind it). Give it a lilac shade side and plum ink, about 0.9 x 0.6 m.
5. **Barrels** must read as gunpowder with the sound off, not wine and not drums: the one `BARREL` model (bellied staves, 2 dark iron hoops, no text or marks, 0.7 m tall) with the black-grain trickle at the bung, bung toward the lens. Same model in shots 1, 4, 9, 11.
6. **Drawbridge chains** are thick iron links, never a single thin line (the "hanging" trap).
7. **Barred window:** the face sits 10+ cm behind the bars and the recess is dark. In shot 11 the empty recess must still read as a window: lit sill, warm bounce on the reveal, bars clear (the tower is backlit).
8. **Sepia vs colour** must be unmistakable: sepia = desaturated + vignette; golden = saturated peach/violet. Sepia → golden always dissolves (8 f, at 728 and 864); sepia → day at 370 is the script's hard "cut back to colour".
9. **No flags with meaning:** no tricolour (anachronistic before 17 July), no royal white flag (it reads as surrender), no text anywhere (coins, portrait, pennants plain).
10. **Moat is dry:** keep it unlit-free and lighter than the walls, so it does not read as a black hole or as water.
11. **Prisoners** are bewildered and comic, never sick, chained or creepy. The madmen are gentle-silly (no spiral eyes).
12. **Courtyard golden shade** must not crush: lantern light pools on the floor and the inner walls lighter, p5 ≥ .2.
13. **Lens near people:** in shot 7 C the crowd runs at the lens; it splits at 2.5 m, and lantern poles and caps stay more than 2 m from the lens.
14. **Parapet:** in shot 7 A the merlons cross de Launay's legs or waist, never his face (lens 1.4 m over the tower floor).
15. **Every hold creeps:** no key without `pushK`. The QA frozen span limit is 12 f.
16. **The cart never comes from the dome:** in shot 4 the dome is behind the camera or out of frame, and the cart is on the near-bank quay, not on the bridge deck.

## 7. Build order (a few hours per owner, in parallel)
1. **cam:** story.ts with SHOTS, CUE, LOC, BARREL, fortState, CAMS, DOF, FG and KICKS. First publish a stub with LOC + CUE + SHOTS + BARREL, so the others can start.
2. **world:**
   - remove the bridge, park, mill and church;
   - stone bridge;
   - Bastille shell (walls, towers, gate, drawbridge, moat, courtyard, window with lit sill + bounce);
   - square + house ring;
   - Invalides facade + dome;
   - procedural trees, lamp posts, the shared barrel and FG props;
   - sun sweep last (optional).
3. **char:** new outfits (phrygian, tricorne, striped trousers, wigs, wild hair), the new poses and props (barrel trickle, horn, cloth, portrait, coins), then the scene switch in `stage()`.
4. **post:** sepia grade + layer grading (with the hard switch at 370). Re-check the ink on the round towers (crease threshold) and the lantern bloom.
