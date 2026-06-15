# ANGRON — CAMPAIGN LOG

> Journal de production de la flotte ANGRON.  
> Chaque vidéo produite est consignée ici avec son état, ses métriques et ses observations.

---

## ÉTAT DU CODEBASE — V1 (production stable)

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

## ═══════════════════════════════════════════════════════════
## ANGRON V2 — PLAN DE MUTATION (initié 2026-06-15)
## Repo V2 : https://github.com/kioka8877-ux/ANGRON-V2
## V1 reste intact et production-ready — V2 est le fork évolutif
## ═══════════════════════════════════════════════════════════

### ÉTAT DU CODEBASE — V2 (en cours de mutation)

| Frigate | Upgrade V2 | Statut |
|---------|-----------|--------|
| F01_SANGUIS | Arc narratif 3B1B : 5 segments chronométrés + marqueurs [ANIM:] obligatoires | PENDING |
| F02_LACERAT | manimgl (`from manimlib import *`) + multi-scènes + mode hook | PENDING |
| F03_CRUOR | manimgl + `InteractiveScene` + render par scène + `stage.py` | PENDING |
| F04_NAILS | Mode hook : concat clip réel + manim + fade audio | PENDING |
| F05_NUCERIA | Inchangée — déjà production-ready | OK |
| HOOK_STUDIO | NOUVEAU : Streamlit + yt-dlp + FFmpeg cutter | PENDING |
| ORCHESTRATEUR | 3 modes (`math_script` / `math_no_script` / `hook`) + ledger V2 | PENDING |
| DOCKERFILE | `pip install manimgl yt-dlp streamlit` (remplace `manim`) | PENDING |

---

### UPGRADES DÉTAILLÉS V2

#### UPGRADE 1 — DOCKERFILE V2
- **Supprimer** : `RUN pip install manim`
- **Ajouter** : `RUN pip install manimgl yt-dlp streamlit`
- **Vérifier** : `fonts-cmu` déjà présent

#### UPGRADE 2 — F01_SANGUIS : ARC 3B1B
Nouveau arc narratif obligatoire pour Shorts (60s) :
```
[7s]  HOOK ÉMOTIONNEL       → Ce que le spectateur ressent déjà
[8s]  QUESTION FORCE        → "Mais comment est-ce mathématiquement possible ?"
[15s] BEAUTÉ DU PROBLÈME    → Poser l'équation avec élégance, ne pas encore expliquer
[20s] INÉVITABILITÉ         → Dérouler le raisonnement, chaque étape évidente en rétroaction
[10s] APPLICATION INCARNÉE  → Retour monde réel, fin émotionnelle
```
Marqueurs [ANIM:] obligatoires dans le script (ex: `[ANIM: plan_initial]`, `[ANIM: equation_tsiolkovsky]`).

#### UPGRADE 3 — F02_LACERAT : METAPROMPT MANIMGL
- Import V2 : `from manimlib import *` (ou `from manim_imports_ext import *`)
- Classe de base : `InteractiveScene` (remplace `Scene`)
- Architecture multi-scènes : 4 à 5 classes séparées au lieu d'un monolithe
- Nommage obligatoire : `01_HookQuestion.py`, `02_EquationReveal.py`, etc.

#### UPGRADE 4 — F03_CRUOR : MULTI-SCÈNES + STAGING
- Render par scène : `manimgl scenes.py NomScene --write_to_movie`
- Assemblage via `stage.py` (concat FFmpeg alphabétique)
- Fichier `stage_scenes.py` pour assemblage modulaire

#### UPGRADE 5 — F04_NAILS : MODE HOOK
Mode hook spécifique :
1. Fade audio fin du clip hook : `ffmpeg -af "afade=t=out:st=3:d=1"`
2. Concat hook + manim : filter_complex concat
3. Merge musique finale

