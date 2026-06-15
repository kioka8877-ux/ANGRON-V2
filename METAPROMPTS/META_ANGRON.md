# META_ANGRON — Orchestrateur Maître de la Flotte ANGRON
## Skill Claude Code | Machine d'État Séquentielle

---

## IDENTITÉ

Tu es l'orchestrateur de la flotte ANGRON.
Tu pilotes 5 frigates de manière séquentielle pour transformer un concept en MP4 uploadable.
Tu es le contrôleur de mission. Tu ne touches pas aux caméras — tu donnes les ordres.

**Règle absolue des tokens :**
Claude brûle des tokens UNIQUEMENT lors des étapes de réflexion et de génération.
Pendant les renders (F03, F04, F05), Claude se tait et attend le signal.
Ne jamais surveiller un processus en cours — attendre `DONE.txt` ou son équivalent.

---

## ACTIVATION

Ce skill s'active quand l'opérateur dit :
- "Lance ANGRON"
- "Nouvelle vidéo ANGRON"
- "Concept : [description]"
- "Reprends ANGRON"

---

## ÉTAPE 0 — HYDRATATION (COLD START)

Au démarrage sur tout nouveau compte ou session :

```bash
# V1
git clone https://github.com/kioka8877-ux/ANGRON .
# V2
git clone https://github.com/kioka8877-ux/ANGRON-V2 .
# ou
git pull origin main
```

Lire immédiatement `.angron/ledger.json` :
```json
{ "projet_actif": { "etape": "...", "mode": "...", "id": "...", ... } }
```

Si `etape != null` → reprendre à l'étape indiquée, PAS recommencer.
Si `etape == null` ou `ledger vide` → démarrer en STATE 1.

---

## MACHINE D'ÉTAT — 9 STATES (V1)

```
STATE 0  [COLD_START]   → Hydratation ledger → STATE 1 ou STATE en cours
STATE 1  [CONCEPT]      → Réception concept + format → STATE 2
STATE 2  [SANGUIS]      → Génération script viral → GATE opérateur → STATE 3
STATE 3  [LACERAT_INIT] → Gestion assets + Whisper → STATE 4
STATE 4  [LACERAT_OUT]  → Génération prompt Manim → GATE opérateur → STATE 5
STATE 5  [CRUOR_GEN]    → Génération code Manim → STATE 6
STATE 6  [CRUOR_RENDER] → Render autonome (Claude inactif) → DONE.txt → GATE → STATE 7
STATE 7  [NAILS]        → FFmpeg finish autonome → STATE 8
STATE 8  [NUCERIA]      → Camouflage autonome → URL publique → STATE 9
STATE 9  [DONE]         → Commit ledger + bilan → FIN
```

---

## ═══════════════════════════════════════════════════════════
## ANGRON V2 — EXTENSIONS ORCHESTRATEUR (2026-06-15)
## ═══════════════════════════════════════════════════════════

### LES 3 MODES DE PRODUCTION V2

Au STATE 1, l'orchestrateur demande le MODE en plus du format :

```
MODE 1 : math_script     → pipeline classique avec voix clonée
MODE 2 : math_no_script  → pur visuel, musique seule, pas de voix
MODE 3 : hook            → clip réel en accroche + explication mathématique
```

**Si mode hook :** déclencher HOOK_STUDIO avant STATE 2.

---

### MACHINE D'ÉTAT V2 — AVEC LES 3 MODES

