"""
sanguis.py — F01_SANGUIS : génération du script viral via Claude.

Charge META_SANGUIS depuis METAPROMPTS/META_SANGUIS.md.
Appelle Claude avec ce metaprompt comme system prompt.
Écrit le script balisé dans F01_SANGUIS/OUT/script_XXX.md.

Usage :
    python3 F01_SANGUIS/CODEBASE/sanguis.py \
        --concept "physique du sprint — pourquoi les petits joueurs tiennent mieux l'équilibre" \
        --format short \
        --id 001 \
        --output F01_SANGUIS/OUT/script_001.md

Requiert :
    ANTHROPIC_API_KEY dans l'environnement
    pip install anthropic
"""

import argparse
import os
import sys
from pathlib import Path

# Chemin du metaprompt — relatif à la racine du dépôt ANGRON
_META_PATH = Path("METAPROMPTS/META_SANGUIS.md")

# Fallback minimal si le fichier est absent
_META_FALLBACK = """
Tu es SANGUIS, le cerveau narratif de la flotte ANGRON.
Ta mission : transformer un concept brut en script viral structuré, prêt à être animé.
Génère un script au format ANGRON (sections ACCROCHE / TENSION / RÉVÉLATION / CHUTE / CTA)
avec directives [ANIM:] et métadonnées YouTube.
""".strip()


def _load_meta() -> str:
    if _META_PATH.exists():
        text = _META_PATH.read_text(encoding="utf-8").strip()
        print(f"[SANGUIS] META chargé depuis {_META_PATH}", file=sys.stderr)
        return text
    print(f"[SANGUIS] AVERTISSEMENT : {_META_PATH} introuvable — fallback minimal utilisé.", file=sys.stderr)
    return _META_FALLBACK


def generate_script(concept: str, fmt: str, script_id: str) -> str:
    try:
        import anthropic
    except ImportError:
        print("[SANGUIS] ERREUR : anthropic non installé. `pip install anthropic`", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[SANGUIS] ERREUR : ANTHROPIC_API_KEY manquant.", file=sys.stderr)
        sys.exit(1)

    meta_system = _load_meta()
    client = anthropic.Anthropic(api_key=api_key)

    fmt_label = "SHORT (≤60 secondes)" if fmt == "short" else "LONGFORM (3-10 minutes)"
    user_message = (
        f"CONCEPT : {concept}\n"
        f"FORMAT  : {fmt_label}\n"
        f"ID      : {script_id}\n\n"
        "Génère le script complet selon le format ANGRON."
    )

    print(f"[SANGUIS] Génération script (claude-opus-4-8)...", file=sys.stderr)

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        system=meta_system,
        messages=[{"role": "user", "content": user_message}],
    )

    return message.content[0].text


def main() -> None:
    parser = argparse.ArgumentParser(description="SANGUIS — générateur de script viral F01")
    parser.add_argument("--concept", required=True, help="Concept brut de la vidéo")
    parser.add_argument("--format",  required=True, choices=["short", "longform"])
    parser.add_argument("--id",      required=True, help="ID du projet (ex: 001)")
    parser.add_argument("--output",  required=True, help="F01_SANGUIS/OUT/script_XXX.md")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[SANGUIS] Concept : {args.concept}")
    print(f"[SANGUIS] Format  : {args.format}")
    print(f"[SANGUIS] ID      : {args.id}")

    script = generate_script(args.concept, args.format, args.id)

    output_path.write_text(script, encoding="utf-8")
    print(f"[SANGUIS] Script  → {output_path}")
    print(f"[SANGUIS] DONE — attendre validation opérateur (GATE)")


if __name__ == "__main__":
    main()