#### NOUVEAU MODULE — HOOK_STUDIO
```
ANGRON-V2/
└── HOOK_STUDIO/
    ├── studio.py       ← Streamlit app (URL + player + curseurs IN/OUT + format)
    ├── downloader.py   ← yt-dlp wrapper
    ├── cutter.py       ← FFmpeg cutter (speed, volume, 9:16 blur-pad / 16:9)
    └── OUT/
        └── hook_ready.mp4
```
Fonctionnalités : download YouTube/Twitter/TikTok/Instagram → trim → speed/volume → format → `hook_ready.mp4` → copie auto dans `F02_LACERAT/IN/HOOK/`.
Champ `hook_question` obligatoire avant CUT → écrit dans `ledger.json`.

---

### RÈGLE TOKEN CLAUDE — V2 (mise à jour)

```
[Claude actif]   Choix du mode : math_script / math_no_script / hook
[Si mode hook]   HOOK_STUDIO → opérateur prépare hook_ready.mp4 manuellement
[Claude actif]   F01_SANGUIS — génération script (arc 3B1B)
[GATE]           opérateur valide le script
[Claude actif]   F02_LACERAT — scenes.py multi-scènes + Whisper sync (si math_script)
[Claude INACTIF] Whisper tourne seul → timestamps
[GATE]           opérateur valide les scènes
[Claude actif]   F03_CRUOR — génère scenes.py + déclenche render.sh par scène
[Claude INACTIF] Docker + manimgl → renders + stage.py → staged.mp4 → DONE.txt
[GATE]           opérateur valide la vidéo brute
[Claude actif]   déclenche finish.sh
[Claude INACTIF] F04_NAILS → NAILS_DONE.txt
[Claude INACTIF] F05_NUCERIA → NUCERIA_DONE.txt
[Claude actif]   URL publique → terminé
```

---

### DIFFÉRENCES API CRITIQUES V1 → V2

| ManimCommunity (V1) | manimgl (V2) |
|---------------------|-------------|
| `from manim import *` | `from manimlib import *` |
| `MathTex()` | `Tex()` |
| `Scene` | `InteractiveScene` |
| `config.pixel_height` | `FRAME_HEIGHT` |
| `self.play(Create(x))` | `self.play(ShowCreation(x))` |
| 1 classe monolithique | N classes séparées |

---

### COLD START V2

```bash
git clone https://github.com/kioka8877-ux/ANGRON-V2 .
docker pull ghcr.io/kioka8877-ux/angron-v2:latest
# Claude lit .angron/ledger.json → reprend à l'étape + mode indiqués
```

---

## FORMAT D'ENTRÉE

```
### [ANGRON-XXX] — NOM DU CONCEPT
- **Date** : YYYY-MM-DD
- **Format** : Short 9:16 / Long-form 16:9
- **Mode** : math_script / math_no_script / hook
- **Concept** : description courte
- **Hook question** : (si mode hook) "Mais comment X peut-il Y ?"
- **Durée vidéo** : Xs
- **Statut** : HOOK_STUDIO → F01_SANGUIS → F02_LACERAT → F03_CRUOR → F04_NAILS → F05_NUCERIA → UPLOAD → LIVE
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
| `HOOK_STUDIO` | Opérateur prépare le clip hook (mode hook uniquement) |
| `STATE_2` | SANGUIS en cours |
| `STATE_2_GATE` | Script généré — attente validation opérateur |
| `STATE_3` | Whisper en cours |
| `STATE_4` | LACERAT storyboard en cours |
| `STATE_4_GATE` | Storyboard généré — attente validation opérateur |
| `STATE_5` | CRUOR génère scenes.py (multi-scènes V2) |
| `STATE_6` | Render Docker en cours (manimgl, par scène) |
| `STATE_6_GATE` | Vidéo brute prête — attente validation opérateur |
| `STATE_7` | NAILS fusion audio/vidéo (+ concat hook si mode hook) |
| `STATE_8` | NUCERIA camouflage |
| `STATE_9` | Archive + commit final (automatique) |
| `UPLOADED` | Vidéo uploadée sur YouTube |
| `LIVE` | Vidéo en ligne, collecte métriques |
| `FAILED` | Échec à une étape — voir observations |
