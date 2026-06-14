# ANGRON — PROMPT MANIM [001]
**Concept :** Boxe : le mythe des géants
**Format :** SHORT 9:16
**Résolution :** 1080x1920
**FPS :** 60
**Durée audio :** 49.37s
**Assets :** aucun

---

## CHARTE GRAPHIQUE (ANGRON_STYLE v1.0)
```python
BG       = "#171717"   # fond — TOUJOURS ce code exact
PRIMARY  = "#58C4DD"   # bleu canard
SECONDARY= "#FFF1B6"   # jaune crème
ACCENT   = "#A6CF98"   # vert sauge
TEXT     = "#ECEFF1"   # blanc cassé
TEXT_DIM = "#90A4AE"   # texte secondaire
HIGHLIGHT= "#FF6D00"   # alerte / focus
FONT     = "CMU Serif"
STROKE   = 2
```

## CONFIGURATION SCÈNE
```python
config.frame_rate = 60
config.pixel_width  = 1080
config.pixel_height = 1920
config.background_color = "#171717"
import manim.utils.font_system as font_system
# La police CMU Serif doit être installée sur le système de CRUOR
```

---

## STORYBOARD BLOC PAR BLOC

### BLOC 1 | [0.0s → 4.359s] | ACCROCHE
**Texte :** "Pourquoi les géants se font éteindre par plus petit qu'eux ?"
**Directive originale :** [ANIM: comparaison_côte_à_côte]
**Traduction Manim :**
```python
gauche_geant = Rectangle(width=2, height=6, color=PRIMARY, fill_opacity=0.2).move_to(LEFT * 2.5)
droite_petit = Rectangle(width=2, height=3.5, color=ACCENT, fill_opacity=0.2).move_to(RIGHT * 2.5 + DOWN * 1.25)
separateur = DashedLine(UP * 4, DOWN * 4, color=TEXT_DIM)
texte = Tex(r"Géant vs Petit", color=TEXT, font_size=48).move_to(UP * 5)

self.play(FadeIn(gauche_geant), FadeIn(droite_petit), Create(separateur), Write(texte), run_time=1.5)
self.wait(2.859)
```
**Timing :** start=0.0, end=4.359, anim=1.5s, wait=2.859s
**Notes :** Indépendant. Représentation stylisée des gabarits.

---

### BLOC 2 | [4.659s → 8.225s] | SUSPENSE
**Texte :** "On croit que des longs bras frappent plus fort."
**Directive originale :** [ANIM: question_apparaît_suspense]
**Traduction Manim :**
```python
question = Tex(r"Les longs bras \\ frappent-ils plus fort ?", color=TEXT, font_size=52, text_alignment="CENTER").move_to(ORIGIN)

self.play(AddTextLetterByLetter(question, time_per_char=0.05), run_time=1.5)
self.wait(2.066)
```
**Timing :** start=4.659, end=8.225, anim=1.5s, wait=2.066s

---

### BLOC 3 | [8.525s → 10.11s] | CONTRE-PIED
**Texte :** "La physique dit l'inverse."
**Directive originale :** [ANIM: réponse_révélée_dessous]
**Traduction Manim :**
```python
reponse = Tex(r"La physique dit \textbf{l'inverse}.", color=HIGHLIGHT, font_size=64).move_to(ORIGIN)
cover = Rectangle(width=10, height=2, color=BG, fill_opacity=1).move_to(ORIGIN)

self.add(reponse, cover)
self.play(FadeOut(cover, shift=RIGHT), run_time=0.6)
self.wait(0.985)
```
**Timing :** start=8.525, end=10.11, anim=0.6s, wait=0.985s

---

### BLOC 4 | [10.41s → 13.58s] | TENSION
**Texte :** "Avoir une immense allonge est un piège biomécanique."
**Directive originale :** [ANIM: titre_frappe_écran]
**Traduction Manim :**
```python
titre = Tex(r"PIÈGE BIOMÉCANIQUE", color=PRIMARY, font_size=72)
titre.scale(0.1)

self.play(GrowFromCenter(titre, point_color=PRIMARY), titre.animate.scale(10), run_time=0.6, rate_func=there_and_back_with_pause)
self.wait(2.57)
```
**Timing :** start=10.41, end=13.58, anim=0.6s, wait=2.57s

---

### BLOC 5 | [13.88s → 18.239s] | ARGUMENT
**Texte :** "Plus ton bras est long, plus il est dur à lancer."
**Directive originale :** [ANIM: surbrillance_mot_clé]
**Traduction Manim :**
```python
phrase = Tex(r"Plus le bras est long,\\ plus il est ", r"dur", r" à lancer.", color=TEXT, font_size=52, text_alignment="CENTER")
phrase.move_to(ORIGIN)

self.play(Write(phrase), run_time=1.5)
self.play(phrase[1].animate.set_color(HIGHLIGHT).scale(1.3), run_time=0.4)
self.wait(2.459)
```
**Timing :** start=13.88, end=18.239, anim=1.9s, wait=2.459s

