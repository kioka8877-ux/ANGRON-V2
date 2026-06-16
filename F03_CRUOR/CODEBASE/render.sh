#!/usr/bin/env bash
# render.sh — F03_CRUOR V2 : render manimgl par scene + assemblage via stage.py.

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

  echo "[CRUOR] Render toutes scenes manimgl + assemblage..."
  echo "  Scenes  : $SCENES"
  echo "  Out dir : $OUT_DIR"
  echo "  Staged  : $STAGED"
  echo "  Image   : $DOCKER_IMAGE"

  SCENE_CLASSES=$(grep -oP '^class \K\w+(?=\(InteractiveScene\))' "$SCENES" | sort || true)
  if [[ -z "$SCENE_CLASSES" ]]; then
    echo "[CRUOR] ERREUR : aucune classe InteractiveScene trouvee dans $SCENES" >&2
    exit 1
  fi

  echo "[CRUOR] Scenes detectees :"
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
    bash /workspace/F03_CRUOR/CODEBASE/docker_render_inner.sh

  DOCKER_EXIT=$?
  END_TS=$(date +%s)
  RENDER_TIME=$(( END_TS - START_TS ))

  if [[ "$DOCKER_EXIT" -ne 0 ]]; then
    echo "[CRUOR] RENDER FAILED (exit $DOCKER_EXIT)" >&2
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

echo "[CRUOR] Mode scene unique non utilise en V2." >&2
exit 1
