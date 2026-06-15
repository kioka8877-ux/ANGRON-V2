"""
stage.py — F03_CRUOR V2 : assemblage alphabétique des scènes manimgl rendues.

Lit tous les .mp4 dans --in-dir, les trie alphabétiquement (01_xxx...05_xxx),
les concatène via FFmpeg et écrit --output (staged_XXX.mp4).

Usage :
    python3 F03_CRUOR/CODEBASE/stage.py \
        --in-dir F03_CRUOR/OUT/ \
        --output F03_CRUOR/OUT/staged_XXX.mp4

Convention de nommage attendue (alphabétique = ordre de montage) :
    01_HookQuestion.mp4
    02_EquationReveal.mp4
    03_ProblemBeauty.mp4
    04_MathAnswer.mp4
    05_BodyApplication.mp4
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def collect_scenes(in_dir: Path) -> list[Path]:
    mp4s = sorted(p for p in in_dir.glob("*.mp4") if not p.name.startswith("staged"))
    return mp4s


def concat_scenes(scenes: list[Path], output: Path) -> None:
    if not scenes:
        print("[STAGE] ERREUR : aucun MP4 dans le répertoire.", file=sys.stderr)
        sys.exit(1)

    print(f"[STAGE] {len(scenes)} scène(s) à assembler :")
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

    print(f"[STAGE] FFmpeg concat → {output}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[STAGE] ERREUR FFmpeg :\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)

    print(f"[STAGE] DONE — {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="STAGE — assemblage scènes manimgl V2")
    parser.add_argument("--in-dir", required=True, help="Dossier contenant les NN_Scene.mp4")
    parser.add_argument("--output", required=True, help="staged_XXX.mp4")
    args = parser.parse_args()

    in_dir = Path(args.in_dir)
    output = Path(args.output)

    if not in_dir.is_dir():
        print(f"[STAGE] ERREUR : répertoire introuvable : {in_dir}", file=sys.stderr)
        sys.exit(1)

    scenes = collect_scenes(in_dir)
    if not scenes:
        print(f"[STAGE] ERREUR : aucun MP4 trouvé dans {in_dir}", file=sys.stderr)
        sys.exit(1)

    concat_scenes(scenes, output)


if __name__ == "__main__":
    main()
