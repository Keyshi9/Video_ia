export const meta = {
  name: 'bastille-short-build',
  description: 'Build the Bastille cartoon short scenes: shot plan, timeline, world/characters/post in sandboxes, merge, verify-and-fix loop, sound bed',
  phases: [
    { title: 'Plan', detail: 'shot plan from script + guide-voice word timings, critiqued and revised' },
    { title: 'Skeleton', detail: 'story.ts timeline, locations contract, first cameras' },
    { title: 'Build', detail: 'world / characters / post in their own sandboxes, sound bed in parallel' },
    { title: 'Merge', detail: 'merge owned files, compile, contact sheets, re-sync sandboxes' },
    { title: 'Verify', detail: 'Opus max look + story verifier, fixes routed to file owners' },
  ],
}

const CTX = `PROJECT CONTEXT (read carefully)
- Windows 11 PC, tools: Bash (Git Bash; HOME there is U:, so always use absolute C:/ paths, never ~) and PowerShell. ffmpeg: C:/Users/pu99cle/AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe (ffprobe next to it). Python 3.13 with numpy.
- Remotion project: C:/Users/pu99cle/remotion-shorts (Remotion 4.0.540, three 0.170, @react-three/fiber 8, postprocessing). Composition id "Bastille", 1080x1920, 30 fps. Main source of this short: src/videos/bastille/ (copied from the skill's bridge template: Bridge.tsx, story.ts, world.ts, build.ts, paint.ts, lights.ts, shade.ts, grade.ts, ink.ts, lensblur.ts, toon.ts, cast.ts, cardshade.ts). Do NOT touch src/videos/bridge or src/videos/revolution.
- The skill (READ ITS SKILL.md, it is the rulebook for look values, camera grammar, readability traps): C:/Users/pu99cle/.claude/skills/cartoon-3d-short/SKILL.md, references in .../references/ (STYLE_BIBLE.md, reports/*.md, frames/*.jpg reference frames 540x960).
- Story: C:/Users/pu99cle/revolution-short/SCRIPT.md (candidate 1 "The Bastille: Stormed for Gunpowder, Not Prisoners" is the APPROVED script; its beats list what we see) and C:/Users/pu99cle/revolution-short/scripts.json (ranked[0]).
- Timing: a GUIDE narration (Piper TTS) public/bastille/voice.wav, word timings public/bastille/words.json (seconds). The user will record their own voice later and match this rhythm, so time shots to these words, ~29.6 s; TOTAL = 900 frames. Visual reactions land 0-3 frames before their word.
- No captions, labels or readable text anywhere in the picture. English only. No gore: muskets/smoke are cartoon, nobody is shown hurt.
- Kenney GLB props are NOT available (public/bridge/kenney is empty; 404s in logs are expected and loadKit just returns fewer items). Build every prop you need procedurally (three.js geometry + painted Canvas2D textures in the existing style).
- Render stills ONLY with: cd C:/Users/pu99cle/remotion-shorts && ENTRY=<entry tsx> node tools/stills.mjs <outPrefix> <f1,f2,...> 0.5   (it queues behind other agents with a lock; one bundle ~40 s, then ~6 s per still; output <outPrefix><f>.jpg, 540x960). Look at your stills with the Read tool. Keep each call to <= 10 frames. Never start a full video render.
- Typecheck: cd C:/Users/pu99cle/remotion-shorts && npx tsc --noEmit 2>&1 | grep "src/videos/<your folder>" . Pre-existing errors in Bridge.tsx ("Element | null") and build.ts getComponent are known and harmless; add no new ones.
- File ownership (only edit the files you own): cam = story.ts | world = build.ts, paint.ts, world.ts, lights.ts, shade.ts | char = toon.ts, cast.ts, cardshade.ts | post = grade.ts, Bridge.tsx, ink.ts, lensblur.ts. Contracts between owners are exported constants in story.ts (SHOTS, LOC locations, crowd/scene modes, DOF, FOREGROUND) and the stage(id, t, b, cam) function in cast.ts called by world.ts. If you need a contract change from another owner, say so in your report instead of editing their file.
- Sandboxes: owner <n> works in src/videos/bastille_<n>/ with entry src/sandboxes/<n>/index.tsx containing exactly:
  import React from "react"; import { Composition, registerRoot } from "remotion"; import { BridgeShort, BRIDGE_FRAMES } from "../../videos/bastille_<n>/Bridge";
  const Root: React.FC = () => <Composition id="Bastille" component={BridgeShort} durationInFrames={BRIDGE_FRAMES} fps={30} width={1080} height={1920} />; registerRoot(Root);
- Your final message is returned to an orchestrator: keep it <= 200 words, factual: what you changed, which frames you checked (paths), open problems, contract requests.`

