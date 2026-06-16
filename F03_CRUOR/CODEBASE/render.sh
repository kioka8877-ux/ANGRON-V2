#!/usr/bin/env bash
# render.sh — F03_CRUOR V2 : render manimgl par scène + assemblage via stage.py.

set -euo pipefail

DOCKER_IMAGE="ghcr.io/kioka8877-ux/angron-v2:latest"

SCENES=""
SCFNE_CLASS=""
OUTPUT=""
OUT_DIR=""
STAGED=""
FORMAT=""
ALL_SCENES=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scenes)      SCENES="$2";      shift 2 ;;
    --scene-class) SCENE_CLASS="$2"; shift 2 ;;
    --output)      OUTPUT="$2";      shift 2 ;;
    --out-dir)     OUT_DIR="$2";     shift 2 ;;
    --staged)      STAGED="$2";      shift 2 ;;
    --format)      FORMAT="$2";      shift 2 ;;
    --all)         ALL_SCENES=true;  shift 1 ;;
    *) echo "[CRUOR] Argument inconnu : $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$SCENES" || -z "$FORMAT" ]]; then
  echo "[CRUOR] ERREUR : --scenes et --format sont obligatoires." >&2
  exit 1
fi

if [[ "$FORMAT" != "short" && "$FORMAT" != "longform" ]]; then
  echo "[CRUOR] ERREUR : --format doit être 'short' ou 'longform'." >&2
  exit 1
fi

if [[ ! -f "$SCENES" ]]; then
  echo "[CRUOR] ERREUR : fichier scenes introuvable : $SCENES" >&2
  exit 1
fi

WORKSPACE="$(pwd)"

# ─── Mode --all : render toutes les scènes + assemblage ──────────────────────
if [[ "$ALL_SCENES" == "true" ]]; then
  if [[ -z "$OUT_DIR" || -z "$STAGED" ]]; then
    echo "[CRUOR] ERREUR : --all requiert --out-dir et --staged." >&2
    exit 1
  fi
  mkdir -p "$OUT_DIR"
  DONE_FILE="$OUT_DIR/DONE.txt"
  ERROR_LOG="$OUT_DIR/error.log"

  echo "[CRUOR] Render toutes scènes manimgl + assemblage..."
  echo "  Scenes  : $SCENES"
  echo "  Out dir : $OUT_DIR"
  echo "  Staged  : $STAGED"
  echo "  Image   : $DOCKER_IMAGE"

  SCENE_CLASSES=$(grep -oP '^class \K\w+(?=\(InteractiveScene\))' "$SCENES" | sort || true)
  if [[ -z "$SCENE_CLASSES" ]]; then
    echo "[CRUOR] ERREUR : aucune classe InteractiveScene trouvée dans $SCENES" >&2
    exit 1
  fi

  echo "[CRUOR] Scènes détectées :"
  echo "$SCENE_CLASSES" | while read -r cls; do echo "  - $cls"; done

  START_TS=$(date +%s)

  docker run --rm \
    --name "angron_cruor_all_$$" \
    -v "${WORKSPACE}:/workspace" \
    -e DISPLAY=:99 \
    "$DOCKER_IMAGE" \
    bash -c "
      set -e
      Xvfb :99 -screen 0 1080x1920x24 2>/dev/null &
      sleep 2

      # Portrait config manimgl — clés flat, 3 chemins (home + cwd + scènes)
      for CFG_PATH in \
          "/root/.config/manim/custom_config.yml" \
          "/workspace/custom_config.yml" \
          "/workspace/F03_CRUOR/CODEBASE/custom_config.yml"; do
        mkdir -p "$(dirname "$CFG_PATH")"
        cat > "$CFG_PATH" << 'CFEOF'
