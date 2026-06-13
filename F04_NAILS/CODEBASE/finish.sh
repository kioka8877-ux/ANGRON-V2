#!/usr/bin/env bash
# finish.sh — F04_NAILS : fusion vidéo Manim + audio voix clonée.
#
# Usage :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --video F03_CRUOR/OUT/cruor_render_[ID].mp4 \
#     --audio F02_LACERAT/IN/voice_[ID].mp3 \
#     --format short|longform \
#     --output F04_NAILS/OUT/nails_out_[ID].mp4
#
# Claude INACTIF pendant l'exécution. Signal de fin : NAILS_DONE.txt.

set -euo pipefail

# --- Parse args ---
VIDEO=""
AUDIO=""
FORMAT=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --video)  VIDEO="$2";  shift 2 ;;
    --audio)  AUDIO="$2";  shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    *) echo "[NAILS] Argument inconnu : $1" >&2; exit 1 ;;
  esac
done

# --- Validation ---
if [[ -z "$VIDEO" || -z "$AUDIO" || -z "$FORMAT" || -z "$OUTPUT" ]]; then
  echo "[NAILS] ERREUR : --video, --audio, --format et --output sont obligatoires." >&2
  exit 1
fi

if [[ "$FORMAT" != "short" && "$FORMAT" != "longform" ]]; then
  echo "[NAILS] ERREUR : --format doit être 'short' ou 'longform'." >&2
  exit 1
fi

if [[ ! -f "$VIDEO" ]]; then
  echo "[NAILS] ERREUR : vidéo introuvable : $VIDEO" >&2
  exit 1
fi

if [[ ! -f "$AUDIO" ]]; then
  echo "[NAILS] ERREUR : audio introuvable : $AUDIO" >&2
  exit 1
fi

OUTPUT_DIR="$(dirname "$OUTPUT")"
mkdir -p "$OUTPUT_DIR"

DONE_FILE="$OUTPUT_DIR/NAILS_DONE.txt"

echo "[NAILS] Fusion audio+vidéo..."
echo "  Vidéo  : $VIDEO"
echo "  Audio  : $AUDIO"
echo "  Format : $FORMAT"
echo "  Output : $OUTPUT"

# --- FFmpeg fusion ---
# Vidéo : stream copy (Manim render est déjà H264 propre)
# Audio  : encode AAC 192k 48kHz stéréo
ffmpeg -y \
  -i "$VIDEO" \
  -i "$AUDIO" \
  -map 0:v:0 \
  -map 1:a:0 \
  -c:v copy \
  -c:a aac \
  -b:a 192k \
  -ar 48000 \
  -ac 2 \
  -shortest \
  "$OUTPUT"

echo "[NAILS] Fusion OK — $(du -h "$OUTPUT" | cut -f1)"

# --- Signal ---
cat > "$DONE_FILE" <<EOF
NAILS_DONE
format=$FORMAT
output=$OUTPUT
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo "[NAILS] Signal  : $DONE_FILE"
echo "[NAILS] DONE    : $OUTPUT"
