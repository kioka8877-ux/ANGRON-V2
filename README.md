# ANGRON V2 — Flotte de Production Automatisée Pop-Science

> *"Il ne réfléchit pas. Il détruit."*
> — Sur le Primärque des World Eaters

---

## DOCTRINE

**ANGRON V2** est l'évolution de la flotte de production automatisée.

V1 produit des vidéos. V2 produit des vidéos **avec trois modes** et la puissance visuelle de **manimgl (fork 3B1B)**.

**Mission** : produire des vidéos pop-science virales (format Court 9:16 et Long-form 16:9) qui occupent le territoire que 3Blue1Brown a laissé vide — la science incarnée dans le corps humain, dans le sport, dans la physique du quotidien — avec des mathématiques visibles et une voix qui porte l'émotion.

**Principe cardinal** : *"L'émotion attire le spectateur. La rigueur mathématique le retient."*

**Règle de production** : Les frigates travaillent. Claude réfléchit. Claude ne regarde jamais la casserole bouillir.

**Repos :**
- V1 (production stable) : https://github.com/kioka8877-ux/ANGRON
- V2 (fork évolutif) : https://github.com/kioka8877-ux/ANGRON-V2

---

## CE QUI CHANGE EN V2

| Composant | V1 | V2 |
|-----------|----|----|
| Moteur Manim | ManimCommunity (`from manim import *`) | manimgl 3B1B (`from manimlib import *`) |
| Classe de base | `Scene` | `InteractiveScene` |
| Architecture scènes | 1 classe monolithique | N classes séparées + `stage.py` |
| Arc narratif | Structure libre | Arc 3B1B : 5 segments chronométrés |
| Modes production | 1 seul | 3 modes : math_script / math_no_script / hook |
| Clips réels | Absent | HOOK_STUDIO (yt-dlp + Streamlit + FFmpeg) |
| F04_NAILS | Audio + vidéo | Audio + vidéo + concat hook |
| Ledger | Basique | Mode + hook_question + renders[] |

---

## NOMENCLATURE

Nommée d'après **Angron**, Primärque des **World Eaters** (XIIème Légion).  
Incarnation de la colère pure et de la destruction absolue.

| Frigate | Nom | Rôle | Statut V2 |
|---------|-----|------|-----------|
| F01_SANGUIS | **SANGUIS** | Cerveau narratif — arc 3B1B + marqueurs [ANIM:] | UPGRADE |
| F02_LACERAT | **LACERAT** | Traducteur — manimgl + multi-scènes + mode hook | UPGRADE |
| F03_CRUOR | **CRUOR** | Moteur render — manimgl headless + stage.py | UPGRADE |
| F04_NAILS | **NAILS** | Finisseur — FFmpeg + concat hook | UPGRADE |
| F05_NUCERIA | **NUCERIA** | Camouflage — wipe métadonnées, zéro fingerprint | INCHANGÉE |
| HOOK_STUDIO | **HOOK_STUDIO** | Téléchargement + découpe clips réels | NOUVEAU |

---

## LES 3 MODES DE PRODUCTION

### Mode 1 : `math_script`
Pipeline classique avec voix clonée.
```
F01 → script narratif (arc 3B1B)
F02 → scenes.py multi-scènes + Whisper sync
F03 → render manimgl par scène + stage.py
F04 → merge audio + vidéo assemblée
F05 → wipe métadonnées
```

### Mode 2 : `math_no_script`
Pas de voix. Musique seule. Pur visuel.
```
F01 → concept visuel (pas de script vocal)
F02 → scenes.py pur (pas de Whisper)
F03 → render manimgl par scène + stage.py
F04 → merge musique + vidéo
F05 → wipe métadonnées
```

### Mode 3 : `hook`
Clip réel en accroche, puis explication mathématique.
```
HOOK_STUDIO → hook_ready.mp4 (préparé manuellement par opérateur)
F01 → script narratif avec contexte hook_question
F02 → scenes.py répondant à la question du hook
F03 → render manimgl + stage.py
F04 → concat [hook_ready.mp4 + staged.mp4] + audio
F05 → wipe métadonnées
```

---

## ARCHITECTURE