---

### BLOC 6 | [18.539s → 20.124s] | MOMENT D'INERTIE
**Texte :** "C'est le moment d'inertie."
**Directive originale :** [ANIM: humanoïde_rotation_moment_inertie]
**Traduction Manim :**
```python
pivot = Dot(ORIGIN, color=TEXT)
bras_long = Line(ORIGIN, RIGHT*4, color=PRIMARY, stroke_width=12)
bras_court = Line(ORIGIN, RIGHT*2, color=ACCENT, stroke_width=12)

# Bras long qui peine à démarrer
self.play(Rotate(bras_long, angle=PI/2, about_point=ORIGIN), run_time=0.5, rate_func=linear)
# Bras court qui "snap" (très rapide)
self.play(Rotate(bras_court, angle=PI/2, about_point=ORIGIN), run_time=0.2, rate_func=rush_into)
self.wait(0.885)
```
**Timing :** start=18.539, end=20.124, anim=0.7s, wait=0.885s
**Notes :** Répond exactement à la directive LACERAT de contraste visuel entre la lenteur et le "snap".

---

### BLOC 7 | [20.424s → 23.594s] | LEVIER COMPACT
**Texte :** "Un bras court agit comme un levier compact."
**Directive originale :** [ANIM: squelette_articulé_mouvement]
**Traduction Manim :**
```python
epaule = Dot(LEFT*2, color=TEXT)
coude = Dot(ORIGIN, color=TEXT)
poing = Dot(RIGHT*2 + UP*2, color=ACCENT, radius=0.15)
biceps = Line(epaule.get_center(), coude.get_center(), stroke_width=10, color=SECONDARY)
avant_bras = Line(coude.get_center(), poing.get_center(), stroke_width=10, color=SECONDARY)

bras = VGroup(epaule, coude, poing, biceps, avant_bras)
bras.move_to(ORIGIN)

self.play(Create(bras), run_time=1.0)
self.play(bras.animate.stretch(0.5, dim=0).set_color(ACCENT), run_time=0.5) # Devient compact
self.wait(1.67)
```
**Timing :** start=20.424, end=23.594, anim=1.5s, wait=1.67s

---

### BLOC 8 | [23.894s → 27.064s] | ACCÉLÉRATION
**Texte :** "Il accélère beaucoup plus vite vers sa cible."
**Directive originale :** [ANIM: vecteur_force_apparaît_sur_corps]
**Traduction Manim :**
```python
poing_cible = Dot(LEFT*3, color=TEXT, radius=0.2)
vecteur = Arrow(LEFT*3, RIGHT*3, color=HIGHLIGHT, buff=0.1, max_tip_length_to_length_ratio=0.15, stroke_width=8)

self.play(FadeIn(poing_cible), run_time=0.5)
self.play(GrowArrow(vecteur), run_time=0.8)
self.wait(1.87)
```
**Timing :** start=23.894, end=27.064, anim=1.3s, wait=1.87s

---

### BLOC 9 | [27.364s → 30.138s] | ÉQUATION (FOCUS)
**Texte :** "Regarde l'énergie cinétique : E = ½mv²."
**Directive originale :** [ANIM: équation_apparaît_progressive]
**Traduction Manim :**
```python
# Groupement précis pour isoler le "^2" (index 5)
eq = MathTex(r"E", r"=", r"\frac{1}{2}", r"m", r"v", r"^2", color=SECONDARY, font_size=80)
eq.move_to(ORIGIN)

self.play(Write(eq), run_time=1.5)
self.play(eq[5].animate.set_color(HIGHLIGHT).scale(1.8), run_time=0.4) # Le carré flashe et s'agrandit
self.wait(0.874)
```
**Timing :** start=27.364, end=30.138, anim=1.9s, wait=0.874s
**Notes :** Respect absolu de la note F02 concernant le carré sur le 'v'.

---

### BLOC 10 | [30.438s → 34.797s] | IMPACT
**Texte :** "La vitesse est au carré. Elle compte double dans le KO."
**Directive originale :** [ANIM: surbrillance_mot_clé]
**Traduction Manim :**
```python
texte_ko = Tex(r"Elle compte ", r"double", r" dans le ", r"KO.", color=TEXT, font_size=56)
texte_ko.move_to(ORIGIN)

self.play(Write(texte_ko), run_time=1.5)
self.play(
    texte_ko[1].animate.set_color(HIGHLIGHT).scale(1.2),
    texte_ko[3].animate.set_color(PRIMARY).scale(1.2),
    run_time=0.4
)
self.wait(2.459)
```
**Timing :** start=30.438, end=34.797, anim=1.9s, wait=2.459s