const PLAN = 'C:/Users/pu99cle/revolution-short/SHOTPLAN.md'

phase('Plan')
await agent(`${CTX}

TASK: write the shot plan for the approved Bastille script to ${PLAN}.
Read SKILL.md, references/STYLE_BIBLE.md, references/reports/motion.md and depth.md, the script beats, words.json, and skim src/videos/bastille/story.ts, cast.ts (stage), world.ts and build.ts (buildTown) so the plan is buildable by extending that code.
The plan must contain:
1. World layout with world coordinates (metres, y up, D0 ground height is 6.0 in story.ts): Paris 1789 - the Bastille (8 round towers, curtain walls, a gate with a drawbridge that can lower, a courtyard visible through the gate, a barred upper window for the Sade flashback), the square in front of it, a separate place with the Invalides-like domed facade where muskets are taken, the street the powder handcart takes, the river/bridge if useful, houses. Reuse what exists (river, quays, town houses, bridge) where it helps and say what to remove (the swing park, mill, church, bridge-collapse machinery not needed).
2. Shot list (8-12 shots for 900 frames) mapped to the script lines with frame ranges from words.json: for each shot, place, light (day / golden) or flashback (sepia grade), cast and what each group does, props, fx (smoke puffs, white cloth, dust), camera keys following the skill grammar (cuts on big jumps, 18-40 f smootherstep glides, every hold creeps 0.15-0.35%/f, 4-5 deg rolls, impact kicks), DOF values, foreground props.
3. Cast list: costumes for 1789 Parisians (sans-culottes with phrygian caps or tricornes and cockades, women with bonnets, Gardes françaises in blue coats, Invalides soldiers, governor de Launay in white uniform and wig, the 7 prisoners: 4 forgers with inky fingers, 2 wild-haired madmen, 1 count in a powdered wig; the Marquis de Sade in a wig at the barred window), expressions per beat, poses and hand props (musket, empty powder horn, barrel carried, lantern).
4. Sound event table (time, event) for the sound designer (crowd, muskets popping, drawbridge chain, cheering, barrels rolling, march drum music).
5. A "contracts" section: the exact exported names story.ts will provide (SHOTS fields incl. scene mode per shot, LOC object with named world points, flashback flag), so world/char/post owners can build in parallel.
Respect the readability traps in SKILL.md. Keep it buildable in a few hours by one agent per owner. Write the file, then return a 150-word summary.`, { label: 'plan:draft', phase: 'Plan' })

const critique = await agent(`${CTX}

TASK: critique the shot plan at ${PLAN} as (a) the skill's director (story readability without captions: can a viewer with the sound OFF follow "they wanted the powder, not the prisoners"?), (b) the camera grammar in SKILL.md / motion.md, (c) buildability in this codebase in a few hours (flag anything too costly: horses, complex interiors, many unique characters), (d) historical fit with the script facts. Return a numbered list of concrete changes (max 15), most important first. Do not edit files.`, { label: 'plan:critic', phase: 'Plan' })

await agent(`${CTX}

TASK: revise the shot plan at ${PLAN} applying the valid points of this critique (ignore ones that conflict with the approved script or the skill rules), and rewrite the file in place. Keep the contracts section exact and complete. Return a 150-word summary of the final plan.

CRITIQUE:
${critique}`, { label: 'plan:revise', phase: 'Plan' })

phase('Skeleton')
const skel = await agent(`${CTX}

ROLE: cam owner. TASK: implement the timeline skeleton in MAIN src/videos/bastille/story.ts following ${PLAN}:
- TOTAL = 900, SHOTS with the plan's fields (scene/crowd mode per shot, light, flashback flag), XFADE (prefer hard cuts; a crossfade means two WebGL canvases at once and crashed our GPU before, so keep XFADE empty), FLASH_AT, the exported LOC locations object and every other contract named in the plan, CAMS per shot following the grammar, KICKS, DOF, FOREGROUND (empty is fine for now).
- Keep every export that other files currently import from story.ts compiling (world.ts, cast.ts, build.ts, Bridge.tsx import bridge-era names such as front, SNAP, PARK, ANCHOR, bridgeState, deckY...): keep them as harmless legacy exports (e.g. bridgeState returns a calm intact state) so the project compiles and renders; the other owners will drop their uses.
- Typecheck, then render one still per shot at 0.5 to out/bastille/skel/x_ via tools/stills.mjs with ENTRY=src/index.tsx and check it renders without errors (the world and cast will still look like the bridge town; that is expected). Cameras will be re-tuned after the world exists.`, { label: 'cam:skeleton', phase: 'Skeleton' })
log('skeleton: ' + String(skel).slice(0, 300))