pixel_width: 1080
pixel_height: 1920
frame_rate: 60
frame_height: 14.222222222222221
CFEOF
      done

      OUT_BASE='/workspace/${OUT_DIR}'
      STEM=\$(basename '/workspace/${SCENES}' .py)

      while IFS= read -r SCENE_CLS; do
        echo \"[CRUOR] Render \$SCENE_CLS...\"
        cd /workspace
        manimgl '${SCENES}' \"\$SCENE_CLS\" -w 2>&1

        MP4=\$(find /workspace/videos -name \"\${SCENE_CLS}.mp4\" 2>/dev/null | sort | tail -1)
        if [[ -z \"\$MP4\" ]]; then
          echo \"ERROR: aucun MP4 pour \$SCENE_CLS\" >&2
          exit 2
        fi
        cp \"\$MP4\" \"\${OUT_BASE}/\${SCENE_CLS}.mp4\"
        echo \"[CRUOR] \$SCENE_CLS → \${OUT_BASE}/\${SCENE_CLS}.mp4\"
      done < <(grep -oP '^class \K\w+(?=\(InteractiveScene\))' '/workspace/${SCENES}' | sort)

      python3 /workspace/F03_CRUOR/CODEBASE/stage.py \
        --in-dir  \"\$OUT_BASE\" \
        --output  '/workspace/${STAGED}' 2>&1
      echo '[CRUOR] Assemblage terminé.'
    " 2>&1 | tee "$ERROR_LOG"

  DOCKER_EXIT="${PIPESTATUS[0]}"
  END_TS=$(date +%s)
  RENDER_TIME=$(( END_TS - START_TS ))

  if [[ "$DOCKER_EXIT" -ne 0 ]]; then
    echo "[CRUOR] RENDER FAILED (exit $DOCKER_EXIT) — voir $ERROR_LOG" >&2
    cat > "$DONE_FILE" <<EOF
STATUS=ERROR
SCENES=$SCENES
RENDER_TIME=${RENDER_TIME}s
ERROR_LOG=$ERROR_LOG
EOF
    exit "$DOCKER_EXIT"
  fi

  DURATION=$(ffprobe -v quiet -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$STAGED" 2>/dev/null || echo "0")

  echo "[CRUOR] Assemblage OK — staged ${DURATION}s, ${RENDER_TIME}s de calcul"

  cat > "$DONE_FILE" <<EOF
STATUS=OK
STAGED=$STAGED
DURATION=${DURATION}s
RENDER_TIME=${RENDER_TIME}s
FORMAT=$FORMAT
EOF

  echo "[CRUOR] Signal  : $DONE_FILE"
  echo "[CRUOR] DONE    : $STAGED"
  exit 0
fi

# ─── Mode scène unique ────────────────────────────────────────────────────────
if [[ -z "$SCENE_CLASS" || -z "$OUTPUT" ]]; then
  echo "[CRUOR] ERREUR : --scene-class et --output obligatoires (mode scène unique)." >&2
  exit 1
fi

OUTPUT_DIR="$(dirname "$OUTPUT")"
DONE_FILE="${OUTPUT_DIR}/DONE_${SCENE_CLASS}.txt"
ERROR_LOG="${OUTPUT_DIR}/error_${SCENE_CLASS}.log"

mkdir -p "$OUTPUT_DIR"

echo "[CRUOR] Render scène : $SCENE_CLASS"
echo "  Scenes : $SCENES"
echo "  Output : $OUTPUT"

START_TS=$(date +%s)

docker run --rm \
  --name "angron_cruor_${SCENE_CLASS}_$$" \
  -v "${WORKSPACE}:/workspace" \
  -e DISPLAY=:99 \
  "$DOCKER_IMAGE" \
  bash -c "
    set -e
    Xvfb :99 -screen 0 1080x1920x24 2>/dev/null &
    sleep 2

    cd /workspace
    manimgl '${SCENES}' '${SCENE_CLASS}' -w 2>&1

    MP4=\$(find /workspace/videos -name '${SCENE_CLASS}.mp4' 2>/dev/null | sort | tail -1)
    if [[ -z \"\$MP4\" ]]; then
      echo 'ERROR: aucun MP4 trouvé' >&2
      exit 2
    fi
    cp \"\$MP4\" '/workspace/${OUTPUT}'
    echo \"MP4 : \$MP4 → /workspace/${OUTPUT}\"
  " 2>&1 | tee "$ERROR_LOG"

DOCKER_EXIT="${PIPESTATUS[0]}"
END_TS=$(date +%s)
RENDER_TIME=$(( END_TS - START_TS ))

if [[ "$DOCKER_EXIT" -ne 0 ]]; then
  echo "[CRUOR] RENDER FAILED (exit $DOCKER_EXIT)" >&2
  echo "STATUS=ERROR" > "$DONE_FILE"
  exit "$DOCKER_EXIT"
fi

DURATION=$(ffprobe -v quiet -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "$OUTPUT" 2>/dev/null || echo "0")

echo "[CRUOR] OK — ${SCENE_CLASS} : ${DURATION}s en ${RENDER_TIME}s"

cat > "$DONE_FILE" <<EOF
STATUS=OK
SCENE_CLASS=$SCENE_CLASS
OUTPUT=$OUTPUT
DURATION=${DURATION}s
RENDER_TIME=${RENDER_TIME}s
EOF

echo "[CRUOR] Signal : $DONE_FILE"
echo "[CRUOR] DONE   : $OUTPUT"