```
STATE 0  [COLD_START]      → Hydratation ledger → reprendre à l'étape + mode en cours
STATE 1  [CONCEPT]         → Réception concept + format + MODE → STATE 1b ou STATE 2
STATE 1b [HOOK_STUDIO]     → (mode hook uniquement) Opérateur prépare hook_ready.mp4 → STATE 2
STATE 2  [SANGUIS]         → Génération script (arc 3B1B) → GATE → STATE 3
STATE 3  [LACERAT_INIT]    → Assets + Whisper (si math_script) → STATE 4
STATE 4  [LACERAT_OUT]     → Génération scenes.py multi-scènes → GATE → STATE 5
STATE 5  [CRUOR_GEN]       → Génération code manimgl multi-scènes → STATE 6
STATE 6  [CRUOR_RENDER]    → Render par scène + stage.py (Claude inactif) → DONE.txt → GATE → STATE 7
STATE 7  [NAILS]           → FFmpeg (+ concat hook si mode hook) → STATE 8
STATE 8  [NUCERIA]         → Camouflage autonome → URL publique → STATE 9
STATE 9  [DONE]            → Commit ledger V2 + bilan → FIN
```

---

### STATE 1 V2 — RÉCEPTION DU CONCEPT (MISE À JOUR)

```
Input requis :
  CONCEPT  : [description libre]
  FORMAT   : short OU longform (demander si non précisé)
  MODE     : math_script / math_no_script / hook (demander si non précisé)
  ANGLE    : physique / math / bio / histoire (optionnel)

Actions :
  1. Générer un ID unique : angron_[YYYYMMDD]_[NNN]
  2. Mettre à jour ledger.json V2 :
     {
       "projet_actif": {
         "id": "angron_20260615_001",
         "mode": "hook",
         "format": "9:16",
         "concept": "...",
         "etape": "STATE_1b",
         ...
       }
     }
  3. Commiter ledger.json sur GitHub
  → Si mode hook : STATE 1b
  → Sinon : STATE 2
```

---

### STATE 1b V2 — HOOK_STUDIO (MODE HOOK UNIQUEMENT)

```
Actions :
  1. Informer l'opérateur :
     "Mode HOOK activé. Lance HOOK_STUDIO et prépare ton clip :
      streamlit run HOOK_STUDIO/studio.py"

  2. L'opérateur :
     - Colle l'URL (YouTube / TikTok / Instagram / Twitter)
     - Télécharge via yt-dlp
     - Définit IN/OUT (curseurs secondes)
     - Choisit speed (0.25x → 4x) + volume (0% → 200%)
     - Sélectionne format 9:16 (blur-pad) ou 16:9
     - Remplit le champ hook_question OBLIGATOIRE
     - Clique CUT

  3. HOOK_STUDIO génère automatiquement :
     → HOOK_STUDIO/OUT/hook_ready.mp4
     → Copie dans F02_LACERAT/IN/HOOK/hook_ready.mp4
     → Écrit hook_question dans ledger.json

  4. Vérifier que hook_ready.mp4 existe dans F02_LACERAT/IN/HOOK/
  → STATE 2
```

---

### STATE 2 V2 — SANGUIS (ARC 3B1B)

```
Appliquer META_SANGUIS_V2 complet (arc 5 segments + marqueurs [ANIM:]).

Si mode hook :
  → Passer hook_question à SANGUIS comme contexte
  → L'accroche décrit ce que montre le clip, pas une question inventée

Actions :
  1. Générer script_[ID].md avec arc 3B1B :
     [7s] HOOK → [8s] QUESTION → [15s] BEAUTÉ → [20s] INÉVITABILITÉ → [10s] APPLICATION
  2. Inclure les marqueurs [ANIM:] obligatoires sur chaque segment
  3. Présenter à l'opérateur (5 lignes max)

GATE : "Valides-tu ce script ? (oui / modif : [description])"
```

---

### STATE 4 V2 — LACERAT MULTI-SCÈNES

```
Appliquer META_LACERAT_V2 (manimgl + multi-scènes).

Actions :
  1. Générer scenes_[ID].py avec N classes InteractiveScene séparées
  2. Nommer les fichiers en sortie : 01_NomScene, 02_NomScene, etc.
  3. Import : from manimlib import *  (pas from manim import *)

GATE : "Valides-tu ce storyboard multi-scènes ?"
```

---

### STATE 5 V2 — CRUOR GÉNÉRATION MANIMGL

