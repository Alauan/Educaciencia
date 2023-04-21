from manim import *
from my_classes import *

class Cena(Scene):
    def construct(self):
        eixos = Axes(x_range=[0, 7, 1], 
                     y_range=[0, 128, 10],
                     x_length=10,
                     tips=False,
                     axis_config={"include_numbers": False}).to_edge(RIGHT)
        
        grafico = eixos.plot(lambda x: 2**x)

        x = ValueTracker(0)

        linhas = VGroup(VMobject(), VMobject())
        def f(m):
            point = eixos.c2p(x.get_value(), 2**x.get_value())
            m.submobjects[0] = eixos.get_horizontal_line(point)
            m.submobjects[1] = eixos.get_vertical_line(point)
        linhas.add_updater(f)

        jaime = Stickman(0.5)
        jaime.core.move_to(eixos.get_critical_point(DL)+LEFT*1.5)
        jaime.core.rotate(PI/2)

        jaime.core.add_updater(lambda m: m.set_y(linhas.submobjects[0].get_center()[1]))

        jaime.walk(3, lambda x: (2**(x*7))/128)

        self.play(Create(eixos))
        self.add(grafico, linhas, jaime)

        self.play(x.animate.set_value(7), run_time=3, rate_func=linear)