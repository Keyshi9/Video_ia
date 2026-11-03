export const meta = {
  name: 'revolution-short-script',
  description: 'Find true French Revolution stories, draft 20-30 s scripts, fact-check adversarially, pick the best',
  phases: [
    { title: 'Research', detail: 'three angles of surprising true stories, with sources' },
    { title: 'Shortlist', detail: 'pick the 3 strongest topics' },
    { title: 'Draft', detail: 'one writer per topic, beat formula' },
    { title: 'Verify', detail: 'fact skeptic + visual feasibility critic per script' },
    { title: 'Final', detail: 'rank and fix the scripts' },
  ],
}

const SKILL_RULES = `Context: we make a vertical animated story short (2D bean-head cartoon characters in a colourful 3D storybook world, rendered with three.js; style "Cartoon 3D story short").
Target: 20-30 seconds of English voice-over at ~3.7 words/s (so 75-105 words). No captions or labels on screen.
Rules: one surprising TRUE story with a physical, visual cause and effect. Jokes must be researched real facts. Story, characters and voice are original. Never describe on screen what the viewer already sees. One steady narrator tone.
Beat formula (compressed for ~25 s): Hook (the absurd fact in one line) -> Setting (year, place) -> Action escalating in 2-3 beats -> Snap (the moment it turns) -> Deadpan double line ("Luckily... / Unluckily...") -> one-line explanation / consequence -> Callback twist ending.
What the 3D world can show cheaply: an 18th-century town with houses, streets, a river, a bridge, a stone fortress, crowds of cartoon people (costumes: tricorne, bonnet, phrygian cap, wigs, uniforms), carriages built from simple shapes, flags, simple props (coins, papers, lanterns). Hard: interiors with many details, battles with physics, horses (possible but costly), close photo-real faces.`

const CAND = {
  type: 'object',
  properties: {
    candidates: { type: 'array', items: { type: 'object', properties: {
      title: { type: 'string' },
      hook: { type: 'string', description: 'the absurd fact in one line' },
      story: { type: 'string', description: '3-6 sentence summary of what happened' },
      visual_cause_effect: { type: 'string' },
      facts: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source: { type: 'string', description: 'URL or precise reference' } }, required: ['claim', 'source'] } },
      myths_to_avoid: { type: 'string', description: 'popular but false versions of this story' },
    }, required: ['title', 'hook', 'story', 'visual_cause_effect', 'facts', 'myths_to_avoid'] } },
  },
  required: ['candidates'],
}

const ANGLES = [
  { key: 'absurd', brief: 'absurd, funny or ironic true episodes of the French Revolution (1789-1799) that sound made up but are documented' },
  { key: 'physical', brief: 'French Revolution episodes driven by a concrete physical object or mechanism (a coin, a door, a clock, a carriage, a bridge, a measurement, bread, weather) where one physical thing caused a big consequence' },
  { key: 'iconic', brief: 'little-known true details hiding inside the most famous French Revolution events (Bastille, Varennes, Tennis Court Oath, Women\'s March on Versailles, the calendar, the metric system) that overturn what most people believe' },
]

phase('Research')
const research = await parallel(ANGLES.map(a => () => agent(
  `${SKILL_RULES}\n\nResearch task: find 3 candidate stories about ${a.brief}. Use WebSearch/WebFetch (load them with ToolSearch "select:WebSearch,WebFetch") and give a real source for every fact (prefer encyclopedias, museums, academic or reputable history sites). Flag popular myths that must NOT be presented as fact. Prefer stories whose cause and effect can be shown visually in the world described above.`,
  { label: `research:${a.key}`, phase: 'Research', schema: CAND })))
const all = research.filter(Boolean).flatMap(r => r.candidates)
log(`${all.length} candidate stories found`)

