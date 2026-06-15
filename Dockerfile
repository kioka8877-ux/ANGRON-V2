# ANGRON — Environnement de rendu complet — V2
# Image : ghcr.io/kioka8877-ux/angron-v2:latest
# Contient : manimgl + LaTeX + FFmpeg + Whisper + Cairo + CMU Serif + yt-dlp + streamlit

FROM python3.11-slim-bookworm

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build tools
    build-essential pkg-config \
    # LaTeX complet pour Manim
    texlive-full \
    # dvisvgm requis par manimgl pour le rendu LaTeX  SVG
    dvisvgm \
    # FFmpeg
    ffmpeg \
    # Cairo + Pango (rendu vectoriel Manim)
    libcairo2-dev libpango1.0-dev \
    # OpenGL headless
    libgl1-mesa-glx libgles2-mesa libegl1-mesa \
    xvfb \
    # Fonts CMU (Computer Modern  style 3B1B)
    fonts-cmu \
    # Audio
    libsndfile1 \
    # Git (pour ledger commits)
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python  Manim + voiceover + Whisper
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Variables d'environnement rendu headless
ENV DIRPLAY=:99
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Point d'entrée par défaut
WORKDIR /workspace
CMD ["/bin/bash"]
