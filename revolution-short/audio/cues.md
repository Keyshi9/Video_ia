# The Bastille: Stormed for Gunpowder, Not Prisoners - sound cue sheet

All music and SFX are original, synthesized in numpy/scipy (`music.py` + `instruments.py`, `sfx.py` + `sfx_gen.py`), mixed by `mix.py`.
The march is an original tune composed for this short (D major, 112 bpm, fife and drum) - not La Marseillaise, not Ca ira, no quoted melody.
Guide voice = `remotion-shorts/public/bastille/voice.wav` (Piper TTS) at unity gain, no processing. Timeline: 900 frames @ 30 fps = 30.000 s.

## Files
| file | content |
|---|---|
| `music_sfx.wav` | music + SFX, **no voice**, music already ducked under the guide-voice word spans; same gains as guide_mix |
| `guide_mix.wav` | music + SFX + guide voice (unchanged) |
| `stem_voice.wav` / `stem_music.wav` / `stem_sfx.wav` | stems at mix gain, pre-limiter (they sum to guide_mix before the true-peak limiter) |

All files: 48 kHz, stereo, 24-bit PCM, 1,440,000 samples = 30.000 s.

When the user records the real voice: keep the same rhythm as words.json; lay it at about the guide's loudness (-12.6 LUFS integrated) on top of `music_sfx.wav`. If its timing moves by more than ~0.15 s, re-run `python mix.py` with the new words.json so the duck follows it.

## Loudness
- **guide_mix.wav**: integrated -12.6 LUFS, true peak -1.0 dBTP, LRA 2.2 LU, max momentary -8.8, max short-term -11.0. Limiter (ceiling -1.0 dBTP): max GR 3.25 dB, active on 29.80 % of samples.
- **music_sfx.wav**: integrated -21.1 LUFS, true peak -3.7 dBTP, LRA 4.6 LU, max momentary -15.0, max short-term -18.6. Limiter (ceiling -1.0 dBTP): max GR -0.00 dB, active on 0.00 % of samples.
- Stems: voice -12.6, music -22.4, sfx -26.1 LUFS.

ffmpeg ebur128, `guide_mix.wav`:
```
Summary:
  Integrated loudness:
    I:         -12.6 LUFS
    Threshold: -22.6 LUFS
  Loudness range:
    LRA:         2.3 LU
    Threshold: -32.6 LUFS
    LRA low:   -13.8 LUFS
    LRA high:  -11.5 LUFS
  True peak:
    Peak:       -1.0 dBFS
```
ffmpeg ebur128, `music_sfx.wav`:
```
Summary:
  Integrated loudness:
    I:         -21.1 LUFS
    Threshold: -31.2 LUFS
  Loudness range:
    LRA:         4.6 LU
    Threshold: -41.4 LUFS
    LRA low:   -23.6 LUFS
    LRA high:  -19.0 LUFS
  True peak:
    Peak:       -3.7 dBFS
```

## Voice on top: per-shot loudness (LUFS, at mix gain)
bed = music + sfx; margin = voice - bed; speech median / p10 = 400 ms momentary margin over windows centred on spoken words.

| shot | time s | voice | music | sfx | bed | margin LU | speech median | speech p10 |
|---|---|---|---|---|---|---|---|---|
| 1 hook | 0.00-3.27 | -11.3 | -20.8 | -25.6 | -19.6 | 8.2 | 8.4 | 6.1 |
| 2 town | 3.27-5.80 | -14.1 | -24.9 | -33.2 | -25.4 | 11.3 | 9.8 | 7.6 |
| 3 muskets | 5.80-9.00 | -11.8 | -21.9 | -26.6 | -20.6 | 8.8 | 8.2 | 3.8 |
| 4 cart (sepia) | 9.00-12.33 | -14.1 | -25.1 | -26.6 | -23.0 | 8.8 | 9.6 | 2.3 |
| 5 turn | 12.33-13.47 | -12.9 | -27.6 | -26.9 | -24.2 | 11.3 | 13.8 | 8.8 |
| 6 siege | 13.47-14.87 | -10.8 | -22.6 | -23.6 | -20.1 | 9.3 | 8.5 | 6.4 |
| 7 surrender | 14.87-17.67 | -13.2 | -20.4 | -21.9 | -18.4 | 5.2 | 6.1 | 2.8 |
| 8 seven | 17.67-21.93 | -12.2 | -25.2 | -31.9 | -25.1 | 12.9 | 12.6 | 8.4 |
| 9 parade | 21.93-24.27 | -12.1 | -21.4 | -23.5 | -19.4 | 7.3 | 8.0 | 3.6 |
| 10 Sade (sepia) | 24.27-28.80 | -12.7 | -23.7 | -33.7 | -23.3 | 10.6 | 11.0 | 7.2 |
| 11 window | 28.80-30.00 | -16.7 | -18.2 | -23.1 | -17.0 | 0.3 | 5.3 | 4.0 |