phase('Shortlist')
const SHORT = { type: 'object', properties: { picks: { type: 'array', items: { type: 'object', properties: { index: { type: 'integer' }, why: { type: 'string' } }, required: ['index', 'why'] } } }, required: ['picks'] }
const short = await agent(
  `${SKILL_RULES}\n\nHere are candidate stories (JSON, indexed from 0):\n${JSON.stringify(all.map((c, i) => ({ i, ...c })), null, 1)}\n\nPick the 3 strongest for a viral 20-30 s short: surprise of the hook, strength of the visual cause-effect, how well documented it is (avoid myth-dependent stories), and how cheaply the 3D world can show it. Return their indexes, best first, with a one-line reason each. Pick 3 different stories.`,
  { label: 'shortlist', phase: 'Shortlist', schema: SHORT })
const picks = (short?.picks ?? []).slice(0, 3).map(p => ({ ...all[p.index], why: p.why })).filter(p => p.title)

const SCRIPT = { type: 'object', properties: {
  title: { type: 'string' },
  script: { type: 'string', description: 'the full voice-over, one line per beat' },
  word_count: { type: 'integer' },
  beats: { type: 'array', items: { type: 'object', properties: { beat: { type: 'string' }, line: { type: 'string' }, picture: { type: 'string', description: 'what we SEE (not what is said): place, characters, action, camera' } }, required: ['beat', 'line', 'picture'] } },
  facts_used: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, source: { type: 'string' } }, required: ['claim', 'source'] } },
}, required: ['title', 'script', 'word_count', 'beats', 'facts_used'] }
const VERDICT = { type: 'object', properties: {
  score: { type: 'integer', description: '0-10' },
  problems: { type: 'array', items: { type: 'object', properties: { claim_or_beat: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' }, evidence: { type: 'string' } }, required: ['claim_or_beat', 'issue', 'fix'] } },
}, required: ['score', 'problems'] }

const verified = await pipeline(picks,
  (c) => agent(
    `${SKILL_RULES}\n\nWrite the script for this story:\n${JSON.stringify(c, null, 1)}\n\nEnglish, 75-105 words, follow the beat formula, punchy deadpan humour from real facts only, no invented quotes, no myths stated as fact. For every beat give what we see on screen (must be showable in the world described). List every factual claim the script makes with its source.`,
    { label: `draft:${c.title}`, phase: 'Draft', schema: SCRIPT }),
  (s, c) => parallel([
    () => agent(`You are a skeptical historian. Try to REFUTE every factual claim in this short-video script about the French Revolution. Check each claim against reliable sources with WebSearch/WebFetch (load via ToolSearch "select:WebSearch,WebFetch"): dates, numbers, names, who did what, and whether "facts" are actually legends (e.g. disputed anecdotes). Also flag claims that are true but misleadingly framed. Default to flagging when the evidence is weak. Score 10 = every claim solid.\n\nSCRIPT:\n${JSON.stringify(s, null, 1)}`,
      { label: `facts:${c.title}`, phase: 'Verify', schema: VERDICT }),
    () => agent(`${SKILL_RULES}\n\nYou are the director. Critique this script for a 20-30 s short: hook strength in the first 2 s, rhythm, word count (75-105), whether each line adds something the picture does not already show, whether the ending lands, and whether every beat's picture is buildable in the described 3D world. Score 10 = ready to produce. Give concrete fixes.\n\nSCRIPT:\n${JSON.stringify(s, null, 1)}`,
      { label: `director:${c.title}`, phase: 'Verify', schema: VERDICT }),
  ]).then(([facts, dir]) => ({ script: s, facts, director: dir, why: c.why, myths: c.myths_to_avoid })))

phase('Final')
const FINAL = { type: 'object', properties: { ranked: { type: 'array', items: SCRIPT }, notes: { type: 'string' } }, required: ['ranked', 'notes'] }
const final = await agent(
  `${SKILL_RULES}\n\nBelow are draft scripts, each with a skeptical fact-check and a director critique. Rewrite each script applying every valid fix (drop or reword any claim the fact-check found weak or legendary; never keep a myth as fact), keep 75-105 words, then rank them best first. In notes, list for each script: final score estimate, what was changed, and any remaining caveat about historical accuracy.\n\n${JSON.stringify(verified.filter(Boolean), null, 1)}`,
  { label: 'final', phase: 'Final', schema: FINAL })
return final