"""
scenes_003.py — F03_CRUOR
ANGRON Projet 003 — Trivela de Lamine — Magnus Effect
Format : SHORT 9:16 | 1080x1920 | 60fps | 68.32s audio
7 scenes InteractiveScene — manimgl
"""

from manimlib import *
import os as _os
import numpy as np

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

FONT = "Liberation Sans"


def T(text, color=TEXT_C, size=44):
    return Text(text, font=FONT, weight="BOLD", color=color, font_size=size)


def _clear_all(scene):
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.15)


class S01HookQuestion(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        line1  = T("Why Lamine's", size=52)
        line2a = T("trivela", color=PRIMARY, size=52)
        line2b = T("is more", size=52)
        line2  = VGroup(line2a, line2b).arrange(RIGHT, buff=0.15)
        line3  = T("spectacular", color=SECONDARY, size=52)
        line4  = T("than you think.", color=TEXT_DIM, size=40)
        group  = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.45)
        group.move_to(ORIGIN)

        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line3, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line4, shift=UP * 0.2), run_time=0.5)
        self.wait(3.28)
        _clear_all(self)


class S02FootKick(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        t2a = T("Kick with the", size=44)
        t2b = T("outside", color=PRIMARY, size=44)
        t2c = T("of your foot.", size=44)
        b2  = VGroup(t2a, t2b, t2c).arrange(DOWN, buff=0.3).move_to(UP * 2.0)

        foot_body   = Ellipse(width=2.0, height=1.0, color=TEXT_DIM, stroke_width=2)
        outside_arc = Arc(radius=1.0, start_angle=PI * 0.1, angle=PI * 0.8,
                          color=PRIMARY, stroke_width=4)
        outside_arc.move_to(foot_body.get_right() + LEFT * 0.1)
        outside_label = T("outside", color=PRIMARY, size=28)
        outside_label.next_to(foot_body, RIGHT, buff=0.3)
        foot_group = VGroup(foot_body, outside_arc, outside_label).move_to(DOWN * 1.5)

        self.play(Write(b2), run_time=1.2)
        self.play(ShowCreation(foot_body), ShowCreation(outside_arc),
                  FadeIn(outside_label), run_time=0.9)
        self.wait(0.62)
        self.play(FadeOut(foot_group), run_time=0.3)

        t3a = T("You don't just", size=44)
        t3b = T("change", color=TEXT_DIM, size=44)
        t3c = T("direction.", size=44)
        b3  = VGroup(t3a, t3b, t3c).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        arrow_dir = Arrow(LEFT * 1.5, RIGHT * 1.5, color=HIGHLIGHT,
                          stroke_width=5, max_tip_length_to_length_ratio=0.18)
        arrow_dir.move_to(DOWN * 2.2)

        self.play(FadeOut(b2, shift=UP * 0.3), FadeIn(b3, shift=UP * 0.3), run_time=0.5)
        self.play(GrowArrow(arrow_dir), run_time=0.7)
        self.wait(1.32)
        _clear_all(self)


class S03SpinAxis(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        flip_line1 = T("You flip the", size=48)
        flip_line2 = T("spin axis.", color=PRIMARY, size=60)
        flip_group = VGroup(flip_line1, flip_line2).arrange(DOWN, buff=0.35)
        flip_group.move_to(UP * 2.8)

        self.play(Write(flip_line1), run_time=0.7)
        self.play(Write(flip_line2), run_time=0.8)

        cw_label     = T("Normal",  color=TEXT_DIM, size=28).move_to(LEFT  * 1.0 + DOWN * 0.2)
        cw_tip_text  = Tex(r"\leftarrow",  color=HIGHLIGHT, font_size=52)
        cw_tip_text.move_to(LEFT  * 1.0 + DOWN * 1.2)

        ccw_label    = T("Trivela", color=PRIMARY,  size=28).move_to(RIGHT * 1.0 + DOWN * 0.2)
        ccw_tip_text = Tex(r"ightarrow", color=PRIMARY,  font_size=52)
        ccw_tip_text.move_to(RIGHT * 1.0 + DOWN * 1.2)

        sep = DashedLine(UP * 0.2, DOWN * 2.2, color=TEXT_DIM, dash_length=0.12)
        sep.move_to(ORIGIN + DOWN * 1.0)

        self.play(
            ShowCreation(sep),
            FadeIn(cw_label), FadeIn(cw_tip_text),
            FadeIn(ccw_label), FadeIn(ccw_tip_text),
            run_time=0.9,
        )
        self.wait(0.7)
        self.play(ccw_tip_text.animate.scale(1.3).set_color(SECONDARY), run_time=0.5)
        self.wait(0.5)

        eq_intro  = Tex(r"F = ho \cdot r \cdot v 	imes \omega", color=SECONDARY, font_size=52)
        eq_intro.move_to(DOWN * 3.0)
        underline = Line(
            eq_intro.get_left()  + DOWN * 0.15,
            eq_intro.get_right() + DOWN * 0.15,
            color=PRIMARY, stroke_width=2,
        )
        self.play(Write(eq_intro), run_time=1.8)
        self.play(ShowCreation(underline), run_time=0.4)
        self.wait(1.38)
        _clear_all(self)


class S04MagnusEffect(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        magnus_title = T("The Magnus Effect.", color=PRIMARY, size=52)
        magnus_title.move_to(UP * 2.5)
        underline = Line(
            magnus_title.get_left()  + DOWN * 0.15,
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

        decide_text = T("It decides every", size=40)
        curve_text  = T("curve",            color=PRIMARY, size=48)
        in_football = T("in football.",     size=40)
        text_group  = VGroup(decide_text, curve_text, in_football).arrange(DOWN, buff=0.25)
        text_group.move_to(DOWN * 2.8)

        self.play(ShowCreation(curve_path), FadeIn(ball), run_time=1.0)
        self.play(Write(text_group), run_time=1.2)
        self.wait(0.42)
        _clear_all(self)


class S05Comparison(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        left_hdr  = T("Normal",  color=TEXT_DIM, size=34).move_to(LEFT  * 1.0 + UP * 3.5)
        right_hdr = T("Trivela", color=PRIMARY,  size=34).move_to(RIGHT * 1.0 + UP * 3.5)
        sep = DashedLine(UP * 3.8, DOWN * 4.5, color=TEXT_DIM, dash_length=0.1)

        normal_shot = T("Right foot shot.", size=24)
        normal_shot.move_to(LEFT * 1.0 + UP * 2.5)

        self.play(FadeIn(left_hdr), FadeIn(right_hdr), ShowCreation(sep), run_time=0.8)
        self.play(Write(normal_shot), run_time=0.9)
        self.wait(0.92)

        cw_spin = T("CW clockwise", color=HIGHLIGHT, size=24)
        cw_spin.move_to(LEFT * 1.0 + UP * 1.5)
        self.play(FadeIn(cw_spin, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.46)

        ball_r = T("ball", color=TEXT_C, size=24)
        arr_r  = Tex(r"ightarrow", color=TEXT_C, font_size=26)
        ball_right = VGroup(ball_r, arr_r).arrange(RIGHT, buff=0.1)
        ball_right.move_to(LEFT * 1.0 + UP * 0.5)
        self.play(FadeIn(ball_right, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.32)

        gk_reads = T("GK reads it.", color=ACCENT, size=24)
        gk_reads.move_to(LEFT * 1.0 + DOWN * 0.5)
        self.play(FadeIn(gk_reads), run_time=0.5)
        self.wait(0.22)

        easy = T("Easy.", color=TEXT_DIM, size=34)
        easy.move_to(LEFT * 1.0 + DOWN * 1.6)
        self.play(FadeIn(easy), run_time=0.15)
        self.wait(1.39)

        trivela_pop = T("Trivela.", color=PRIMARY, size=44)
        trivela_pop.move_to(RIGHT * 1.0 + UP * 2.5)
        self.play(FadeIn(trivela_pop, scale=0.7), run_time=0.4)
        self.wait(0.99)

        ccw_spin = T("CCW counter", color=PRIMARY, size=24)
        ccw_spin.move_to(RIGHT * 1.0 + UP * 1.5)
        self.play(FadeIn(ccw_spin, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.80)

        same_body = T("Same body.", color=SECONDARY, size=24)
        same_body.move_to(RIGHT * 1.0 + UP * 0.5)
        self.play(FadeIn(same_body), run_time=0.5)
        self.wait(0.62)

        arr_l  = Tex(r"\leftarrow", color=PRIMARY, font_size=26)
        ball_l = T("ball", color=PRIMARY, size=24)
        ball_left = VGroup(arr_l, ball_l).arrange(RIGHT, buff=0.1)
        ball_left.move_to(RIGHT * 1.0 + DOWN * 0.5)
        self.play(FadeIn(ball_left, shift=LEFT * 0.3), run_time=0.6)
        self.wait(1.58)
        _clear_all(self)


class S06Numbers(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

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

        deg_label     = Tex(r"70^\circ", color=SECONDARY, font_size=52)
        deg_label.move_to(center + RIGHT * 0.9 + UP * 0.5)
        off_axis      = T("off-axis",     color=PRIMARY,  size=40)
        off_axis.move_to(center + DOWN * 1.6)
        contact_label = T("contact point", color=TEXT_DIM, size=28)
        contact_label.move_to(center + UP * 2.5)

        self.play(ShowCreation(axis_line), run_time=0.5)
        self.play(ShowCreation(foot_line), run_time=0.6)
        self.play(ShowCreation(arc_angle), Write(deg_label), run_time=0.7)
        self.play(FadeIn(off_axis), FadeIn(contact_label), run_time=0.5)
        self.wait(2.08)

        big_10  = T("10",       color=SECONDARY, size=128)
        big_10.move_to(DOWN * 1.2)
        rev_s   = T("rev / s",  color=PRIMARY,   size=44)
        rev_s.next_to(big_10, DOWN, buff=0.25)
        roughly = T("roughly",  color=TEXT_DIM,  size=28)
        roughly.next_to(big_10, UP, buff=0.2)

        self.play(FadeIn(big_10, scale=0.6), run_time=0.7)
        self.play(FadeIn(rev_s), FadeIn(roughly), run_time=0.5)
        self.wait(2.21)

        double_txt   = T("Double",             color=HIGHLIGHT, size=52)
        standard_txt = T("the standard shot.", color=TEXT_C,    size=38)
        double_group = VGroup(double_txt, standard_txt).arrange(DOWN, buff=0.35)
        double_group.move_to(DOWN * 2.8)
        self.play(FadeIn(double_group), run_time=0.6)
        self.wait(1.62)

        gk_line = T("The goalkeeper",      color=TEXT_C,    size=38)
        never   = T("never had a chance.", color=HIGHLIGHT, size=38)
        gk_group = VGroup(gk_line, never).arrange(DOWN, buff=0.3)
        gk_group.move_to(UP * 3.2)
        self.play(FadeIn(gk_group, shift=DOWN * 0.3), run_time=0.8)
        self.wait(1.24)
        _clear_all(self)


class S07Conclusion(InteractiveScene):
    CONFIG = {"camera_config": {"pixel_width": 1080, "pixel_height": 1920, "fps": 60}}

    def construct(self):
        not_trick  = T("This isn't",    size=46)
        not_trick2 = T("a trick shot.", color=TEXT_DIM, size=46)
        t20 = VGroup(not_trick, not_trick2).arrange(DOWN, buff=0.3).move_to(UP * 2.5)
        self.play(Write(not_trick), run_time=0.8)
        self.play(Write(not_trick2), run_time=0.6)
        self.wait(1.14)

        physics_exp = T("It's a",           size=46)
        exploit     = T("physics exploit.", color=HIGHLIGHT, size=56)
        t21 = VGroup(physics_exp, exploit).arrange(DOWN, buff=0.25).move_to(ORIGIN)
        self.play(FadeIn(t21, shift=UP * 0.2), run_time=0.7)
        self.wait(1.74)

        baked  = T("baked into the", size=38)
        geom   = T("geometry",       color=PRIMARY, size=50)
        ofctct = T("of contact.",    size=38)
        t22 = VGroup(baked, geom, ofctct).arrange(DOWN, buff=0.25).move_to(DOWN * 1.8)
        self.play(Write(t22), run_time=1.5)
        self.wait(0.96)

        body_lies = T("The body lies.", color=TEXT_DIM, size=42)
        body_lies.move_to(UP * 3.5)
        self.play(FadeIn(body_lies, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(0.94)

        eq_dont = T("The equations don't.", color=SECONDARY, size=44)
        eq_dont.move_to(UP * 3.5 + DOWN * 1.0)

        cta_follow  = T("Follow for more",        color=TEXT_DIM, size=30)
        cta_physics = T("physics",                color=PRIMARY,  size=38)
        cta_suffix  = T("hiding in plain sight.", color=TEXT_DIM, size=30)
        cta = VGroup(cta_follow, cta_physics, cta_suffix).arrange(DOWN, buff=0.25)
        cta.move_to(DOWN * 3.0)

        self.play(FadeOut(body_lies, shift=LEFT * 0.3), FadeIn(eq_dont, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(cta, shift=UP * 0.3), run_time=0.7)
        self.wait(0.88)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
