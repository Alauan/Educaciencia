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
        interrogacoes = []
        for i in range(10):
            seed(i+20)
            interrogacoes.append(Text("?", color=YELLOW_C, font="Bitstream Charter"))
            interrogacoes[i].font_size = 140
            interrogacoes[i].move_to([(random()-0.5)*12, (random()-0.5)*6, 0])

        self.play(DrawBorderThenFill(func_repr))
        #self.wait()
        self.play(AnimationGroup(*[DrawBorderThenFill(interrogacao) for interrogacao in interrogacoes], lag_ratio=0.1))
        #self.wait()
        self.remove(*interrogacoes)


        #self.wait(0.5)
        self.play(func_repr[0].animate.set_color(ORANGE))
        #self.wait(0.5)
        self.play(func_repr[2].animate.set_color(BLUE))
        #self.wait(0.5)

        eixo_t = NumberLine([-5, 5], 15, include_numbers=True, numbers_to_exclude=[-5, 5])
        eixo_st = NumberLine([-5, 5], 15, include_numbers=True, numbers_to_exclude=[-5, 5]).shift(2*DOWN)
        

        self.play(func_repr.animate.shift(2*UP))
        self.play(Create(eixo_t))
        self.play(Create(eixo_st))

        func_repr_copy = func_repr.copy()

        func_repr_copy[2].generate_target()
        func_repr_copy[2].target.move_to([-6.5, 1, 0]).scale(0.6)
        self.play(MoveToTarget(func_repr_copy[2]))

        func_repr_copy[0].generate_target()
        func_repr_copy[0].target.move_to([-6.5, -1, 0]).scale(0.6)
        self.play(MoveToTarget(func_repr_copy[0]))

        #------------- COLOCANDO PONTOS NAS RETAS -----------------
        ponto_t = Dot(color=BLUE_C, point=eixo_t.n2p(1))
        num_t = DecimalNumber(color=BLUE_C)
        num_t.add_updater(lambda m: m.set_value(eixo_t.p2n(ponto_t.get_center())))
        num_t.add_updater(lambda m: m.move_to(ponto_t.get_center()+UP))
        num_t.update()

        ponto_st = Dot(color=ORANGE)
        ponto_st.add_updater(lambda m: m.move_to(eixo_st.n2p(2*eixo_t.p2n(ponto_t.get_center()))))
        ponto_st.update()
        num_st = DecimalNumber(color=ORANGE)
        num_st.add_updater(lambda m: m.set_value(eixo_st.p2n(ponto_st.get_center())))
        num_st.add_updater(lambda m: m.move_to(ponto_st.get_center()+UP))
        num_st.update()


        self.add(ponto_t, num_t)

        num_t_repr = DecimalNumber(font_size=90, color=BLUE)
        num_t_repr.add_updater(lambda m: m.set_value(num_t.get_value()))
        num_t_repr.add_updater(lambda m: m.next_to(func_repr[1], RIGHT))
        num_t_repr.update()
        self.play(func_repr[2].animate.become(num_t_repr))
        self.remove(func_repr[2])
        self.add(num_t_repr)


        self.add(ponto_st, num_st)

        num_st_repr = DecimalNumber(font_size=90, color=ORANGE)
        num_st_repr.add_updater(lambda m: m.set_value(num_st.get_value()))
        num_st_repr.add_updater(lambda m: m.next_to(func_repr[1], LEFT))
        num_st_repr.update()
        self.play(func_repr[0].animate.become(num_st_repr))
        self.remove(func_repr[0])
        self.add(num_st_repr)

        self.play(ponto_t.animate.move_to(eixo_t.n2p(-2)), run_time=2)
        self.play(ponto_t.animate.move_to(eixo_t.n2p(-0.5)))
        self.wait()

        #levando a legenda ao eixo vertical

        a = eixo_t.n2p(0)
        self.play(MoveRotateNumberLine(eixo_st, lambda a: a*2*UP, lambda a: a*PI/2, 1), func_repr_copy[0].animate.move_to(3.5*DOWN+0.5*LEFT))
        self.wait()













