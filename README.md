# ANGRON — Flotte de Production Automatisée Pop-Science

> *"Il ne réfléchit pas. Il détruit."*
> — Sur le Primärque des World Eaters

---

## DOCTRINE

**ANGRON** est la première flotte entièrement pilotée par une intelligence artificielle.

Là où DORN construit avec précision et patience, ANGRON frappe vite et sans pitié.  
Un concept. Un trigger. Un MP4 propre, prêt à l'upload. Automatiquement.

**Mission** : produire des vidéos pop-science virales (format Court 9:16 et Long-form 16:9) qui occupent le territoire que 3Blue1Brown a laissé vide — la science incarnée dans le corps humain, dans le sport, dans la physique du quotidien — avec des mathématiques visibles et une voix qui porte l'émotion.

**Principe cardinal** : *"L'émotion attire le spectateur. La rigueur mathématique le retient."*

**Règle de production** : Les frigates travaillent. Claude réfléchit. Claude ne regarde jamais la casserole bouillir.

---

## NOMENCLATURE

Nommée d'après **Angron**, Primärque des **World Eaters** (XIIème Légion).  
Incarnation de la colère pure et de la destruction absolue.  
Ses fils ne connaissent pas la défaite — ils connaissent l'assaut.

| Frigate | Nom | Rôle |
|---------|-----|------|
| ANGRON-F01 | **SANGUIS** | Cerveau narratif — génération du script viral |
| ANGRON-F02 | **LACERAT** | Traducteur tactique — prompt Manim + sync Whisper |
| ANGRON-F03 | **CRUOR** | Moteur de rendu — Manim headless autonome |
| ANGRON-F04 | **NAILS** | Finisseur — FFmpeg fusion audio/vidéo |
| ANGRON-F05 | **NUCERIA** | Camouflage — wipe métadonnées, zéro fingerprint |

---

## ARCHITECTURE

```
TRIGGER OPÉRATEUR (concept brut)
         │
         ▼
┌─────────────────────────────────────┐
│  ANGRON-F01 SANGUIS                 │
│  Input  : concept + format cible    │
│  Output : script viral + [ANIM:]    │
└──────────────┬──────────────────────┘
               │  [GATE : validation script]
               ▼
┌─────────────────────────────────────┐
│  ANGRON-F02 LACERAT                 │
│  Input  : script + voix_clonée.mp3  │
│  Output : prompt Manim + timings    │
└──────────────┬──────────────────────┘
               │  [GATE : validation prompt]
               ▼
┌─────────────────────────────────────┐
│  ANGRON-F03 CRUOR                   │
│  Input  : prompt Manim + assets     │
│  Output : render_brut.mp4           │
│  Mode   : Docker headless autonome  │
│  Claude : INACTIF pendant le rendu  │
└──────────────┬──────────────────────┘
               │  [GATE : validation vidéo brute]
               ▼
┌─────────────────────────────────────┐
│  ANGRON-F04 NAILS                   │
│  Input  : render_brut + audio       │
│  Output : nails_out.mp4             │
│  Mode   : FFmpeg autonome           │
│  Claude : INACTIF                   │
└──────────────┬──────────────────────┘
               │  (automatique)
               ▼
┌─────────────────────────────────────┐
│  ANGRON-F05 NUCERIA                 │
│  Input  : nails_out.mp4             │
│  Output : youtube_final.mp4         │
│  Mode   : FFmpeg re-encode + wipe   │
│  Claude : INACTIF                   │
└──────────────┬──────────────────────┘
               │
               ▼
        ./outputs/youtube_final.mp4
        URL publique Happycapy
```

---

## STRUCTURE DU DÉPÔT

