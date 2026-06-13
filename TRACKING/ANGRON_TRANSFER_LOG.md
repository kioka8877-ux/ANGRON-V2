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

*(Aucun transfert enregistré — en attente du premier cycle de production)*

---

## CONVENTION DE NOMMAGE DES FICHIERS

| Type | Convention | Exemple |
|------|-----------|---------|
| Script SANGUIS | `script_XXX.md` | `script_001.md` |
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
SANGUIS/OUT/   → LACERAT/IN/    script_XXX.md
LACERAT/IN/    → LACERAT/OUT/   prompt_XXX.md + timestamps_XXX.json
LACERAT/OUT/   → CRUOR/IN/      prompt_XXX.md + timestamps_XXX.json + assets
CRUOR/OUT/     → NAILS/IN/      cruor_render_XXX.mp4
LACERAT/IN/    → NAILS/IN/      voice_XXX.mp3  (audio direct)
NAILS/OUT/     → NUCERIA/IN/    nails_out_XXX.mp4
NUCERIA/OUT/   → ./outputs/     youtube_short/longform_XXX.mp4
```
