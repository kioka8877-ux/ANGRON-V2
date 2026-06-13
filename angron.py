"""
angron.py — Point d'entrée de la flotte ANGRON.

Ce fichier est le seul point d'orchestration que Claude connaît.
Il lit le ledger.json, détermine l'étape en cours, et coordonne la frigate appropriée.

RÈGLE ABSOLUE : Ce script ne fait rien de lourd.
Il délègue aux scripts autonomes des frigates via subprocess.
Claude l'appelle. Claude se tait. Claude reprend quand le signal est reçu.
"""

import json
import sys
from pathlib import Path

LEDGER_PATH = Path(".angron/ledger.json")


def load_ledger() -> dict:
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(ledger: dict) -> None:
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def status() -> None:
    """Affiche l'état actuel de la flotte pour Claude."""
    ledger = load_ledger()
    projet = ledger["projet_actif"]
    print("=" * 50)
    print(f"FLOTTE ANGRON — ÉTAT")
    print("=" * 50)
    print(f"Projet actif : {projet['id'] or 'AUCUN'}")
    print(f"Étape        : {projet['etape']}")
    print(f"Concept      : {projet['concept'] or '—'}")
    print(f"Format       : {projet['format'] or '—'}")
    print("-" * 50)
    print(f"Videos produites : {ledger['stats']['videos_produites']}")
    print(f"Videos uploadées : {ledger['stats']['videos_uploadees']}")
    print("=" * 50)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        status()
    else:
        status()
