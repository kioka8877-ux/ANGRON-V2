"""
stage.py — F03_CRUOR V2 : assemblage alphabetique des scenes manimgl rendues.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def collect_scenes(in_dir: Path) -> list[Path]:
    mp4s = sorted(
        p for p in in_dir.glob("*.mp4")
        if not p.name.startswith("staged")
        and not p.name.startswith("cruor_render_")
    )
    return mp4s


def concat_scenes(scenes: list[Path], output: Path) -> None:
    if not scenes:
        print("[STAGE] ERREUR : aucun MP4 dans le repertoire.", file=sys.stderr)
        sys.exit(1)

    print(f"[STAGE] {len(scenes)} scene(s) a assembler :")
    for s in scenes:
        print(f"  {s.name}")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as flist:
        for scene in scenes:
            flist.write(f"file '{scene.resolve()}'\n")
        flist_path = flist.name

    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", flist_path,
        "-c", "copy",
        str(output),
    ]

    print(f"[STAGE] FFmpeg concat -> {output}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[STAGE] ERREUR FFmpeg :\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)

    print(f"[STAGE] DONE -- {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="STAGE -- assemblage scenes manimgl V2")
    parser.add_argument("--in-dir", required=True, help="Dossier contenant les scenes .mp4")
    parser.add_argument("--output", required=True, help="cruor_render_XXX.mp4")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    output = Path(args.output)

    if not in_dir.is_dir():
        print(f"[STAGE] ERREUR : repertoire introuvable : {in_dir}", file=sys.stderr)
        sys.exit(1)

    scenes = collect_scenes(in_dir)
    if not scenes:
        print(f"[STAGE] ERREUR : aucun MP4 trouve dans {in_dir}", file=sys.stderr)
        sys.exit(1)

    concat_scenes(scenes, output)


if __name__ == "__main__":
    main()
