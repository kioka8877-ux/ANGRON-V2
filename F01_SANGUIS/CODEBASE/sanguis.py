"""
sanguis.py — F01_SANGUIS : génération du script viral via Claude.

Charge META_SANGUIS depuis METAPROMPTS/META_SANGUIS.md.
Appelle Claude avec ce metaprompt comme system prompt.
Écrit le script balisé dans F01_SANGUIS/OUT/script_XXX.md.

Usage :
    python3 F01_SANGUIS/CODEBASE/sanguis.py \
        --concept "physique du sprint" \
        --format short \
        --mode math_script \
        --id 002 \
        --output F01_SANGUIS/OUT/script_002.md

    # Mode hook (avec question obligatoire) :
    python3 F01_SANGUIS/CODEBASE/sanguis.py \
        --concept "CR7 courbe la balle" \
        --format short \
        --mode hook \
        --hook-question "Mais comment CR7 peut-il courber la balle comme ça ?" \
        --id 003 \
        --output F01_SANGUIS/OUT/script_003.md

Requiert :
    ANTHROPIC_API_KEY dans l'environnement
    pip install anthropic
"""

import argparse
import os
import sys
from pathlib import Path

_META_PATH = Path("METAPROMPTS/META_SANGUIS.md")

_META_FALLBACK = """
Tu es SANGUIS, cerveau narratif de la flotte ANGRON.
Structure obligatoire V2 — ARC 3B1B pour les Shorts :
[7s]  HOOK ÉMOTIONNEL — ce que le spectateur ressent déjà
[8s]  QUESTION QUI FORCE L'ÉCOUTE — "Mais comment X peut-il Y ?"
[15s] BEAUTÉ DU PROBLÈME — poser l'équation avec élégance, ne pas encore expliquer
[20s] INÉVITABILITÉ — dérouler le raisonnement, chaque étape évidente en rétroaction
[10s] APPLICATION INCARNÉE — retour monde réel, fin émotionnelle
Marqueurs [ANIM:] obligatoires : ex [ANIM: equation_reveal], [ANIM: plan_initial].
""".strip()

MODES = ["math_script", "math_no_script", "hook"]


def _load_meta() -> str:
    if _META_PATH.exists():
        text = _META_PATH.read_text(encoding="utf-8").strip()
        print(f"[SANGUIS] META chargé depuis {_META_PATH}", file=sys.stderr)
        return text
    print(f"[SANGUIS] AVERTISSEMENT : {_META_PATH} introuvable — fallback minimal utilisé.", file=sys.stderr)
    return _META_FALLBACK


def generate_script(concept: str, fmt: str, mode: str, script_id: str, hook_question: str | None) -> str:
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
        f"CONCEPT       : {concept}\n"
        f"FORMAT        : {fmt_label}\n"
        f"MODE          : {mode}\n"
        f"ID            : {script_id}\n"
    )

    if mode == "hook":
        if not hook_question:
            print("[SANGUIS] ERREUR : --hook-question obligatoire en mode hook.", file=sys.stderr)
            sys.exit(1)
        user_message += f"HOOK_QUESTION  : {hook_question}\n"
        user_message += (
            "\nInstructions spécifiques mode hook :\n"
            "- Le segment [7s] HOOK ÉMOTIONNEL doit décrire en 1 phrase choc ce que montre le clip vidéo réel.\n"
            "- La hook_question doit apparaître mot pour mot dans le segment [8s].\n"
            "- Les marqueurs [ANIM:] s'intègrent APRÈS le clip hook, pas pendant.\n"
        )
    elif mode == "math_no_script":
        user_message += (
            "\nInstructions spécifiques mode math_no_script :\n"
            "- Pas de voix off — les [ANIM:] portent tout le sens.\n"
            "- Chaque segment du script décrit les visuels, pas un texte parlé.\n"
            "- Les marqueurs [ANIM:] sont plus nombreux et plus détaillés qu'en mode math_script.\n"
        )

    user_message += "\nGénère le script complet selon l'arc 3B1B V2 avec tous les marqueurs [ANIM:]."

    print(f"[SANGUIS] Mode   : {mode}", file=sys.stderr)
    print(f"[SANGUIS] Génération script (claude-opus-4-8)...", file=sys.stderr)

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        system=meta_system,
        messages=[{"role": "user", "content": user_message}],
    )

    return message.content[0].text


def main() -> None:
    parser = argparse.ArgumentParser(description="SANGUIS — générateur de script viral F01 V2")
    parser.add_argument("--concept",       required=True, help="Concept brut de la vidéo")
    parser.add_argument("--format",        required=True, choices=["short", "longform"])
    parser.add_argument("--mode",          required=True, choices=MODES,
                        help="math_script | math_no_script | hook")
    parser.add_argument("--id",            required=True, help="ID du projet (ex: 002)")
    parser.add_argument("--output",        required=True, help="F01_SANGUIS/OUT/script_XXX.md")
    parser.add_argument("--hook-question", default=None,
                        help="(mode hook) 'Mais comment X peut-il Y ?' — obligatoire si mode=hook")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[SANGUIS] Concept : {args.concept}")
    print(f"[SANGUIS] Format  : {args.format}")
    print(f"[SANGUIS] Mode    : {args.mode}")
    print(f"[SANGUIS] ID      : {args.id}")

    script = generate_script(
        concept=args.concept,
        fmt=args.format,
        mode=args.mode,
        script_id=args.id,
        hook_question=getattr(args, "hook_question", None),
    )

    output_path.write_text(script, encoding="utf-8")
    print(f"[SANGUIS] Script  → {output_path}")
    print(f"[SANGUIS] DONE — attendre validation opérateur (STATE_2_GATE)")


if __name__ == "__main__":
    main()
