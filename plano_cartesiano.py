from manim import *
from my_classes import *
from random import random, seed

class Cena1(Scene):
    def construct(self):
        # -------------- CENA 1 ---------------------
        reta = NumberLine([-5, 5], 15, include_numbers=True, numbers_to_exclude=[-5, 5])
        ponto = Dot(color=BLUE_C).move_to(reta.n2p(3))
        num = DecimalNumber(color=BLUE_C)
        num.add_updater(lambda m: m.set_value(reta.p2n(num.get_center())))
        num.add_updater(lambda m: m.move_to(ponto.get_center()+UP))
        num.update()
        
        self.play(Create(reta))
        self.add(num, ponto)
        self.wait()
        self.play(ponto.animate.move_to(reta.n2p(-3)), run_time=3)
        self.wait()
        self.play(FadeOut(reta, ponto, num))

class Cena2(Scene):
    def construct(self):
        # ------------- CENA 2 ----------------------
        
        func_repr = MathTex(r"{{S(t)}} = 2\cdot{{t}}")
        func_repr.font_size = 100
        interrogacao = Text("?", color=YELLOW_C, font="Bitstream Charter", font_size=350)

        self.play(Write(func_repr))
        #self.wait()
        self.play(DrawBorderThenFill(interrogacao))
        self.wait()
        self.play(FadeOut(interrogacao))
        


        #self.wait(0.5)
        self.play(func_repr[0].animate.set_color(ORANGE), run_time=0.5)
        self.play(Wiggle(func_repr[0]))
        #self.wait(0.5)
        self.play(func_repr[2].animate.set_color(BLUE), run_time=0.5)
        self.play(Wiggle(func_repr[2]))
        #self.wait(0.5)

        eixo_t = NumberLine([-5, 5], 15, include_numbers=True, numbers_to_exclude=[-5, 5])
        eixo_st = NumberLine([-5, 5], 15, include_numbers=True, numbers_to_exclude=[-5, 5]).shift(2*DOWN)
        

        self.play(func_repr.animate.shift(2*UP))
        self.play(Create(eixo_t))
        self.play(Create(eixo_st))

        func_repr_copy = func_repr.copy()

        func_repr_copy[2].generate_target()
        func_repr_copy[2].target.move_to([-6.5, 0.6, 0]).scale(0.6)
        self.play(MoveToTarget(func_repr_copy[2]))

        func_repr_copy[0].generate_target()
        func_repr_copy[0].target.move_to([-6.5, -1.4, 0]).scale(0.6)
        self.play(MoveToTarget(func_repr_copy[0]))

        #------------- COLOCANDO PONTOS NAS RETAS -----------------
        ponto_t = Dot(color=BLUE_C, point=eixo_t.n2p(1))
        num_t = DecimalNumber(color=BLUE_C)
        num_t.add_updater(lambda m: m.set_value(eixo_t.p2n(ponto_t.get_center())))
        num_t.add_updater(num_t_movement_updater:=lambda m: m.move_to(ponto_t.get_center()+UP))
        num_t.update()

        ponto_st = Dot(color=ORANGE)
        ponto_st.add_updater(lambda m: m.move_to(eixo_st.n2p(2*eixo_t.p2n(ponto_t.get_center()))))
        ponto_st.update()
        num_st = DecimalNumber(color=ORANGE)
        num_st.add_updater(lambda m: m.set_value(eixo_st.p2n(ponto_st.get_center())))
        num_st.add_updater(num_st_movement_updater:=lambda m: m.move_to(ponto_st.get_center()+UP*sin(a:=eixo_st.get_angle()+PI/2)+RIGHT*cos(a)))
        num_st.update()


        self.add_foreground_mobjects(ponto_t, num_t)

        num_t_repr = DecimalNumber(font_size=90, color=BLUE)
        num_t_repr.add_updater(lambda m: m.set_value(num_t.get_value()))
        num_t_repr.add_updater(lambda m: m.next_to(func_repr[1], RIGHT))
        num_t_repr.update()
        self.play(func_repr[2].animate.become(num_t_repr))
        self.remove(func_repr[2])
        self.add(num_t_repr)


        self.add_foreground_mobjects(ponto_st, num_st)

        num_st_repr = DecimalNumber(font_size=90, color=ORANGE)
        num_st_repr.add_updater(lambda m: m.set_value(num_st.get_value()))
        num_st_repr.add_updater(lambda m: m.next_to(func_repr[1], LEFT))
        num_st_repr.update()
        self.play(func_repr[0].animate.become(num_st_repr))
        self.remove(func_repr[0])
        self.add(num_st_repr)

        self.play(ponto_t.animate.move_to(eixo_t.n2p(-2)), run_time=2)
        self.play(ponto_t.animate.move_to(eixo_t.n2p(-1)))
        self.wait()

        #virando eixo st
        func_repr[1].generate_target()
        func_repr[1].target.move_to([-5, 3, 0]).scale(0.5)

        self.play(MoveRotateNumberLine(eixo_st, lambda a: a*2*UP, lambda a: a*PI/2), func_repr_copy[0].animate.move_to(3.5*DOWN+0.8*LEFT),
                  MoveToTarget(func_repr[1]), num_st_repr.animate.scale(0.5), num_t_repr.animate.scale(0.5))

        #Transição para plano cartesiano
        ax = Axes([-5, 5], [-5, 5], 15, 15,a:={"include_numbers":True, "numbers_to_exclude":[0]}, a)
        self.add(ax)
        self.remove(eixo_st, eixo_t)

        ponto = Dot()
        dotted_vert = VMobject()
        dotted_hori = VMobject()
        ponto.add_updater(lambda m: m.set_x(ponto_t.get_center()[0]))
        ponto.add_updater(lambda m: m.set_y(ponto_st.get_center()[1]))
        dotted_vert.add_updater(lambda m: m.become(ax.get_vertical_line([ponto_t.get_center()[0], ponto_st.get_center()[1], 0])))
        dotted_hori.add_updater(lambda m: m.become(ax.get_horizontal_line([ponto_t.get_center()[0], ponto_st.get_center()[1], 0])))
        dotted_hori.update()
        dotted_vert.update()

        dotted_hori.suspend_updating()
        dotted_vert.suspend_updating()
        self.play(Create(dotted_hori))
        self.play(Create(dotted_vert))
        dotted_vert.resume_updating()
        dotted_hori.resume_updating()
        self.play(Create(ponto))

        
        # montagem da coordenada
        coordenada = VGroup(MathTex("("), num_t, MathTex(","), num_st, MathTex(")"))
        coordenada[0].add_updater(lambda m: m.next_to(num_t, LEFT))
        coordenada[4].add_updater(lambda m: m.next_to(num_st, RIGHT))

        def f(m):
            if ponto.get_center()[0] < 0:
                m.move_to(ponto.get_center() + 0.5*DOWN + 2*LEFT)
            else:
                m.move_to(ponto.get_center() + 2*RIGHT)
            num_t.update()
            num_st.update()
            coordenada[0].update()
            coordenada[4].update()
        coordenada[2].add_updater(f)
        
        coordenada[2].update()
        num_t.remove_updater(num_t_movement_updater)
        num_st.remove_updater(num_st_movement_updater)
        self.play(Create(coordenada[2]), num_t.animate.next_to(coordenada[2], LEFT + 0.1*UP), num_st.animate.next_to(coordenada[2], RIGHT + 0.1*UP))
        self.play(FadeIn(coordenada[0]), FadeIn(coordenada[4]))

        num_t.add_updater(lambda m: m.next_to(coordenada[2], LEFT + 0.1*UP))
        num_st.add_updater(lambda m: m.next_to(coordenada[2], RIGHT + 0.1*UP))
        
        #Adicionando pontos
        pontos = VGroup()
        self.add(pontos)
        for i in range(5):
            self.play(ponto_t.animate.move_to(eixo_t.n2p((i-2)/2)))
            self.play(Indicate(ponto))
            pontos += Dot([ponto_t.get_center()[0], ponto_st.get_center()[1], 0], color=YELLOW)


        grafico = ax.plot(lambda x: 2*x, color=YELLOW)
        self.play(Create(grafico))

        dotted_hori.suspend_updating()
        dotted_vert.suspend_updating()
        self.play(FadeOut(coordenada, ponto, pontos, dotted_hori, dotted_vert, func_repr[1], ponto_t, ponto_st, num_st_repr, num_t_repr))
        self.remove(num_st, num_t, ponto_st, ponto_t, num_st_repr, num_t_repr)

        self.wait()

