## Music map
Original march, D major, 112 bpm (quarter = 0.5357 s): fife 1, fife 2 (a third below), field snare, rope bass drum, soft low reed. Sepia flashbacks = solo music box of the same tune + vinyl crackle.
Speech duck -3 dB keyed from words.json. Section targets (LU under the voice): hook -9.5, town -10.5, muskets -10.0, flashback1 -11.0, siege -9.5, courtyard -13.0, parade -9.5, flashback2 -11.0, finale -9.0. Applied section gains (dB): hook -1.7, town -1.5, muskets -1.1, flashback1 -5.8, siege -2.2, courtyard +4.2, parade -3.5, flashback2 -1.2, finale -2.5.

| time s | frame | music |
|---|---|---|
| 0.00 | 0 | hook: theme bars 1-2, two fifes + snare + bass drum + low reed; bass-drum lift on 'stormed' |
| 2.55 | 76 | snare roll into the white flash |
| 3.20 | 96 | D button (fifes D6/A5, drum accent) exactly on the flash (f96); band cut |
| 3.50 | 105 | town: light drum tap-in (shot 2, 'Paris, July 14, 1789.') |
| 4.46 | 134 | fife 1 alone, theme bar 1, light drum |
| 6.60 | 198 | TUTTI on muskets-up (f198): cymbal + bass drum downbeat, both fifes, theme bars 2-3 |
| 8.20 | 246 | band cut on the horn close-up (f246): empty comic pause |
| 8.47 | 254 | fife droops a fifth (muskets lowering, f254); bassoon 'womp' at 8.70 after 'powder.' |
| 8.87 | 266 | sepia flashback: music-box version of the theme (bars 1-2) + vinyl crackle |
| 11.83 | 355 | music box stops dead on the gate slam (f355); crackle only to the cut |
| 12.33 | 370 | hard cut to colour (f370): drums snap back in, bass-drum hit on the cut |
| 13.82 | 415 | siege: fifes theme bar 3, driving snare |
| 15.55 | 466 | snare roll under the drawbridge chain run |
| 15.97 | 479 | TUTTI on the drawbridge slam (f479): bass drum + cymbal, theme bars 5-6 loud |
| 17.67 | 530 | cut to the courtyard (f530): band stops - awkward |
| 18.75 | 562 | courtyard: tiptoe pizzicato on the beat, sparse |
| 19.73 | 592 | silly bassoon blip (two notes, low-high) on the wandering footsteps (f592) |
| 21.93 | 658 | march back full on the cheer (f658): theme bars 7-8, roll-in, cymbal |
| 23.07 | 692 | bass-drum hit on the barrel set-down (f692) |
| 24.18 | 726 | sepia flashback 2 (Sade): music-box theme bars 5-6, crackle |
| 28.80 | 864 | back to colour (f864): tutti hit + cymbal, fife cadence A-G-E, snare roll |
| 29.83 | 895 | final D hit (f895): drum + cymbal + fifes, ring-out faded to silence at 30.000 |

## SFX events
Level convention: EVENT naive level = LU vs the voice (event max momentary); applied = naive - 6 dB (standard mix). BEDs are integrated loudness vs the voice and are not reduced. Reverb: 'square' (open, 1.0 s) or 'stone' (gate arch / courtyard, 1.8 s).

