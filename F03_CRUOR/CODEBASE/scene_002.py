"""
scene_002.py — F03_CRUOR
ANGRON Projet 002 — Trivela de Lamine — Magnus Effect
Format : SHORT 9:16 | 1080x1920 | 60fps | 68.32s audio
"""

from manim import *

BG        = "#171717"
PRIMARY   = "#58C4DD"
SECONDARY = "#FFF1B6"
ACCENT    = "#A6CF98"
TEXT_C    = "#ECEFF1"
TEXT_DIM  = "#90A4AE"
HIGHLIGHT = "#FF6D00"

config.frame_rate       = 60
config.pixel_width      = 1080
config.pixel_height     = 1920
config.background_color = BG


class AngronScene(Scene):

    def _clear(self):
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=0.15)

    def construct(self):
        self._bloc1()
        self._clear()
        self._bloc2()
        self._clear()
        self._bloc3()
        self._clear()
        self._bloc4()
        self._clear()
        self._bloc5()
        self._clear()
        self._bloc6()
        self._clear()
        self._bloc7()

    # -----------------------------------------------------------------------
    # BLOC 1 | [0.0 → 5.93s] | HOOK QUESTION
    # Bloc whisper 1 : "Why Lameen's Trivela..." (0.0–5.08s) + 0.85s trailing
    # -----------------------------------------------------------------------
    def _bloc1(self):
        line1 = Tex(r"Why Lamine's", color=TEXT_C, font_size=72)
        line2 = VGroup(
            Tex(r"trivela", color=PRIMARY, font_size=72),
            Tex(r"is more", color=TEXT_C, font_size=72),
        ).arrange(RIGHT, buff=0.15)
        line3 = Tex(r"spectacular", color=SECONDARY, font_size=72)
        line4 = Tex(r"than you think.", color=TEXT_DIM, font_size=56)

        group = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line3, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line4, shift=UP * 0.2), run_time=0.5)
        self.wait(3.43)

    # -----------------------------------------------------------------------
    # BLOC 2 | [5.93 → 12.47s]  duration 6.54s | FOOT + DIRECTION
    # Bloc 2 : "Kick with the outside..." (0.0–2.72s rel)
    # Bloc 3 : "You don't just change direction." (3.48–5.88s rel)
    # -----------------------------------------------------------------------
    def _bloc2(self):
        # SUB-BLOC 2 (rel 0.0-2.72s)
        t_kick1 = Tex(r"Kick with the", color=TEXT_C, font_size=60)
        t_kick2 = VGroup(
            Tex(r"outside", color=PRIMARY, font_size=60),
            Tex(r"of your foot.", color=TEXT_C, font_size=60),
        ).arrange(RIGHT, buff=0.15)
        kick_group = VGroup(t_kick1, t_kick2).arrange(DOWN, buff=0.3).move_to(UP * 1.8)

        foot = Ellipse(width=2.2, height=1.0, color=TEXT_DIM, stroke_width=2).move_to(DOWN * 1.5)
        outside_dot = Dot(foot.get_right() + LEFT * 0.1 + UP * 0.05, color=PRIMARY, radius=0.12)
        out_arrow = Arrow(
            outside_dot.get_center() + RIGHT * 0.2,
            outside_dot.get_center() + RIGHT * 1.2,
            color=PRIMARY, stroke_width=4, max_tip_length_to_length_ratio=0.25,
        )

        self.play(Write(kick_group), run_time=0.9)
        self.play(Create(foot), FadeIn(outside_dot), GrowArrow(out_arrow), run_time=0.7)
        self.wait(1.02)  # hold + 0.76s gap → t=3.48

        # SUB-BLOC 3 (rel 3.48-5.88s)
        t_dir1 = Tex(r"You don't just", color=TEXT_C, font_size=60)
        t_dir2 = Tex(r"change direction.", color=TEXT_DIM, font_size=60)
        dir_group = VGroup(t_dir1, t_dir2).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        dir_arrow = Arrow(
            LEFT * 1.8, RIGHT * 1.8, color=HIGHLIGHT,
            stroke_width=5, max_tip_length_to_length_ratio=0.15,
        ).move_to(DOWN * 2.0)

        self.play(
            FadeOut(VGroup(kick_group, foot, outside_dot, out_arrow), shift=UP * 0.3),
            FadeIn(dir_group, shift=UP * 0.3),
            run_time=0.4,
        )
        self.play(GrowArrow(dir_arrow), run_time=0.6)
        self.wait(1.6)  # hold to 5.88s + 0.66s trailing → 6.54s

    # -----------------------------------------------------------------------
    # BLOC 3 | [12.47 → 22.48s]  duration 10.01s | SPIN AXIS + EQUATION
    # Bloc 4 : "You flip the spin... F = ρ r v × ω" (0.0–9.18s rel)
    # -----------------------------------------------------------------------
    def _bloc3(self):
        # Part A: "You flip the spin axis." (rel 0.0–2.5s)
        flip1 = Tex(r"You flip the", color=TEXT_C, font_size=64)
        flip2 = Tex(r"spin axis.", color=PRIMARY, font_size=80)
        flip_g = VGroup(flip1, flip2).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        self.play(Write(flip1), run_time=0.6)
        self.play(Write(flip2), run_time=0.7)

        # Part B: two rotation symbols side by side (rel 1.3–4.0s)
        sep = DashedLine(UP * 1.5, DOWN * 0.8, color=TEXT_DIM, dash_length=0.12).move_to(ORIGIN)

        cw_sym   = Tex(r"$\circlearrowleft$", color=HIGHLIGHT, font_size=96).move_to(LEFT * 1.3 + DOWN * 0.3)
        cw_lbl   = Tex(r"Normal", color=TEXT_DIM, font_size=38).next_to(cw_sym, DOWN, buff=0.15)

        ccw_sym  = Tex(r"$\circlearrowright$", color=PRIMARY, font_size=96).move_to(RIGHT * 1.3 + DOWN * 0.3)
        ccw_lbl  = Tex(r"Trivela", color=PRIMARY, font_size=38).next_to(ccw_sym, DOWN, buff=0.15)

        self.play(
            Create(sep),
            FadeIn(cw_sym), FadeIn(cw_lbl),
            FadeIn(ccw_sym), FadeIn(ccw_lbl),
            run_time=0.9,
        )
        self.play(ccw_sym.animate.scale(1.25).set_color(SECONDARY), run_time=0.5)
        self.wait(0.5)

        # Part C: Magnus equation (rel 4.5–9.18s)
        eq = MathTex(
            r"F", r"=", r"\rho \cdot r \cdot v \times \omega",
            color=SECONDARY, font_size=72,
        ).move_to(DOWN * 3.0)
        underline = Line(
            eq.get_left() + DOWN * 0.12,
            eq.get_right() + DOWN * 0.12,
            color=PRIMARY, stroke_width=2,
        )

        self.play(Write(eq), run_time=1.6)
        self.play(Create(underline), run_time=0.3)
        self.wait(2.38)  # hold to 9.18s + 0.83s trailing → 10.01s

    # -----------------------------------------------------------------------
    # BLOC 4 | [22.48 → 27.92s]  duration 5.44s | MAGNUS EFFECT
    # Bloc 5 : "That's the Magnus Effect." (0.0–1.76s rel)
    # Bloc 6 : "It decides every curve in football." (2.44–5.02s rel)
    # -----------------------------------------------------------------------
    def _bloc4(self):
        # SUB-BLOC 5 (rel 0.0-1.76s)
        title = Tex(r"The Magnus Effect.", color=PRIMARY, font_size=68)
        title.move_to(UP * 2.5)
        underline = Line(
            title.get_left() + DOWN * 0.12,
            title.get_right() + DOWN * 0.12,
            color=PRIMARY, stroke_width=2,
        )
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.7)
        self.play(Create(underline), run_time=0.3)
        self.wait(0.68)  # gap to bloc 6 at 2.44s

        # SUB-BLOC 6 (rel 2.44-5.02s)
        ball = Circle(radius=0.35, color=TEXT_C, stroke_width=2, fill_opacity=0.2)
        ball.set_fill(TEXT_DIM)
        ball.move_to(LEFT * 1.5 + DOWN * 0.5)

        curve = ArcBetweenPoints(
            LEFT * 1.5 + DOWN * 0.5,
            RIGHT * 1.5 + DOWN * 1.8,
            angle=-TAU / 5,
        )
        curve.set_color(PRIMARY).set_stroke(width=3)

        decide  = Tex(r"It decides", color=TEXT_C, font_size=52)
        every   = Tex(r"every ", color=TEXT_C, font_size=52)
        curve_w = Tex(r"curve", color=PRIMARY, font_size=64)
        row     = VGroup(every, curve_w).arrange(RIGHT, buff=0.08)
        in_foot = Tex(r"in football.", color=TEXT_C, font_size=52)
        text_g  = VGroup(decide, row, in_foot).arrange(DOWN, buff=0.2).move_to(DOWN * 3.0)

        self.play(Create(curve), FadeIn(ball), run_time=0.8)
        self.play(Write(text_g), run_time=1.0)
        self.wait(0.42)  # trailing to 5.44s

    # -----------------------------------------------------------------------
    # BLOC 5 | [27.92 → 44.12s]  duration 16.20s | NORMAL vs TRIVELA
    # Blocs 7–15 — builds progressively on screen
    # -----------------------------------------------------------------------
    def _bloc5(self):
        # Setup: column headers + separator
        left_hdr  = Tex(r"Normal", color=TEXT_DIM, font_size=52).move_to(LEFT * 1.1 + UP * 3.5)
        right_hdr = Tex(r"Trivela", color=PRIMARY, font_size=52).move_to(RIGHT * 1.1 + UP * 3.5)
        sep = DashedLine(UP * 3.8, DOWN * 4.5, color=TEXT_DIM, dash_length=0.1)
        normal_shot = Tex(r"Right foot shot.", color=TEXT_C, font_size=40).move_to(LEFT * 1.1 + UP * 2.5)

        # Bloc 7 (rel 0.0–2.62s)
        self.play(FadeIn(left_hdr), FadeIn(right_hdr), Create(sep), run_time=0.5)
        self.play(Write(normal_shot), run_time=0.7)
        self.wait(2.04)  # to rel 3.24

        # Bloc 8 (rel 3.24–4.32s)
        cw_spin = Tex(r"$\circlearrowleft$  clockwise", color=HIGHLIGHT, font_size=44)
        cw_spin.move_to(LEFT * 1.1 + UP * 1.5)
        self.play(FadeIn(cw_spin, shift=LEFT * 0.2), run_time=0.5)
        self.wait(1.18)  # to rel 4.92

        # Bloc 9 (rel 4.92–5.74s)
        ball_right = Tex(r"ball $\rightarrow$", color=TEXT_C, font_size=44)
        ball_right.move_to(LEFT * 1.1 + UP * 0.5)
        self.play(FadeIn(ball_right, shift=RIGHT * 0.25), run_time=0.4)
        self.wait(1.18)  # to rel 6.50

        # Bloc 10 (rel 6.50–7.22s)
        gk_reads = Tex(r"GK reads it.", color=ACCENT, font_size=40)
        gk_reads.move_to(LEFT * 1.1 + DOWN * 0.5)
        self.play(FadeIn(gk_reads), run_time=0.4)
        self.wait(0.60)  # to rel 7.50

        # Bloc 11 (rel 7.50–7.76s) — "Easy." deadpan
        easy = Tex(r"Easy.", color=TEXT_DIM, font_size=48)
        easy.move_to(LEFT * 1.1 + DOWN * 1.6)
        self.play(FadeIn(easy), run_time=0.15)
        self.wait(1.44)  # to rel 9.09

        # Bloc 12 (rel 9.09–9.55s) — "Trivela." big pop on right
        trivela_pop = Tex(r"Trivela.", color=PRIMARY, font_size=72)
        trivela_pop.move_to(RIGHT * 1.1 + UP * 2.5)
        self.play(FadeIn(trivela_pop, scale=0.7), run_time=0.3)
        self.wait(1.15)  # to rel 10.54

        # Bloc 13 (rel 10.54–11.94s)
        ccw_spin = Tex(r"$\circlearrowright$  counter-CW", color=PRIMARY, font_size=44)
        ccw_spin.move_to(RIGHT * 1.1 + UP * 1.5)
        self.play(FadeIn(ccw_spin, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.34)  # to rel 12.48

        # Bloc 14 (rel 12.48–13.28s)
        same_body = Tex(r"Same body.", color=SECONDARY, font_size=40)
        same_body.move_to(RIGHT * 1.1 + UP * 0.5)
        self.play(FadeIn(same_body), run_time=0.4)
        self.wait(1.02)  # to rel 13.90

        # Bloc 15 (rel 13.90–15.02s)
        ball_left = Tex(r"$\leftarrow$ ball", color=PRIMARY, font_size=44)
        ball_left.move_to(RIGHT * 1.1 + DOWN * 0.5)
        self.play(FadeIn(ball_left, shift=LEFT * 0.25), run_time=0.5)
        self.wait(1.80)  # to rel 16.20

    # -----------------------------------------------------------------------
    # BLOC 6 | [44.12 → 56.94s]  duration 12.82s | NUMBERS
    # Bloc 16 : "70 degrees off axis" (0.0–4.40s rel)
    # Bloc 17 : "10 revolutions per second" (4.72–7.68s rel)
    # Bloc 18 : "Double the standard shot." (8.00–9.88s rel)
    # Bloc 19 : "The goalkeeper never had a chance." (10.70–12.82s rel)
    # -----------------------------------------------------------------------
    def _bloc6(self):
        center = UP * 1.2

        # BLOC 16 — 70° diagram (rel 0.0–4.40s)
        axis_line = Line(center + LEFT * 2.0, center + RIGHT * 2.0,
                         color=TEXT_DIM, stroke_width=2)
        foot_vec = np.array([np.cos(np.radians(70)), np.sin(np.radians(70)), 0])
        foot_line = Line(center, center + 2.0 * foot_vec,
                         color=PRIMARY, stroke_width=4)
        arc_70 = Arc(radius=0.65, start_angle=0, angle=np.radians(70),
                     color=SECONDARY, stroke_width=2, arc_center=center)
        deg_label = MathTex(r"70^\circ", color=SECONDARY, font_size=64)
        deg_label.move_to(center + RIGHT * 1.0 + UP * 0.55)
        off_axis = Tex(r"off-axis", color=PRIMARY, font_size=52).move_to(center + DOWN * 1.6)
        contact  = Tex(r"contact point", color=TEXT_DIM, font_size=36).move_to(center + UP * 2.4)

        self.play(Create(axis_line), run_time=0.4)
        self.play(Create(foot_line), run_time=0.5)
        self.play(Create(arc_70), Write(deg_label), run_time=0.6)
        self.play(FadeIn(off_axis), FadeIn(contact), run_time=0.4)
        self.wait(2.82)  # hold to 4.40s + gap to 4.72s → 2.22 + 0.32 gap

        # BLOC 17 — big "10" (rel 4.72–7.68s)
        self.play(FadeOut(VGroup(axis_line, foot_line, arc_70, deg_label, off_axis, contact)), run_time=0.2)

        big_10  = Tex(r"10", color=SECONDARY, font_size=160).move_to(DOWN * 1.0)
        rev_s   = Tex(r"rev / s", color=PRIMARY, font_size=64).next_to(big_10, DOWN, buff=0.15)
        roughly = Tex(r"roughly", color=TEXT_DIM, font_size=38).next_to(big_10, UP, buff=0.15)

        self.play(FadeIn(big_10, scale=0.6), run_time=0.6)
        self.play(FadeIn(rev_s), FadeIn(roughly), run_time=0.4)
        self.wait(2.24)  # to rel 8.00

        # BLOC 18 — "Double the standard shot." (rel 8.00–9.88s)
        self.play(FadeOut(VGroup(big_10, rev_s, roughly)), run_time=0.2)

        double_w = Tex(r"Double", color=HIGHLIGHT, font_size=80).move_to(UP * 0.5)
        standard = Tex(r"the standard shot.", color=TEXT_C, font_size=52).move_to(DOWN * 0.5)

        self.play(FadeIn(double_w, scale=0.8), run_time=0.5)
        self.play(FadeIn(standard), run_time=0.4)
        self.wait(0.98)  # to rel 9.88 + gap to 10.70

        # BLOC 19 — "The goalkeeper never had a chance." (rel 10.70–12.82s)
        self.play(FadeOut(VGroup(double_w, standard)), run_time=0.2)

        gk_l1 = Tex(r"The goalkeeper", color=TEXT_C, font_size=56)
        gk_l2 = Tex(r"never had a chance.", color=HIGHLIGHT, font_size=52)
        gk_g  = VGroup(gk_l1, gk_l2).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(gk_g, shift=DOWN * 0.3), run_time=0.7)
        self.wait(1.12)  # to 12.82s

    # -----------------------------------------------------------------------
    # BLOC 7 | [56.94 → 68.32s]  duration 11.38s | CONCLUSION + CTA
    # Bloc 20 : "This isn't a trick shot." (0.0–2.54s rel)
    # Bloc 21 : "It's a physics exploit." (3.04–4.20s rel)
    # Bloc 22 : "baked into the geometry of contact." (5.32–7.36s rel)
    # Bloc 23 : "The body lies." (8.26–9.32s rel)
    # Bloc 24 : "The equations don't." (9.84–11.38s rel)
    # -----------------------------------------------------------------------
    def _bloc7(self):
        # BLOC 20 (rel 0.0–2.54s)
        t20_1 = Tex(r"This isn't", color=TEXT_C, font_size=60)
        t20_2 = Tex(r"a trick shot.", color=TEXT_DIM, font_size=60)
        t20 = VGroup(t20_1, t20_2).arrange(DOWN, buff=0.25).move_to(UP * 2.5)

        self.play(Write(t20_1), run_time=0.7)
        self.play(Write(t20_2), run_time=0.6)
        self.wait(1.74)  # to 2.54s + gap to 3.04s

        # BLOC 21 (rel 3.04–4.20s)
        physics  = Tex(r"It's a", color=TEXT_C, font_size=60)
        exploit  = Tex(r"physics exploit.", color=HIGHLIGHT, font_size=72)
        t21 = VGroup(physics, exploit).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeIn(t21, shift=UP * 0.2), run_time=0.6)
        self.wait(1.62)  # to 4.20s + gap to 5.32s

        # BLOC 22 (rel 5.32–7.36s)
        baked   = Tex(r"baked into the", color=TEXT_C, font_size=52)
        geom    = Tex(r"geometry", color=PRIMARY, font_size=64)
        ofctct  = Tex(r"of contact.", color=TEXT_C, font_size=52)
        t22 = VGroup(baked, geom, ofctct).arrange(DOWN, buff=0.2).move_to(DOWN * 1.8)

        self.play(Write(t22), run_time=1.4)
        self.wait(1.56)  # to 7.36s + gap to 8.26s

        # BLOC 23 (rel 8.26–9.32s)
        body_lies = Tex(r"The body lies.", color=TEXT_DIM, font_size=56)
        body_lies.move_to(UP * 3.5)
        self.play(FadeIn(body_lies, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(1.06)  # to 9.32s + gap to 9.84s

        # BLOC 24 (rel 9.84–11.38s)
        eq_dont = Tex(r"The equations don't.", color=SECONDARY, font_size=64)
        eq_dont.move_to(UP * 2.5)

        cta1 = Tex(r"Follow for more", color=TEXT_DIM, font_size=40)
        cta2 = Tex(r"physics", color=PRIMARY, font_size=48)
        cta3 = Tex(r"hiding in plain sight.", color=TEXT_DIM, font_size=40)
        cta  = VGroup(cta1, cta2, cta3).arrange(DOWN, buff=0.2).move_to(DOWN * 3.0)

        self.play(FadeOut(body_lies, shift=LEFT * 0.3), FadeIn(eq_dont, shift=UP * 0.3), run_time=0.4)
        self.play(FadeIn(cta, shift=UP * 0.3), run_time=0.6)
        self.wait(0.88)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.5)