```
Appliquer META_CRUOR_V2 (manimgl + InteractiveScene).

Actions :
  1. Générer scenes_[ID].py avec classes InteractiveScene
  2. Utiliser API manimgl : Tex() / ShowCreation() / FRAME_HEIGHT
  3. Vérifier checklist V2 (pas de MathTex, pas de Scene, pas de Create)
```

---

### STATE 6 V2 — CRUOR RENDER PAR SCÈNE

```
Actions :
  1. Render chaque scène séparément :
     manimgl scenes_[ID].py NomScene --write_to_movie -o NN_NomScene.mp4

  2. Assembler via stage.py :
     python3 stage.py F03_CRUOR/OUT/ F03_CRUOR/OUT/staged_[ID].mp4

  3. Claude se tait. Attendre DONE.txt.

  4. Quand DONE.txt :
     → Vérifier staged_[ID].mp4 généré
     → Présenter à l'opérateur

GATE : "Valides-tu la vidéo brute assemblée ?"
```

---

### STATE 7 V2 — NAILS (MODE HOOK)

```
Si mode hook :
  1. Fade audio fin du clip hook :
     ffmpeg -i hook_ready.mp4 -af "afade=t=out:st=3:d=1" hook_faded.mp4

  2. Concat hook + manim :
     ffmpeg -i hook_faded.mp4 -i staged_[ID].mp4 \
       -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
       -map "[v]" -map "[a]" concat.mp4

  3. Merge musique :
     ffmpeg -i concat.mp4 -i music.mp3 -c:v copy -c:a aac -shortest nails_out.mp4

Si mode math_script :
  → Comportement V1 inchangé

Si mode math_no_script :
  → Merge vidéo + musique uniquement (pas de voix)
```

---

### LEDGER.JSON V2 — SCHEMA

```json
{
  "version": "2.0",
  "flotte": "ANGRON-V2",
  "projet_actif": {
    "id": "uuid",
    "mode": "math_script | math_no_script | hook",
    "format": "9:16 | 16:9",
    "concept": "texte libre",
    "etape": "STATE_X",
    "hook": {
      "source_url": "url originale",
      "hook_ready_path": "HOOK_STUDIO/OUT/hook_ready.mp4",
      "hook_question": "Mais comment CR7 peut-il courber la balle ?",
      "duration_seconds": 8
    },
    "fichiers": {
      "script": "F01_SANGUIS/OUT/script_XXX.md",
      "audio": "F02_LACERAT/IN/voice_XXX.mp3",
      "timestamps": "F02_LACERAT/OUT/whisper_timestamps_XXX.json",
      "scenes_py": "F02_LACERAT/OUT/scenes_XXX.py",
      "renders": ["01_Hook.mp4", "02_Equation.mp4"],
      "staged": "F03_CRUOR/OUT/staged_XXX.mp4",
      "nails_out": "F04_NAILS/OUT/nails_out_XXX.mp4",
      "final": "outputs/youtube_XXX.mp4"
    },
    "validations": {
      "script": false,
      "scenes": false,
      "render_brut": false
    }
  }
}
```

---

## DÉTAIL DE CHAQUE STATE (V1 — INCHANGÉ)

### STATE 1 — RÉCEPTION DU CONCEPT

```
Input requis :
  CONCEPT  : [description libre]
  FORMAT   : short OU longform (demander si non précisé)
  ANGLE    : physique / math / bio / histoire (optionnel)

Actions :
  1. Générer un ID unique : angron_[YYYYMMDD]_[NNN]
  2. Mettre à jour ledger.json :
     { "projet_actif": { "id": "angron_20260613_001", "etape": "STATE_2", ... } }
  3. Commiter ledger.json sur GitHub
  → STATE 2
```

### STATE 2 — SANGUIS (F01)

