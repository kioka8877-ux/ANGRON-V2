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

## CONVENTION DE NOMMAGE DES FICHIERS

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

---

## TRANSFERTS PAR FRIGATE

```
F01_SANGUIS/OUT/   → F02_LACERAT/IN/    script_XXX.md
F02_LACERAT/IN/    → F02_LACERAT/OUT/   prompt_XXX.md + timestamps_XXX.json
F02_LACERAT/OUT/   → F03_CRUOR/IN/      prompt_XXX.md + timestamps_XXX.json + assets
F03_CRUOR/OUT/     → F04_NAILS/IN/      cruor_render_XXX.mp4
F02_LACERAT/IN/    → F04_NAILS/IN/      voice_XXX.mp3  (audio direct)
F04_NAILS/OUT/     → F05_NUCERIA/IN/    nails_out_XXX.mp4
F05_NUCERIA/OUT/   → ./outputs/         youtube_short/longform_XXX.mp4
```

---

## STATUT BUILD DES TRANSFERTS

| Transfert | Script responsable | Statut |
|-----------|-------------------|--------|
| F03→F04 (cruor_render) | `finish.sh` (F04) — `--video` arg | DONE — 2026-06-13 |
| F02→F04 (voice direct) | `finish.sh` (F04) — `--audio` arg | DONE — 2026-06-13 |
| F04→F05 (nails_out) | `nuceria.py` (F05) — `--input` arg | DONE — 2026-06-13 |
| F05→outputs | `nuceria.py` (F05) — `--output` arg | DONE — 2026-06-13 |
| F02→F03 (prompt+timestamps) | `render.sh` (F03) — `--scene` arg | DONE — 2026-06-13 |
| F01→F02 (script) | `whisper_sync.py` (F02) — `--script` arg | DONE — 2026-06-13 |
| CONCEPT→F01 (script gen) | `sanguis.py` (F01) — `--concept` + `--format` args | DONE — 2026-06-13 |