const OWN = {
  world: 'build.ts, paint.ts, world.ts, lights.ts, shade.ts',
  char: 'toon.ts, cast.ts, cardshade.ts',
  post: 'grade.ts, Bridge.tsx, ink.ts, lensblur.ts',
  cam: 'story.ts',
}
const BRIEF = {
  world: `Build the Paris 1789 world of ${PLAN}: the Bastille (towers, curtain walls, crenellations, gate + drawbridge that story time can lower, courtyard, barred window), the square, the Invalides-like domed facade, streets and houses (reuse the house/facade painters), the powder barrels stacks and handcart, white cloth on a tower, smoke puffs (reuse the chimney smoke sprites idea), per-shot world posing in world.ts driven by SHOTS/LOC. Remove the bridge-collapse machinery, swing park, mill, church where the plan says. Keep the established look values (lights.ts presets, painted textures, ink-friendly geometry). Keep calling stage(id, t, b, cam) from cast.ts.`,
  char: `Build the cast of ${PLAN} in toon.ts/cast.ts: 1789 costumes (phrygian cap with cockade, tricorne, bonnet, Gardes françaises coat, Invalides veteran, governor in white with wig, 4 forgers with ink-black fingers, 2 wild-haired madmen, a count in a powdered wig, Sade in a wig), hand props drawn on the cards (musket, empty powder horn/pouch tipping out nothing, barrel carried or rolled, lantern), expressions per beat, and stage() staging per shot/scene mode using LOC from story.ts (crowds at the Invalides, crowd at the square, the 7 prisoners shuffling out, the parade on shoulders, the human chain passing barrels, guards walking Sade out). Keep the established character look (bean heads, plum ink, 3.5 head-heights, blinks, walk bob, contact shadows, NOINK layer).`,
  post: `Post for ${PLAN}: a sepia/old-print flashback grade for the flashback shots (driven by the SHOTS flashback flag; warm desaturated, slight vignette, still inked; no film grain), make sure the grade switch is per shot with no pop inside a shot, check the composer order and the ink/lens values still hold on the new world, and remove bridge-only post code paths from Bridge.tsx if any. Verify on stills of a normal shot and a flashback shot.`,
  cam: `Re-tune cameras/DOF/FOREGROUND in story.ts so every shot frames its subject per ${PLAN} in the now-built world and cast: readable silhouettes, eyes of the front row in focus on close shots, foreground props in ~1/3 of shots, no lens inside geometry, the camera grammar of SKILL.md.`,
}

const sandboxPrep = (n) => `First (re)create your sandbox: copy every file of MAIN src/videos/bastille/ over src/videos/bastille_${n}/ (cp -f, create it if missing) and write src/sandboxes/${n}/index.tsx as specified. Work only in your sandbox and only on your files (${OWN[n]}). Render stills with ENTRY=src/sandboxes/${n}/index.tsx to out/bastille/${n}/<round>_ . `

phase('Build')
const [buildReports, soundReport] = await Promise.all([
  parallel(['world', 'char', 'post'].map((n) => () => agent(`${CTX}

ROLE: ${n} owner. ${sandboxPrep(n)}
TASK: ${BRIEF[n]}
Iterate: implement, typecheck, render the key frames of the shots you affect (one or two per shot), look at them, fix, repeat until they read clearly. Use round prefix b_.`, { label: `build:${n}`, phase: 'Build' }))),
  agent(`${CTX}

ROLE: sound designer. Work in C:/Users/pu99cle/revolution-short/audio/ (copy the skill's templates/audio/*.py there and adapt; never write into the skill folder). Using the sound event table in ${PLAN} and words.json timings, synthesize: SFX (crowd murmur/cheer, musket pops at a distance, drawbridge chain rattle and thud, barrels rolling, footsteps), an original 18th-century style march (fife and snare drum feel, NOT La Marseillaise or any copyrighted tune) and the mix. Deliver exactly 30.000 s at 48 kHz: music_sfx.wav (no voice, with the music already ducked where the guide voice speaks, standard mix music +3 dB, SFX -6 dB relative to the template defaults), guide_mix.wav (same plus the guide voice public/bastille/voice.wav unchanged), stems, and cues.md. Check loudness with ffmpeg (ebur128) and report it.`, { label: 'sound', phase: 'Build' }),
])
log('build reports in; sound: ' + String(soundReport).slice(0, 200))

