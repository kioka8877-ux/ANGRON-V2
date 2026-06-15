# ANGRON — TRANSFER LOG

> Journal des transferts inter-frigates.  
> Chaque transfert de fichier entre frigates est consigné ici pour traçabilité et débogage.

---

## FORMAT D'ENTRÉE

```
### [ANGRON-XXX] — TRANSFERT FXX → FYY
- **Date** : YYYY-MM-DD HH:MM
- **Source** : FRIGATE_NOM/OUT/nom_fichier.ext
- **Destination** : FRIGATE_NOM/IN/nom_fichier.ext
- **Taille** : X MB
- **Hash SHA256** : (optionnel)
- **Statut** : OK / FAILED
- **Notes** : —
```

---

## LOG

### [ANGRON-001] — TRANSFERT F01 → F02
- **Date** : 2026-06-14 07:54
- **Source** : F01_SANGUIS/OUT/script_001.md
- **Destination** : F02_LACERAT/IN/ (référence script)
- **Taille** : ~3.6 KB
- **Statut** : OK
- **Notes** : Script généré session précédente. Concept : BOXE LE MYTHE DES GÉANTS, SHORT 45s.

### [ANGRON-001] — TRANSFERT AUDIO → F02
- **Date** : 2026-06-14 07:54
- **Source** : opérateur (TTS externe)
- **Destination** : F02_LACERAT/IN/Generated-Audio-June-14_-2026-8_19AM.mp3
- **Taille** : ~0.8 MB (49.37s MP3)
- **Statut** : OK
- **Notes** : Audio TTS voix opérateur. Durée réelle : 49.37s (cible 45s).

### [ANGRON-001] — TRANSFERT F02 WHISPER → F02 OUT
- **Date** : 2026-06-14 07:54
- **Source** : whisper_sync.py (mode synthétique — Whisper non dispo dans cet env)
- **Destination** : F02_LACERAT/OUT/whisper_timestamps_001.json
- **Taille** : ~3.2 KB (14 blocs, 49.37s)
- **Statut** : OK
- **Notes** : Timestamps proportionnels au nombre de mots. Version 1.0-SYNTHETIC.

### [ANGRON-001] — TRANSFERT F02 LACERAT → F02 OUT
- **Date** : 2026-06-14 07:54
- **Source** : lacerat.py (via AI Gateway google/gemini-3.1-pro-preview)
- **Destination** : F02_LACERAT/OUT/prompt_001.md
- **Taille** : ~10.7 KB (14 blocs Manim storyboardés)
- **Statut** : OK — STATE_4_GATE atteint
- **Notes** : Storyboard complet conforme ANGRON_STYLE v1.0. Aucun asset requis.

---

## ═══════════════════════════════════════════════════════════
## ANGRON V2 — PATTERNS DE TRANSFERT (initié 2026-06-15)
## ═══════════════════════════════════════════════════════════

### FLUX DE TRANSFERT V2 — MODE math_script

```
CONCEPT → F01_SANGUIS
F01_SANGUIS/OUT/script_XXX.md          → F02_LACERAT/IN/
voix_opérateur.mp3                     → F02_LACERAT/IN/voice_XXX.mp3
F02_LACERAT/OUT/scenes.py              → F03_CRUOR/CODEBASE/
F02_LACERAT/OUT/whisper_timestamps.json → F03_CRUOR/IN/
F02_LACERAT/OUT/01_Scene.mp4 ... Nème  → F03_CRUOR/OUT/ (après render par scène)
F03_CRUOR/OUT/staged.mp4               → F04_NAILS/IN/
F02_LACERAT/IN/voice_XXX.mp3           → F04_NAILS/IN/  (audio direct)
F04_NAILS/OUT/nails_out_XXX.mp4        → F05_NUCERIA/IN/
F05_NUCERIA/OUT/youtube_XXX.mp4        → outputs/
```

### FLUX DE TRANSFERT V2 — MODE math_no_script

```
CONCEPT → F01_SANGUIS  (concept visuel, pas de script vocal)
F01_SANGUIS/OUT/script_XXX.md          → F02_LACERAT/IN/
F02_LACERAT/OUT/scenes.py              → F03_CRUOR/CODEBASE/
F03_CRUOR/OUT/staged.mp4               → F04_NAILS/IN/
musique.mp3                            → F04_NAILS/IN/
F04_NAILS/OUT/nails_out_XXX.mp4        → F05_NUCERIA/IN/
F05_NUCERIA/OUT/youtube_XXX.mp4        → outputs/
```

### FLUX DE TRANSFERT V2 — MODE hook

```
URL_CLIP → HOOK_STUDIO/downloader.py → clip_brut.mp4
HOOK_STUDIO/cutter.py → HOOK_STUDIO/OUT/hook_ready.mp4
HOOK_STUDIO/OUT/hook_ready.mp4         → F02_LACERAT/IN/HOOK/hook_ready.mp4
hook_question                          → .angron/ledger.json (écrit au CUT)
F01_SANGUIS/OUT/script_XXX.md          → F02_LACERAT/IN/  (avec contexte hook)
F02_LACERAT/OUT/scenes.py              → F03_CRUOR/CODEBASE/
F03_CRUOR/OUT/staged.mp4               → F04_NAILS/IN/
F02_LACERAT/IN/HOOK/hook_ready.mp4     → F04_NAILS/IN/  (concat en tête)
voix_opérateur.mp3                     → F04_NAILS/IN/  (si math_script)
F04_NAILS/OUT/nails_out_XXX.mp4        → F05_NUCERIA/IN/
F05_NUCERIA/OUT/youtube_XXX.mp4        → outputs/
```

