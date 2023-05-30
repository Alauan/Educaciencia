from my_classes import *
from manim import *
from manim.utils.rate_functions import ease_in_out_quart, ease_in_sine

class Intro(Scene):
    def construct(self):
        ax = Axes(x_range=[-4, 4], y_range=[-4, 4], x_length=7, y_length=7)
        graficos = [ax.plot(lambda x: x, color=YELLOW),
                    ax.plot(lambda x: 2**x, color=YELLOW),
                    ax.plot(lambda x: 0.3*x**3 - 0.2*x**2 - x + 0.5, color=YELLOW),
                    ax.plot(lambda x: sin(x), color=YELLOW)]

        self.wait(1)
        self.play(FadeIn(ax))
        self.play(Create(graficos[0]))
        self.wait(1)
        for grafico in graficos[1:]:
            self.play(Transform(graficos[0], grafico))
            self.wait(1)

        self.play(FadeOut(graficos[0]))
        self.play(Wiggle(ax))
        self.wait()
        self.play(Shrink(ax), run_time=0.5)
        self.wait()

class Barbante(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        def movimenta_formiga(formiga: Mobject, posicoes: list) -> None:
            for posicao in posicoes:
                d = abs(formiga.get_center()[0] - posicao)
                run_time = d/(2+0.2*d**1.6)
                self.play(formiga.animate.set_x(posicao), run_time=run_time, rate_func=ease_in_out_quart)
                self.wait(0.5)


        def cria_decimal(seguir, formiga, casas_decimais):
            decimal = DecimalNumber(num_decimal_places=casas_decimais, group_with_commas= True)
            decimal.add_updater(lambda m: m.next_to(seguir))
            decimal.add_updater(lambda m: m.set_value(formiga.get_center()[0]))
            decimal.update()
            return decimal


        barbante = Line(6.5*LEFT, 6.5*RIGHT)
        barbante_grande = Line(100*LEFT, 100*RIGHT)
        comeco = Line(6.5*LEFT, 2*LEFT, stroke_color=[WHITE, ORANGE, ORANGE, ORANGE])
        meio = Line(4*LEFT, 4*RIGHT, stroke_color=[WHITE, ORANGE, ORANGE, WHITE])
        formiga = Dot().next_to(barbante, direction=UP, aligned_edge=DOWN)
        mao = MathTex("mao apontando.png").move_to(RIGHT*3 + DOWN*2)
        xis = VGroup(
            Line(mao.get_critical_point(UL), mao.get_critical_point(DR), color=RED),
            Line(mao.get_critical_point(UR), mao.get_critical_point(DL), color=RED),
        )


        self.play(FadeIn(formiga))
        self.play(Create(barbante))

        movimenta_formiga(formiga, [3, 1, -6.2, -2.5])

        self.play(FadeIn(mao, target_position=DOWN*4 + RIGHT*7))
        self.play(Create(xis))
        self.wait()
        self.remove(xis, mao)
        self.wait()

        self.play(FadeIn(comeco), run_time=0.5)
        self.wait()
        self.play(FadeOut(comeco), run_time=0.5)
        self.play(FadeIn(meio), run_time=0.5)
        self.wait()

        movimenta_formiga(formiga, [0, 2, -1.3, 1])

        self.wait()

        # ------------ REGUA E MARCAS ------------------

        marcas = VGroup(VGroup(*[Line(0.2*UP + c*RIGHT, 0.2*DOWN+c*RIGHT, stroke_color=ORANGE) for c in range(-7, 7)]),
                        VGroup(*[MathTex(str(i), color=ORANGE).move_to(DOWN*0.6 + i*RIGHT) for i in range(-7, 7)]),
                        VGroup(*[Line(0.1*UP + (c/10)*RIGHT, 0.1*DOWN + (c/10)*RIGHT, stroke_width=2, color=ORANGE) for c in range(-65, 66)]),
                        VGroup(*[Line(0.05*UP + (c/100)*RIGHT, 0.05*DOWN + (c/100)*RIGHT, stroke_width=0.3, color=ORANGE) for c in range(40, 260)]),
                        VGroup(*[Line(0.2*UP + c*RIGHT, 0.2*DOWN+c*RIGHT, stroke_color=ORANGE) for c in range(-100, 100)]),
                        VGroup(*[MathTex(str(i), color=ORANGE).move_to(DOWN*0.6 + i*RIGHT) for i in range(-100, 100)]))
        
        regua = VGroup(
            Rectangle(height=2, width=8, stroke_width=2).move_to(RIGHT*3.5 + DOWN*2),
            VGroup(*[Line(DOWN + c*RIGHT, 1.5*DOWN+c*RIGHT) for c in range(0, 8)]),
            VGroup(*[Line(DOWN + (c/10)*RIGHT, 1.2*DOWN + (c/10)*RIGHT, stroke_width=1) for c in range(0, 83)])
        )

        self.play(Transform(meio, marcas[0][7], replace_mobject_with_target_in_scene=True))
        self.play(Write(marcas[1][7]))
        self.play(Create(regua))

        regua_marcas_cm_copia = regua[1].copy()

        self.play(AnimationGroup(*[Transform(regua_marcas_cm_copia[i], marcas[0][i+7], replace_mobject_with_target_in_scene=True) for i in range(1, 7)], lag_ratio=0.2))
        self.play(AnimationGroup(*[Write(marcas[1][i]) for i in range(8, 14)], lag_ratio=0.2))

        coordenadas = VGroup(MathTex("P="))
        coordenadas += cria_decimal(coordenadas[0], formiga, 0)
        
        coordenadas.add_updater(lambda m: m.next_to(formiga, UP, buff=1))

        coordenadas.update()

        self.play(FadeIn(coordenadas, target_position=formiga))

        movimenta_formiga(formiga, [4])
        self.wait(1)
        movimenta_formiga(formiga, [0])
        self.wait(2)

        self.play(regua.animate.flip(about_point=ORIGIN))
        regua_marcas_cm_copia = regua[1].copy()
        self.play(AnimationGroup(*[Transform(regua_marcas_cm_copia[i], marcas[0][7-i], replace_mobject_with_target_in_scene=True) for i in range(1, 7)], lag_ratio=0.2))
        self.play(AnimationGroup(*[Write(marcas[1][i]) for i in range(6, 0, -1)], lag_ratio=0.1))
        self.wait()

        movimenta_formiga(formiga, [-1, -2, -3, -4])

        self.wait()

        movimenta_formiga(formiga, [-4.3])

        self.wait()

        self.play(AnimationGroup(*[FadeIn(mark, target_position=mark.get_center()+UP) for mark in marcas[2]], lag_ratio=0.01))

        self.wait()
        coordenadas.remove(coordenadas[1])
        coordenadas += cria_decimal(coordenadas[0], formiga, 1)
        self.play(Indicate(coordenadas[1]))

        movimenta_formiga(formiga, [0.3, 1.423])
        self.wait()

        self.play(self.camera.frame.animate.scale(0.15).move_to(marcas[2][80]))
        coordenada_pequena = MathTex("{{P=1,4}}{{2}}{{3841...}}", font_size=DEFAULT_FONT_SIZE*0.15).next_to(formiga, 0.15*UP)

        self.remove(regua)

        self.play(Write(coordenada_pequena[0]))
        self.play(AnimationGroup(*[FadeIn(mark, target_position=mark.get_center()+UP) for mark in marcas[3]], lag_ratio=0.01), Write(coordenada_pequena[1]))
        self.wait()
        self.play(Write(coordenada_pequena[2]))
        self.wait()

        self.play(Restore(self.camera.frame), FadeOut(coordenada_pequena, marcas[3]))

        self.wait()

        self.remove(marcas[0], marcas[1], barbante)
        self.add(barbante_grande, marcas[4], marcas[5])
        self.play(self.camera.frame.animate.scale(6), FadeOut(marcas[2]), run_time=3, rate_func=ease_in_sine)
        self.play(FadeOut(*self.mobjects), self.camera.frame.animate.scale(2), run_time=3, rate_func=linear)


class Tabuleiro(ThreeDScene):
    def construct(self):
        pass

class Outro(Scene):
    def construct(self):
        pass

class LineGradient(Scene):
    def construct(self):
        line = Line(
            start=[-3, 0, 0],
            end=[3, 0, 0],
            stroke_width=20,
        )
        line.set_color_by_gradient(WHITE, ORANGE, WHITE)
        self.play(Create(line))

