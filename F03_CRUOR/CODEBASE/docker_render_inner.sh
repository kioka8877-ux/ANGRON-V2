#!/usr/bin/env bash
set -e

# Install bold sans-serif font for Text() rendering
apt-get install -y --no-install-recommends fonts-liberation > /dev/null 2>&1 || true
fc-cache -fv > /dev/null 2>&1 || true

Xvfb :99 -screen 0 1080x1920x24 2>/dev/null &
sleep 2

printf 'camera:
  resolution: (1080, 1920)
  fps: 60
' > /tmp/angron_portrait.yml
cp /tmp/angron_portrait.yml /workspace/custom_config.yml
echo "[CRUOR] Config portrait OK"

OUT_BASE="/workspace/${MANIMGL_OUT_DIR}"

while IFS= read -r SCENE_CLS; do
  echo "[CRUOR] Render $SCENE_CLS..."
  cd /workspace
  manimgl --config_file /tmp/angron_portrait.yml "${MANIMGL_SCENES}" "$SCENE_CLS" -w 2>&1

  MP4=$(find /workspace/videos -name "${SCENE_CLS}.mp4" 2>/dev/null | sort | tail -1)
  if [[ -z "$MP4" ]]; then
    echo "ERROR: aucun MP4 pour $SCENE_CLS" >&2
    exit 2
  fi
  echo "[DEBUG] Dimensions $SCENE_CLS : $(ffprobe -v quiet -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "$MP4" 2>/dev/null)"
  cp "$MP4" "${OUT_BASE}/${SCENE_CLS}.mp4"
  echo "[CRUOR] $SCENE_CLS -> ${OUT_BASE}/${SCENE_CLS}.mp4"
done < <(grep -oP '^class \K\w+(?=\(InteractiveScene\))' "/workspace/${MANIMGL_SCENES}" | sort)

python3 /workspace/F03_CRUOR/CODEBASE/stage.py   --in-dir  "$OUT_BASE"   --output  "/workspace/${MANIMGL_STAGED}" 2>&1

echo "[CRUOR] Assemblage OK"
