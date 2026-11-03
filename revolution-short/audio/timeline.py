# Picture timeline of "The Bastille: Stormed for Gunpowder, Not Prisoners" (read-only mirror of SHOTPLAN.md section 2
# and the sound event table in section 4). 900 frames at 30 fps = 30.000 s. Guide voice timings: public/bastille/words.json.
import json

FPS = 30
TOTAL = 900
DUR = TOTAL / FPS            # 30.000 s exactly
fr = lambda f: f / FPS

# id: (first frame, end frame, look, scene)
SHOTS = {
    1: (0, 98, "golden", "hook"), 2: (98, 174, "day", "town"), 3: (174, 270, "day", "muskets"),
    4: (270, 370, "sepia", "cart"), 5: (370, 404, "day", "turn"), 6: (404, 446, "day", "siege"),
    7: (446, 530, "golden", "surrender"), 8: (530, 658, "golden", "seven"), 9: (658, 728, "golden", "parade"),
    10: (728, 864, "sepia", "sade"), 11: (864, 900, "golden", "window"),
}
XFADE = {3: 6, 4: 8, 6: 6, 7: 8, 9: 6, 10: 8, 11: 8}

# key picture cues (frames from SHOTPLAN)
FLASH_AT = fr(96)          # white flash, cut to shot 2 at 98
CHEER_STORMED = fr(39)
MUSKETS_UP = fr(198)
HORN_TIP = fr(246)
HORN_PUFF = fr(250)
ARMS_DOWN = fr(254)
FLASHBACK1 = (fr(266), fr(370))   # sepia: music box
BARREL_KNOCK = fr(304)
GATE_SLAM = fr(355)
COLOUR1 = fr(370)
WHIP = fr(385)
SIEGE = (fr(404), fr(446))
CHAIN_RUN = (fr(468), fr(479))
DB_SLAM = fr(479)
SURGE = fr(483)
COURTYARD = fr(530)
HUSH = (fr(550), fr(555))
COINS = (fr(571), fr(590))
BLIP = fr(592)
CHEER_BACK = fr(658)
HUP = fr(669)
SETDOWN = fr(692)
FLASHBACK2 = (fr(724), fr(864))
COLOUR2 = fr(864)
FINAL_HIT = fr(895)


def shot_t(i):
    a, b = SHOTS[i][:2]
    return fr(a), fr(b)


def words(path):
    """words.json uses start/end; return dicts with s/e as the mixer expects"""
    w = json.load(open(path, encoding="utf-8"))
    return [dict(w=x["word"], s=float(x["start"]), e=float(x["end"])) for x in w]