```
TRIGGER OPÉRATEUR (concept + format + mode)
         │
         ▼ [si mode hook]
┌─────────────────────────────────────┐
│  HOOK_STUDIO                        │
│  Input  : URL YouTube/TikTok/etc.   │
│  Output : hook_ready.mp4            │
│  Tools  : yt-dlp + Streamlit        │
│  Opérateur : décide IN/OUT/speed    │
└──────────────┬──────────────────────┘
               │ hook_ready.mp4 → F02_LACERAT/IN/HOOK/
               ▼
┌─────────────────────────────────────┐
│  F01_SANGUIS                        │
│  Input  : concept + format + mode   │
│  Output : script (arc 3B1B 5 seg.)  │
└──────────────┬──────────────────────┘
               │  [GATE : validation script]
               ▼
┌─────────────────────────────────────┐
│  F02_LACERAT                        │
│  Input  : script + voix_clonée.mp3  │
│  Output : scenes.py (N classes)     │
│  Engine : manimgl (InteractiveScene)│
└──────────────┬──────────────────────┘
               │  [GATE : validation scènes]
               ▼
┌─────────────────────────────────────┐
│  F03_CRUOR                          │
│  Input  : scenes.py + assets        │
│  Output : staged.mp4                │
│  Mode   : Docker headless manimgl   │
│  Render : par scène + stage.py      │
│  Claude : INACTIF pendant le rendu  │
└──────────────┬──────────────────────┘
               │  [GATE : validation vidéo brute]
               ▼
┌─────────────────────────────────────┐
│  F04_NAILS                          │
│  Input  : staged.mp4 + audio        │
│  Mode hook : concat hook + staged   │
│  Output : nails_out.mp4             │
│  Claude : INACTIF                   │
└──────────────┬──────────────────────┘
               │  (automatique)
               ▼
┌─────────────────────────────────────┐
│  F05_NUCERIA                        │
│  Input  : nails_out.mp4             │
│  Output : youtube_final.mp4         │
│  Mode   : FFmpeg re-encode + wipe   │
│  Claude : INACTIF                   │
└──────────────┬──────────────────────┘
               │
               ▼
        ./outputs/youtube_final.mp4
        URL publique
```

---

## STRUCTURE DU DÉPÔT V2

```
ANGRON-V2/
├── .angron/
│   └── ledger.json              ← mémoire nomade V2 (mode + hook + renders[])
├── .github/
│   └── workflows/
│       ├── docker-build.yml
│       ├── cruor-render.yml
│       ├── lacerat-whisper.yml
│       ├── nails-finish.yml
│       └── nuceria-final.yml
├── F01_SANGUIS/                 ← Cerveau narratif (arc 3B1B)
│   ├── CODEBASE/sanguis.py
│   ├── IN/
│   └── OUT/
├── F02_LACERAT/                 ← Traducteur manimgl + multi-scènes
│   ├── CODEBASE/lacerat.py + whisper_sync.py
│   ├── IN/
│   │   ├── HOOK/                ← hook_ready.mp4 (mode hook)
│   │   └── assets/
│   └── OUT/
├── F03_CRUOR/                   ← Moteur manimgl
│   ├── CODEBASE/render.sh + stage.py
│   ├── IN/
│   └── OUT/
├── F04_NAILS/                   ← Finisseur FFmpeg (+ mode hook)
│   ├── CODEBASE/finish.sh
│   ├── IN/
│   └── OUT/
├── F05_NUCERIA/                 ← Camouflage métadonnées (inchangée)
│   ├── CODEBASE/nuceria.py
│   ├── IN/
│   └── OUT/
├── HOOK_STUDIO/                 ← NOUVEAU — Clips réels
│   ├── studio.py                ← Streamlit app
│   ├── downloader.py            ← yt-dlp wrapper
│   ├── cutter.py                ← FFmpeg cutter
│   └── OUT/
│       └── hook_ready.mp4
├── METAPROMPTS/
│   ├── META_ANGRON.md           ← Orchestrateur (3 modes + manimgl)
│   ├── META_SANGUIS.md          ← Arc 3B1B
│   ├── META_LACERAT.md          ← manimgl + multi-scènes
│   └── META_CRUOR.md            ← manimgl + InteractiveScene
├── TRACKING/
│   ├── ANGRON_CAMPAIGN_LOG.md   ← journal de production (V1 + V2)
│   └── ANGRON_TRANSFER_LOG.md   ← journal transferts (V1 + V2)
├── SHARED/
├── Dockerfile                   ← manimgl + yt-dlp + streamlit
├── ANGRON_STYLE.py              ← charte graphique immuable
├── angron.py                    ← orchestrateur (3 modes)
└── README.md
```

---

## CHARTE GRAPHIQUE — ANGRON_STYLE (inchangée)

Palette inspirée 3Blue1Brown. **Jamais modifiée par Claude sans validation opérateur.**

| Élément | Valeur |
|---------|--------|
| Fond | `#171717` — gris-noir mat, jamais noir pur |
| Primaire | `#58C4DD` — bleu canard |
| Secondaire | `#FFF1B6` — jaune crème |
| Accent | `#A6CF98` — vert sauge |
| Texte | `#ECEFF1` — blanc cassé |
| Police | `CMU Serif` — Computer Modern (police 3B1B) |
| Trait | `stroke_width=2` maximum |
| Transition | `smooth` — zéro arrêt net robotique |
| Formats | Short `1080x1920` (9:16) / Long-form `1920x1080` (16:9) |
| FPS | 60 |