| # | time s | frame | cue | what | naive LU | applied LU | room | pan |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.00 | 0 | cheer_bed (bed) | crowd cheering on the golden square (column + 20 extras) | -18 | -18.0 | square | +0.00 |
| 2 | 0.00 | 0 | grain_hiss (bed) | faint gunpowder trickling from the barrel bungs | -34 | -34.0 | square | +0.00 |
| 3 | 0.00 | 0 | plank_creak (bed) | drawbridge planks creaking under the barrel column | -28 | -28.0 | square | +0.00 |
| 4 | 0.00 | 0 | plank_steps (bed) | loose column footsteps on the drawbridge planks | -24 | -24.0 | square | +0.00 |
| 5 | 1.30 | 39 | cheer_swell | cheer swell, barrels hoisted ('stormed' 1.38) | -6 | -12.0 | square | +0.00 |
| 6 | 2.00 | 60 | barrel_thump | barrel bumped on a shoulder | -12 | -18.0 | square | -0.30 |
| 7 | 2.27 | 68 | barrel_thump | barrel bumped on a shoulder | -12 | -18.0 | square | +0.25 |
| 8 | 2.52 | 76 | barrel_thump | barrel bumped on a shoulder | -12 | -18.0 | square | -0.10 |
| 9 | 2.78 | 83 | barrel_thump | barrel bumped on a shoulder | -12 | -18.0 | square | +0.40 |
| 10 | 3.00 | 90 | barrel_thump | barrel bumped on a shoulder | -12 | -18.0 | square | +0.00 |
| 11 | 3.20 | 96 | flash_whoosh | reverse swell + shimmer into the white flash (f96) + soft low whoomp | -6 | -12.0 | square | +0.00 |
| 12 | 3.27 | 98 | amb_town (bed) | Paris morning: breeze, sparrows, river lapping, three distant church-bell strokes | -24 | -24.0 | square | +0.00 |
| 13 | 3.30 | 99 | town_cheer | small cheer from the townsfolk waving (f99-130) | -14 | -20.0 | square | +0.00 |
| 14 | 3.97 | 119 | whoosh_crane | long soft crane whoosh toward the eight towers | -14 | -20.0 | square | +0.00 |
| 15 | 5.75 | 172 | murmur_esplanade (bed) | crowd of 70 murmuring on the esplanade | -20 | -20.0 | square | +0.00 |
| 16 | 6.57 | 197 | musket_rattle | 70 muskets lifted overhead: wood and metal rattle in a ripple | -8 | -14.0 | square | +0.00 |
| 17 | 6.60 | 198 | big_cheer | big cheer as the muskets go up | -6 | -12.0 | square | +0.00 |
| 18 | 6.80 | 204 | whoosh_crane | crane up over the forest of muskets | -14 | -20.0 | square | +0.00 |
| 19 | 8.20 | 246 | horn_creak | leather strap creak: horn flipped upside down | -16 | -22.0 | square | +0.15 |
| 20 | 8.20 | 246 | murmur_low (bed) | murmur drops, held breath (behind the horn close-up) | -30 | -30.0 | square | +0.00 |
| 21 | 8.33 | 250 | horn_tap | hollow tap on the empty powder horn 1/2 | -12 | -18.0 | square | +0.15 |
| 22 | 8.45 | 254 | horn_tap | hollow tap on the empty powder horn 2/2 | -12 | -18.0 | square | +0.15 |
| 23 | 8.47 | 254 | musket_lower | muskets lowering in a wave: wood clunks | -12 | -18.0 | square | +0.00 |
| 24 | 8.52 | 256 | ohh | disappointed crowd 'ohhh' (non-verbal) | -10 | -16.0 | square | +0.00 |
| 25 | 8.60 | 258 | grain_tick | one single grain ticks out - then the comic empty pause | -22 | -28.0 | square | +0.15 |
| 26 | 8.87 | 266 | cart_steps (bed) | carters walking beside the cart | -30 | -30.0 | square | +0.00 |
| 27 | 8.87 | 266 | cart_wheels (bed) | flashback: cart wheels on the quay cobbles, axle creaks, harness jingle | -22 | -22.0 | square | +0.00 |
| 28 | 8.87 | 266 | river_lap (bed) | river lapping along the quay | -32 | -32.0 | square | +0.00 |
| 29 | 10.13 | 304 | barrel_knock | barrels knock together on the cart | -10 | -16.0 | square | -0.20 |
| 30 | 10.45 | 314 | barrel_roll | powder barrels rolled off the cart into the fortress | -14 | -20.0 | square | +0.25 |
| 31 | 10.83 | 325 | gate_amb (bed) | inside the gate: stone echo ambience, a few steps | -30 | -30.0 | stone | +0.00 |
| 32 | 11.83 | 355 | gate_slam | HEAVY GATE DOORS SLAM + bolt clank (f355) | -1 | -7.0 | stone | +0.00 |
| 33 | 12.33 | 370 | murmur_back (bed) | crowd murmur back in colour (Invalides) | -20 | -20.0 | square | +0.00 |
| 34 | 12.40 | 372 | heads_swish | heads turn: collective clothing swish | -12 | -18.0 | square | +0.00 |
| 35 | 12.83 | 385 | whip_whoosh | whip-pan whoosh | -9 | -15.0 | square | +0.00 |
| 36 | 13.45 | 404 | siege_bed (bed) | siege: crowd roar + distant cartoon musket pops from the towers every 0.3-0.5 s | -16 | -16.0 | square | +0.00 |
| 37 | 13.50 | 405 | musket_pop | crowd musket pop (mid distance) | -12 | -18.0 | square | -0.40 |
| 38 | 13.77 | 413 | musket_pop | crowd musket pop (mid distance) | -12 | -18.0 | square | +0.35 |
| 39 | 14.20 | 426 | musket_pop_close | close musket pop + powder-puff whoomph (cartoon, nobody hit) | -8 | -14.0 | square | +0.30 |
| 40 | 14.37 | 431 | musket_pop_close | close musket pop + powder-puff whoomph (cartoon, nobody hit) | -8 | -14.0 | square | -0.20 |
| 41 | 14.53 | 436 | musket_pop_close | close musket pop + powder-puff whoomph (cartoon, nobody hit) | -8 | -14.0 | square | +0.10 |
| 42 | 14.85 | 446 | tower_wind (bed) | wind on the tower top (roar fades under it) | -26 | -26.0 | square | +0.00 |
| 43 | 15.23 | 457 | cloth_flutter | white cloth flutters | -14 | -20.0 | square | +0.20 |
| 44 | 15.60 | 468 | chain_run | DRAWBRIDGE CHAIN RUN: heavy ratchet rattle accelerating (f468-479) | -5 | -11.0 | square | -0.20 |
| 45 | 15.97 | 479 | drawbridge_slam | DRAWBRIDGE SLAMS DOWN + dust whoomph (f479) | +0 | -6.0 | square | +0.00 |
| 46 | 16.10 | 483 | surge_roar | crowd surge roar | -8 | -14.0 | square | +0.00 |
| 47 | 16.15 | 485 | running_feet (bed) | running feet over the drawbridge | -18 | -18.0 | square | +0.00 |
| 48 | 16.40 | 492 | arch_rush | inside the gate: the crowd rushes past the lens left and right (stone arch) | -8 | -14.0 | stone | +0.00 |
| 49 | 17.13 | 514 | caps_cheer | caps thrown: whoosh + cheer peak | -6 | -12.0 | stone | +0.00 |
| 50 | 17.67 | 530 | awkward_murmur (bed) | courtyard: the roar drops to an awkward murmur, then hush (18.33) | -20 | -20.0 | stone | +0.00 |
| 51 | 18.33 | 550 | court_air (bed) | empty courtyard air, soft stone room tone | -36 | -36.0 | square | +0.00 |
| 52 | 18.33 | 550 | shuffle | hush: shuffling feet on the courtyard stones | -16 | -22.0 | stone | +0.00 |
| 53 | 19.03 | 571 | coins | a forger's coins tinkle out: 12 small bounces | -12 | -18.0 | stone | +0.20 |
| 54 | 19.73 | 592 | wander_step | a 'madman' wanders: footstep 1/2 | -16 | -22.0 | stone | -0.25 |
| 55 | 20.03 | 601 | wander_step | a 'madman' wanders: footstep 2/2 | -16 | -22.0 | stone | -0.05 |
| 56 | 20.33 | 610 | cuff_tug | fabric tug at a cuff | -18 | -24.0 | stone | +0.10 |
| 57 | 20.60 | 618 | cuff_tug | fabric tug at a cuff | -18 | -24.0 | stone | +0.10 |
| 58 | 20.85 | 626 | cuff_tug | fabric tug at a cuff | -18 | -24.0 | stone | +0.10 |
| 59 | 21.33 | 640 | portrait_tap | small wood tap (portrait) | -16 | -22.0 | stone | +0.00 |
| 60 | 21.93 | 658 | cheer_back (bed) | crowd cheer back up on the square | -16 | -16.0 | square | +0.00 |
| 61 | 21.93 | 658 | march_steps (bed) | brisk march of the barrel carriers | -24 | -24.0 | square | +0.00 |
| 62 | 22.28 | 668 | hup | 'hup!' as the barrels are hoisted (non-verbal grunt) + cheer | -8 | -14.0 | square | +0.00 |
| 63 | 23.07 | 692 | setdown | barrel set-down thud 1/7 | -10 | -16.0 | square | -0.60 |
| 64 | 23.13 | 694 | setdown | barrel set-down thud 2/7 | -10 | -16.5 | square | -0.40 |
| 65 | 23.17 | 695 | setdown | barrel set-down thud 3/7 | -11 | -17.0 | square | -0.20 |
| 66 | 23.20 | 696 | barrel_roll2 | a barrel rolled across the cobbles | -14 | -20.0 | square | +0.35 |
| 67 | 23.23 | 697 | setdown | barrel set-down thud 4/7 | -12 | -17.5 | square | +0.00 |
| 68 | 23.25 | 698 | chain_thump | barrel swung down the human chain: hollow thump | -14 | -20.0 | square | +0.50 |
| 69 | 23.27 | 698 | setdown | barrel set-down thud 5/7 | -12 | -18.0 | square | +0.20 |
| 70 | 23.33 | 700 | setdown | barrel set-down thud 6/7 | -12 | -18.5 | square | +0.40 |
| 71 | 23.37 | 701 | setdown | barrel set-down thud 7/7 | -13 | -19.0 | square | +0.60 |
| 72 | 23.43 | 703 | whoosh_cam | camera whoosh | -12 | -18.0 | square | +0.00 |
| 73 | 23.55 | 706 | chain_thump | barrel swung down the human chain: hollow thump | -14 | -20.0 | square | +0.20 |
| 74 | 23.82 | 715 | chain_thump | barrel swung down the human chain: hollow thump | -14 | -20.0 | square | -0.10 |
| 75 | 24.05 | 722 | chain_thump | barrel swung down the human chain: hollow thump | -14 | -20.0 | square | -0.40 |
| 76 | 24.13 | 724 | quiet_square (bed) | flashback: quiet square, birds | -30 | -30.0 | square | +0.00 |
| 77 | 25.77 | 773 | shouting | muffled non-verbal yelling from the high barred window (stone echo) | -14 | -20.0 | stone | -0.35 |
| 78 | 26.07 | 782 | gasp | passers-by gasp | -14 | -20.0 | square | +0.20 |
| 79 | 27.47 | 824 | basket_drop | basket drops, a hat hops | -10 | -16.0 | square | +0.30 |
| 80 | 28.00 | 840 | guard_steps | guards' footsteps on the drawbridge planks | -14 | -20.0 | square | +0.00 |
| 81 | 28.80 | 864 | final_roar | huge crowd roar, back to colour | -4 | -10.0 | square | +0.00 |
| 82 | 28.80 | 864 | final_steps (bed) | marching carriers | -22 | -22.0 | square | +0.00 |
| 83 | 28.85 | 866 | final_thump | barrel thumps on shoulders | -12 | -18.0 | square | -0.50 |
| 84 | 29.12 | 874 | final_thump | barrel thumps on shoulders | -12 | -18.0 | square | +0.40 |
| 85 | 29.38 | 881 | final_thump | barrel thumps on shoulders | -12 | -18.0 | square | -0.20 |
| 86 | 29.62 | 889 | final_thump | barrel thumps on shoulders | -12 | -18.0 | square | +0.20 |
