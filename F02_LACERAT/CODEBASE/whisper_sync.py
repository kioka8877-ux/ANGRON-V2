"""
whisper_sync.py — F02_LACERAT : extraction des timestamps Whisper.

Lance Whisper sur l'audio voix, aligne avec le script SANGUIS,
produit whisper_timestamps.json que LACERAT utilise pour storyboarder.

Usage :
    python3 F02_LACERAT/CODEBASE/whisper_sync.py \
        --audio F02_LACERAT/IN/voice_XXX.mp3 \
        --script F01_SANGUIS/OUT/script_XXX.md \
        --output F02_LACERAT/OUT/whisper_timestamps.json \
        --format short

Claude INACTIF pendant l'exécution.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_script_blocs(script_path: Path) -> list[dict]:
    """Extrait les lignes de narration (hors [ANIM:], hors titres markdown)."""
    blocs = []
    text = script_path.read_text(encoding="utf-8")

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("[ANIM:"):
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            continue
        if stripped.startswith("---"):
            continue
        # Ligne de narration
        # Nettoie les balises markdown basiques (**bold**, *italic*)
        clean = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", stripped)
        if clean:
            blocs.append(clean)

    return blocs


def run_whisper(audio_path: Path, model: str = "base") -> list[dict]:
    """Lance Whisper et retourne les segments avec timestamps."""
    try:
        import whisper
    except ImportError:
        print(
            "[WHISPER] ERREUR : whisper non installé. `pip install openai-whisper`",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"[WHISPER] Chargement modèle '{model}'...")
    model_obj = whisper.load_model(model)

    print(f"[WHISPER] Transcription : {audio_path}")
    result = model_obj.transcribe(
        str(audio_path),
        language="fr",
        word_timestamps=True,
        verbose=False,
    )

    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "id":    seg["id"] + 1,
            "texte": seg["text"].strip(),
            "start": round(seg["start"], 3),
            "end":   round(seg["end"],   3),
        })

    return segments, result.get("segments", [])[-1]["end"] if result.get("segments") else 0.0


def align_blocs(whisper_segments: list[dict], script_lines: list[str]) -> list[dict]:
    """
    Tente d'aligner les segments Whisper avec les lignes de script.
    Si les comptes divergent, retourne les segments Whisper tels quels
    (LACERAT alignera manuellement).
    """
    if len(whisper_segments) == len(script_lines):
        aligned = []
        for i, (seg, line) in enumerate(zip(whisper_segments, script_lines)):
            aligned.append({
                "id":     i + 1,
                "texte":  line,          # texte script (plus propre)
                "whisper": seg["texte"], # transcription Whisper pour vérif
                "start":  seg["start"],
                "end":    seg["end"],
            })
        return aligned

    # Compte différent : on retourne Whisper brut, LACERAT aligne
    return whisper_segments


def main() -> None:
    parser = argparse.ArgumentParser(description="LACERAT whisper_sync — timestamps F02")
    parser.add_argument("--audio",  required=True, help="voice_XXX.mp3")
    parser.add_argument("--script", required=True, help="script_XXX.md (F01 output)")
    parser.add_argument("--output", required=True, help="whisper_timestamps.json")
    parser.add_argument("--format", default="short", choices=["short", "longform"])
    parser.add_argument("--model",  default="base",
                        choices=["tiny", "base", "small", "medium", "large"],
                        help="Modèle Whisper (défaut: base ~150MB)")
    args = parser.parse_args()

    audio_path  = Path(args.audio)
    script_path = Path(args.script)
    output_path = Path(args.output)

    if not audio_path.exists():
        print(f"[WHISPER] ERREUR : audio introuvable : {audio_path}", file=sys.stderr)
        sys.exit(1)
    if not script_path.exists():
        print(f"[WHISPER] ERREUR : script introuvable : {script_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    script_lines = parse_script_blocs(script_path)
    print(f"[WHISPER] Script : {len(script_lines)} lignes de narration détectées")

    segments, duree_totale = run_whisper(audio_path, model=args.model)
    print(f"[WHISPER] Segments Whisper : {len(segments)}, durée totale : {duree_totale:.1f}s")

    blocs = align_blocs(segments, script_lines)

    aligned_flag = len(segments) == len(script_lines)
    print(f"[WHISPER] Alignement : {'AUTO (1:1)' if aligned_flag else 'MANUEL requis par LACERAT'}")

    output = {
        "version":       "1.0",
        "audio":         str(audio_path),
        "script":        str(script_path),
        "format":        args.format,
        "duree_totale":  round(duree_totale, 3),
        "nb_blocs":      len(blocs),
        "aligned":       aligned_flag,
        "blocs":         blocs,
    }

    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[WHISPER] Timestamps → {output_path}")
    print(f"[WHISPER] DONE")


if __name__ == "__main__":
    main()
