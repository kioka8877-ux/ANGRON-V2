"""
scenes_004.py — F03_CRUOR
ANGRON Projet 004 — Trivela de Lamine — Magnus Effect (image_bg mode)
Format : SHORT 9:16 | 1080x1920 | 60fps | 68.32s audio
9 scenes InteractiveScene — manimgl
C1 (hook_ready.mp4) est gere par NAILS, pas ici.
"""

from manimlib import *
import numpy as np

BG        = "#171717"
PRIMARY   = "#58C4DD"
SECONDARY = "#FFF1B6"
ACCENT    = "#A6CF98"
TEXT_C    = "#ECEFF1"
TEXT_DIM  = "#90A4AE"
HIGHLIGHT = "#EF5350"

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 60
config.background_color = BG

FONT = "Liberation Sans"


def T(text, color=TEXT_C, size=44, bold=True):
    w = "BOLD" if bold else "NORMAL"
    return Text(text, font=FONT, weight=w, color=color, font_size=size)


def _clear(scene, t=0.2):
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=t)


def _tip_polygon(point, direction, color, scale=0.15):
    """Triangle arrowhead a placer manuellement."""
    tip = Triangle(color=color, fill_color=color, fill_opacity=1).scale(scale)
    angle = np.arctan2(direction[1], direction[0])
    tip.rotate(angle - PI / 2)
    tip.move_to(point)
    return tip