---

## RÈGLE TOKEN CLAUDE V2 — ABSOLUE

```
[Claude actif]   Choix mode (math_script / math_no_script / hook)
[Si mode hook]   Opérateur lance HOOK_STUDIO seul — Claude guide si besoin
[Claude actif]   F01_SANGUIS — génération script (arc 3B1B)
[GATE]           opérateur valide le script
[Claude actif]   F02_LACERAT — scenes.py manimgl + Whisper sync (si math_script)
[Claude INACTIF] Whisper tourne seul → timestamps extraits
[GATE]           opérateur valide les scènes
[Claude actif]   F03_CRUOR — génère scenes.py + déclenche render.sh par scène
[Claude INACTIF] Docker + manimgl → renders + stage.py → staged.mp4 → DONE.txt
[GATE]           opérateur valide la vidéo brute assemblée
[Claude actif]   déclenche finish.sh
[Claude INACTIF] F04_NAILS → NAILS_DONE.txt
[Claude INACTIF] F05_NUCERIA → NUCERIA_DONE.txt
[Claude actif]   URL publique → terminé
```

**4 moments d'activité Claude. Zéro token pendant les renders.**

---

## NOMADISME — HYDRATATION INSTANTANÉE V2

ANGRON V2 est **nomade**. GitHub est le Grand Livre d'État.

Sur tout nouveau compte :

```bash
git clone https://github.com/kioka8877-ux/ANGRON-V2 .
docker pull ghcr.io/kioka8877-ux/angron-v2:latest
# Claude lit .angron/ledger.json → sait exactement où reprendre + quel mode
```

---

## INFRASTRUCTURE DOCKER V2

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg xvfb \
    texlive-full \
    libcairo2-dev libpango1.0-dev \
    libgl1-mesa-glx libglu1-mesa \
    fonts-cmu \
    git

RUN pip install \
    manimgl \
    faster-whisper \
    yt-dlp \
    streamlit \
    pydub soundfile \
    Pillow numpy scipy

RUN fc-cache -f -v
```

**Différence V1 → V2 :** `manim` remplacé par `manimgl` + ajout `yt-dlp` + `streamlit`.

---

## HOOK_STUDIO — GUIDE RAPIDE

```bash
streamlit run HOOK_STUDIO/studio.py
# → Interface dans le navigateur
# 1. Coller URL (YouTube / TikTok / Instagram / Twitter)
# 2. Cliquer Download
# 3. Régler curseurs IN/OUT (secondes)
# 4. Choisir vitesse (0.25x → 4x) et volume (0% → 200%)
# 5. Sélectionner format : 9:16 (blur-pad) ou 16:9
# 6. Remplir hook_question OBLIGATOIRE
# 7. Cliquer CUT
# → hook_ready.mp4 généré + copié dans F02_LACERAT/IN/HOOK/
# → hook_question écrit dans .angron/ledger.json
```

---

## AVANTAGE CONCURRENTIEL V2

| | Le barbu | 3Blue1Brown | **ANGRON V2** |
|---|---|---|---|
| Script | Prompt générique | Manuel, 6 mois | Arc 3B1B automatique (5 segments) |
| Animation | Manim sans âme | Manim custom 3B1B | **manimgl 3B1B** + multi-scènes |
| Voix | Aucune | Manuelle | Voix clonée synchronisée Whisper |
| Formats | Indéfini | Long-form uniquement | Short 9:16 + Long-form 16:9 |
| Modes | 1 | 1 | **3 modes** (math / muet / hook) |
| Clips réels | Aucun | N/A | **HOOK_STUDIO** — yt-dlp + cutter |
| Camouflage | Aucun | N/A | NUCERIA — zéro fingerprint |
| Pipeline | 30 min manuel | 6 mois manuel | **1 trigger → MP4 propre** |

---

## ÉTAT DU CODEBASE V2 — 2026-06-15

| Composant | Fichier | Statut |
|-----------|---------|--------|
| Dockerfile | `Dockerfile` + `requirements.txt` | DONE |
| F01_SANGUIS | `sanguis.py` | DONE |
| F02_LACERAT | `lacerat.py` | DONE |
| F03_CRUOR | `render.sh` + `stage.py` | DONE |
| F04_NAILS | `finish.sh` | DONE |
| HOOK_STUDIO | `studio.py` + `downloader.py` + `cutter.py` | DONE |
| Orchestrateur | `angron.py` | DONE |
| F05_NUCERIA | `nuceria.py` | INCHANGÉE (V1 production-ready) |

---

*ANGRON V2 ne réfléchit pas. Il produit. Mieux.*

