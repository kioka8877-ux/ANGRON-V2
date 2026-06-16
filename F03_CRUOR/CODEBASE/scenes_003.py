"""
scenes_003.py — F03_CRUOR
ANGRON Projet 003 — Trivela de Lamine — Magnus Effect (test run)
Format : SHORT 9:16 | 1080x1920 | 60fps | 68.32s audio
7 scènes InteractiveScene — manimgl
"""

from manimlib import *

# ─── ANGRON_STYLE PALETTE ─────────────────────────────────────────────────────
BG        = "#171717"
PRIMARY   = "#58C4DD"
SECONDARY = "#FFF1B6"
ACCENT    = "#A6CF98"
TEXT_C    = "#ECEFF1"
TEXT_DIM  = "#90A4AE"
HIGHLIGHT = "#FF6D00"

config.pixel_width      = 1080
config.pixel_height     = 1920
config.frame_rate       = 60
config.background_color = BG


def _clear_all(scene):
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.15)


# ═══════════════════════════════════════════════════════════════════════════════
# S01 — HOOK QUESTION  [0.0 → 5.93s]
# ═══════════════════════════════════════════════════════════════════════════════
class S01HookQuestion(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        line1 = Tex(r"Why Lamine's", color=TEXT_C, font_size=72)
        line2a = Tex(r"trivela", color=PRIMARY, font_size=72)
        line2b = Tex(r" is more", color=TEXT_C, font_size=72)
        line2  = VGroup(line2a, line2b).arrange(RIGHT, buff=0.05)
        line3 = Tex(r"spectacular", color=SECONDARY, font_size=72)
        line4 = Tex(r"than you think.", color=TEXT_DIM, font_size=56)

        group = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.35)
        group.move_to(ORIGIN)

        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line3, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line4, shift=UP * 0.2), run_time=0.5)
        self.wait(3.28)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S02 — FOOT + DIRECTION  [5.93 → 12.47s]
