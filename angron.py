"""
angron.py — Orchestrateur de la flotte ANGRON V2.

Point d'entrée unique. Lit le ledger, détermine l'état, dispatche vers les frigates.
Supporte 3 modes : math_script / math_no_script / hook.

Usage :
    python3 angron.py status
    python3 angron.py init --concept "..." --format short|longform --mode math_script|math_no_script|hook
    python3 angron.py update --state STATE_3 [--script ...] [--audio ...] [...]
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
MODES = ["math_script", "math_no_script", "hook"]


def load_ledger() -> dict:
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_ledger(ledger: dict) -> None:
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _next_id(ledger: dict) -> str:
    n = len(ledger.get("historique", [])) + 1
    return f"{n:03d}"


def _empty_fichiers() -> dict:
    return {
        "script":    None,
        "audio":     None,
        "timestamps": None,
        "scenes_py": None,
        "renders":   [],
        "staged":    None,
        "nails_out": None,
        "final":     None,
    }


def _empty_hook() -> dict:
    return {
        "source_url":     None,
        "hook_ready_path": None,
        "hook_question":  None,
        "duration_seconds": None,
    }


def _empty_validations() -> dict:
    return {
        "script":    False,
        "scenes":    False,
        "render_brut": False,
    }


# ─────────────────────────────────────────────────────────────────────────────
# COMMANDES
# ─────────────────────────────────────────────────────────────────────────────

def status() -> None:
    ledger = load_ledger()
    projet = ledger["projet_actif"]
    stats  = ledger.get("stats", {})

    print("=" * 60)
    print("ANGRON V2 — FLOTTE ÉTAT")
    print("=" * 60)
    print(f"Projet actif     : {projet.get('id') or 'AUCUN'}")
    print(f"Mode             : {projet.get('mode') or '—'}")
    print(f"Étape            : {projet.get('etape') or 'INIT'}")
    print(f"Concept          : {projet.get('concept') or '—'}")
    print(f"Format           : {projet.get('format') or '—'}")
    print(f"Début            : {projet.get('debut') or '—'}")
    print(f"Dernière MAJ     : {projet.get('derniere_mise_a_jour') or '—'}")

    hook = projet.get("hook", {})
    if hook.get("hook_question"):
        print(f"Hook question    : {hook['hook_question']}")
    if hook.get("hook_ready_path"):
        print(f"Hook ready       : {hook['hook_ready_path']}")

    print("-" * 60)
    fichiers = projet.get("fichiers", {})
    for k, v in fichiers.items():
        if isinstance(v, list):
            val = ", ".join(v) if v else "—"
        else:
            val = v or "—"
        print(f"  {k:<16} : {val}")

    validations = projet.get("validations", {})
    if any(validations.values()):
        print("-" * 60)
        for k, v in validations.items():
            print(f"  validé {k:<12} : {'OUI' if v else 'non'}")

    print("-" * 60)
    print(f"Vidéos produites : {stats.get('videos_produites', 0)}")
    print(f"Vidéos uploadées : {stats.get('videos_uploadees', 0)}")
    print(f"Cycles complets  : {stats.get('cycles_complets', 0)}")
    print("=" * 60)

    hist = ledger.get("historique", [])
    if hist:
        print("\nHistorique :")
        for e in hist:
            mode_label = f" [{e.get('mode', '?')}]" if e.get("mode") else ""
            print(f"  [{e.get('id')}]{mode_label} {e.get('concept','?')} ({e.get('format','?')}) — {e.get('date','?')[:10]}")


def init_project(concept: str, fmt: str, mode: str,
                 hook_question: str | None = None) -> None:
    if mode not in MODES:
        print(f"[ANGRON] ERREUR : mode invalide '{mode}'. Valeurs : {MODES}", file=sys.stderr)
        sys.exit(1)

    ledger    = load_ledger()
    projet_id = _next_id(ledger)

    # Mode hook : première étape est STATE_1b (attente HOOK_STUDIO)
    first_state = "STATE_1b" if mode == "hook" else "STATE_2"

    hook = _empty_hook()
    if hook_question:
        hook["hook_question"] = hook_question

    ledger["projet_actif"] = {
        "id":      projet_id,
        "mode":    mode,
        "concept": concept,
        "format":  fmt,
        "etape":   first_state,
        "hook":    hook,
        "fichiers": _empty_fichiers(),
        "validations": _empty_validations(),
        "debut":                now_iso(),
        "derniere_mise_a_jour": now_iso(),
    }
    save_ledger(ledger)

    print(f"[ANGRON] Projet initialisé : {projet_id}")
    print(f"[ANGRON] Concept : {concept}")
    print(f"[ANGRON] Format  : {fmt}")
    print(f"[ANGRON] Mode    : {mode}")
    print(f"[ANGRON] État    : {first_state}")

    if mode == "hook":
        print(f"[ANGRON] → Lancer HOOK_STUDIO : streamlit run HOOK_STUDIO/studio.py")
        print(f"[ANGRON]   Puis : python3 angron.py update --state STATE_2 --hook-ready F02_LACERAT/IN/HOOK/hook_ready.mp4")


def update_state(new_state: str, **kwargs) -> None:
    ledger  = load_ledger()
    projet  = ledger["projet_actif"]

    if not projet or not projet.get("id"):
        print("[ANGRON] ERREUR : aucun projet actif.", file=sys.stderr)
        sys.exit(1)

    projet["etape"]                = new_state
    projet["derniere_mise_a_jour"] = now_iso()

    fichiers    = projet.setdefault("fichiers", _empty_fichiers())
    hook        = projet.setdefault("hook", _empty_hook())
    validations = projet.setdefault("validations", _empty_validations())

    FICHIER_KEYS = set(fichiers.keys())
    HOOK_KEYS    = {"hook_ready", "hook_question", "source_url"}
    VALID_KEYS   = {"validate_script", "validate_scenes", "validate_render"}

    for k, v in kwargs.items():
        if v is None:
            continue
        if k in FICHIER_KEYS:
            fichiers[k] = v
        elif k == "hook_ready":
            hook["hook_ready_path"] = v
        elif k == "hook_question":
            hook["hook_question"] = v
        elif k == "source_url":
            hook["source_url"] = v
        elif k == "validate_script":
            validations["script"] = bool(v)
        elif k == "validate_scenes":
            validations["scenes"] = bool(v)
        elif k == "validate_render":
            validations["render_brut"] = bool(v)

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
        "mode":    projet.get("mode"),
        "date":    projet.get("debut"),
        "final":   projet.get("fichiers", {}).get("final"),
    }
    ledger.setdefault("historique", []).append(entry)
    ledger["stats"]["videos_produites"] = ledger["stats"].get("videos_produites", 0) + 1
    ledger["stats"]["cycles_complets"]  = ledger["stats"].get("cycles_complets", 0) + 1

    ledger["projet_actif"] = {
        "id": None, "mode": None, "concept": None, "format": None,
        "etape": "INIT",
        "hook": _empty_hook(),
        "fichiers": _empty_fichiers(),
        "validations": _empty_validations(),
        "debut": None,
        "derniere_mise_a_jour": now_iso(),
    }

    save_ledger(ledger)
    print(f"[ANGRON] Projet {entry['id']} archivé.")


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
    mode   = projet.get("mode", "math_script")
    hook   = projet.get("hook", {})
    id_num = pid if pid and pid != "???" else "001"

    if etape == "INIT":
        print("[ANGRON] Aucun projet actif.")
        print("[ANGRON] Lance : python3 angron.py init --concept '...' --format short --mode math_script")
        return

    print(f"[ANGRON] Dispatch → {etape}  (projet {pid}, mode {mode})")

    # ── STATE_1b : attente HOOK_STUDIO ────────────────────────────────────────
    if etape == "STATE_1b":
        hook_ready = hook.get("hook_ready_path")
        if hook_ready and Path(hook_ready).exists():
            print(f"[ANGRON] hook_ready.mp4 détecté : {hook_ready}")
            update_state("STATE_2")
            commit_ledger(f"ANGRON {pid} — STATE_1b : hook prêt → STATE_2")
        else:
            print(f"[ANGRON] En attente de hook_ready.mp4.")
            print(f"[ANGRON] Lance HOOK_STUDIO : streamlit run HOOK_STUDIO/studio.py")
            print(f"[ANGRON] Puis : python3 angron.py update --state STATE_2 --hook-ready F02_LACERAT/IN/HOOK/hook_ready.mp4")
        return

    # ── STATE_2 : SANGUIS ─────────────────────────────────────────────────────
    elif etape == "STATE_2":
        output      = f"F01_SANGUIS/OUT/script_{id_num}.md"
        cmd         = [
            "python3", "F01_SANGUIS/CODEBASE/sanguis.py",
            "--concept", projet["concept"],
            "--format",  fmt,
            "--mode",    mode,
            "--id",      id_num,
            "--output",  output,
        ]
        if mode == "hook" and hook.get("hook_question"):
            cmd += ["--hook-question", hook["hook_question"]]
        _run(cmd)
        update_state("STATE_2_GATE", script=output)
        commit_ledger(f"ANGRON {pid} — STATE_2 : script SANGUIS généré")

    # ── STATE_3 : Whisper (skippé en math_no_script) ──────────────────────────
    elif etape == "STATE_3":
        if mode == "math_no_script":
            print("[ANGRON] Mode math_no_script — Whisper skippé.")
            update_state("STATE_4")
            commit_ledger(f"ANGRON {pid} — STATE_3 : Whisper skippé (math_no_script)")
            return

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

    # ── STATE_4 : LACERAT — génère scenes_XXX.py ─────────────────────────────
    elif etape == "STATE_4":
        script     = projet["fichiers"].get("script") or f"F01_SANGUIS/OUT/script_{id_num}.md"
        timestamps = projet["fichiers"].get("timestamps")
        output     = f"F02_LACERAT/OUT/scenes_{id_num}.py"
        cmd        = [
            "python3", "F02_LACERAT/CODEBASE/lacerat.py",
            "--script", script,
            "--mode",   mode,
            "--id",     id_num,
            "--format", fmt,
            "--output", output,
        ]
        if timestamps:
            cmd += ["--timestamps", timestamps]
        if mode == "hook" and hook.get("hook_ready_path"):
            cmd += ["--hook-path", hook["hook_ready_path"]]
        _run(cmd)
        update_state("STATE_4_GATE", scenes_py=output)
        commit_ledger(f"ANGRON {pid} — STATE_4 : scenes.py LACERAT généré")

    # ── STATE_6 : CRUOR — render toutes scènes + staged ──────────────────────
    elif etape == "STATE_6":
        scenes_py = projet["fichiers"].get("scenes_py") or f"F03_CRUOR/CODEBASE/scenes_{id_num}.py"
        out_dir   = f"F03_CRUOR/OUT/"
        staged    = f"F03_CRUOR/OUT/staged_{id_num}.mp4"
        _run([
            "bash", "F03_CRUOR/CODEBASE/render.sh",
            "--scenes",  scenes_py,
            "--all",
            "--out-dir", out_dir,
            "--staged",  staged,
            "--format",  fmt,
        ])
        update_state("STATE_6_GATE", staged=staged)
        commit_ledger(f"ANGRON {pid} — STATE_6 : staged.mp4 CRUOR produit")

    # ── STATE_7 : NAILS — fusion + mode hook ─────────────────────────────────
    elif etape == "STATE_7":
        staged = projet["fichiers"].get("staged") or f"F03_CRUOR/OUT/staged_{id_num}.mp4"
        audio  = projet["fichiers"].get("audio")  or f"F02_LACERAT/IN/voice_{id_num}.mp3"
        output = f"F04_NAILS/OUT/nails_out_{id_num}.mp4"
        cmd    = [
            "bash", "F04_NAILS/CODEBASE/finish.sh",
            "--staged", staged,
            "--mode",   mode,
            "--format", fmt,
            "--output", output,
        ]
        if mode in ("math_script", "hook") and Path(audio).exists():
            cmd += ["--audio", audio]
        if mode == "hook" and hook.get("hook_ready_path"):
            cmd += ["--hook", hook["hook_ready_path"]]
        _run(cmd)
        update_state("STATE_8", nails_out=output)
        commit_ledger(f"ANGRON {pid} — STATE_7 : fusion NAILS terminée")

    # ── STATE_8 : NUCERIA — camouflage final ──────────────────────────────────
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
        archive_projet()
        commit_ledger(f"ANGRON {pid} — production terminée — archivé")

    # ── GATES / états manuels ─────────────────────────────────────────────────
    else:
        gate_msgs = {
            "STATE_2_GATE": "Valider le script → python3 angron.py update --state STATE_3 --validate-script 1",
            "STATE_4_GATE": "Valider scenes.py → copier vers F03_CRUOR/CODEBASE/ puis : python3 angron.py update --state STATE_6 --scenes-py F03_CRUOR/CODEBASE/scenes_XXX.py",
            "STATE_5":      "Copier scenes.py généré dans F03_CRUOR/CODEBASE/ puis : python3 angron.py update --state STATE_6",
            "STATE_6_GATE": "Valider vidéo brute → python3 angron.py update --state STATE_7 --validate-render 1",
            "STATE_9":      "Projet terminé — archivé. URL à remplir dans le log.",
        }
        msg = gate_msgs.get(etape, f"État '{etape}' attend une action manuelle.")
        print(f"[ANGRON] {msg}")


def _run(cmd: list[str]) -> None:
    print(f"[ANGRON] → {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"[ANGRON] ÉCHEC (exit {result.returncode})", file=sys.stderr)
        sys.exit(result.returncode)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="ANGRON V2 — Orchestrateur de flotte")
    sub    = parser.add_subparsers(dest="command")

    sub.add_parser("status",   help="Afficher l'état de la flotte")
    sub.add_parser("dispatch", help="Dispatcher vers la frigate selon l'état en cours")
    sub.add_parser("archive",  help="Archiver le projet actif")

    p_init = sub.add_parser("init", help="Initialiser un nouveau projet")
    p_init.add_argument("--concept",       required=True)
    p_init.add_argument("--format",        required=True, choices=["short", "longform"])
    p_init.add_argument("--mode",          required=True, choices=MODES)
    p_init.add_argument("--hook-question", default=None, dest="hook_question")

    p_update = sub.add_parser("update", help="Mettre à jour l'état du ledger")
    p_update.add_argument("--state",           required=True)
    p_update.add_argument("--script",          default=None)
    p_update.add_argument("--audio",           default=None)
    p_update.add_argument("--timestamps",      default=None)
    p_update.add_argument("--scenes-py",       default=None, dest="scenes_py")
    p_update.add_argument("--staged",          default=None)
    p_update.add_argument("--nails-out",       default=None, dest="nails_out")
    p_update.add_argument("--final",           default=None)
    p_update.add_argument("--hook-ready",      default=None, dest="hook_ready")
    p_update.add_argument("--hook-question",   default=None, dest="hook_question")
    p_update.add_argument("--source-url",      default=None, dest="source_url")
    p_update.add_argument("--validate-script", default=None, type=int, dest="validate_script")
    p_update.add_argument("--validate-scenes", default=None, type=int, dest="validate_scenes")
    p_update.add_argument("--validate-render", default=None, type=int, dest="validate_render")

    p_commit = sub.add_parser("commit", help="Commiter le ledger sur GitHub")
    p_commit.add_argument("--message", required=True)

    args = parser.parse_args()

    if args.command == "status" or args.command is None:
        status()
    elif args.command == "init":
        init_project(
            concept=args.concept,
            fmt=args.format,
            mode=args.mode,
            hook_question=getattr(args, "hook_question", None),
        )
    elif args.command == "update":
        kwargs = {}
        for k in ("script", "audio", "timestamps", "scenes_py", "staged",
                  "nails_out", "final", "hook_ready", "hook_question",
                  "source_url", "validate_script", "validate_scenes", "validate_render"):
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
