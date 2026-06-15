#!/usr/bin/env bash
# finish.sh — F04_NAILS V2 : fusion vidéo + audio + mode hook (concat clip réel).
#
# Usage — mode math_script (voix off) :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --staged F03_CRUOR/OUT/staged_XXX.mp4 \
#     --audio  F02_LACERAT/IN/voice_XXX.mp3 \
#     --mode   math_script \
#     --format short|longform \
#     --output F04_NAILS/OUT/nails_out_XXX.mp4
#
# Usage — mode math_no_script (musique) :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --staged F03_CRUOR/OUT/staged_XXX.mp4 \
#     --audio  F04_NAILS/IN/music_XXX.mp3 \
#     --mode   math_no_script \
#     --format short|longform \
#     --output F04_NAILS/OUT/nails_out_XXX.mp4
#
# Usage — mode hook (clip réel + manim concat) :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --staged F03_CRUOR/OUT/staged_XXX.mp4 \
#     --audio  F02_LACERAT/IN/voice_XXX.mp3 \
#     --hook   F02_LACERAT/IN/HOOK/hook_ready.mp4 \
#     --mode   hook \
#     --format short|longform \
#     --output F04_NAILS/OUT/nails_out_XXX.mp4
#
# Claude INACTIF pendant l'exécution. Signal de fin : NAILS_DONE.txt.

set -euo pipefail

STAGED=""
AUDIO=""
HOOK=""
FORMAT=""
MODE=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --staged) STAGED="$2"; shift 2 ;;
    --audio)  AUDIO="$2";  shift 2 ;;
    --hook)   HOOK="$2";   shift 2 ;;
    --mode)   MODE="$2";   shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    # Compat V1 — --video accepté comme alias de --staged
    --video)  STAGED="$2"; shift 2 ;;
    *) echo "[NAILS] Argument inconnu : $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$STAGED" || -z "$FORMAT" || -z "$OUTPUT" || -z "$MODE" ]]; then
  echo "[NAILS] ERREUR : --staged, --mode, --format et --output sont obligatoires." >&2
  exit 1
fi

if [[ "$FORMAT" != "short" && "$FORMAT" != "longform" ]]; then
  echo "[NAILS] ERREUR : --format doit être 'short' ou 'longform'." >&2
  exit 1
fi

if [[ ! -f "$STAGED" ]]; then
  echo "[NAILS] ERREUR : vidéo staged introuvable : $STAGED" >&2
  exit 1
fi

if [[ "$MODE" == "hook" && -z "$HOOK" ]]; then
  echo "[NAILS] ERREUR : mode hook requiert --hook <hook_ready.mp4>" >&2
  exit 1
fi

if [[ -n "$HOOK" && ! -f "$HOOK" ]]; then
  echo "[NAILS] ERREUR : hook introuvable : $HOOK" >&2
  exit 1
fi

OUTPUT_DIR="$(dirname "$OUTPUT")"
mkdir -p "$OUTPUT_DIR"
DONE_FILE="$OUTPUT_DIR/NAILS_DONE.txt"

echo "[NAILS] Mode : $MODE"
echo "[NAILS] Staged  : $STAGED"
[[ -n "$AUDIO" ]] && echo "[NAILS] Audio   : $AUDIO"
[[ -n "$HOOK"  ]] && echo "[NAILS] Hook    : $HOOK"
echo "[NAILS] Format  : $FORMAT"
echo "[NAILS] Output  : $OUTPUT"

HOOK_FADED=""

# ─── Mode hook : fade audio clip + concat clip + manim ───────────────────────
if [[ "$MODE" == "hook" ]]; then
  HOOK_FADED="$OUTPUT_DIR/hook_faded.mp4"

  # Durée du clip hook — utilisée pour fade OUT et pour décaler la voix off
  HOOK_DUR=$(ffprobe -v quiet -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$HOOK" 2>/dev/null || echo "5")
  FADE_START=$(echo "$HOOK_DUR - 1" | bc)

  echo "[NAILS] Fade audio clip hook (1s à t=${FADE_START}s)..."
  ffmpeg -y \
    -i "$HOOK" \
    -af "afade=t=out:st=${FADE_START}:d=1" \
    -c:v copy \
    "$HOOK_FADED"

  # Concat hook_faded + staged (vidéo seule — audio ajouté après)
  CONCAT_NO_AUDIO="$OUTPUT_DIR/concat_no_audio.mp4"
  echo "[NAILS] Concat hook + manim..."
  ffmpeg -y \
    -i "$HOOK_FADED" \
    -i "$STAGED" \
    -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[vout]" \
    -map "[vout]" \
    -c:v libx264 -crf 18 -preset fast \
    "$CONCAT_NO_AUDIO"

  # Fusion concat + voix — la voix démarre après la fin du clip hook
  if [[ -n "$AUDIO" && -f "$AUDIO" ]]; then
    # Délai en millisecondes = durée hook * 1000
    HOOK_DUR_MS=$(python3 -c "import math; print(int(math.ceil(float('${HOOK_DUR}') * 1000)))")
    echo "[NAILS] Fusion concat + voix (délai voix : ${HOOK_DUR}s = ${HOOK_DUR_MS}ms)..."
    ffmpeg -y \
      -i "$CONCAT_NO_AUDIO" \
      -i "$AUDIO" \
      -filter_complex "[1:a]adelay=${HOOK_DUR_MS}|${HOOK_DUR_MS}[a_delayed]" \
      -map 0:v:0 \
      -map "[a_delayed]" \
      -c:v copy \
      -c:a aac -b:a 192k -ar 48000 -ac 2 \
      -shortest \
      "$OUTPUT"
  else
    # Pas de voix — on prend l'audio du clip hook seulement
    cp "$CONCAT_NO_AUDIO" "$OUTPUT"
  fi

# ─── Mode math_script ou math_no_script : fusion staged + audio ──────────────
else
  if [[ -z "$AUDIO" || ! -f "$AUDIO" ]]; then
    echo "[NAILS] ERREUR : --audio requis en mode $MODE" >&2
    exit 1
  fi

  echo "[NAILS] Fusion vidéo + audio..."
  ffmpeg -y \
    -i "$STAGED" \
    -i "$AUDIO" \
    -map 0:v:0 \
    -map 1:a:0 \
    -c:v copy \
    -c:a aac -b:a 192k -ar 48000 -ac 2 \
    -shortest \
    "$OUTPUT"
fi

echo "[NAILS] Fusion OK — $(du -h "$OUTPUT" | cut -f1)"

cat > "$DONE_FILE" <<EOF
NAILS_DONE
mode=$MODE
format=$FORMAT
output=$OUTPUT
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo "[NAILS] Signal  : $DONE_FILE"
echo "[NAILS] DONE    : $OUTPUT"
