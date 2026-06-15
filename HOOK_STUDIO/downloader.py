"""
downloader.py — HOOK_STUDIO : téléchargement de clips via yt-dlp.

Supporte YouTube, Twitter/X, TikTok, Instagram.
Télécharge en meilleure qualité disponible, merge audio+vidéo si nécessaire.

Usage :
    python3 HOOK_STUDIO/downloader.py \
        --url "https://youtube.com/watch?v=..." \
        --output HOOK_STUDIO/tmp/clip_brut.mp4
"""

import argparse
import subprocess
import sys
from pathlib import Path


SUPPORTED_PATTERNS = [
    "youtube.com", "youtu.be",
    "twitter.com", "x.com",
    "tiktok.com",
    "instagram.com",
]


def download_clip(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    supported = any(p in url for p in SUPPORTED_PATTERNS)
    if not supported:
        print(f"[DOWNLOADER] AVERTISSEMENT : domaine non listé — tentative quand même.", file=sys.stderr)

    print(f"[DOWNLOADER] URL    : {url}")
    print(f"[DOWNLOADER] Output : {output}")

    cmd = [
        "yt-dlp",
        "--merge-output-format", "mp4",
        "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--output", str(output),
        "--no-playlist",
        "--no-warnings",
        url,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[DOWNLOADER] ERREUR yt-dlp :\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)

    if not output.exists():
        print(f"[DOWNLOADER] ERREUR : fichier absent après download : {output}", file=sys.stderr)
        sys.exit(1)

    size_mb = output.stat().st_size / (1024 * 1024)
    print(f"[DOWNLOADER] OK — {output.name} ({size_mb:.1f} MB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="DOWNLOADER — yt-dlp wrapper HOOK_STUDIO")
    parser.add_argument("--url",    required=True, help="URL YouTube/Twitter/TikTok/Instagram")
    parser.add_argument("--output", required=True, help="Chemin de sortie du clip brut (.mp4)")
    args = parser.parse_args()

    download_clip(url=args.url, output=Path(args.output))


if __name__ == "__main__":
    main()
