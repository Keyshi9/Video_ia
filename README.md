# Short « Bastille » : état du projet et reprise

Arrêté le 2026-11-03 vers 14 h 20, en pleine phase de construction. Ce fichier sert à reprendre sur un autre PC, avec ou sans Claude Code.

## Contenu du dépôt

| Dossier | Contenu |
| --- | --- |
| `remotion-shorts/` | Projet Remotion (sans `node_modules`) |
| `revolution-short/` | Script, plan de plans, voix guide, son |

Le skill n'est **pas** dans ce dépôt : ses images de référence ne doivent pas être publiées. Récupère-le depuis le dépôt d'origine (voir l'installation).

## Ce qui est fait

1. **Script validé** : « The Bastille: Stormed for Gunpowder, Not Prisoners », en anglais, ~100 mots. Les faits et les sources sont dans `revolution-short/SCRIPT.md` (candidat 1).
2. **Voix guide** (Piper, voix `en_US-ryan-high`) : `revolution-short/voice/voice.wav`, 29,6 s. Les horodatages des mots sont dans `voice/words.json`, recopiés dans `remotion-shorts/public/bastille/`. Elle sert seulement au timing : l'utilisateur enregistrera sa propre voix.
3. **Plan de plans v2** : `revolution-short/SHOTPLAN.md`. 11 plans sur 900 images (30 s, 30 fps), les plans 4 et 10 sont des flashbacks sépia. Il contient la disposition du monde avec ses coordonnées, le casting, la table des sons et les contrats entre fichiers.
4. **Timeline** : `remotion-shorts/src/videos/bastille/story.ts` (plans, objet `LOC`, caméras, profondeur de champ). Elle compile et rend.
5. **Post-production, terminée** dans le sandbox `src/videos/bastille_post/` : `grade.ts` (préréglage `GRADE_SEPIA`) et `Bridge.tsx`. **Pas encore fusionnée** dans `src/videos/bastille/`.
6. **Son, livré** : `revolution-short/audio/`
   - `music_sfx.wav` : musique et bruitages sans voix, 30 s, 48 kHz ;
   - `guide_mix.wav` : le même avec la voix guide ;
   - les pistes séparées (stems) et `cues.md`.
   À réécouter. Le niveau sonore (loudness) n'a pas été vérifié.

## Ce qui est en cours, à terminer

- **Monde** (sandbox `src/videos/bastille_world/`) : `build.ts` et `paint.ts` ont été commencés (Bastille, place, etc.). `world.ts`, `lights.ts` et `shade.ts` n'ont pas encore été touchés.
- **Personnages** (sandbox `src/videos/bastille_char/`) : seul `toon.ts` a été commencé (costumes). `cast.ts`, qui gère la mise en scène des foules par plan, n'a pas été fait.
- Ensuite :
  1. fusionner les sandboxes dans `src/videos/bastille/` ;
  2. faire les planches contact ;
  3. faire 2 ou 3 tours de vérification et de correction ;
  4. rendre la vidéo finale ;
  5. passer le contrôle qualité (`scripts/short_qa.py`).

Les fichiers modifiés dans un sandbox ne sont pas forcément cohérents entre eux, puisque le travail a été coupé en cours. Il faut lancer `tsc` avant de fusionner.

## Installation sur le nouveau PC

1. Node 24, Python 3.13, Google Chrome (dans `C:/Program Files/Google/Chrome/Application/`), et ffmpeg (`winget install Gyan.FFmpeg`).
2. Installer le skill : `git clone https://github.com/mromidev/claude-animated-shorts.git %USERPROFILE%\.claude\skills\cartoon-3d-short`.
3. Dans `remotion-shorts/` : `npm install`. Puis copier `templates/scripts/*` et `templates/audio/*` du skill dans `remotion-shorts/scripts/` et `remotion-shorts/audio/` s'ils manquent. Les versions sont figées dans `package.json` : three 0.170, Remotion 4.0.540, `@react-three/fiber` 8.
4. Si tu as besoin de refaire la voix : `pip install --user piper-tts==1.3.0 faster-whisper==1.1.1`, puis télécharger la voix depuis `https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/high/en_US-ryan-high.onnx` (et le `.onnx.json`) dans `remotion-shorts/voices/`.
5. Variable d'environnement : `REMOTION_TMP` doit pointer vers un dossier sur un disque avec de la place.
6. Les chemins `C:/Users/pu99cle/...` sont écrits en dur dans `tools/stills.mjs`, `tools/bastille-build-workflow.js` et `revolution-short/voice/build_voice.py`. Sur un autre compte Windows, il faut les adapter.

## Outils

- `node tools/stills.mjs out/bastille/x_ 100,400 0.5` : rend des images fixes. On choisit la composition avec `ENTRY=src/sandboxes/<n>/index.tsx` et `COMP=Bastille`. Un verrou fait passer les rendus un par un.
- `python tools/words.py voix.wav words.json` : horodatage des mots (pour recaler les plans sur ta propre voix).
- Rendu final, sans fondus enchaînés (deux contextes WebGL en même temps font planter un GPU intégré) et avec `--concurrency=2` (sinon Chrome manque de mémoire) :
  `npx remotion render Bastille out/bastille/video.mp4 --codec h264 --crf 16 --gl=angle --concurrency=2`
- `tools/bastille-build-workflow.js` : le workflow Claude Code utilisé (plan, squelette, construction, fusion, vérification). Pour reprendre, demander à Claude Code de le relire et de le relancer en sautant les phases Plan et Squelette, qui sont déjà faites.

## Pièges rencontrés

- three 0.160 rend un écran vide, car `NeutralToneMapping` n'existe qu'à partir de r162.
- Remotion 4.0.250 plante sous Node 24 : il faut la version 4.0.540.
- Le bloc `XFADE` doit rester vide (fondus enchaînés, voir plus haut).
- Les modèles 3D Kenney sont absents (`public/bridge/kenney/` est vide). kenney.nl refuse les téléchargements automatiques : il faut les télécharger à la main (Nature Kit, Fantasy Town Kit) si on en veut. Sinon les accessoires sont construits en code.
