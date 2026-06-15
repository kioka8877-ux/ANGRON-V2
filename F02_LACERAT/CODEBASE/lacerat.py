"""
lacerat.py — F02_LACERAT : génération des scènes manimgl via Claude.

V2 : génère scenes_XXX.py (multi-scènes manimgl) au lieu d'un storyboard markdown.
Architecture V2 : 4-5 classes InteractiveScene séparées nommées 01_xxx...05_xxx.

Usage :
    # Mode math_script (voix off + timestamps Whisper) :
    python3 F02_LACERAT/CODEBASE/lacerat.py \
        --script     F01_SANGUIS/OUT/script_XXX.md \
        --timestamps F02_LACERAT/OUT/whisper_timestamps_XXX.json \
        --mode       math_script \
        --id         XXX \
        --format     short \
        --output     F02_LACERAT/OUT/scenes_XXX.py

    # Mode math_no_script (pas de voix, [ANIM:] seuls) :
    python3 F02_LACERAT/CODEBASE/lacerat.py \
        --script F01_SANGUIS/OUT/script_XXX.md \
        --mode   math_no_script \
        --id     XXX \
        --format short \
        --output F02_LACERAT/OUT/scenes_XXX.py

    # Mode hook (clip réel en tête, arc 3B1B après) :
    python3 F02_LACERAT/CODEBASE/lacerat.py \
        --script    F01_SANGUIS/OUT/script_XXX.md \
        --timestamps F02_LACERAT/OUT/whisper_timestamps_XXX.json \
        --mode      hook \
        --hook-path F02_LACERAT/IN/HOOK/hook_ready.mp4 \
        --id        XXX \
        --format    short \
        --output    F02_LACERAT/OUT/scenes_XXX.py

Requiert :
    ANTHROPIC_API_KEY dans l'environnement
    pip install anthropic
"""

import argparse
import json
import os
import sys
from pathlib import Path

_META_PATH = Path("METAPROMPTS/META_LACERAT.md")

_META_FALLBACK = """
Tu es LACERAT, le traducteur tactique de la flotte ANGRON.
Tu génères du code manimgl V2. Règles strictes :
- Import : from manimlib import *
- Classe de base : InteractiveScene (jamais Scene)
- 4 à 5 classes séparées, une par segment de l'arc 3B1B
- Nommage : classes HookQuestion, EquationReveal, ProblemBeauty, MathAnswer, BodyApplication
- ShowCreation() (pas Create()), Tex() (pas MathTex()), FRAME_HEIGHT (pas config.pixel_height)
- Chaque classe est autonome et renderable séparément
""".strip()

MODES = ["math_script", "math_no_script", "hook"]

_SCENE_NAMES_SHORT = [
    "01_HookQuestion",
    "02_EquationReveal",
    "03_ProblemBeauty",
    "04_MathAnswer",
    "05_BodyApplication",
]


def _load_meta() -> str:
    if _META_PATH.exists():
        text = _META_PATH.read_text(encoding="utf-8").strip()
        print(f"[LACERAT] META chargé depuis {_META_PATH}", file=sys.stderr)
        return text
    print(f"[LACERAT] AVERTISSEMENT : {_META_PATH} introuvable — fallback minimal utilisé.", file=sys.stderr)
    return _META_FALLBACK


def load_timestamps(ts_path: Path) -> dict:
    return json.loads(ts_path.read_text(encoding="utf-8"))


def list_assets(assets_dir: Path) -> list[str]:
    if not assets_dir.exists():
        return []
    return [
        f.name
        for f in sorted(assets_dir.iterdir())
        if f.is_file() and not f.name.startswith(".")
    ]