```
ANGRON/
├── .angron/
│   └── ledger.json              ← mémoire nomade (état de production)
├── .github/
│   └── workflows/
│       └── docker-build.yml     ← build + push ghcr.io automatique
├── SANGUIS/                     ← F01 Cerveau narratif
│   ├── CODEBASE/
│   ├── IN/
│   └── OUT/
├── LACERAT/                     ← F02 Traducteur tactique
│   ├── CODEBASE/
│   ├── IN/
│   └── OUT/
├── CRUOR/                       ← F03 Moteur Manim
│   ├── CODEBASE/
│   ├── IN/
│   └── OUT/
├── NAILS/                       ← F04 Finisseur FFmpeg
│   ├── CODEBASE/
│   ├── IN/
│   └── OUT/
├── NUCERIA/                     ← F05 Camouflage métadonnées
│   ├── CODEBASE/
│   ├── IN/
│   └── OUT/
├── METAPROMPTS/                 ← Metaprompts des frigates
├── SHARED/
│   ├── IN/
│   └── OUT/
├── TRACKING/
│   ├── ANGRON_CAMPAIGN_LOG.md   ← journal de production
│   └── ANGRON_TRANSFER_LOG.md  ← journal des transferts inter-frigates
├── Dockerfile                   ← environnement complet ANGRON
├── ANGRON_STYLE.py              ← charte graphique immuable
├── angron.py                    ← orchestrateur Claude (point d'entrée)
└── README.md
```

---

## CHARTE GRAPHIQUE — ANGRON_STYLE

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

## RÈGLE TOKEN CLAUDE — ABSOLUE

```
[Claude actif]   F01 SANGUIS — génération script
[GATE]           opérateur valide le script
[Claude actif]   F02 LACERAT — prompt Manim + Whisper sync
[Claude INACTIF] Whisper tourne seul → timestamps extraits
[GATE]           opérateur valide le prompt
[Claude actif]   F03 CRUOR — génère scene.py + déclenche render.sh
[Claude INACTIF] Docker + Manim → DONE.txt
[GATE]           opérateur valide la vidéo brute
[Claude actif]   déclenche finish.sh
[Claude INACTIF] FFmpeg F04 → NAILS_DONE.txt
[Claude INACTIF] FFmpeg F05 → NUCERIA_DONE.txt
[Claude actif]   URL publique → terminé
```

**4 moments d'activité Claude. Zéro token pendant les renders.**

---

## NOMADISME — HYDRATATION INSTANTANÉE

ANGRON est **nomade**. Happycapy est une cellule de calcul jetable.  
GitHub est le Grand Livre d'État.

Sur tout nouveau compte Happycapy :

```bash
git clone https://github.com/kioka8877-ux/ANGRON
docker pull ghcr.io/kioka8877-ux/angron:latest
# Claude lit .angron/ledger.json → sait exactement où reprendre
```

---

## INFRASTRUCTURE DOCKER

L'image `ghcr.io/kioka8877-ux/angron:latest` contient :

- Python 3.11
- Manim Community Edition + manim-voiceover
- LaTeX complet (texlive-full)
- FFmpeg
- Cairo + Pango + OpenGL Mesa headless
- Whisper base (~150MB, CPU)
- CMU Serif font

**Une seule commande pour tout avoir. Aucune installation à refaire.**

---

## TRACKER GITHUB

Le fichier `.angron/ledger.json` est commité automatiquement à chaque étape.  
L'opérateur peut suivre l'état de production en temps réel depuis GitHub (mobile ou desktop) sans ouvrir Happycapy.

---

## AVANTAGE CONCURRENTIEL

| | Le barbu | 3Blue1Brown | **ANGRON** |
|---|---|---|---|
| Script | Prompt générique | Manuel, 6 mois | META_01_SCRIPT automatique |
| Animation | Manim sans âme | Manim custom | Manim storyboardé ligne par ligne |
| Voix | Aucune | Manuelle | Voix clonée synchronisée Whisper |
| Formats | Indéfini | Long-form uniquement | Short 9:16 + Long-form 16:9 |
| Camouflage | Aucun | N/A | NUCERIA — zéro fingerprint |
| Pipeline | 30 min manuel | 6 mois manuel | **1 trigger → MP4 propre** |
| Territoire | Copie 3B1B | Long-form horizontal | **Shorts pop-science vertical — terrain libre** |

---

*ANGRON ne réfléchit pas. Il produit.*
