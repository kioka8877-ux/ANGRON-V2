#!/usr/bin/env bash
# render.sh — F03_CRUOR V2 : render manimgl par scène + assemblage via stage.py.

set -euo pipefail

DOCKER_IMAGE="ghcr.io/kioka8877-ux/angron-v2:latest"

SCENES=""
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

if [[ ! -f "$SCENES" ]]; then
  echo "[CRUOR] ERREUR : fichier scenes introuvable : $SCENES" >&2
  exit 1
fi

WORKSPACE="$(pwd)"

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
    -e MANIMGL_OUT_DIR="${OUT_DIR}" \
    -e MANIMGL_STAGED="${STAGED}" \
    -e MANIMGL_SCENES="${SCENES}" \
    "$DOCKER_IMAGE" \
    bash << 'DOCKEREOF'
set -e
Xvfb :99 -screen 0 1080x1920x24 2>/dev/null &
sleep 2

echo "=== [DEBUG] default_config.yml manimgl ==="
find /usr/local/lib/python3.11/site-packages/manimlib -name "default_config.yml" -exec cat {} \;
echo "=== [DEBUG] fin default_config ==="

# Config portrait — clés officielles manimgl default_config.yml
mkdir -p /root/.config/manim
cat > /root/.config/manim/custom_config.yml << 'CFEOF'
camera:
  resolution: (1080, 1920)
  fps: 60
CFEOF

# Aussi en CWD + répertoire scènes
cp /root/.config/manim/custom_config.yml /workspace/custom_config.yml
cp /root/.config/manim/custom_config.yml /workspace/F03_CRUOR/CODEBASE/custom_config.yml

echo "=== [DEBUG] custom_config.yml écrit ==="
cat /root/.config/manim/custom_config.yml
echo "=== [DEBUG] fin custom_config ==="

OUT_BASE="/workspace/${MANIMGL_OUT_DIR}"

while IFS= read -r SCENE_CLS; do
  echo "[CRUOR] Render $SCENE_CLS..."
  cd /workspace
  manimgl "${MANIMGL_SCENES}" "$SCENE_CLS" -w 2>&1

  MP4=$(find /workspace/videos -name "${SCENE_CLS}.mp4" 2>/dev/null | sort | tail -1)
  if [[ -z "$MP4" ]]; then
    echo "ERROR: aucun MP4 pour $SCENE_CLS" >&2
    exit 2
  fi
  echo "[DEBUG] Dimensions $SCENE_CLS : $(ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$MP4" 2>/dev/null)"
  cp "$MP4" "${OUT_BASE}/${SCENE_CLS}.mp4"
  echo "[CRUOR] $SCENE_CLS → ${OUT_BASE}/${SCENE_CLS}.mp4"
done < <(grep -oP '^class \K\w+(?=\(InteractiveScene\))' "/workspace/${MANIMGL_SCENES}" | sort)

python3 /workspace/F03_CRUOR/CODEBASE/stage.py \
  --in-dir  "$OUT_BASE" \
  --output  "/workspace/${MANIMGL_STAGED}" 2>&1
echo "[CRUOR] Assemblage terminé."
DOCKEREOF

  DOCKER_EXIT="${PIPESTATUS[0]}"
  END_TS=$(date +%s)
  RENDER_TIME=$(( END_TS - START_TS ))

  if [[ "$DOCKER_EXIT" -ne 0 ]]; then
    echo "[CRUOR] RENDER FAILED (exit $DOCKER_EXIT) — voir $ERROR_LOG" >&2
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

  echo "[CRUOR] DONE : $STAGED"
  exit 0
fi

# ─── Mode scène unique ────────────────────────────────────────────────────────
echo "[CRUOR] Mode scène unique non utilisé en V2." >&2
exit 1