---

### BLOC 11 | [35.097s → 37.078s] | DÉTAIL
**Texte :** "Le détail qui tue ?"
**Directive originale :** [ANIM: question_apparaît_suspense]
**Traduction Manim :**
```python
detail = Tex(r"Le détail qui tue ?", color=TEXT_DIM, font_size=60)
self.play(AddTextLetterByLetter(detail, time_per_char=0.06), run_time=1.0)
self.wait(0.981)
```
**Timing :** start=35.097, end=37.078, anim=1.0s, wait=0.981s

---

### BLOC 12 | [37.378s → 41.737s] | CENTRE DE GRAVITÉ
**Texte :** "Un centre de gravité bas permet un transfert de poids instantané."
**Directive originale :** [ANIM: humanoïde_court_centre_gravité_bas]
**Traduction Manim :**
```python
# Représentation stylisée d'un humanoïde court
corps = RoundedRectangle(corner_radius=0.5, height=2.5, width=1.2, color=TEXT, fill_opacity=0.1)
cg = Dot(corps.get_bottom() + UP*0.8, color=ACCENT, radius=0.15)
arrow_cg = Arrow(cg.get_center() + RIGHT*2, cg.get_center(), color=ACCENT)
label = Tex(r"CG Bas", color=ACCENT, font_size=40).next_to(arrow_cg, RIGHT)

groupe_cg = VGroup(corps, cg, arrow_cg, label).move_to(ORIGIN)

self.play(Create(corps), FadeIn(cg), run_time=1.0)
self.play(GrowArrow(arrow_cg), Write(label), run_time=0.5)
self.wait(2.859)
```
**Timing :** start=37.378, end=41.737, anim=1.5s, wait=2.859s

---

### BLOC 13 | [42.037s → 45.999s] | RÉSULTAT GRAPHIQUE
**Texte :** "Résultat : la même force de destruction. L'agilité en plus."
**Directive originale :** [ANIM: graphe_barres_croissance]
**Traduction Manim :**
```python
axes = Axes(x_range=[0, 3, 1], y_range=[0, 10, 2], x_length=6, y_length=5, axis_config={"color": TEXT_DIM})
barre_force = Rectangle(width=1, height=4, color=PRIMARY, fill_opacity=0.8).move_to(axes.c2p(1, 0), aligned_edge=DOWN)
barre_agilite = Rectangle(width=1, height=0.1, color=ACCENT, fill_opacity=0.8).move_to(axes.c2p(2, 0), aligned_edge=DOWN)

label_f = Tex(r"Force", font_size=36).next_to(barre_force, DOWN)
label_a = Tex(r"Agilité", font_size=36).next_to(barre_agilite, DOWN, buff=1.0) # buff fixe temporaire

self.play(Create(axes), FadeIn(barre_force), Write(label_f), Write(label_a), run_time=1.0)
self.play(barre_agilite.animate.stretch_to_fit_height(4.5).move_to(axes.c2p(2,0), aligned_edge=DOWN), run_time=1.0)
self.wait(1.962)
```
**Timing :** start=42.037, end=45.999, anim=2.0s, wait=1.962s

---

### BLOC 14 | [46.299s → 49.073s] | OUTRO
**Texte :** "Quel autre mythe sportif on pulvérise ?"
**Directive originale :** [ANIM: transition_dissolve_suivant]
**Traduction Manim :**
```python
outro = Tex(r"Quel autre mythe\\on pulvérise ?", color=TEXT, font_size=64, text_alignment="CENTER")
self.play(FadeIn(outro, shift=UP), run_time=1.0)
self.wait(0.974)
self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
```
**Timing :** start=46.299, end=49.073, anim=1.8s, wait=0.974s

---

## ASSETS REQUIS
| Fichier | Usage | Bloc |
|---------|-------|------|
| (aucun) | N/A | Tous |

## NOTES CRUOR
- **Indépendance stricte :** Chaque bloc est totalement isolé et crée ses propres variables. Aucune référence croisée.
- **Paramétrage MathTex :** Dans le Bloc 9, l'équation `E = \frac{1}{2}mv^2` a été subdivisée en 6 groupes textuels bruts pour cibler exactement `^2` à l'index `[5]`. Ne pas modifier les `r""` sous peine de briser les index.
- **Absence d'assets :** Tout est géré par la géométrie native de Manim (rectangles, lignes, points) pour garantir une exécution stand-alone immédiate.
- L'import global `import manim.utils.font_system as font_system` pourrait être requis sur certaines versions de Manim pour forcer `CMU Serif`.