def generate_scenes(
    script_text: str,
    mode: str,
    script_id: str,
    fmt: str,
    timestamps: dict | None,
    assets: list[str],
    hook_path: str | None,
) -> str:
    try:
        import anthropic
    except ImportError:
        print("[LACERAT] ERREUR : anthropic non installé. `pip install anthropic`", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[LACERAT] ERREUR : ANTHROPIC_API_KEY manquant.", file=sys.stderr)
        sys.exit(1)

    meta_system = _load_meta()
    client = anthropic.Anthropic(api_key=api_key)

    fmt_label  = "SHORT 9:16 (1080x1920)" if fmt == "short" else "LONGFORM 16:9 (1920x1080)"
    assets_str = "\n".join(f"  - {a}" for a in assets) if assets else "  (aucun)"

    scene_names_str = "\n".join(f"  {n}" for n in _SCENE_NAMES_SHORT)

    user_message = (
        f"ID PROJET : {script_id}\n"
        f"FORMAT    : {fmt_label}\n"
        f"MODE      : {mode}\n\n"
        f"--- SCRIPT SANGUIS ---\n{script_text}\n\n"
    )

    if timestamps:
        user_message += (
            f"--- TIMESTAMPS WHISPER ---\n"
            f"{json.dumps(timestamps, indent=2, ensure_ascii=False)}\n\n"
        )
    else:
        user_message += "--- TIMESTAMPS WHISPER --- : non fournis (mode math_no_script)\n\n"

    if mode == "hook" and hook_path:
        user_message += (
            f"--- MODE HOOK ---\n"
            f"Le clip hook_ready.mp4 est à : {hook_path}\n"
            f"Les scènes manimgl commencent APRÈS ce clip (F04_NAILS fait la concat).\n"
            f"La scène 01_HookQuestion peut faire référence visuellement au clip mais n'en dépend pas.\n\n"
        )

    user_message += (
        f"--- ASSETS DISPONIBLES ---\n{assets_str}\n\n"
        f"--- NOMMAGE DES SCÈNES (obligatoire) ---\n{scene_names_str}\n\n"
        "Génère un fichier Python manimgl complet avec 5 classes InteractiveScene.\n"
        "Chaque classe correspond à un segment de l'arc 3B1B (7s/8s/15s/20s/10s).\n"
        "Import obligatoire : from manimlib import *\n"
        "NE PAS importer from manim import *\n"
    )

    if mode == "math_no_script":
        user_message += (
            "\nMode math_no_script : pas de voix off.\n"
            "Les animations doivent être auto-suffisantes et auto-explicatives.\n"
            "Texte à l'écran (Tex/Text) peut remplacer la narration.\n"
        )

    print(f"[LACERAT] Génération scenes.py (claude-opus-4-8)...", file=sys.stderr)

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=8192,
        system=meta_system,
        messages=[{"role": "user", "content": user_message}],
    )

    return message.content[0].text


def main() -> None:
    parser = argparse.ArgumentParser(description="LACERAT — générateur scenes manimgl F02 V2")
    parser.add_argument("--script",      required=True, help="script_XXX.md (F01 output)")
    parser.add_argument("--mode",        required=True, choices=MODES,
                        help="math_script | math_no_script | hook")
    parser.add_argument("--id",          required=True, help="ID projet (ex: 002)")
    parser.add_argument("--format",      required=True, choices=["short", "longform"])
    parser.add_argument("--output",      required=True, help="F02_LACERAT/OUT/scenes_XXX.py")
    parser.add_argument("--timestamps",  default=None,
                        help="whisper_timestamps_XXX.json (optionnel en mode math_no_script)")
    parser.add_argument("--assets",      default="F02_LACERAT/IN/assets",
                        help="Dossier assets (défaut: F02_LACERAT/IN/assets)")
    parser.add_argument("--hook-path",   default=None,
                        help="(mode hook) chemin vers hook_ready.mp4")
    args = parser.parse_args()

    script_path = Path(args.script)
    output_path = Path(args.output)
    assets_dir  = Path(args.assets)

    if not script_path.exists():
        print(f"[LACERAT] ERREUR : script introuvable : {script_path}", file=sys.stderr)
        sys.exit(1)

    timestamps = None
    if args.timestamps:
        ts_path = Path(args.timestamps)
        if not ts_path.exists():
            print(f"[LACERAT] ERREUR : timestamps introuvables : {ts_path}", file=sys.stderr)
            sys.exit(1)
        timestamps = load_timestamps(ts_path)

    if args.mode == "math_script" and not timestamps:
        print("[LACERAT] AVERTISSEMENT : mode math_script sans timestamps — le sync sera approximatif.", file=sys.stderr)

    hook_path = getattr(args, "hook_path", None)
    if args.mode == "hook" and not hook_path:
        print("[LACERAT] AVERTISSEMENT : mode hook sans --hook-path — hook ignoré.", file=sys.stderr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    assets = list_assets(assets_dir)

    ts_info = f"{timestamps.get('nb_blocs', '?')} blocs, {timestamps.get('duree_totale', '?')}s" if timestamps else "non fournis"

    print(f"[LACERAT] Script     : {script_path}")
    print(f"[LACERAT] Mode       : {args.mode}")
    print(f"[LACERAT] Timestamps : {ts_info}")
    print(f"[LACERAT] Assets     : {len(assets)} fichier(s)")
    print(f"[LACERAT] Format     : {args.format}")

    scenes_py = generate_scenes(
        script_text=script_path.read_text(encoding="utf-8"),
        mode=args.mode,
        script_id=args.id,
        fmt=args.format,
        timestamps=timestamps,
        assets=assets,
        hook_path=hook_path,
    )

    output_path.write_text(scenes_py, encoding="utf-8")
    print(f"[LACERAT] scenes.py  → {output_path}")
    print(f"[LACERAT] DONE — copier vers F03_CRUOR/CODEBASE/ puis valider (STATE_4_GATE)")


if __name__ == "__main__":
    main()
