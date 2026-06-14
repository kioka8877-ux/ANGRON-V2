"""
scene_001.py — F03_CRUOR
ANGRON Projet 001 — Boxe : le mythe des géants
Format : SHORT 9:16 | 1080x1920 | 60fps | 49.37s
Généré par CRUOR depuis prompt_001.md
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
        self._clear()
        self._bloc8()
        self._clear()
        self._bloc9()
        self._clear()
        self._bloc10()
        self._clear()
        self._bloc11()
        self._clear()
        self._bloc12()
        self._clear()
        self._bloc13()
        self._clear()
        self._bloc14()

    # -----------------------------------------------------------------------
    # BLOC 1 | [0.0s → 4.359s] | ACCROCHE
    # -----------------------------------------------------------------------
    def _bloc1(self):
        gauche_geant = Rectangle(width=2, height=6, color=PRIMARY, fill_opacity=0.2).move_to(LEFT * 2.5)
        droite_petit = Rectangle(width=2, height=3.5, color=ACCENT, fill_opacity=0.2).move_to(RIGHT * 2.5 + DOWN * 1.25)
        separateur   = DashedLine(UP * 4, DOWN * 4, color=TEXT_DIM)
        texte        = Tex(r"G\'eant vs Petit", color=TEXT_C, font_size=48).move_to(UP * 5)

        self.play(
            FadeIn(gauche_geant),
            FadeIn(droite_petit),
            Create(separateur),
            Write(texte),
            run_time=1.5,
        )
        self.wait(2.859)

    # -----------------------------------------------------------------------
    # BLOC 2 | [4.659s → 8.225s] | SUSPENSE
    # -----------------------------------------------------------------------
    def _bloc2(self):
        line1 = Tex(r"Les longs bras", color=TEXT_C, font_size=52)
        line2 = Tex(r"frappent-ils plus fort ?", color=TEXT_C, font_size=52)
        question = VGroup(line1, line2).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(AddTextLetterByLetter(line1, time_per_char=0.05), run_time=0.65)
        self.play(AddTextLetterByLetter(line2, time_per_char=0.05), run_time=0.85)
        self.wait(2.066)

    # -----------------------------------------------------------------------
    # BLOC 3 | [8.525s → 10.11s] | CONTRE-PIED
    # -----------------------------------------------------------------------
    def _bloc3(self):
        reponse = Tex(
            r"La physique dit \textbf{l'inverse}.",
            color=HIGHLIGHT, font_size=64,
        ).move_to(ORIGIN)
        cover = Rectangle(
            width=12, height=3,
            fill_color=BG, fill_opacity=1, stroke_width=0,
        ).move_to(ORIGIN)

        self.add(reponse, cover)
        self.play(FadeOut(cover, shift=RIGHT * 7), run_time=0.6)
        self.wait(0.985)

    # -----------------------------------------------------------------------
    # BLOC 4 | [10.41s → 13.58s] | TENSION
    # -----------------------------------------------------------------------
    def _bloc4(self):
        titre = Tex(r"PI\`EGE BIOM\'ECANIQUE", color=PRIMARY, font_size=72)
        titre.scale(0.4)
        self.play(titre.animate.scale(2.5), run_time=0.6, rate_func=rush_into)
        self.wait(2.57)

    # -----------------------------------------------------------------------
    # BLOC 5 | [13.88s → 18.239s] | ARGUMENT
    # -----------------------------------------------------------------------
    def _bloc5(self):
        line1   = Tex(r"Plus le bras est long,", color=TEXT_C, font_size=46)
        line2a  = Tex(r"plus il est ", color=TEXT_C, font_size=46)
        mot_dur = Tex(r"dur", color=TEXT_C, font_size=46)
        line2b  = Tex(r" \`a lancer.", color=TEXT_C, font_size=46)
        row2    = VGroup(line2a, mot_dur, line2b).arrange(RIGHT, buff=0.05)
        phrase  = VGroup(line1, row2).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(Write(phrase), run_time=1.5)
        self.play(mot_dur.animate.set_color(HIGHLIGHT).scale(1.3), run_time=0.4)
        self.wait(2.459)

    # -----------------------------------------------------------------------
    # BLOC 6 | [18.539s → 20.124s] | MOMENT D'INERTIE
    # -----------------------------------------------------------------------
    def _bloc6(self):
        pivot      = Dot(ORIGIN, color=TEXT_C)
        bras_long  = Line(ORIGIN, RIGHT * 3.5, color=PRIMARY, stroke_width=12)
        bras_court = Line(ORIGIN, RIGHT * 2,   color=ACCENT,  stroke_width=12)

        self.add(pivot, bras_long, bras_court)
        self.play(Rotate(bras_long,  angle=PI / 2, about_point=ORIGIN), run_time=0.5, rate_func=linear)
        self.play(Rotate(bras_court, angle=PI / 2, about_point=ORIGIN), run_time=0.2, rate_func=rush_into)
        self.wait(0.885)

    # -----------------------------------------------------------------------
    # BLOC 7 | [20.424s → 23.594s] | LEVIER COMPACT
    # -----------------------------------------------------------------------
    def _bloc7(self):
        epaule     = Dot(LEFT * 2,          color=TEXT_C)
        coude      = Dot(ORIGIN,            color=TEXT_C)
        poing      = Dot(RIGHT * 2 + UP * 2, color=ACCENT, radius=0.15)
        biceps     = Line(epaule.get_center(), coude.get_center(), stroke_width=10, color=SECONDARY)
        avant_bras = Line(coude.get_center(), poing.get_center(),  stroke_width=10, color=SECONDARY)
        bras       = VGroup(epaule, coude, poing, biceps, avant_bras).move_to(ORIGIN)

        self.play(Create(bras), run_time=1.0)
        self.play(bras.animate.stretch(0.5, dim=0), run_time=0.5)
        self.wait(1.67)

    # -----------------------------------------------------------------------
    # BLOC 8 | [23.894s → 27.064s] | ACCÉLÉRATION
    # -----------------------------------------------------------------------
    def _bloc8(self):
        poing_cible = Dot(LEFT * 3, color=TEXT_C, radius=0.2)
        vecteur     = Arrow(
            LEFT * 3, RIGHT * 3, color=HIGHLIGHT, buff=0.1,
            max_tip_length_to_length_ratio=0.15, stroke_width=8,
        )

        self.play(FadeIn(poing_cible), run_time=0.5)
        self.play(GrowArrow(vecteur), run_time=0.8)
        self.wait(1.87)

    # -----------------------------------------------------------------------
    # BLOC 9 | [27.364s → 30.138s] | ÉQUATION
    # -----------------------------------------------------------------------
    def _bloc9(self):
        eq = MathTex(
            r"E", r"=", r"\frac{1}{2}", r"m", r"v", r"^2",
            color=SECONDARY, font_size=80,
        ).move_to(ORIGIN)

        self.play(Write(eq), run_time=1.5)
        self.play(eq[5].animate.set_color(HIGHLIGHT).scale(1.8), run_time=0.4)
        self.wait(0.874)

    # -----------------------------------------------------------------------
    # BLOC 10 | [30.438s → 34.797s] | IMPACT
    # -----------------------------------------------------------------------
    def _bloc10(self):
        t1       = Tex(r"Elle compte ", color=TEXT_C, font_size=52)
        t_double = Tex(r"double",       color=TEXT_C, font_size=52)
        t2       = Tex(r" dans le ",    color=TEXT_C, font_size=52)
        t_ko     = Tex(r"KO.",          color=TEXT_C, font_size=52)
        texte_ko = VGroup(t1, t_double, t2, t_ko).arrange(RIGHT, buff=0.05).move_to(ORIGIN)

        self.play(Write(texte_ko), run_time=1.5)
        self.play(
            t_double.animate.set_color(HIGHLIGHT).scale(1.2),
            t_ko.animate.set_color(PRIMARY).scale(1.2),
            run_time=0.4,
        )
        self.wait(2.459)

    # -----------------------------------------------------------------------
    # BLOC 11 | [35.097s → 37.078s] | DÉTAIL
    # -----------------------------------------------------------------------
    def _bloc11(self):
        detail = Tex(r"Le d\'etail qui tue ?", color=TEXT_DIM, font_size=60).move_to(ORIGIN)
        self.play(AddTextLetterByLetter(detail, time_per_char=0.06), run_time=1.0)
        self.wait(0.981)

    # -----------------------------------------------------------------------
    # BLOC 12 | [37.378s → 41.737s] | CENTRE DE GRAVITÉ
    # -----------------------------------------------------------------------
    def _bloc12(self):
        corps    = RoundedRectangle(corner_radius=0.5, height=2.5, width=1.2, color=TEXT_C, fill_opacity=0.1)
        cg       = Dot(corps.get_bottom() + UP * 0.8, color=ACCENT, radius=0.15)
        arrow_cg = Arrow(cg.get_center() + RIGHT * 2, cg.get_center(), color=ACCENT)
        label    = Tex(r"CG Bas", color=ACCENT, font_size=40).next_to(arrow_cg, RIGHT)
        groupe   = VGroup(corps, cg, arrow_cg, label).move_to(ORIGIN)

        self.play(Create(corps), FadeIn(cg), run_time=1.0)
        self.play(GrowArrow(arrow_cg), Write(label), run_time=0.5)
        self.wait(2.859)

    # -----------------------------------------------------------------------
    # BLOC 13 | [42.037s → 45.999s] | RÉSULTAT GRAPHIQUE
    # -----------------------------------------------------------------------
    def _bloc13(self):
        axes = Axes(
            x_range=[0, 3, 1], y_range=[0, 10, 2],
            x_length=6, y_length=5,
            axis_config={"color": TEXT_DIM},
        )
        barre_force   = Rectangle(width=1, height=4,   color=PRIMARY, fill_opacity=0.8).move_to(axes.c2p(1, 0), aligned_edge=DOWN)
        barre_agilite = Rectangle(width=1, height=0.1, color=ACCENT,  fill_opacity=0.8).move_to(axes.c2p(2, 0), aligned_edge=DOWN)
        label_f = Tex(r"Force",   font_size=36, color=TEXT_C).next_to(barre_force,   DOWN)
        label_a = Tex(r"Agilit\'e", font_size=36, color=TEXT_C).next_to(barre_agilite, DOWN, buff=1.0)

        self.play(Create(axes), FadeIn(barre_force), Write(label_f), Write(label_a), run_time=1.0)
        self.play(
            barre_agilite.animate.stretch_to_fit_height(4.5).move_to(axes.c2p(2, 0), aligned_edge=DOWN),
            run_time=1.0,
        )
        self.wait(1.962)

    # -----------------------------------------------------------------------
    # BLOC 14 | [46.299s → 49.073s] | OUTRO
    # -----------------------------------------------------------------------
    def _bloc14(self):
        line1 = Tex(r"Quel autre mythe", color=TEXT_C, font_size=64)
        line2 = Tex(r"on pulv\'erise ?",  color=TEXT_C, font_size=64)
        outro = VGroup(line1, line2).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(outro, shift=UP), run_time=1.0)
        self.wait(1.271)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
