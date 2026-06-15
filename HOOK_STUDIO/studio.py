"""
studio.py — HOOK_STUDIO : interface Streamlit pour préparer un clip hook.

Workflow :
  1. Entrer l'URL du clip source
  2. Télécharger via downloader.py
  3. Prévisualiser + ajuster IN/OUT, speed, volume, format
  4. Entrer la hook_question
  5. CUT → hook_ready.mp4 → copie auto dans F02_LACERAT/IN/HOOK/

Lancer :
    streamlit run HOOK_STUDIO/studio.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).parent.parent
_TMP  = Path(__file__).parent / "tmp"
_OUT  = Path(__file__).parent / "OUT"
_TMP.mkdir(exist_ok=True)
_OUT.mkdir(exist_ok=True)

st.set_page_config(page_title="HOOK_STUDIO — ANGRON V2", layout="wide")

st.title("HOOK_STUDIO")
st.caption("Préparer un clip hook pour la flotte ANGRON V2")

# ─── Section 1 : URL + Download ──────────────────────────────────────────────
st.header("1. Source du clip")

url = st.text_input(
    "URL (YouTube / Twitter / TikTok / Instagram)",
    placeholder="https://youtube.com/watch?v=...",
)

clip_brut = _TMP / "clip_brut.mp4"

col_dl, col_status = st.columns([1, 3])
with col_dl:
    dl_button = st.button("Télécharger", disabled=not url)

if dl_button and url:
    with st.spinner("Téléchargement en cours..."):
        result = subprocess.run(
            [sys.executable, str(_ROOT / "HOOK_STUDIO/downloader.py"),
             "--url", url, "--output", str(clip_brut)],
            capture_output=True, text=True,
        )
    if result.returncode == 0:
        st.session_state["clip_ready"] = True
        st.success(f"Clip téléchargé : {clip_brut.name}")
    else:
        st.error(f"Erreur download :\n{result.stderr}")

# ─── Section 2 : Trim + paramètres ───────────────────────────────────────────
if st.session_state.get("clip_ready") and clip_brut.exists():
    st.header("2. Découpe et paramètres")

    st.video(str(clip_brut))

    col1, col2 = st.columns(2)
    with col1:
        in_point  = st.number_input("IN (secondes)", min_value=0.0, value=0.0, step=0.1, format="%.1f")
        out_point = st.number_input("OUT (secondes)", min_value=0.1, value=5.0, step=0.1, format="%.1f")
        fmt       = st.radio("Format", ["9:16 (Short blur-pad)", "16:9 (Longform)"], index=0)
    with col2:
        speed  = st.slider("Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.05)
        volume = st.slider("Volume", min_value=0.0, max_value=2.0, value=1.0, step=0.05)

    fmt_arg = "9:16" if "9:16" in fmt else "16:9"
    duration = out_point - in_point
    st.info(f"Durée du clip hook : **{duration:.1f}s**")

    # ─── Section 3 : Hook question ────────────────────────────────────────────
    st.header("3. Hook question")
    hook_question = st.text_input(
        "Question hook (obligatoire pour le ledger)",
        placeholder='Mais comment CR7 peut-il courber la balle comme ça ?',
    )

    # ─── Section 4 : CUT ─────────────────────────────────────────────────────
    st.header("4. CUT")

    can_cut = hook_question.strip() != ""
    if not can_cut:
        st.warning("Entrez la hook_question avant de couper.")

    hook_ready = _OUT / "hook_ready.mp4"

    cut_button = st.button("CUT — Générer hook_ready.mp4", disabled=not can_cut)

    if cut_button and can_cut:
        with st.spinner("FFmpeg en cours..."):
            result = subprocess.run(
                [sys.executable, str(_ROOT / "HOOK_STUDIO/cutter.py"),
                 "--input",         str(clip_brut),
                 "--output",        str(hook_ready),
                 "--in-point",      str(in_point),
                 "--out-point",     str(out_point),
                 "--format",        fmt_arg,
                 "--speed",         str(speed),
                 "--volume",        str(volume),
                 "--hook-question", hook_question],
                capture_output=True, text=True,
                cwd=str(_ROOT),
            )
        if result.returncode == 0:
            st.success(f"hook_ready.mp4 généré et copié dans F02_LACERAT/IN/HOOK/")
            st.video(str(hook_ready))
            st.session_state["hook_done"] = True
            st.session_state["hook_question"] = hook_question
        else:
            st.error(f"Erreur FFmpeg :\n{result.stderr}")

# ─── Section 5 : Résumé ──────────────────────────────────────────────────────
if st.session_state.get("hook_done"):
    st.header("5. Prêt")
    st.success("hook_ready.mp4 disponible. Lancer SANGUIS en mode hook.")
    st.code(
        f'python3 F01_SANGUIS/CODEBASE/sanguis.py \\\n'
        f'    --concept "..." \\\n'
        f'    --format short \\\n'
        f'    --mode hook \\\n'
        f'    --hook-question "{st.session_state.get("hook_question", "")}" \\\n'
        f'    --id XXX \\\n'
        f'    --output F01_SANGUIS/OUT/script_XXX.md',
        language="bash",
    )
