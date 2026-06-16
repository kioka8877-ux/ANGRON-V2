#!/usr/bin/env bash
# finish.sh — F04_NAILS V2 : fusion video + audio + modes hook / image_bg / math_*.
#
# Usage — mode hook :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --staged F03_CRUOR/OUT/cruor_render_XXX.mp4 \
#     --audio  F02_LACERAT/IN/voice_XXX.mp3 \
#     --hook   F02_LACERAT/IN/HOOK/hook_ready.mp4 \
#     --mode   hook --format short --output F04_NAILS/OUT/nails_out_XXX.mp4
#
# Usage — mode image_bg (manim flotte sur photo apres le hook) :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --staged   F03_CRUOR/OUT/cruor_render_XXX.mp4 \
#     --audio    F02_LACERAT/IN/voice_XXX.mp3 \
#     --hook     F02_LACERAT/IN/HOOK/hook_ready.mp4 \
#     --bg-image F02_LACERAT/IN/bg_lamine.jpg \
#     --mode     image_bg --format short --output F04_NAILS/OUT/nails_out_XXX.mp4
#
# Usage — mode math_script / math_no_script :
#   bash F04_NAILS/CODEBASE/finish.sh \
#     --staged F03_CRUOR/OUT/cruor_render_XXX.mp4 \
#     --audio  F02_LACERAT/IN/voice_XXX.mp3 \
#     --mode   math_script --format short --output F04_NAILS/OUT/nails_out_XXX.mp4

set -euo pipefail

STAGED=""
AUDIO=""
HOOK=""
BG_IMAGE=""
FORMAT=""
MODE=""
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --staged)   STAGED="$2";   shift 2 ;;
    --audio)    AUDIO="$2";    shift 2 ;;
    --hook)     HOOK="$2";     shift 2 ;;
    --bg-image) BG_IMAGE="$2"; shift 2 ;;
    --mode)     MODE="$2";     shift 2 ;;
    --format)   FORMAT="$2";   shift 2 ;;
    --output)   OUTPUT="$2";   shift 2 ;;
    --video)    STAGED="$2";   shift 2 ;;
    *) echo "[NAILS] Argument inconnu : $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$STAGED" || -z "$FORMAT" || -z "$OUTPUT" || -z "$MODE" ]]; then
  echo "[NAILS] ERREUR : --staged, --mode, --format et --output sont obligatoires." >&2; exit 1
fi
if [[ "$FORMAT" != "short" && "$FORMAT" != "longform" ]]; then
  echo "[NAILS] ERREUR : --format doit etre short ou longform." >&2; exit 1
fi
if [[ ! -f "$STAGED" ]]; then
  echo "[NAILS] ERREUR : video staged introuvable : $STAGED" >&2; exit 1
fi
if [[ "$MODE" == "hook" || "$MODE" == "image_bg" ]] && [[ -z "$HOOK" ]]; then
  echo "[NAILS] ERREUR : modes hook et image_bg requierent --hook <hook_ready.mp4>" >&2; exit 1
fi
if [[ -n "$HOOK" && ! -f "$HOOK" ]]; then
  echo "[NAILS] ERREUR : hook introuvable : $HOOK" >&2; exit 1
fi

OUTPUT_DIR="$(dirname "$OUTPUT")"
mkdir -p "$OUTPUT_DIR"
DONE_FILE="$OUTPUT_DIR/NAILS_DONE.txt"
ORIGINAL_MODE="$MODE"

echo "[NAILS] Mode    : $MODE"
echo "[NAILS] Staged  : $STAGED"
[[ -n "$AUDIO"    ]] && echo "[NAILS] Audio   : $AUDIO"
[[ -n "$HOOK"     ]] && echo "[NAILS] Hook    : $HOOK"
[[ -n "$BG_IMAGE" ]] && echo "[NAILS] BgImage : $BG_IMAGE"
echo "[NAILS] Format  : $FORMAT"
echo "[NAILS] Output  : $OUTPUT"

# ---- mode image_bg : composite manim sur photo, puis logique hook ------------
if [[ "$MODE" == "image_bg" ]]; then
  if [[ -z "$BG_IMAGE" || ! -f "$BG_IMAGE" ]]; then
    echo "[NAILS] ERREUR : mode image_bg requiert --bg-image <image.jpg|.png>" >&2; exit 1
  fi

  STAGED_DUR=$(ffprobe -v quiet -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$STAGED" 2>/dev/null || echo "60")

  COMPOSITED="$OUTPUT_DIR/composited.mp4"
  echo "[NAILS] Composite manim sur image bg (screen blend, duree ${STAGED_DUR}s)..."

  # Scale image en portrait 1080x1920, boucle sur la duree de la video,
  # puis blend mode screen : supprime le fond noir, laisse passer les elements lumineux.
  # Formule screen : resultat = 1 - (1-a)*(1-b)  -> zones noires = transparentes.
  ffmpeg -y \
    -loop 1 -i "$BG_IMAGE" \
    -i "$STAGED" \
    -filter_complex \
      "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2[bg];[bg][1:v]blend=all_mode=screen[vout]" \
    -map "[vout]" \
    -c:v libx264 -crf 18 -preset fast \
    -t "$STAGED_DUR" \
    "$COMPOSITED"

  STAGED="$COMPOSITED"
  MODE="hook"
  echo "[NAILS] Composite OK -> poursuite en logique hook"
fi

HOOK_FADED=""

# ---- mode hook (et image_bg apres preprocessing) ----------------------------
if [[ "$MODE" == "hook" ]]; then
  HOOK_FADED="$OUTPUT_DIR/hook_faded.mp4"

  HOOK_DUR=$(ffprobe -v quiet -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$HOOK" 2>/dev/null || echo "5")
  FADE_START=$(echo "$HOOK_DUR - 1" | bc)

  echo "[NAILS] Fade audio clip hook (1s a t=${FADE_START}s)..."
  ffmpeg -y \
    -i "$HOOK" \
    -af "afade=t=out:st=${FADE_START}:d=1" \
    -c:v copy \
    "$HOOK_FADED"

  CONCAT_NO_AUDIO="$OUTPUT_DIR/concat_no_audio.mp4"
  echo "[NAILS] Concat hook + manim (composited si image_bg)..."
  ffmpeg -y \
    -i "$HOOK_FADED" \
    -i "$STAGED" \
    -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[vout]" \
    -map "[vout]" \
    -c:v libx264 -crf 18 -preset fast \
    "$CONCAT_NO_AUDIO"

  if [[ -n "$AUDIO" && -f "$AUDIO" ]]; then
    HOOK_DUR_MS=$(python3 -c "import math; print(int(math.ceil(float('${HOOK_DUR}') * 1000)))")
    echo "[NAILS] Fusion concat + voix (delai voix : ${HOOK_DUR}s = ${HOOK_DUR_MS}ms)..."
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
    cp "$CONCAT_NO_AUDIO" "$OUTPUT"
  fi

# ---- mode math_script ou math_no_script -------------------------------------
else
  if [[ -z "$AUDIO" || ! -f "$AUDIO" ]]; then
    echo "[NAILS] ERREUR : --audio requis en mode $MODE" >&2; exit 1
  fi

  echo "[NAILS] Fusion video + audio..."
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

echo "[NAILS] Fusion OK -- $(du -h "$OUTPUT" | cut -f1)"

cat > "$DONE_FILE" <<EOF
NAILS_DONE
mode=$ORIGINAL_MODE
format=$FORMAT
output=$OUTPUT
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo "[NAILS] Signal  : $DONE_FILE"
echo "[NAILS] DONE    : $OUTPUT"