---

## CONVENTION DE NOMMAGE DES FICHIERS — V2

### Nommage V1 (conservé pour compatibilité)

| Type | Convention | Exemple |
|------|-----------|---------|
| Script F01_SANGUIS | `script_XXX.md` | `script_001.md` |
| Voix opérateur | `voice_XXX.mp3` | `voice_001.mp3` |
| Prompt Manim | `prompt_XXX.md` | `prompt_001.md` |
| Timestamps Whisper | `timestamps_XXX.json` | `timestamps_001.json` |
| Asset image | `asset_XXX_description.png` | `asset_001_messi_sprint.png` |
| Code Manim | `scene_XXX.py` | `scene_001.py` |
| Render brut | `cruor_render_XXX.mp4` | `cruor_render_001.mp4` |
| Nails output | `nails_out_XXX.mp4` | `nails_out_001.mp4` |
| Final Short | `youtube_short_XXX.mp4` | `youtube_short_001.mp4` |
| Final Long-form | `youtube_longform_XXX.mp4` | `youtube_longform_001.mp4` |

### Nommage V2 — Nouveautés

| Type | Convention | Exemple |
|------|-----------|---------|
| Scènes multi (F02 OUT) | `scenes_XXX.py` | `scenes_001.py` |
| Renders par scène (F03 OUT) | `NN_NomScene.mp4` (préfixe 2 chiffres) | `01_HookQuestion.mp4` |
| Staged (F03 OUT) | `staged_XXX.mp4` | `staged_001.mp4` |
| Hook source | `hook_ready.mp4` | `hook_ready.mp4` |
| Hook faded | `hook_faded.mp4` | `hook_faded.mp4` |

**Règle de nommage des scènes V2 (obligatoire pour stage.py alphabétique) :**
```
01_HookQuestion.mp4
02_EquationReveal.mp4
03_ProblemBeauty.mp4
04_MathAnswer.mp4
05_BodyApplication.mp4
```

---

## TRANSFERTS PAR FRIGATE — V1 (inchangé)

```
F01_SANGUIS/OUT/   → F02_LACERAT/IN/    script_XXX.md
F02_LACERAT/IN/    → F02_LACERAT/OUT/   prompt_XXX.md + timestamps_XXX.json
F02_LACERAT/OUT/   → F03_CRUOR/IN/      prompt_XXX.md + timestamps_XXX.json + assets
F03_CRUOR/OUT/     → F04_NAILS/IN/      cruor_render_XXX.mp4
F02_LACERAT/IN/    → F04_NAILS/IN/      voice_XXX.mp3  (audio direct)
F04_NAILS/OUT/     → F05_NUCERIA/IN/    nails_out_XXX.mp4
F05_NUCERIA/OUT/   → ./outputs/         youtube_short/longform_XXX.mp4
```

## TRANSFERTS PAR FRIGATE — V2 (additions)

```
[MODE hook seulement]
URL_SOURCE         → HOOK_STUDIO/IN/    (URL yt-dlp)
HOOK_STUDIO/OUT/   → F02_LACERAT/IN/HOOK/  hook_ready.mp4

[Toujours en V2]
F02_LACERAT/OUT/   → F03_CRUOR/CODEBASE/   scenes_XXX.py  (multi-scènes)
F03_CRUOR/OUT/     → F03_CRUOR/OUT/        staged_XXX.mp4 (stage.py assemble les renders)
F03_CRUOR/OUT/     → F04_NAILS/IN/         staged_XXX.mp4 (remplace cruor_render)

[MODE hook — F04_NAILS spécifique]
F02_LACERAT/IN/HOOK/hook_ready.mp4 + F03_CRUOR/OUT/staged_XXX.mp4 → concat → nails_out_XXX.mp4
```

---

## STATUT BUILD DES TRANSFERTS — V1

| Transfert | Script responsable | Statut |
|-----------|-------------------|--------|
| F03→F04 (cruor_render) | `finish.sh` (F04) — `--video` arg | DONE — 2026-06-13 |
| F02→F04 (voice direct) | `finish.sh` (F04) — `--audio` arg | DONE — 2026-06-13 |
| F04→F05 (nails_out) | `nuceria.py` (F05) — `--input` arg | DONE — 2026-06-13 |
| F05→outputs | `nuceria.py` (F05) — `--output` arg | DONE — 2026-06-13 |
| F02→F03 (prompt+timestamps) | `render.sh` (F03) — `--scene` arg | DONE — 2026-06-13 |
| F01→F02 (script) | `whisper_sync.py` (F02) — `--script` arg | DONE — 2026-06-13 |
| CONCEPT→F01 (script gen) | `sanguis.py` (F01) — `--concept` + `--format` args | DONE — 2026-06-13 |

## STATUT BUILD DES TRANSFERTS — V2 (à implémenter)

| Transfert | Script responsable | Statut |
|-----------|-------------------|--------|
| URL→HOOK_STUDIO (download) | `downloader.py` — `download_clip(url, path)` | PENDING |
| HOOK_STUDIO→F02 (hook_ready) | `studio.py` — copie auto au CUT | PENDING |
| F02→F03 (scenes.py multi) | `render.sh` V2 — render par scène | PENDING |
| F03 renders→staged | `stage.py` — concat alphabétique | PENDING |
| F03 staged→F04 | `finish.sh` V2 — `--staged` arg | PENDING |
| hook_ready+staged→concat | `finish.sh` V2 mode hook | PENDING |
