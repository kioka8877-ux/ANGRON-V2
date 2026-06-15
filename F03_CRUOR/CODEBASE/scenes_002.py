"""
scenes_002.py — F03_CRUOR
ANGRON Projet 002 — Trivela de Lamine — Magnus Effect
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
# Bloc 1: "Why Lameen's Trivela is more spectacular than you think." (0.0–5.08s)
# ═══════════════════════════════════════════════════════════════════════════════
class S01HookQuestion(InteractiveScene):
    def construct(self):
        # Line 1
        line1 = Tex(r"Why Lamine's", color=TEXT_C, font_size=72)
        # Line 2 — keyword highlighted
        line2a = Tex(r"trivela", color=PRIMARY, font_size=72)
        line2b = Tex(r" is more", color=TEXT_C, font_size=72)
        line2  = VGroup(line2a, line2b).arrange(RIGHT, buff=0.05)
        # Line 3
        line3 = Tex(r"spectacular", color=SECONDARY, font_size=72)
        # Line 4
        line4 = Tex(r"than you think.", color=TEXT_DIM, font_size=56)

        group = VGroup(line1, line2, line3, line4).arrange(DOWN, buff=0.35)
        group.move_to(ORIGIN)

        # Staggered reveal: 0.0s → ~3.5s
        self.play(FadeIn(line1, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(line2, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line3, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(line4, shift=UP * 0.2), run_time=0.5)
        # Hold through end of bloc (5.08s) + trailing (5.93s)
        self.wait(3.28)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S02 — FOOT + DIRECTION  [5.93 → 12.47s]  duration 6.54s
# Bloc 2: "Kick with the outside of your foot." (0.0–2.72s relative)
# Bloc 3: "You don't just change direction."    (3.48–5.88s relative)
# ═══════════════════════════════════════════════════════════════════════════════
class S02FootKick(InteractiveScene):
    def construct(self):
        # BLOC 2 ──────────────────────────────────────────────────────────────
        t2a = Tex(r"Kick with the", color=TEXT_C, font_size=60)
        t2b = Tex(r"outside", color=PRIMARY, font_size=60)
        t2c = Tex(r"of your foot.", color=TEXT_C, font_size=60)
        b2  = VGroup(t2a, t2b, t2c).arrange(DOWN, buff=0.25).move_to(UP * 1.5)

        # Simple foot diagram: oval body + outside edge highlighted
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
        # Hold to 2.72s, then gap 0.76s
        self.wait(0.62)

        # BLOC 3 ──────────────────────────────────────────────────────────────
        # Transition: fade out foot, keep context
        self.play(FadeOut(foot_group), run_time=0.3)

        t3a = Tex(r"You don't just", color=TEXT_C, font_size=60)
        t3b = Tex(r"change", color=TEXT_DIM, font_size=60)
        t3c = Tex(r"direction.", color=TEXT_C, font_size=60)
        b3  = VGroup(t3a, t3b, t3c).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        # Arrow showing direction
        arrow_dir = Arrow(LEFT * 1.5, RIGHT * 1.5, color=HIGHLIGHT,
                          stroke_width=5, max_tip_length_to_length_ratio=0.18)
        arrow_dir.move_to(DOWN * 2.0)

        self.play(
            FadeOut(b2, shift=UP * 0.3),
            FadeIn(b3, shift=UP * 0.3),
            run_time=0.5,
        )
        self.play(GrowArrow(arrow_dir), run_time=0.7)
        # Hold through 5.88s + trailing to 6.54s
        self.wait(1.32)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S03 — SPIN AXIS FLIP + EQUATION  [12.47 → 22.48s]  duration 10.01s
# Bloc 4: "You flip the spin ... F = ρ r v × ω" (0.0–9.18s relative)
# ═══════════════════════════════════════════════════════════════════════════════
class S03SpinAxis(InteractiveScene):
    def construct(self):
        # Part A: "You flip the spin axis." [0-2.5s]
        flip_line1 = Tex(r"You flip the", color=TEXT_C, font_size=64)
        flip_line2 = Tex(r"spin axis.", color=PRIMARY, font_size=80)
        flip_group = VGroup(flip_line1, flip_line2).arrange(DOWN, buff=0.3)
        flip_group.move_to(UP * 2.8)

        self.play(Write(flip_line1), run_time=0.7)
        self.play(Write(flip_line2), run_time=0.8)

        # Part B: Two spin arrows (clockwise vs counter-clockwise) [2.5-5.5s]
        # Left: clockwise (normal shot)
        cw_label  = Tex(r"Normal", color=TEXT_DIM, font_size=36).move_to(LEFT * 1.4 + DOWN * 0.3)
        cw_arrow  = Arc(radius=0.7, start_angle=PI * 0.5, angle=-PI * 1.6,
                        color=HIGHLIGHT, stroke_width=4)
        cw_arrow.move_to(LEFT * 1.4 + DOWN * 1.4)
        cw_tip_text = Tex(r"$\circlearrowleft$", color=HIGHLIGHT, font_size=60)
        cw_tip_text.move_to(LEFT * 1.4 + DOWN * 1.4)

        # Right: counter-clockwise (trivela)
        ccw_label = Tex(r"Trivela", color=PRIMARY, font_size=36).move_to(RIGHT * 1.4 + DOWN * 0.3)
        ccw_tip_text = Tex(r"$\circlearrowright$", color=PRIMARY, font_size=60)
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

        # Highlight the trivela side
        self.play(
            ccw_tip_text.animate.scale(1.3).set_color(SECONDARY),
            run_time=0.5,
        )
        self.wait(0.5)

        # Part C: Magnus equation builds [5.5-9.18s]
        eq_intro = Tex(r"$F = \rho \cdot r \cdot v \times \omega$",
                       color=SECONDARY, font_size=72)
        eq_intro.move_to(DOWN * 3.2)

        underline = Line(
            eq_intro.get_left() + DOWN * 0.15,
            eq_intro.get_right() + DOWN * 0.15,
            color=PRIMARY, stroke_width=2,
        )

        self.play(Write(eq_intro), run_time=1.8)
        self.play(ShowCreation(underline), run_time=0.4)
        # Hold to 9.18s then trailing 0.83s
        self.wait(1.38)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S04 — MAGNUS EFFECT  [22.48 → 27.92s]  duration 5.44s
# Bloc 5: "That's the Magnus Effect." (0.0–1.76s)
# Bloc 6: "It decides every curve in football." (2.44–5.02s)
# ═══════════════════════════════════════════════════════════════════════════════
class S04MagnusEffect(InteractiveScene):
    def construct(self):
        # BLOC 5: Magnus Effect title ─────────────────────────────────────────
        magnus_title = Tex(r"The Magnus Effect.", color=PRIMARY, font_size=72)
        magnus_title.move_to(UP * 2.5)
        underline = Line(
            magnus_title.get_left() + DOWN * 0.15,
            magnus_title.get_right() + DOWN * 0.15,
            color=PRIMARY, stroke_width=2,
        )

        self.play(FadeIn(magnus_title, shift=UP * 0.3), run_time=0.8)
        self.play(ShowCreation(underline), run_time=0.3)
        self.wait(0.66)  # gap to bloc 6

        # BLOC 6: Ball curving diagram ─────────────────────────────────────────
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
        # Hold through 5.02s + trailing to 5.44s
        self.wait(0.42)
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S05 — NORMAL vs TRIVELA COMPARISON  [27.92 → 44.12s]  duration 16.20s
# Blocs 7–15 — rapid-fire comparison
# ═══════════════════════════════════════════════════════════════════════════════
class S05Comparison(InteractiveScene):
    def construct(self):
        # Column headers
        left_hdr  = Tex(r"Normal", color=TEXT_DIM, font_size=52).move_to(LEFT * 1.1 + UP * 3.5)
        right_hdr = Tex(r"Trivela", color=PRIMARY, font_size=52).move_to(RIGHT * 1.1 + UP * 3.5)
        sep = DashedLine(UP * 3.8, DOWN * 4.5, color=TEXT_DIM, dash_length=0.1)

        # BLOC 7: "Normal right foot shot." [0–2.62s] ─────────────────────────
        normal_shot = Tex(r"Right foot shot.", color=TEXT_C, font_size=40)
        normal_shot.move_to(LEFT * 1.1 + UP * 2.5)

        self.play(
            FadeIn(left_hdr), FadeIn(right_hdr), ShowCreation(sep),
            run_time=0.8,
        )
        self.play(Write(normal_shot), run_time=0.9)
        self.wait(0.92)  # hold + gap 0.62s to bloc 8

        # BLOC 8: "Clockwise spin." [3.24–4.32s] ─────────────────────────────
        cw_spin = Tex(r"$\circlearrowleft$ clockwise", color=HIGHLIGHT, font_size=44)
        cw_spin.move_to(LEFT * 1.1 + UP * 1.5)

        self.play(FadeIn(cw_spin, shift=LEFT * 0.2), run_time=0.6)
        self.wait(0.46)  # gap to bloc 9 (0.60s)

        # BLOC 9: "Ball goes right." [4.92–5.74s] ─────────────────────────────
        ball_right = Tex(r"ball $\rightarrow$", color=TEXT_C, font_size=44)
        ball_right.move_to(LEFT * 1.1 + UP * 0.5)

        self.play(FadeIn(ball_right, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(0.32)  # gap to bloc 10

        # BLOC 10: "Goalkeeper reads it." [6.50–7.22s] ────────────────────────
        gk_reads = Tex(r"GK reads it.", color=ACCENT, font_size=40)
        gk_reads.move_to(LEFT * 1.1 + DOWN * 0.5)

        self.play(FadeIn(gk_reads), run_time=0.5)
        self.wait(0.22)  # gap to bloc 11

        # BLOC 11: "Easy." [7.50–7.76s] — deadpan ────────────────────────────
        easy = Tex(r"Easy.", color=TEXT_DIM, font_size=56)
        easy.move_to(LEFT * 1.1 + DOWN * 1.6)

        self.play(FadeIn(easy), run_time=0.15)
        self.wait(1.39)  # gap 1.33s to bloc 12

        # BLOC 12: "Trivela." [9.09–9.55s] ────────────────────────────────────
        trivela_pop = Tex(r"Trivela.", color=PRIMARY, font_size=72)
        trivela_pop.move_to(RIGHT * 1.1 + UP * 2.5)

        self.play(FadeIn(trivela_pop, scale=0.7), run_time=0.4)
        self.wait(0.99)  # gap to bloc 13

        # BLOC 13: "Counterclockwise spin." [10.54–11.94s] ────────────────────
        ccw_spin = Tex(r"$\circlearrowright$ counter-CW", color=PRIMARY, font_size=44)
        ccw_spin.move_to(RIGHT * 1.1 + UP * 1.5)

        self.play(FadeIn(ccw_spin, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.80)  # gap to bloc 14

        # BLOC 14: "Same body position." [12.48–13.28s] ───────────────────────
        same_body = Tex(r"Same body.", color=SECONDARY, font_size=40)
        same_body.move_to(RIGHT * 1.1 + UP * 0.5)

        self.play(FadeIn(same_body), run_time=0.5)
        self.wait(0.62)  # gap to bloc 15

        # BLOC 15: "Ball goes left." [13.90–15.02s] ───────────────────────────
        ball_left = Tex(r"$\leftarrow$ ball", color=PRIMARY, font_size=44)
        ball_left.move_to(RIGHT * 1.1 + DOWN * 0.5)

        self.play(FadeIn(ball_left, shift=LEFT * 0.3), run_time=0.6)
        self.wait(1.58)  # trailing to 16.20s
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S06 — NUMBERS : 70° + 10 REV/S  [44.12 → 56.94s]  duration 12.82s
# Bloc 16: "70 degrees off axis" (0.0–4.40s)
# Bloc 17: "10 revolutions per second" (4.72–7.68s)
# Bloc 18: "Double the standard shot." (8.00–9.88s)
# Bloc 19: "The goalkeeper never had a chance." (10.70–12.82s)
# ═══════════════════════════════════════════════════════════════════════════════
class S06Numbers(InteractiveScene):
    def construct(self):
        # BLOC 16: 70° off-axis diagram ────────────────────────────────────────
        # Central point, axis line, foot line at 70°
        center = ORIGIN + UP * 1.2
        axis_line = Line(center + LEFT * 2.0, center + RIGHT * 2.0,
                         color=TEXT_DIM, stroke_width=2)
        foot_line = Line(center, center + 2.0 * np.array([
            np.cos(np.radians(70)), np.sin(np.radians(70)), 0
        ]), color=PRIMARY, stroke_width=4)

        arc_angle = Arc(radius=0.6, start_angle=0, angle=np.radians(70),
                        color=SECONDARY, stroke_width=2)
        arc_angle.move_to(center)

        deg_label = Tex(r"$70^\circ$", color=SECONDARY, font_size=64)
        deg_label.move_to(center + RIGHT * 0.9 + UP * 0.5)

        off_axis = Tex(r"off-axis", color=PRIMARY, font_size=52)
        off_axis.move_to(center + DOWN * 1.6)

        contact_label = Tex(r"contact point", color=TEXT_DIM, font_size=36)
        contact_label.move_to(center + UP * 2.5)

        self.play(ShowCreation(axis_line), run_time=0.5)
        self.play(ShowCreation(foot_line), run_time=0.6)
        self.play(ShowCreation(arc_angle), Write(deg_label), run_time=0.7)
        self.play(FadeIn(off_axis), FadeIn(contact_label), run_time=0.5)
        # Hold to 4.40s + gap 0.32s
        self.wait(2.08)

        # BLOC 17: 10 rev/s big number ─────────────────────────────────────────
        big_10 = Tex(r"10", color=SECONDARY, font_size=160)
        big_10.move_to(DOWN * 1.2)
        rev_s  = Tex(r"rev / s", color=PRIMARY, font_size=64)
        rev_s.next_to(big_10, DOWN, buff=0.2)
        roughly = Tex(r"roughly", color=TEXT_DIM, font_size=36)
        roughly.next_to(big_10, UP, buff=0.2)

        self.play(FadeIn(big_10, scale=0.6), run_time=0.7)
        self.play(FadeIn(rev_s), FadeIn(roughly), run_time=0.5)
        # Hold to 7.68s + gap 0.32s
        self.wait(2.21)

        # BLOC 18: "Double the standard shot." ─────────────────────────────────
        double_txt = Tex(r"Double", color=HIGHLIGHT, font_size=72)
        standard_txt = Tex(r"the standard shot.", color=TEXT_C, font_size=52)
        double_group = VGroup(double_txt, standard_txt).arrange(DOWN, buff=0.3)
        double_group.move_to(DOWN * 2.8)

        self.play(FadeIn(double_group), run_time=0.6)
        # Hold to 9.88s + gap 0.82s
        self.wait(1.62)

        # BLOC 19: "The goalkeeper never had a chance." ─────────────────────────
        gk_line = Tex(r"The goalkeeper", color=TEXT_C, font_size=52)
        never   = Tex(r"never had a chance.", color=HIGHLIGHT, font_size=52)
        gk_group = VGroup(gk_line, never).arrange(DOWN, buff=0.25)
        gk_group.move_to(UP * 3.2)

        self.play(FadeIn(gk_group, shift=DOWN * 0.3), run_time=0.8)
        self.wait(1.24)  # hold to 12.82s
        _clear_all(self)


# ═══════════════════════════════════════════════════════════════════════════════
# S07 — CONCLUSION + CTA  [56.94 → 68.32s]  duration 11.38s
# Bloc 20: "This isn't a trick shot." (0.0–2.54s)
# Bloc 21: "It's a physics exploit." (3.04–4.20s)
# Bloc 22: "baked into the geometry of contact." (5.32–7.36s)
# Bloc 23: "The body lies." (8.26–9.32s)
# Bloc 24: "The equations don't." (9.84–11.38s) + CTA
# ═══════════════════════════════════════════════════════════════════════════════
class S07Conclusion(InteractiveScene):
    def construct(self):
        # BLOC 20: "This isn't a trick shot." ──────────────────────────────────
        not_trick = Tex(r"This isn't", color=TEXT_C, font_size=60)
        not_trick2 = Tex(r"a trick shot.", color=TEXT_DIM, font_size=60)
        t20 = VGroup(not_trick, not_trick2).arrange(DOWN, buff=0.25).move_to(UP * 2.5)

        self.play(Write(not_trick), run_time=0.8)
        self.play(Write(not_trick2), run_time=0.6)
        # Hold to 2.54s + gap 0.50s
        self.wait(1.14)

        # BLOC 21: "It's a physics exploit." ───────────────────────────────────
        physics_exp = Tex(r"It's a", color=TEXT_C, font_size=60)
        exploit     = Tex(r"physics exploit.", color=HIGHLIGHT, font_size=72)
        t21 = VGroup(physics_exp, exploit).arrange(DOWN, buff=0.2).move_to(ORIGIN)

        self.play(FadeIn(t21, shift=UP * 0.2), run_time=0.7)
        # Hold to 4.20s + gap 1.12s
        self.wait(1.74)

        # BLOC 22: "baked into the geometry of contact." ────────────────────────
        baked  = Tex(r"baked into the", color=TEXT_C, font_size=52)
        geom   = Tex(r"geometry", color=PRIMARY, font_size=64)
        ofctct = Tex(r"of contact.", color=TEXT_C, font_size=52)
        t22 = VGroup(baked, geom, ofctct).arrange(DOWN, buff=0.2).move_to(DOWN * 1.8)

        self.play(Write(t22), run_time=1.5)
        # Hold to 7.36s + gap 0.90s
        self.wait(0.96)

        # BLOC 23: "The body lies." ─────────────────────────────────────────────
        body_lies = Tex(r"The body lies.", color=TEXT_DIM, font_size=56)
        body_lies.move_to(UP * 3.5)

        self.play(FadeIn(body_lies, shift=RIGHT * 0.3), run_time=0.6)
        # Hold to 9.32s + gap 0.52s
        self.wait(0.94)

        # BLOC 24: "The equations don't." + CTA ────────────────────────────────
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
