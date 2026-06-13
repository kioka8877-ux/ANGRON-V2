"""
ANGRON_STYLE — Charte graphique immuable de la flotte ANGRON.

Ce fichier EST la loi esthétique. Claude ne réinterprète pas ces valeurs.
LACERAT injecte ce dictionnaire tel quel dans chaque prompt Manim généré.
"""

ANGRON_STYLE = {
    # Couleurs — palette 3B1B épurée
    "background":   "#171717",   # gris-noir mat absorbant — jamais noir pur pixel
    "primary":      "#58C4DD",   # bleu canard — couleur principale
    "secondary":    "#FFF1B6",   # jaune crème — mise en évidence
    "accent":       "#A6CF98",   # vert sauge — troisième voix
    "text":         "#ECEFF1",   # blanc cassé — texte principal
    "text_dim":     "#90A4AE",   # gris bleuté — texte secondaire
    "highlight":    "#FF6D00",   # orange vif — alerte / focus exceptionnel
    "error":        "#EF5350",   # rouge doux — erreur

    # Typographie
    "font":         "CMU Serif",  # Computer Modern — police 3B1B
    "font_mono":    "CMU Typewriter Text",

    # Trait et géométrie
    "stroke_width": 2,            # maximum — jamais dépasser 3
    "stroke_width_bold": 3,       # pour les éléments à fort contraste
    "transition":   "smooth",     # INTERDIT : cut sec, arrêt net robotique

    # Formats de sortie
    "formats": {
        "short":    {
            "resolution": "1080x1920",
            "ratio":      "9:16",
            "width":      1080,
            "height":     1920
        },
        "longform": {
            "resolution": "1920x1080",
            "ratio":      "16:9",
            "width":      1920,
            "height":     1080
        }
    },

    # Rendu
    "fps":          60,
    "pixel_format": "yuv420p",
    "codec":        "libx264",
    "crf":          18,
    "preset":       "fast",

    # Audio (standard YouTube)
    "audio_loudnorm": "I=-14:TP=-1:LRA=11",
    "audio_bitrate":  "192k",
    "audio_rate":     48000,
    "audio_channels": 2,

    # Métadonnées camouflage (NUCERIA)
    "meta_encoder": "",
    "meta_title_template": "{concept}",
    "fingerprints_interdits": [
        "manim", "remotion", "opencv", "python", "openai",
        "runway", "stable-diffusion", "lavf", "lavc",
        "moviepy", "ffmpeg-python", "angron", "claude"
    ]
}

# Version de la charte — incrémenter à chaque modification validée par l'opérateur
ANGRON_STYLE_VERSION = "1.0"