const MERGE = (k, owners) => agent(`${CTX}

ROLE: integrator, round ${k}. TASK:
1. Back up MAIN src/videos/bastille/ to C:/Users/pu99cle/remotion-shorts/backup/bastille_r${k}/.
2. For each owner in [${owners.join(', ')}], copy that owner's files from src/videos/bastille_<owner>/ into MAIN (only the owned files, per the ownership list).
3. Typecheck MAIN. If owners' work does not fit together (contract mismatches), make the smallest glue fix in the file of the owner whose side is wrong, and report it.
4. Render a contact set from MAIN (ENTRY=src/index.tsx): for every shot in SHOTS two frames (a third into it and two thirds into it) at 0.5 into out/bastille/r${k}/x_ . Then make one sheet per ~6 frames with ffmpeg (hstack, scale each to 360 wide) at out/bastille/r${k}/sheet_<i>.jpg.
5. Re-sync every sandbox that exists (src/videos/bastille_world, _char, _post, _cam): cp -f MAIN/* into it.
Return: the list of sheet paths and frame paths with their shot ids, typecheck status, and any glue fixes.`, { label: `merge:r${k}`, phase: 'Merge' })

const FIXES = {
  type: 'object',
  properties: {
    scores: { type: 'object', properties: {
      story_readability: { type: 'integer' }, colour: { type: 'integer' }, lighting: { type: 'integer' }, ink: { type: 'integer' },
      textures: { type: 'integer' }, characters: { type: 'integer' }, depth: { type: 'integer' }, composition: { type: 'integer' } } },
    verdict: { type: 'string' },
    fixes: { type: 'array', items: { type: 'object', properties: {
      owner: { type: 'string', enum: ['world', 'char', 'post', 'cam'] }, frames: { type: 'string' }, fix: { type: 'string' } }, required: ['owner', 'fix'] } },
  },
  required: ['scores', 'verdict', 'fixes'],
}

let mergeOut = await MERGE(1, ['world', 'char', 'post'])
let lastVerdict = null
for (let round = 1; round <= 3; round++) {
  phase('Verify')
  const v = await agent(`${CTX}

ROLE: verifier (be demanding, the skill wants an Opus max verdict). Look at the round ${round} contact sheets and frames listed below with the Read tool, compare them against 3-4 reference frames from the skill's references/frames/ and the look targets in SKILL.md, and against ${PLAN} and the script beats. Score each area 0-10 (story_readability = can a viewer follow each beat with the sound off). Then a numbered fix list (max 12, most impactful first), each fix assigned to exactly one owner (world / char / post / cam) with the frame numbers, concrete and buildable. Check the readability traps of SKILL.md (cut-off blobs at frame edges, props reading as something else, flags, text on screen, cameras inside geometry).

MERGE OUTPUT:
${mergeOut}`, { label: `verify:r${round}`, phase: 'Verify', schema: FIXES, effort: 'max' })
  if (!v) break
  lastVerdict = v
  log(`round ${round} scores ${JSON.stringify(v.scores)}`)
  const byOwner = {}
  for (const f of v.fixes) (byOwner[f.owner] ||= []).push(f)
  const owners = Object.keys(byOwner)
  const avg = Object.values(v.scores).reduce((a, b) => a + b, 0) / Math.max(1, Object.values(v.scores).length)
  if (!owners.length || (round > 1 && avg >= 7.5)) break
  phase('Build')
  await parallel(owners.map((n) => () => agent(`${CTX}

ROLE: ${n} owner, fix round ${round}. ${sandboxPrep(n)}
${n === 'cam' ? '' : 'Context of your area: ' + BRIEF[n]}
Apply these verifier fixes (render the listed frames before and after, round prefix f${round}_):
${byOwner[n].map((f, i) => `${i + 1}. [frames ${f.frames || '-'}] ${f.fix}`).join('\n')}`, { label: `fix:r${round}:${n}`, phase: 'Build' })))
  mergeOut = await MERGE(round + 1, owners)
}
return { lastVerdict, mergeOut: String(mergeOut).slice(0, 2000), sound: soundReport }