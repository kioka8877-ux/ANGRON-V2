# ANGRON — Environnement de rendu complet — V2
# Image : ghcr.io/kioka8877-ux/angron-v2:latest
# Contient : manimgl + LaTeX + FFmpeg + Whisper + Cairo + CMU Serif + yt-dlp + streamlit

FROM python:3.11-slim-bookworm

# Dependances systeme
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config \
    texlive-full \
    dvisvgm \
    ffmpeg \
    libcairo2-dev libpango1.0-dev \
    libgl1-mesa-glx libgles2-mesa libegl1-mesa \
    xvfb \
    fonts-cmu \
    libsndfile1 \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python — manimgl + Whisper
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

ENV DISPLAY=:99
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace
CMD ["/bin/bash"]