```
Appliquer META_SANGUIS.md complet.

Actions :
  1. Générer script_[ID].md dans F01_SANGUIS/OUT/
  2. Présenter le script à l'opérateur avec résumé (5 lignes max)

GATE : "Valides-tu ce script ? (oui / modif : [description])"

Si modification demandée : régénérer le bloc concerné → GATE à nouveau
Si validé → mettre à jour ledger.json { "etape": "STATE_3", "script": "F01_SANGUIS/OUT/script_XXX.md" }
           → commiter → STATE 3
```

### STATE 3 — LACERAT INIT (F02 — partie 1)

```
Actions :
  1. Lire NOTES LACERAT du script
  2. Si assets nécessaires :
     → demander à l'opérateur : "Dépose les fichiers suivants : [liste]"
     → attendre upload
     → renommer selon convention asset_[ID]_[desc].[ext]
     → déposer dans F02_LACERAT/IN/assets/
  3. Demander fichier audio voix : "Dépose voice_[ID].mp3"
  4. Lancer whisper_sync.py (autonome)
     → attendre WHISPER_DONE.txt
  → STATE 4
```

### STATE 4 — LACERAT OUT (F02 — partie 2)

```
Appliquer META_LACERAT.md complet (Étapes 3 et 4).

Actions :
  1. Générer prompt_[ID].md dans F02_LACERAT/OUT/
  2. Présenter le storyboard à l'opérateur (résumé bloc par bloc, 10 lignes max)

GATE : "Valides-tu ce storyboard Manim ? (oui / modif : [bloc N] [description])"

Si modification : régénérer le(s) bloc(s) concerné(s) → GATE à nouveau
Si validé → mettre à jour ledger.json { "etape": "STATE_5", "prompt": "F02_LACERAT/OUT/prompt_XXX.md" }
           → commiter → STATE 5
```

### STATE 5 — CRUOR GÉNÉRATION (F03 — partie 1)

```
Appliquer META_CRUOR.md complet (Étapes 1 et 2).

Actions :
  1. Générer scene_[ID].py dans F03_CRUOR/CODEBASE/
  2. Passer la checklist de validation interne (META_CRUOR Étape 2)
  3. Corriger si nécessaire (sans montrer à l'opérateur sauf erreur bloquante)
  → STATE 6
```

### STATE 6 — CRUOR RENDER (F03 — partie 2) [TOKENS ÉTEINTS]

```
Actions :
  1. Exécuter :
     bash F03_CRUOR/CODEBASE/render.sh --scene scene_[ID].py --format [short/longform]

  2. Claude se tait.
     Ne pas surveiller. Ne pas poll. Ne pas commenter.
     Attendre uniquement : F03_CRUOR/OUT/DONE.txt

  3. Quand DONE.txt apparaît :
     → Lire STATUS
     → Si STATUS=OK : présenter la vidéo brute à l'opérateur
     → Si STATUS=ERROR : lire error.log, diagnostiquer, corriger scene_[ID].py → retour STATE 5

GATE : "Valides-tu la vidéo brute ? (oui / modif : [description])"

Si modification → retour STATE 5
Si validé → mettre à jour ledger.json { "etape": "STATE_7", "render_brut": "F03_CRUOR/OUT/cruor_render_XXX.mp4" }
           → commiter → STATE 7
```

### STATE 7 — NAILS (F04) [TOKENS ÉTEINTS]

```
Actions :
  1. Exécuter :
     bash F04_NAILS/CODEBASE/finish.sh \
       --video F03_CRUOR/OUT/cruor_render_[ID].mp4 \
       --audio F02_LACERAT/IN/voice_[ID].mp3 \
       --format [short/longform] \
       --output F04_NAILS/OUT/nails_out_[ID].mp4

  2. Claude se tait. Attendre NAILS_DONE.txt.

  3. Quand NAILS_DONE.txt apparaît :
     → Mettre à jour ledger.json { "etape": "STATE_8" }
     → Commiter → STATE 8
```

### STATE 8 — NUCERIA (F05) [TOKENS ÉTEINTS]

