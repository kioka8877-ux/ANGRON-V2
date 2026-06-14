# ANGRON — CAMPAIGN LOG

> Journal de production de la flotte ANGRON.  
> Chaque vidéo produite est consignée ici avec son état, ses métriques et ses observations.

---

## ÉTAT DU CODEBASE

| Frigate | Script principal | Statut build |
|---------|-----------------|--------------|
| F01_SANGUIS | `sanguis.py` | DONE — 2026-06-13 |
| F02_LACERAT | `whisper_sync.py` + `lacerat.py` | DONE — 2026-06-13 |
| F03_CRUOR | `render.sh` | DONE — 2026-06-13 |
| F04_NAILS | `finish.sh` | DONE — 2026-06-13 |
| F05_NUCERIA | `nuceria.py` | DONE — 2026-06-13 |
| ORCHESTRATEUR | `angron.py` | DONE — 2026-06-14 |

---

## CORRECTIONS APPLIQUÉES — 2026-06-14

| Fichier | Problème | Correction |
|---------|---------|------------|
| `angron.py` | Stub minimal — pas d'orchestration réelle | Reconstruit complet : `init`, `update`, `dispatch`, `commit_ledger`, `archive` |
| `F01_SANGUIS/CODEBASE/sanguis.py` | META_SANGUIS hardcodé inline (version tronquée) | Charge depuis `METAPROMPTS/META_SANGUIS.md` avec fallback |
| `F02_LACERAT/CODEBASE/lacerat.py` | META_LACERAT hardcodé inline (version tronquée) | Charge depuis `METAPROMPTS/META_LACERAT.md` avec fallback |
| `METAPROMPTS/META_LACERAT.md` | Chemin bug ligne 617 : `CRUOR/CODEBASE/whisper_sync.py` | Corrigé → `F02_LACERAT/CODEBASE/whisper_sync.py` |
| `angron.py` | STATE_8 ne appelait pas `archive_projet()` | Auto-archive atomique : STATE_9 + archive en une seule opération |
| `nuceria-final.yml` | Inline Python fragile pour ledger — pas d'archive | Remplacé par `angron.py update` + `angron.py archive` |

---

## FORMAT D'ENTRÉE

```
### [ANGRON-XXX] — NOM DU CONCEPT
- **Date** : YYYY-MM-DD
- **Format** : Short 9:16 / Long-form 16:9
- **Concept** : description courte
- **Durée vidéo** : Xs
- **Statut** : F01_SANGUIS → F02_LACERAT → F03_CRUOR → F04_NAILS → F05_NUCERIA → UPLOAD → LIVE
- **Observations** : notes opérateur
- **Performances** : vues / likes / rétention (à remplir post-upload)
```

---

## LOG

### [ANGRON-001] — BOXE : LE MYTHE DES GÉANTS
- **Date** : 2026-06-14
- **Format** : Short 9:16 (1080x1920)
- **Concept** : Un boxeur court a la même puissance de frappe et plus d'agilité qu'un boxeur grand — la physique le prouve
- **Durée audio** : 49.37s
- **Statut** : `UPLOADED — EN LIGNE`
- **Fichier final** : `F05_NUCERIA/OUT/youtube_short_001.mp4` (1.73 MB)
- **QA** : OK — aucun fingerprint détecté
- **Observations** :
  - F01 DONE : script_001.md
  - F02 DONE : timestamps synthétiques (14 blocs, 49.37s) + prompt_001.md (Gemini 3.1 Pro)
  - F03 DONE : cruor_render_001.mp4 (568 KB, Manim)
  - F04 DONE : nails_out_001.mp4 (1.68 MB, FFmpeg fusion audio/vidéo) — 2026-06-14T11:23:24Z
  - F05 DONE : youtube_short_001.mp4 (1.73 MB, H264 CRF18 + loudnorm + wipe métadonnées) — 2026-06-14T11:42:12Z
  - Ledger archivé : videos_produites=1, cycles_complets=1
- **Performances** : — (à remplir post-upload)

---

## LÉGENDE STATUTS

| Statut | Signification |
|--------|---------------|
| `INIT` | Projet créé, aucune frigate lancée |
| `STATE_2` | SANGUIS en cours |
| `STATE_2_GATE` | Script généré — attente validation opérateur |
| `STATE_3` | Whisper en cours |
| `STATE_4` | LACERAT storyboard en cours |
| `STATE_4_GATE` | Storyboard généré — attente validation opérateur |
| `STATE_5` | CRUOR génère scene_XXX.py |
| `STATE_6` | Render Docker en cours |
| `STATE_6_GATE` | Vidéo brute prête — attente validation opérateur |
| `STATE_7` | NAILS fusion audio/vidéo |
| `STATE_8` | NUCERIA camouflage |
| `STATE_9` | Archive + commit final (automatique) |
| `UPLOADED` | Vidéo uploadée sur YouTube |
| `LIVE` | Vidéo en ligne, collecte métriques |
| `FAILED` | Échec à une étape — voir observations |
