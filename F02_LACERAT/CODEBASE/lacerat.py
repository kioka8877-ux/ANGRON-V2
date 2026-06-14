"""
lacerat.py — F02_LACERAT : génération du storyboard Manim via Claude.

Charge META_LACERAT depuis METAPROMPTS/META_LACERAT.md.
Prend le script SANGUIS + les timestamps Whisper + les assets disponibles.
Appelle Claude avec ce metaprompt comme system prompt.
Produit prompt_XXX.md (storyboard Manim complet avec timings).

Usage :
    python3 F02_LACERAT/CODEBASE/lacerat.py \
        --script  F01_SANGUIS/OUT/script_XXX.md \
        --timestamps F02_LACERAT/OUT/whisper_timestamps_XXX.json \
        --id      XXX \
        --format  short|longform \
        --output  F02_LACERAT/OUT/prompt_XXX.md \
        [--assets F02_LACERAT/IN/assets/]

Requiert :
    ANTHROPIC_API_KEY dans l'environnement
    pip install anthropic
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Chemin du metaprompt — relatif à la racine du dépôt ANGRON
_META_PATH = Path("METAPROMPTS/META_LACERAT.md")

# Fallback minimal si le fichier est absent
_META_FALLBACK = """
Tu es LACERAT, le traducteur tactique de la flotte ANGRON.
Tu reçois un script humain balisé et tu produis un prompt Manim storyboardé au millimètre.
Tu ne crées pas — tu traduis. La créativité appartient à SANGUIS.
Génère un storyboard bloc par bloc avec timings Whisper, directives Manim et charte ANGRON_STYLE.
""".strip()


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


def generate_prompt(
    script_text: str,
    timestamps: dict,
    assets: list[str],
    script_id: str,
    fmt: str,
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

    user_message = (
        f"ID PROJET : {script_id}\n"
        f"FORMAT    : {fmt_label}\n\n"
        f"--- SCRIPT SANGUIS ---\n{script_text}\n\n"
        f"--- TIMESTAMPS WHISPER ---\n{json.dumps(timestamps, indent=2, ensure_ascii=False)}\n\n"
        f"--- ASSETS DISPONIBLES ---\n{assets_str}\n\n"
        "Génère le storyboard Manim complet selon le format ANGRON."
    )

    print(f"[LACERAT] Génération storyboard (claude-opus-4-8)...", file=sys.stderr)

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=8192,
        system=meta_system,
        messages=[{"role": "user", "content": user_message}],
    )

    return message.content[0].text


def main() -> None:
    parser = argparse.ArgumentParser(description="LACERAT — storyboard Manim F02")
    parser.add_argument("--script",     required=True, help="script_XXX.md (F01 output)")
    parser.add_argument("--timestamps", required=True, help="whisper_timestamps_XXX.json")
    parser.add_argument("--id",         required=True, help="ID projet (ex: 001)")
    parser.add_argument("--format",     required=True, choices=["short", "longform"])
    parser.add_argument("--output",     required=True, help="F02_LACERAT/OUT/prompt_XXX.md")
    parser.add_argument("--assets",     default="F02_LACERAT/IN/assets",
                        help="Dossier assets (défaut: F02_LACERAT/IN/assets)")
    args = parser.parse_args()

    script_path = Path(args.script)
    ts_path     = Path(args.timestamps)
    output_path = Path(args.output)
    assets_dir  = Path(args.assets)

    if not script_path.exists():
        print(f"[LACERAT] ERREUR : script introuvable : {script_path}", file=sys.stderr)
        sys.exit(1)
    if not ts_path.exists():
        print(f"[LACERAT] ERREUR : timestamps introuvables : {ts_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    script_text = script_path.read_text(encoding="utf-8")
    timestamps  = load_timestamps(ts_path)
    assets      = list_assets(assets_dir)

    print(f"[LACERAT] Script     : {script_path}")
    print(f"[LACERAT] Timestamps : {ts_path} ({timestamps.get('nb_blocs', '?')} blocs, {timestamps.get('duree_totale', '?')}s)")
    print(f"[LACERAT] Assets     : {len(assets)} fichier(s)")
    print(f"[LACERAT] Format     : {args.format}")

    prompt_md = generate_prompt(script_text, timestamps, assets, args.id, args.format)

    output_path.write_text(prompt_md, encoding="utf-8")
    print(f"[LACERAT] Storyboard → {output_path}")
    print(f"[LACERAT] DONE — attendre validation opérateur (GATE)")


if __name__ == "__main__":
    main()
