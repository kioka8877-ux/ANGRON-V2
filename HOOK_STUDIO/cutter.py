"""
cutter.py — HOOK_STUDIO : découpe et mise en forme du clip hook via FFmpeg.

Fonctionnalités :
  - Trim IN/OUT (secondes flottantes)
  - Speed (0.5x à 2.0x)
  - Volume (0.0 à 2.0)
  - Format 9:16 blur-pad (Short) ou 16:9 (Longform)
  - Sortie : HOOK_STUDIO/OUT/hook_ready.mp4

Usage :
    python3 HOOK_STUDIO/cutter.py \
        --input  HOOK_STUDIO/tmp/clip_brut.mp4 \
        --output HOOK_STUDIO/OUT/hook_ready.mp4 \
        --in-point  3.5 \
        --out-point 12.0 \
        --format 9:16 \
        [--speed 1.0] \
        [--volume 1.0]
"""

import argparse
import subprocess
import sys
from pathlib import Path


def build_filter(
    speed: float,
    volume: float,
    fmt: str,
) -> tuple[str, str]:
    """Retourne (vf, af) pour ffmpeg -vf / -af."""
    vf_parts = []
    af_parts = []

    if fmt == "9:16":
        # Blur-pad : background flouté + crop 9:16 centré
        vf_parts.append(
            "split[orig][bg];"
            "[bg]scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,boxblur=20:20[blurred];"
            "[orig]scale=1080:1920:force_original_aspect_ratio=decrease[scaled];"
            "[blurred][scaled]overlay=(W-w)/2:(H-h)/2"
        )
    else:
        # 16:9 standard
        vf_parts.append("scale=1920:1080:force_original_aspect_ratio=decrease,"
                        "pad=1920:1080:(ow-iw)/2:(oh-ih)/2")

    if speed != 1.0:
        vf_parts.append(f"setpts={1.0/speed:.4f}*PTS")
        af_parts.append(f"atempo={speed:.2f}")

    if volume != 1.0:
        af_parts.append(f"volume={volume:.2f}")

    vf = ",".join(vf_parts) if vf_parts else "null"
    af = ",".join(af_parts) if af_parts else "anull"
    return vf, af


def cut_clip(
    input_path: Path,
    output_path: Path,
    in_point: float,
    out_point: float,
    fmt: str,
    speed: float,
    volume: float,
) -> None:
    if not input_path.exists():
        print(f"[CUTTER] ERREUR : input introuvable : {input_path}", file=sys.stderr)
        sys.exit(1)

    duration = out_point - in_point
    if duration <= 0:
        print(f"[CUTTER] ERREUR : out_point ({out_point}) <= in_point ({in_point})", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    vf, af = build_filter(speed, volume, fmt)

    print(f"[CUTTER] Trim  : {in_point}s → {out_point}s ({duration:.1f}s)")
    print(f"[CUTTER] Speed : {speed}x  Volume : {volume}x  Format : {fmt}")
    print(f"[CUTTER] Output: {output_path}")

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(in_point),
        "-i", str(input_path),
        "-t", str(duration),
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[CUTTER] ERREUR FFmpeg :\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"[CUTTER] DONE — {output_path.name} ({size_mb:.1f} MB)")


def copy_to_lacerat(hook_ready: Path) -> None:
    dest_dir = Path("F02_LACERAT/IN/HOOK")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "hook_ready.mp4"

    import shutil
    shutil.copy2(str(hook_ready), str(dest))
    print(f"[CUTTER] Copie auto → {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CUTTER — FFmpeg cutter HOOK_STUDIO")
    parser.add_argument("--input",      required=True, help="Clip brut .mp4")
    parser.add_argument("--output",     required=True, help="hook_ready.mp4")
    parser.add_argument("--in-point",   required=True, type=float, help="Début trim (secondes)")
    parser.add_argument("--out-point",  required=True, type=float, help="Fin trim (secondes)")
    parser.add_argument("--format",     required=True, choices=["9:16", "16:9"],
                        help="9:16 = Short blur-pad | 16:9 = Longform")
    parser.add_argument("--speed",      default=1.0, type=float, help="Vitesse (0.5–2.0)")
    parser.add_argument("--volume",     default=1.0, type=float, help="Volume (0.0–2.0)")
    parser.add_argument("--no-copy",    action="store_true",
                        help="Ne pas copier vers F02_LACERAT/IN/HOOK/ automatiquement")
    parser.add_argument("--hook-question", default=None,
                        help="Question hook à écrire dans ledger.json")
    args = parser.parse_args()

    input_path  = Path(args.input)
    output_path = Path(args.output)

    cut_clip(
        input_path=input_path,
        output_path=output_path,
        in_point=args.in_point,
        out_point=args.out_point,
        fmt=args.format,
        speed=args.speed,
        volume=args.volume,
    )

    if not args.no_copy:
        copy_to_lacerat(output_path)

    # Ecrire hook_question dans ledger si fournie
    if args.hook_question:
        _write_hook_question_to_ledger(args.hook_question, output_path)


def _write_hook_question_to_ledger(question: str, hook_path: Path) -> None:
    import json
    ledger_path = Path(".angron/ledger.json")
    if not ledger_path.exists():
        print(f"[CUTTER] AVERTISSEMENT : ledger.json introuvable — hook_question non écrite.", file=sys.stderr)
        return

    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["projet_actif"]["hook"]["hook_question"]   = question
        ledger["projet_actif"]["hook"]["hook_ready_path"] = str(hook_path)
        ledger_path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[CUTTER] hook_question → ledger.json")
    except Exception as e:
        print(f"[CUTTER] AVERTISSEMENT : impossible d'écrire ledger : {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