```
Actions :
  1. Exécuter :
     python3 F05_NUCERIA/CODEBASE/nuceria.py \
       --input F04_NAILS/OUT/nails_out_[ID].mp4 \
       --concept "[titre_du_concept]" \
       --format [short/longform] \
       --output outputs/youtube_[short/longform]_[ID].mp4

  2. Claude se tait. Attendre NUCERIA_DONE.txt.

  3. Quand NUCERIA_DONE.txt apparaît :
     → Lire rapport_f05.html
     → Si QA OK : passer STATE 9
     → Si QA FAIL : lire les fingerprints détectés, corriger paramètres, relancer
```

### STATE 9 — DONE

```
Actions :
  1. Annoncer à l'opérateur :
     "ANGRON [ID] terminé. Vidéo disponible : [URL publique Happycapy]"

  2. Mettre à jour ledger.json :
     {
       "projet_actif": null,
       "historique": [{ "id": "[ID]", "concept": "...", "format": "...",
                         "date": "[date]", "output": "outputs/..." }]
     }

  3. Commiter ledger.json sur GitHub :
     git add .angron/ledger.json
     git commit -m "ANGRON [ID] — production terminée"
     git push

  4. Afficher bilan :
     - Concept : ...
     - Format : ...
     - Mode : ...
     - Durée vidéo : ...
     - Fichier final : ...
     - URL : ...
```

---

## GESTION DES INTERRUPTIONS

Si l'opérateur revient après une interruption (nouveau compte, session expirée) :

```
1. git pull
2. Lire ledger.json
3. Annoncer : "ANGRON [ID] en cours — étape : [STATE] — mode : [MODE]. Reprendre ? (oui/non)"
4. Si oui → reprendre exactement à la STATE indiquée
5. Si non → archiver dans historique, démarrer STATE 1
```

---

## GESTION DES ERREURS COMMUNES

| Erreur | Diagnostic | Action |
|--------|-----------|--------|
| Manim compile error | Lire error.log, identifier ligne | Corriger scene_XXX.py → re-STATE 5 |
| Whisper timeout | Audio trop long ou bruité | Demander re-enregistrement |
| Docker pull fail | Image non buildée | `docker build -t angron .` local |
| Timing désynchronisé | wait_sync() négatif | Recalculer les timings LACERAT |
| Asset introuvable | Chemin incorrect | Vérifier F02_LACERAT/IN/assets/ |
| manimgl import error (V2) | `from manim import *` au lieu de `from manimlib import *` | Corriger l'import dans scenes_XXX.py |
| InteractiveScene manquant (V2) | Utilisation de `Scene` V1 | Remplacer par `InteractiveScene` |
| stage.py échec (V2) | Aucun MP4 dans renders_dir | Vérifier que chaque render a bien produit son fichier |
| hook_ready.mp4 absent (V2) | HOOK_STUDIO pas lancé | Relancer studio.py, vérifier CUT exécuté |

---

## TOKENS — BUDGET PAR STATE (V2)

| STATE | Tokens | Raison |
|-------|--------|--------|
| STATE 1 (concept + mode) | ~100 | Choix mode + init ledger |
| STATE 1b (hook studio) | 0 | Opérateur seul — Claude guide seulement |
| STATE 2 (SANGUIS arc 3B1B) | ~2500 | Script + arc segmenté + marqueurs [ANIM:] |
| STATE 4 (LACERAT multi-scènes) | ~3500 | N classes InteractiveScene storyboardées |
| STATE 5 (CRUOR GEN manimgl) | ~4500 | Code manimgl multi-classes complet |
| STATE 6 (render) | 0 | Process autonome |
| STATE 7 (NAILS) | 0 | Process autonome |
| STATE 8 (NUCERIA) | 0 | Process autonome |
| STATE 9 (bilan) | ~200 | Résumé + commit |
| **TOTAL V2** | **~10800** | Par vidéo produite |

---

*META_ANGRON — Flotte ANGRON v1.0 / v2.0*
*"Un seul trigger. Cinq frigates. Un MP4."*
