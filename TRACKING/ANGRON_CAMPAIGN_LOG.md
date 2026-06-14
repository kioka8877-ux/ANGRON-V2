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
- **Statut** : `STATE_4_GATE` — storyboard Manim généré, attente validation opérateur
- **Observations** :
  - F01 DONE : script_001.md (SANGUIS, session précédente)
  - Audio TTS fourni par opérateur : 49.37s réelles (cible 45s)
  - Whisper non disponible en env sandbox — timestamps synthétiques proportionnels (14 blocs)
  - F02 DONE : prompt_001.md généré (LACERAT via google/gemini-3.1-pro-preview)
  - Prochain : validation storyboard → lancer F03_CRUOR (scene_001.py)
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
| `STATE_9` | Archive + commit final |
| `UPLOADED` | Vidéo uploadée sur YouTube |
| `LIVE` | Vidéo en ligne, collecte métriques |
| `FAILED` | Échec à une étape — voir observations |
