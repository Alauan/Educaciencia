from manim import *
from my_classes import *


class Teste(Scene):
    def construct(self):
        plano = Axes(x_range=[0, 7, 1], 
                     y_range=[0, 128, 10],
                     x_length=10,
                     tips=False,
                     axis_config={"include_numbers": False}).to_edge(RIGHT)
        
        grafico = plano.plot(lambda x: 2**x, x_range=[0, 7])

        # placing the stickman
        jaimeII = Stickman(0.5)
        jaimeII.core.move_to(plano.get_critical_point(DL)+LEFT*1.5)

        # defining horizontal and vertical lines
        x_value = ValueTracker(0)
        lines = VGroup(VMobject(), VMobject())
        def f(m: Mobject):
            point = plano.c2p(x_value.get_value(), 2**x_value.get_value())
            m.submobjects[0] = plano.get_horizontal_line(point)
            m.submobjects[1] = plano.get_vertical_line(point)
        lines.add_updater(f)
        
        def rate_function_exp(x:float):
            return ((x*7)**2)/128
        


        self.play(Create(plano), Create(grafico))
        self.add(jaimeII, lines)
        jaimeII.walk(3, rate_func=rate_function_exp)
        self.play(x_value.animate.set_value(7), 
                  MoveRotateAligned(jaimeII.core, lambda x: rate_function_exp(x)*7*UP), 
                  run_time=3, rate_func=linear)
        self.wait(1)

