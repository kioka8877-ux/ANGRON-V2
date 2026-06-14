"""
angron.py — Orchestrateur de la flotte ANGRON.

Point d'entrée unique. Lit le ledger, détermine l'état, dispatche vers les frigates.
Claude l'appelle. Le script gère. Claude reprend sur signal.

Usage :
    python3 angron.py status
    python3 angron.py init --concept "..." --format short|longform
    python3 angron.py update --state STATE_3 [--script ...] [--audio ...]
    python3 angron.py dispatch
    python3 angron.py commit --message "..."
    python3 angron.py archive
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

LEDGER_PATH = Path(".angron/ledger.json")


def load_ledger() -> dict:
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(ledger: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _generate_id() -> str:
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    ledger = load_ledger()
    n = len(ledger.get("historique", [])) + 1
    return f"angron_{date_str}_{n:03d}"


def _empty_fichiers() -> dict:
    return {
        "script":       None,
        "audio":        None,
        "timestamps":   None,
        "prompt_manim": None,
        "assets":       [],
        "scene_py":     None,
        "render_brut":  None,
        "nails_out":    None,
        "final":        None,
    }


# ---------------------------------------------------------------------------
# COMMANDES
# ---------------------------------------------------------------------------

def status() -> None:
    ledger = load_ledger()
    projet = ledger["projet_actif"]
    stats  = ledger.get("stats", {})

    print("=" * 56)
    print("ANGRON — FLOTTE ÉTAT")
    print("=" * 56)
    print(f"Projet actif     : {projet.get('id') or 'AUCUN'}")
    print(f"Étape            : {projet.get('etape') or 'INIT'}")
    print(f"Concept          : {projet.get('concept') or '—'}")
    print(f"Format           : {projet.get('format') or '—'}")
    print(f"Début            : {projet.get('debut') or '—'}")
    print(f"Dernière MAJ     : {projet.get('derniere_mise_a_jour') or '—'}")
    print("-" * 56)

    fichiers = projet.get("fichiers", {})
    for k, v in fichiers.items():
        if isinstance(v, list):
            val = ", ".join(v) if v else "—"
        else:
            val = v or "—"
        print(f"  {k:<16} : {val}")

    print("-" * 56)
    print(f"Vidéos produites : {stats.get('videos_produites', 0)}")
    print(f"Vidéos uploadées : {stats.get('videos_uploadees', 0)}")
    print(f"Cycles complets  : {stats.get('cycles_complets', 0)}")
    print("=" * 56)

    hist = ledger.get("historique", [])
    if hist:
        print("\nHistorique :")
        for e in hist:
            print(f"  [{e.get('id')}] {e.get('concept','?')} ({e.get('format','?')}) — {e.get('date','?')[:10]}")


def init_project(concept: str, fmt: str) -> None:
    ledger    = load_ledger()
    projet_id = _generate_id()

    ledger["projet_actif"] = {
        "id":      projet_id,
        "concept": concept,
        "format":  fmt,
        "etape":   "STATE_2",
        "fichiers": _empty_fichiers(),
        "debut":                now_iso(),
        "derniere_mise_a_jour": now_iso(),
    }
    save_ledger(ledger)

    print(f"[ANGRON] Projet initialisé : {projet_id}")
    print(f"[ANGRON] Concept : {concept}")
    print(f"[ANGRON] Format  : {fmt}")
    print(f"[ANGRON] État    : STATE_2 — prêt pour SANGUIS")


def update_state(new_state: str, **fichier_kwargs) -> None:
    ledger  = load_ledger()
    projet  = ledger["projet_actif"]

    if not projet or not projet.get("id"):
        print("[ANGRON] ERREUR : aucun projet actif.", file=sys.stderr)
        sys.exit(1)

    projet["etape"]                = new_state
    projet["derniere_mise_a_jour"] = now_iso()

    for k, v in fichier_kwargs.items():
        if k in projet["fichiers"]:
            projet["fichiers"][k] = v
        else:
            projet[k] = v

    ledger["projet_actif"] = projet
    save_ledger(ledger)
    print(f"[ANGRON] État → {new_state}")


def archive_projet() -> None:
    ledger  = load_ledger()
    projet  = ledger["projet_actif"]

    if not projet or not projet.get("id"):
        print("[ANGRON] Aucun projet actif à archiver.")
        return

    entry = {
        "id":      projet.get("id"),
        "concept": projet.get("concept"),
        "format":  projet.get("format"),
        "date":    projet.get("debut"),
        "final":   projet.get("fichiers", {}).get("final"),
    }
    ledger.setdefault("historique", []).append(entry)
    ledger["stats"]["videos_produites"] = ledger["stats"].get("videos_produites", 0) + 1
    ledger["stats"]["cycles_complets"]  = ledger["stats"].get("cycles_complets", 0) + 1

    ledger["projet_actif"] = {
        "id": None, "concept": None, "format": None,
        "etape": "INIT",
        "fichiers": _empty_fichiers(),
        "debut": None, "derniere_mise_a_jour": None,
    }

    save_ledger(ledger)
    print(f"[ANGRON] Projet {entry['id']} archivé dans l'historique.")


def commit_ledger(message: str) -> None:
    for cmd in [
        ["git", "add", str(LEDGER_PATH)],
        ["git", "commit", "-m", message],
        ["git", "push"],
    ]:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            label = " ".join(cmd[:2])
            print(f"[ANGRON] {label} ERREUR :\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

    print(f"[ANGRON] Ledger commité : {message}")


def dispatch() -> None:
    ledger = load_ledger()
    projet = ledger["projet_actif"]
    etape  = projet.get("etape", "INIT")
    pid    = projet.get("id", "???")
    fmt    = projet.get("format", "short")
    id_num = pid.split("_")[-1] if pid and pid != "???" else "001"

    if etape == "INIT":
        print("[ANGRON] Aucun projet actif.")
        print("[ANGRON] Lance : python3 angron.py init --concept '...' --format short|longform")
        return

    print(f"[ANGRON] Dispatch → {etape}  (projet {pid})")

    # -----------------------------------------------------------------------
    if etape == "STATE_2":
        output = f"F01_SANGUIS/OUT/script_{id_num}.md"
        _run([
            "python3", "F01_SANGUIS/CODEBASE/sanguis.py",
            "--concept", projet["concept"],
            "--format",  fmt,
            "--id",      id_num,
            "--output",  output,
        ])
        update_state("STATE_2_GATE", script=output)
        commit_ledger(f"ANGRON {pid} — STATE_2 : script SANGUIS généré")

    # -----------------------------------------------------------------------
    elif etape == "STATE_3":
        audio  = projet["fichiers"].get("audio") or f"F02_LACERAT/IN/voice_{id_num}.mp3"
        script = projet["fichiers"].get("script") or f"F01_SANGUIS/OUT/script_{id_num}.md"
        output = f"F02_LACERAT/OUT/whisper_timestamps_{id_num}.json"
        _run([
            "python3", "F02_LACERAT/CODEBASE/whisper_sync.py",
            "--audio",  audio,
            "--script", script,
            "--output", output,
            "--format", fmt,
        ])
        update_state("STATE_4", timestamps=output)
        commit_ledger(f"ANGRON {pid} — STATE_3 : timestamps Whisper extraits")

    # -----------------------------------------------------------------------
    elif etape == "STATE_4":
        script     = projet["fichiers"].get("script")     or f"F01_SANGUIS/OUT/script_{id_num}.md"
        timestamps = projet["fichiers"].get("timestamps") or f"F02_LACERAT/OUT/whisper_timestamps_{id_num}.json"
        output     = f"F02_LACERAT/OUT/prompt_{id_num}.md"
        _run([
            "python3", "F02_LACERAT/CODEBASE/lacerat.py",
            "--script",     script,
            "--timestamps", timestamps,
            "--id",         id_num,
            "--format",     fmt,
            "--output",     output,
        ])
        update_state("STATE_4_GATE", prompt_manim=output)
        commit_ledger(f"ANGRON {pid} — STATE_4 : storyboard LACERAT généré")

    # -----------------------------------------------------------------------
    elif etape == "STATE_6":
        scene_py = projet["fichiers"].get("scene_py") or f"F03_CRUOR/CODEBASE/scene_{id_num}.py"
        output   = f"F03_CRUOR/OUT/cruor_render_{id_num}.mp4"
        _run([
            "bash", "F03_CRUOR/CODEBASE/render.sh",
            "--scene",  scene_py,
            "--output", output,
            "--format", fmt,
        ])
        update_state("STATE_6_GATE", render_brut=output)
        commit_ledger(f"ANGRON {pid} — STATE_6 : render brut CRUOR produit")

    # -----------------------------------------------------------------------
    elif etape == "STATE_7":
        video  = projet["fichiers"].get("render_brut") or f"F03_CRUOR/OUT/cruor_render_{id_num}.mp4"
        audio  = projet["fichiers"].get("audio")       or f"F02_LACERAT/IN/voice_{id_num}.mp3"
        output = f"F04_NAILS/OUT/nails_out_{id_num}.mp4"
        _run([
            "bash", "F04_NAILS/CODEBASE/finish.sh",
            "--video",  video,
            "--audio",  audio,
            "--format", fmt,
            "--output", output,
        ])
        update_state("STATE_8", nails_out=output)
        commit_ledger(f"ANGRON {pid} — STATE_7 : fusion NAILS terminée")

    # -----------------------------------------------------------------------
    elif etape == "STATE_8":
        nails   = projet["fichiers"].get("nails_out") or f"F04_NAILS/OUT/nails_out_{id_num}.mp4"
        concept = projet.get("concept", "ANGRON")
        output  = f"F05_NUCERIA/OUT/youtube_{fmt}_{id_num}.mp4"
        _run([
            "python3", "F05_NUCERIA/CODEBASE/nuceria.py",
            "--input",   nails,
            "--concept", concept,
            "--format",  fmt,
            "--output",  output,
        ])
        update_state("STATE_9", final=output)
        # Archive immediatement — STATE_9 n'a pas de gate, pas de raison d'attendre
        archive_projet()
        commit_ledger(f"ANGRON {pid} — production terminée — archivé")

    # -----------------------------------------------------------------------
    elif etape == "STATE_9":
        final = projet["fichiers"].get("final", "—")
        print(f"[ANGRON] Projet {pid} terminé.")
        print(f"[ANGRON] Fichier final : {final}")
        archive_projet()
        commit_ledger(f"ANGRON {pid} — production terminée — archivé")

    # -----------------------------------------------------------------------
    else:
        print(f"[ANGRON] État '{etape}' attend une action manuelle.")
        print(f"[ANGRON] États GATE : STATE_2_GATE (valider script)")
        print(f"[ANGRON]             STATE_4_GATE (valider storyboard)")
        print(f"[ANGRON]             STATE_5      (générer scene_XXX.py via CRUOR)")
        print(f"[ANGRON]             STATE_6_GATE (valider vidéo brute)")


def _run(cmd: list[str]) -> None:
    print(f"[ANGRON] → {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"[ANGRON] ÉCHEC (exit {result.returncode})", file=sys.stderr)
        sys.exit(result.returncode)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="ANGRON — Orchestrateur de flotte")
    sub    = parser.add_subparsers(dest="command")

    sub.add_parser("status",   help="Afficher l'état de la flotte")
    sub.add_parser("dispatch", help="Dispatcher vers la frigate selon l'état en cours")
    sub.add_parser("archive",  help="Archiver le projet actif dans l'historique")

    p_init = sub.add_parser("init", help="Initialiser un nouveau projet")
    p_init.add_argument("--concept", required=True, help="Concept brut de la vidéo")
    p_init.add_argument("--format",  required=True, choices=["short", "longform"])

    p_update = sub.add_parser("update", help="Mettre à jour l'état du ledger")
    p_update.add_argument("--state",       required=True, help="Nouvel état (ex: STATE_3)")
    p_update.add_argument("--script",      default=None)
    p_update.add_argument("--audio",       default=None)
    p_update.add_argument("--timestamps",  default=None)
    p_update.add_argument("--prompt-manim", default=None, dest="prompt_manim")
    p_update.add_argument("--scene-py",    default=None, dest="scene_py")
    p_update.add_argument("--render-brut", default=None, dest="render_brut")
    p_update.add_argument("--nails-out",   default=None, dest="nails_out")
    p_update.add_argument("--final",       default=None)

    p_commit = sub.add_parser("commit", help="Commiter le ledger sur GitHub")
    p_commit.add_argument("--message", required=True)

    args = parser.parse_args()

    if args.command == "status" or args.command is None:
        status()
    elif args.command == "init":
        init_project(args.concept, args.format)
    elif args.command == "update":
        kwargs = {}
        for k in ("script", "audio", "timestamps", "prompt_manim",
                  "scene_py", "render_brut", "nails_out", "final"):
            v = getattr(args, k, None)
            if v is not None:
                kwargs[k] = v
        update_state(args.state, **kwargs)
    elif args.command == "dispatch":
        dispatch()
    elif args.command == "commit":
        commit_ledger(args.message)
    elif args.command == "archive":
        archive_projet()


if __name__ == "__main__":
    main()