# ═══════════════════════════════════════════════════════════════════════════════
class S02FootKick(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        t2a = Tex(r"Kick with the", color=TEXT_C, font_size=60)
        t2b = Tex(r"outside", color=PRIMARY, font_size=60)
        t2c = Tex(r"of your foot.", color=TEXT_C, font_size=60)
        b2  = VGroup(t2a, t2b, t2c).arrange(DOWN, buff=0.25).move_to(UP * 1.5)

        foot_body   = Ellipse(width=2.0, height=1.0, color=TEXT_DIM, stroke_width=2)
        outside_arc = Arc(radius=1.0, start_angle=PI * 0.1, angle=PI * 0.8,
                          color=PRIMARY, stroke_width=4)
        outside_arc.move_to(foot_body.get_right() + LEFT * 0.1)
        outside_label = Tex(r"outside", color=PRIMARY, font_size=36)
        outside_label.next_to(foot_body, RIGHT, buff=0.3)
        foot_group = VGroup(foot_body, outside_arc, outside_label).move_to(DOWN * 1.5)

        self.play(Write(b2), run_time=1.2)
        self.play(ShowCreation(foot_body), ShowCreation(outside_arc),
                  FadeIn(outside_label), run_time=0.9)
        self.wait(0.62)

        self.play(FadeOut(foot_group), run_time=0.3)

        t3a = Tex(r"You don't just", color=TEXT_C, font_size=60)
        t3b = Tex(r"change", color=TEXT_DIM, font_size=60)
        t3c = Tex(r"direction.", color=TEXT_C, font_size=60)
        b3  = VGroup(t3a, t3b, t3c).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        arrow_dir = Arrow(LEFT * 1.5, RIGHT * 1.5, color=HIGHLIGHT,
                          stroke_width=5, max_tip_length_to_length_ratio=0.18)
        arrow_dir.move_to(DOWN * 2.0)

        self.play(
            FadeOut(b2, shift=UP * 0.3),
            FadeIn(b3, shift=UP * 0.3),
            run_time=0.5,
        )
        self.play(GrowArrow(arrow_dir), run_time=0.7)
        self.wait(1.32)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S03 — SPIN AXIS FLIP + EQUATION  [12.47 → 22.48s]
# ═══════════════════════════════════════════════════════════════════════════════
class S03SpinAxis(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        flip_line1 = Tex(r"You flip the", color=TEXT_C, font_size=64)
        flip_line2 = Tex(r"spin axis.", color=PRIMARY, font_size=80)
        flip_group = VGroup(flip_line1, flip_line2).arrange(DOWN, buff=0.3)
        flip_group.move_to(UP * 2.8)

        self.play(Write(flip_line1), run_time=0.7)
        self.play(Write(flip_line2), run_time=0.8)

        cw_label  = Tex(r"Normal", color=TEXT_DIM, font_size=36).move_to(LEFT * 1.4 + DOWN * 0.3)
        cw_tip_text = Tex(r"\leftarrow", color=HIGHLIGHT, font_size=60)
        cw_tip_text.move_to(LEFT * 1.4 + DOWN * 1.4)

        ccw_label = Tex(r"Trivela", color=PRIMARY, font_size=36).move_to(RIGHT * 1.4 + DOWN * 0.3)
        ccw_tip_text = Tex(r"\rightarrow", color=PRIMARY, font_size=60)
        ccw_tip_text.move_to(RIGHT * 1.4 + DOWN * 1.4)

        sep = DashedLine(UP * 0.2, DOWN * 2.5, color=TEXT_DIM, dash_length=0.12)
        sep.move_to(ORIGIN + DOWN * 1.1)

        self.play(
            ShowCreation(sep),
            FadeIn(cw_label), FadeIn(cw_tip_text),
            FadeIn(ccw_label), FadeIn(ccw_tip_text),
            run_time=0.9,
        )
        self.wait(0.7)

        self.play(
            ccw_tip_text.animate.scale(1.3).set_color(SECONDARY),
            run_time=0.5,
        )
        self.wait(0.5)

        eq_intro = Tex(r"F = \rho \cdot r \cdot v \times \omega",
                       color=SECONDARY, font_size=72)
        eq_intro.move_to(DOWN * 3.2)

        underline = Line(
            eq_intro.get_left() + DOWN * 0.15,
            eq_intro.get_right() + DOWN * 0.15,
            color=PRIMARY, stroke_width=2,
        )

        self.play(Write(eq_intro), run_time=1.8)
        self.play(ShowCreation(underline), run_time=0.4)
        self.wait(1.38)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S04 — MAGNUS EFFECT  [22.48 → 27.92s]
# ═══════════════════════════════════════════════════════════════════════════════
class S04MagnusEffect(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        magnus_title = Tex(r"The Magnus Effect.", color=PRIMARY, font_size=72)
        magnus_title.move_to(UP * 2.5)
        underline = Line(
            magnus_title.get_left() + DOWN * 0.15,
            magnus_title.get_right() + DOWN * 0.15,
            color=PRIMARY, stroke_width=2,
        )

        self.play(FadeIn(magnus_title, shift=UP * 0.3), run_time=0.8)
        self.play(ShowCreation(underline), run_time=0.3)
        self.wait(0.66)

        ball = Circle(radius=0.4, color=TEXT_C, stroke_width=2)
        ball.set_fill(TEXT_DIM, opacity=0.3)
        ball.move_to(LEFT * 1.5 + DOWN * 0.5)

        curve_path = ArcBetweenPoints(
            LEFT * 1.5 + DOWN * 0.5,
            RIGHT * 1.5 + DOWN * 1.8,
            angle=-TAU / 5,
        )
        curve_path.set_color(PRIMARY)
        curve_path.set_stroke(width=3)

        decide_text = Tex(r"It decides every", color=TEXT_C, font_size=52)
        curve_text  = Tex(r"curve", color=PRIMARY, font_size=64)
        in_football = Tex(r"in football.", color=TEXT_C, font_size=52)
        text_group  = VGroup(decide_text, curve_text, in_football).arrange(DOWN, buff=0.2)
        text_group.move_to(DOWN * 3.0)

        self.play(
            ShowCreation(curve_path),
            FadeIn(ball),
            run_time=1.0,
        )
        self.play(Write(text_group), run_time=1.2)
        self.wait(0.42)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S05 — NORMAL vs TRIVELA COMPARISON  [27.92 → 44.12s]
# ═══════════════════════════════════════════════════════════════════════════════
class S05Comparison(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        left_hdr  = Tex(r"Normal", color=TEXT_DIM, font_size=52).move_to(LEFT * 1.1 + UP * 3.5)
        right_hdr = Tex(r"Trivela", color=PRIMARY, font_size=52).move_to(RIGHT * 1.1 + UP * 3.5)
        sep = DashedLine(UP * 3.8, DOWN * 4.5, color=TEXT_DIM, dash_length=0.1)

        normal_shot = Tex(r"Right foot shot.", color=TEXT_C, font_size=40)
        normal_shot.move_to(LEFT * 1.1 + UP * 2.5)

        self.play(
            FadeIn(left_hdr), FadeIn(right_hdr), ShowCreation(sep),
            run_time=0.8,
        )
        self.play(Write(normal_shot), run_time=0.9)
        self.wait(0.92)

        cw_spin = Tex(r"CW (clockwise)", color=HIGHLIGHT, font_size=44)
        cw_spin.move_to(LEFT * 1.1 + UP * 1.5)
        self.play(FadeIn(cw_spin, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.46)

        ball_right = Tex(r"\text{ball} \rightarrow", color=TEXT_C, font_size=44)
        ball_right.move_to(LEFT * 1.1 + UP * 0.5)
        self.play(FadeIn(ball_right, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.32)

        gk_reads = Tex(r"GK reads it.", color=ACCENT, font_size=40)
        gk_reads.move_to(LEFT * 1.1 + DOWN * 0.5)
        self.play(FadeIn(gk_reads), run_time=0.5)
        self.wait(0.22)

        easy = Tex(r"Easy.", color=TEXT_DIM, font_size=56)
        easy.move_to(LEFT * 1.1 + DOWN * 1.6)
        self.play(FadeIn(easy), run_time=0.15)
        self.wait(1.39)

        trivela_pop = Tex(r"Trivela.", color=PRIMARY, font_size=72)
        trivela_pop.move_to(RIGHT * 1.1 + UP * 2.5)
        self.play(FadeIn(trivela_pop, scale=0.7), run_time=0.4)
        self.wait(0.99)

        ccw_spin = Tex(r"CCW (counter-CW)", color=PRIMARY, font_size=44)
        ccw_spin.move_to(RIGHT * 1.1 + UP * 1.5)
        self.play(FadeIn(ccw_spin, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.80)

        same_body = Tex(r"Same body.", color=SECONDARY, font_size=40)
        same_body.move_to(RIGHT * 1.1 + UP * 0.5)
        self.play(FadeIn(same_body), run_time=0.5)
        self.wait(0.62)

        ball_left = Tex(r"\leftarrow \text{ball}", color=PRIMARY, font_size=44)
        ball_left.move_to(RIGHT * 1.1 + DOWN * 0.5)
        self.play(FadeIn(ball_left, shift=LEFT * 0.3), run_time=0.6)
        self.wait(1.58)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S06 — NUMBERS : 70° + 10 REV/S  [44.12 → 56.94s]
# ═══════════════════════════════════════════════════════════════════════════════
class S06Numbers(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        center = ORIGIN + UP * 1.2
        axis_line = Line(center + LEFT * 2.0, center + RIGHT * 2.0,
                         color=TEXT_DIM, stroke_width=2)
        foot_line = Line(center, center + 2.0 * np.array([
            np.cos(np.radians(70)), np.sin(np.radians(70)), 0
        ]), color=PRIMARY, stroke_width=4)

        arc_angle = Arc(radius=0.6, start_angle=0, angle=np.radians(70),
                        color=SECONDARY, stroke_width=2)
        arc_angle.move_to(center)

        deg_label = Tex(r"70^\circ", color=SECONDARY, font_size=64)
        deg_label.move_to(center + RIGHT * 0.9 + UP * 0.5)

        off_axis = Tex(r"off-axis", color=PRIMARY, font_size=52)
        off_axis.move_to(center + DOWN * 1.6)

        contact_label = Tex(r"contact point", color=TEXT_DIM, font_size=36)
        contact_label.move_to(center + UP * 2.5)

        self.play(ShowCreation(axis_line), run_time=0.5)
        self.play(ShowCreation(foot_line), run_time=0.6)
        self.play(ShowCreation(arc_angle), Write(deg_label), run_time=0.7)
        self.play(FadeIn(off_axis), FadeIn(contact_label), run_time=0.5)
        self.wait(2.08)

        big_10 = Tex(r"10", color=SECONDARY, font_size=160)
        big_10.move_to(DOWN * 1.2)
        rev_s  = Tex(r"rev / s", color=PRIMARY, font_size=64)
        rev_s.next_to(big_10, DOWN, buff=0.2)
        roughly = Tex(r"roughly", color=TEXT_DIM, font_size=36)
        roughly.next_to(big_10, UP, buff=0.2)

        self.play(FadeIn(big_10, scale=0.6), run_time=0.7)
        self.play(FadeIn(rev_s), FadeIn(roughly), run_time=0.5)
        self.wait(2.21)

        double_txt = Tex(r"Double", color=HIGHLIGHT, font_size=72)
        standard_txt = Tex(r"the standard shot.", color=TEXT_C, font_size=52)
        double_group = VGroup(double_txt, standard_txt).arrange(DOWN, buff=0.3)
        double_group.move_to(DOWN * 2.8)

        self.play(FadeIn(double_group), run_time=0.6)
        self.wait(1.62)

        gk_line = Tex(r"The goalkeeper", color=TEXT_C, font_size=52)
        never   = Tex(r"never had a chance.", color=HIGHLIGHT, font_size=52)
        gk_group = VGroup(gk_line, never).arrange(DOWN, buff=0.25)
        gk_group.move_to(UP * 3.2)

        self.play(FadeIn(gk_group, shift=DOWN * 0.3), run_time=0.8)
        self.wait(1.24)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S07 — CONCLUSION + CTA  [56.94 → 68.32s]
# ═══════════════════════════════════════════════════════════════════════════════
class S07Conclusion(InteractiveScene):
    CONFIG = {
        "camera_config": {
            "pixel_width": 1080,
            "pixel_height": 1920,
            "fps": 60,
        },
    }
    def construct(self):
        not_trick = Tex(r"This isn't", color=TEXT_C, font_size=60)
        not_trick2 = Tex(r"a trick shot.", color=TEXT_DIM, font_size=60)
        t20 = VGroup(not_trick, not_trick2).arrange(DOWN, buff=0.25).move_to(UP * 2.5)

        self.play(Write(not_trick), run_time=0.8)
        self.play(Write(not_trick2), run_time=0.6)
        self.wait(1.14)

        physics_exp = Tex(r"It's a", color=TEXT_C, font_size=60)
        exploit     = Tex(r"physics exploit.", color=HIGHLIGHT, font_size=72)
        t21 = VGroup(physics_exp, exploit).arrange(DOWN, buff=0.2).move_to(ORIGIN)

        self.play(FadeIn(t21, shift=UP * 0.2), run_time=0.7)
        self.wait(1.74)

        baked  = Tex(r"baked into the", color=TEXT_C, font_size=52)
        geom   = Tex(r"geometry", color=PRIMARY, font_size=64)
        ofctct = Tex(r"of contact.", color=TEXT_C, font_size=52)
        t22 = VGroup(baked, geom, ofctct).arrange(DOWN, buff=0.2).move_to(DOWN * 1.8)

        self.play(Write(t22), run_time=1.5)
        self.wait(0.96)

        body_lies = Tex(r"The body lies.", color=TEXT_DIM, font_size=56)
        body_lies.move_to(UP * 3.5)

        self.play(FadeIn(body_lies, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(0.94)

        eq_dont = Tex(r"The equations don't.", color=SECONDARY, font_size=64)
        eq_dont.move_to(UP * 3.5 + DOWN * 1.0)

        cta_follow = Tex(r"Follow for more", color=TEXT_DIM, font_size=40)
        cta_physics = Tex(r"physics", color=PRIMARY, font_size=48)
        cta_suffix  = Tex(r"hiding in plain sight.", color=TEXT_DIM, font_size=40)
        cta = VGroup(cta_follow, cta_physics, cta_suffix).arrange(DOWN, buff=0.2)
        cta.move_to(DOWN * 3.0)

        self.play(
            FadeOut(body_lies, shift=LEFT * 0.3),
            FadeIn(eq_dont, shift=UP * 0.3),
            run_time=0.5,
        )
        self.play(FadeIn(cta, shift=UP * 0.3), run_time=0.7)
        self.wait(0.88)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