# ──────────────────────────────────────────────────────────────────────────────
# C2 — QUESTION  blocs 1  | voix 0.0–5.08s | scene totale 5.93s
# ──────────────────────────────────────────────────────────────────────────────
class S01QuestionScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        # Animation principale : texte qui se construit ligne par ligne, tres grand
        why    = T("Why", color=TEXT_C,  size=86)
        lamine = T("Lamine's", color=TEXT_C,  size=86)
        trivela = T("trivela", color=PRIMARY, size=100)
        group_top = VGroup(why, lamine, trivela).arrange(DOWN, buff=0.5)
        group_top.move_to(UP * 1.2)

        underline = Line(
            trivela.get_left()  + DOWN * 0.2,
            trivela.get_right() + DOWN * 0.2,
            color=PRIMARY, stroke_width=3,
        )

        caption = T("is more spectacular than you think.", color=TEXT_DIM, size=30, bold=False)
        caption.move_to(DOWN * 2.8)

        # cascade d'entrees
        self.play(FadeIn(why,    shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(lamine, shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(trivela, scale=0.85),    run_time=0.5)
        self.play(ShowCreation(underline),         run_time=0.3)
        self.play(FadeIn(caption),                 run_time=0.4)
        self.wait(3.43)   # total scene : 5.93s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C3 — OUTSIDE FOOT  blocs 2-3  | voix 5.93–11.81s | scene totale 6.54s
# ──────────────────────────────────────────────────────────────────────────────
class S02OutsideFootScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        origin = DOWN * 1.5

        # Pied (ellipse) — element central
        foot = Ellipse(width=2.8, height=1.2, color=TEXT_C, stroke_width=2)
        foot.move_to(origin)
        foot_label = T("foot", color=TEXT_DIM, size=24)
        foot_label.next_to(foot, DOWN, buff=0.2)

        # Axe de spin (vertical pointille)
        spin_axis = DashedLine(origin + DOWN * 0.6, origin + UP * 4.5,
                               color=SECONDARY, dash_length=0.18, stroke_width=2)
        spin_label = T("spin axis", color=SECONDARY, size=26)
        spin_label.next_to(spin_axis, RIGHT, buff=0.2).shift(UP * 1.5)

        # Direction normale (droite, gris)
        dir_normal = Arrow(origin + UP * 1.8, origin + UP * 1.8 + RIGHT * 3.0,
                           color=TEXT_DIM, stroke_width=3,
                           max_tip_length_to_length_ratio=0.18)
        label_normal = T("normal", color=TEXT_DIM, size=24)
        label_normal.next_to(dir_normal, RIGHT, buff=0.15)

        # Direction trivela (gauche, bleu) — plus epaisse, dominante
        dir_trivela = Arrow(origin + UP * 1.8, origin + UP * 1.8 + LEFT * 3.0,
                            color=PRIMARY, stroke_width=5,
                            max_tip_length_to_length_ratio=0.18)
        label_trivela = T("trivela", color=PRIMARY, size=24)
        label_trivela.next_to(dir_trivela, LEFT, buff=0.15)

        # Flip label — grand
        flip = T("flip spin →", color=SECONDARY, size=44)
        flip.move_to(UP * 3.5)

        self.play(FadeIn(foot), FadeIn(foot_label), run_time=0.6)
        self.play(ShowCreation(spin_axis), FadeIn(spin_label), run_time=0.7)
        self.play(GrowArrow(dir_normal), FadeIn(label_normal), run_time=0.5)
        self.play(GrowArrow(dir_trivela), FadeIn(label_trivela), run_time=0.6)
        self.play(FadeIn(flip, scale=0.8), run_time=0.5)
        self.wait(3.64)   # total 6.54s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C4 — MAGNUS EQUATION  blocs 4-6  | voix 12.47–27.5s | scene totale 15.45s
# ──────────────────────────────────────────────────────────────────────────────
class S03MagnusEquationScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        center = UP * 1.5

        # Balle grande — element principal
        ball = Circle(radius=1.8, color=TEXT_C, stroke_width=2)
        ball.set_fill(BG, opacity=0.8)
        ball.move_to(center)

        # Bras rotatif (vecteur spin) — montre la rotation
        arm = Line(center, center + UP * 1.8, color=PRIMARY, stroke_width=5)
        arm_tip = Triangle(color=PRIMARY, fill_color=PRIMARY, fill_opacity=1).scale(0.14)
        arm_tip.move_to(center + UP * 1.8)

        # Arc de trajectoire (courbe Magnus) — sort de la balle
        traj = ArcBetweenPoints(
            center + RIGHT * 1.8,
            center + RIGHT * 3.5 + DOWN * 2.5,
            angle=-PI / 3,
        )
        traj.set_color(SECONDARY)
        traj.set_stroke(width=3)

        self.play(ShowCreation(ball), run_time=0.8)
        self.play(ShowCreation(arm), FadeIn(arm_tip), run_time=0.5)
        # rotation CCW → montre le spin
        self.play(Rotate(arm,     angle=TAU * 1.5, about_point=center, run_time=3.0, rate_func=linear),
                  Rotate(arm_tip, angle=TAU * 1.5, about_point=center, run_time=3.0, rate_func=linear))
        self.play(ShowCreation(traj), run_time=1.0)
        self.wait(0.5)

        # Equation — grande, apparait par morceaux
        eq = Tex(r"F = \rho \cdot r \cdot v \times \omega",
                 color=TEXT_C, font_size=66)
        eq.move_to(DOWN * 1.2)
        self.play(Write(eq), run_time=2.5)

        # Labels variables (petits, en dessous de chaque terme)
        labels_data = [
            ("force", -3.0),
            (r"\rho", -1.5),
            ("r", -0.5),
            ("v", 0.6),
            (r"\omega", 1.9),
        ]
        labels = VGroup(*[
            T(txt if not txt.startswith("\\") else txt, color=SECONDARY, size=22)
                .move_to(DOWN * 2.2 + RIGHT * x)
            for txt, x in labels_data
        ])
        self.play(FadeIn(labels, shift=UP * 0.2), run_time=0.8)

        # Magnus Effect — grand, dominant
        magnus = T("Magnus Effect", color=PRIMARY, size=58)
        magnus.move_to(DOWN * 3.4)
        self.play(FadeIn(magnus, scale=0.85), run_time=0.7)
        self.wait(4.32)   # total 15.45s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C5 — CLOCKWISE  blocs 7-11  | voix 27.92–35.68s | scene totale 9.09s
# ──────────────────────────────────────────────────────────────────────────────
class S04ClockwiseScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        center = UP * 0.8

        # Balle rouge/CW — tres grande
        ball = Circle(radius=2.2, color=HIGHLIGHT, stroke_width=3)
        ball.set_fill(BG, opacity=0.85)
        ball.move_to(center)

        # Bras rotatif CW
        arm = Line(center, center + UP * 2.2, color=HIGHLIGHT, stroke_width=6)
        arm_tip = Triangle(color=HIGHLIGHT, fill_color=HIGHLIGHT, fill_opacity=1).scale(0.16)
        arm_tip.move_to(center + UP * 2.2)

        label_cw = T("CLOCKWISE  ↻", color=HIGHLIGHT, size=38)
        label_cw.move_to(UP * 3.8)

        self.play(ShowCreation(ball), FadeIn(label_cw), run_time=0.7)
        self.play(ShowCreation(arm), FadeIn(arm_tip), run_time=0.4)
        # Rotation CW = angle negatif
        self.play(Rotate(arm,     angle=-TAU * 1.5, about_point=center, run_time=2.5, rate_func=linear),
                  Rotate(arm_tip, angle=-TAU * 1.5, about_point=center, run_time=2.5, rate_func=linear))

        # Ball goes right →
        arr_right = Arrow(DOWN * 1.6 + LEFT * 2.5, DOWN * 1.6 + RIGHT * 2.5,
                          color=HIGHLIGHT, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)
        label_right = T("ball goes right", color=TEXT_DIM, size=30)
        label_right.next_to(arr_right, DOWN, buff=0.25)

        self.play(GrowArrow(arr_right), FadeIn(label_right), run_time=0.6)
        self.wait(0.59)

        # "Easy." — seul, tombe, pause longue
        easy = T('"Easy."', color=TEXT_C, size=60, bold=False)
        easy.move_to(DOWN * 3.3)
        self.play(FadeIn(easy, shift=DOWN * 0.4), run_time=0.3)
        self.wait(2.49)   # total 9.09s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C6 — TRIVELA CCW  blocs 12-15  | voix 37.01–42.94s | scene totale 7.11s
# ──────────────────────────────────────────────────────────────────────────────
class S05TrivelaScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        center = UP * 0.8

        # Balle bleue/CCW — meme taille que S04 pour la comparaison
        ball = Circle(radius=2.2, color=PRIMARY, stroke_width=3)
        ball.set_fill(BG, opacity=0.85)
        ball.move_to(center)

        # Meme bras, CCW cette fois
        arm = Line(center, center + UP * 2.2, color=PRIMARY, stroke_width=6)
        arm_tip = Triangle(color=PRIMARY, fill_color=PRIMARY, fill_opacity=1).scale(0.16)
        arm_tip.move_to(center + UP * 2.2)

        label_ccw = T("TRIVELA  ↺", color=PRIMARY, size=38)
        label_ccw.move_to(UP * 3.8)

        same = T("same body position", color=SECONDARY, size=26)
        same.move_to(UP * 3.0)

        self.play(ShowCreation(ball), FadeIn(label_ccw), run_time=0.5)
        self.play(FadeIn(same), run_time=0.4)
        self.play(ShowCreation(arm), FadeIn(arm_tip), run_time=0.4)
        # CCW = angle positif
        self.play(Rotate(arm,     angle=TAU * 1.5, about_point=center, run_time=2.0, rate_func=linear),
                  Rotate(arm_tip, angle=TAU * 1.5, about_point=center, run_time=2.0, rate_func=linear))

        # Ball goes LEFT ← (inverse de S04)
        arr_left = Arrow(DOWN * 1.6 + RIGHT * 2.5, DOWN * 1.6 + LEFT * 2.5,
                         color=PRIMARY, stroke_width=5,
                         max_tip_length_to_length_ratio=0.15)
        label_left = T("ball goes left", color=PRIMARY, size=30)
        label_left.next_to(arr_left, DOWN, buff=0.25)

        self.play(GrowArrow(arr_left), FadeIn(label_left), run_time=0.6)
        self.wait(2.71)   # total 7.11s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C7 — 70 DEGREES  bloc 16  | voix 44.12–48.52s | scene totale 4.72s
# ──────────────────────────────────────────────────────────────────────────────
class S06SeventyDegreesScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        pivot = DOWN * 0.5

        # Axe de reference horizontal
        axis = Line(pivot + LEFT * 3.5, pivot + RIGHT * 3.5,
                    color=TEXT_DIM, stroke_width=2)
        axis_label = T("reference axis", color=TEXT_DIM, size=22)
        axis_label.next_to(axis, DOWN, buff=0.2)

        # Ligne de frappe trivela — 70° depuis l'axe
        angle_rad = np.radians(70)
        end_trivela = pivot + 4.0 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
        foot_line = Line(pivot, end_trivela, color=SECONDARY, stroke_width=5)

        # Arc 70° — grand rayon
        arc_70 = Arc(radius=1.4, start_angle=0, angle=angle_rad,
                     color=SECONDARY, stroke_width=3)
        arc_70.move_to(pivot)

        # Chiffre 70° — TRES GRAND, element dominant
        deg_label = Tex(r"70^\circ", color=SECONDARY, font_size=140)
        deg_label.move_to(pivot + RIGHT * 1.2 + UP * 2.0)

        off_axis = T("off-axis contact", color=TEXT_DIM, size=26)
        off_axis.move_to(UP * 3.5)

        self.play(ShowCreation(axis), FadeIn(axis_label), run_time=0.5)
        self.play(ShowCreation(foot_line), run_time=0.6)
        self.play(ShowCreation(arc_70), run_time=0.5)
        self.play(FadeIn(deg_label, scale=0.7), run_time=0.4)
        self.play(FadeIn(off_axis), run_time=0.3)
        self.wait(1.92)   # total 4.72s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C8 — 10 REV/S  blocs 17-19  | voix 48.84–56.94s | scene totale 8.1s
# ──────────────────────────────────────────────────────────────────────────────
class S07RevolutionsScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        # Chiffre "10" tres grand — element dominant
        big_10   = T("10",      color=SECONDARY, size=180)
        rev_unit = T("rev / s", color=PRIMARY,   size=52)
        big_10.move_to(UP * 2.2)
        rev_unit.next_to(big_10, DOWN, buff=0.2)

        self.play(FadeIn(big_10, scale=0.6), run_time=0.7)
        self.play(FadeIn(rev_unit), run_time=0.4)
        self.wait(0.5)

        # Deux barres comparatives qui poussent depuis le bas
        bar_w = 1.1
        bar_base_y = DOWN * 0.5

        # Barre standard — courte, grise
        bar_std = Rectangle(width=bar_w, height=1.8, color=TEXT_DIM,
                            fill_color=TEXT_DIM, fill_opacity=0.9)
        bar_std.move_to(bar_base_y + LEFT * 1.1 + DOWN * 0.9 + UP * 0.9)
        bar_std.set_height(1.8, stretch=True)

        # Barre trivela — double, bleue
        bar_triv = Rectangle(width=bar_w, height=3.6, color=PRIMARY,
                             fill_color=PRIMARY, fill_opacity=0.9)
        bar_triv.move_to(bar_base_y + RIGHT * 1.1 + DOWN * 0.9 + UP * 1.8)
        bar_triv.set_height(3.6, stretch=True)

        lbl_std  = T("standard", color=TEXT_DIM, size=22).next_to(bar_std,  DOWN, buff=0.2)
        lbl_triv = T("trivela",  color=PRIMARY,  size=22).next_to(bar_triv, DOWN, buff=0.2)
        val_std  = T("5",  color=TEXT_DIM, size=28).next_to(bar_std,  UP, buff=0.15)
        val_triv = T("10", color=SECONDARY, size=28).next_to(bar_triv, UP, buff=0.15)
        x2_badge = T("× 2", color=ACCENT, size=34).move_to(bar_base_y + UP * 0.8)

        # Barres grandissent depuis le bas
        bar_std_start  = bar_std.copy().set_height(0.05, stretch=True).move_to(bar_std.get_bottom())
        bar_triv_start = bar_triv.copy().set_height(0.05, stretch=True).move_to(bar_triv.get_bottom())
        self.add(bar_std_start, bar_triv_start)
        self.play(
            bar_std_start.animate.become(bar_std),
            bar_triv_start.animate.become(bar_triv),
            run_time=1.2,
        )
        self.play(
            FadeIn(lbl_std), FadeIn(lbl_triv),
            FadeIn(val_std), FadeIn(val_triv),
            FadeIn(x2_badge),
            run_time=0.6,
        )

        # "The goalkeeper never had a chance." — tombe seul
        gk_line1 = T('"The goalkeeper', color=TEXT_C, size=32, bold=False)
        gk_line2 = T('never had a chance."', color=HIGHLIGHT, size=32, bold=False)
        gk_group = VGroup(gk_line1, gk_line2).arrange(DOWN, buff=0.2)
        gk_group.move_to(DOWN * 3.8)
        self.play(FadeIn(gk_group, shift=DOWN * 0.4), run_time=0.5)
        self.wait(3.18)   # total 8.1s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C9 — PHYSICS EXPLOIT  blocs 20-22  | voix 56.94–64.3s | scene totale 8.26s
# ──────────────────────────────────────────────────────────────────────────────
class S08PhysicsExploitScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        ball_center = UP * 1.2

        # Balle — grande
        ball = Circle(radius=1.6, color=TEXT_C, stroke_width=2)
        ball.set_fill(BG, opacity=0.8)
        ball.move_to(ball_center)

        # Pied qui arrive de la gauche
        foot = Ellipse(width=2.0, height=0.8, color=TEXT_C, stroke_width=2)
        foot.move_to(ball_center + LEFT * 2.8 + DOWN * 0.5)

        # Vecteur de contact (force sur la balle)
        contact_vec = Arrow(
            ball_center + LEFT * 2.0 + DOWN * 0.5,
            ball_center + LEFT * 0.4,
            color=SECONDARY, stroke_width=5,
            max_tip_length_to_length_ratio=0.2,
        )

        # Arc spin sur la balle (CCW)
        spin_arc = Arc(radius=1.0, start_angle=PI / 4, angle=TAU * 0.7,
                       color=PRIMARY, stroke_width=3)
        spin_arc.move_to(ball_center)
        spin_tip = Triangle(color=PRIMARY, fill_color=PRIMARY, fill_opacity=1).scale(0.12)
        end_angle = PI / 4 + TAU * 0.7
        spin_tip.move_to(ball_center + 1.0 * np.array([np.cos(end_angle), np.sin(end_angle), 0]))
        spin_tip.rotate(end_angle - PI / 2)

        # Angle de contact (petit arc vert)
        contact_arc = Arc(radius=0.55, start_angle=PI, angle=-PI / 4,
                          color=ACCENT, stroke_width=2)
        contact_arc.move_to(ball_center + LEFT * 0.4)

        # "physics exploit" — tres grand, dominant
        word1 = T("physics",  color=SECONDARY, size=72)
        word2 = T("exploit",  color=SECONDARY, size=72)
        words = VGroup(word1, word2).arrange(DOWN, buff=0.3)
        words.move_to(DOWN * 1.8)

        geo_label = T("geometry of contact", color=ACCENT, size=28)
        geo_label.move_to(DOWN * 3.6)
        geo_underline = Line(
            geo_label.get_left() + DOWN * 0.1,
            geo_label.get_right() + DOWN * 0.1,
            color=ACCENT, stroke_width=1,
        )

        self.play(ShowCreation(ball), run_time=0.6)
        self.play(FadeIn(foot, shift=RIGHT * 0.5), run_time=0.5)
        self.play(GrowArrow(contact_vec), run_time=0.6)
        self.play(ShowCreation(spin_arc), FadeIn(spin_tip), ShowCreation(contact_arc), run_time=0.8)
        self.play(FadeIn(words, scale=0.75), run_time=0.7)
        self.play(FadeIn(geo_label), ShowCreation(geo_underline), run_time=0.5)
        self.wait(3.54)   # total 8.26s
        _clear(self)


# ──────────────────────────────────────────────────────────────────────────────
# C10 — CHUTE FINALE  blocs 23-24  | voix 65.2–68.32s | scene totale 3.12s
# ──────────────────────────────────────────────────────────────────────────────
class S09FinalScene(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        # Silhouette corps abstrait en haut — body lies
        head    = Circle(radius=0.35, color=TEXT_C, stroke_width=2).move_to(UP * 3.6)
        torso   = Line(UP * 3.2, UP * 1.8, color=TEXT_C, stroke_width=2)
        arm_l   = Line(UP * 2.8, UP * 2.8 + LEFT  * 0.8 + DOWN * 0.6, color=TEXT_C, stroke_width=2)
        arm_r   = Line(UP * 2.8, UP * 2.8 + RIGHT * 0.8 + DOWN * 0.6, color=TEXT_C, stroke_width=2)
        leg_l   = Line(UP * 1.8, UP * 1.8 + LEFT  * 0.6 + DOWN * 1.2, color=TEXT_C, stroke_width=2)
        leg_r   = Line(UP * 1.8, UP * 1.8 + RIGHT * 0.6 + DOWN * 1.2, color=TEXT_C, stroke_width=2)
        silhou  = VGroup(head, torso, arm_l, arm_r, leg_l, leg_r)
        silhou.set_stroke(opacity=0.45)

        # X sur le corps (body lies)
        cross1 = Line(UP * 3.8 + LEFT * 0.7, UP * 0.8 + RIGHT * 0.7,
                      color=HIGHLIGHT, stroke_width=3)
        cross2 = Line(UP * 3.8 + RIGHT * 0.7, UP * 0.8 + LEFT * 0.7,
                      color=HIGHLIGHT, stroke_width=3)

        # "The body lies." — tombe
        line1 = T('"The body lies."', color=TEXT_C, size=46, bold=False)
        line1.move_to(DOWN * 0.2)

        # "The equations don't." — en PRIMARY, apres pause
        line2 = T('"The equations don\'t."', color=PRIMARY, size=46, bold=False)
        line2.move_to(DOWN * 1.5)

        # CTA en bas — encadre
        cta_text = T("Follow for physics", color=SECONDARY, size=34)
        cta_text.move_to(DOWN * 3.4)
        cta_box = Rectangle(
            width=cta_text.get_width() + 0.8,
            height=cta_text.get_height() + 0.4,
            color=SECONDARY, stroke_width=1.5,
        )
        cta_box.move_to(cta_text.get_center())

        self.play(FadeIn(silhou, shift=DOWN * 0.2), run_time=0.3)
        self.play(ShowCreation(cross1), ShowCreation(cross2), run_time=0.4)
        self.play(FadeIn(line1, shift=DOWN * 0.3), run_time=0.35)
        self.wait(0.3)
        self.play(FadeIn(line2, shift=DOWN * 0.3), run_time=0.35)
        self.play(ShowCreation(cta_box), FadeIn(cta_text), run_time=0.4)
        self.wait(0.97)   # total 3.12s
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.3)

