from manim import *
from my_classes import *


class Teste(Scene):
    def construct(self):
        b = Stickman(size=0.5)
        self.add(b)

        b.walk(run_time=2, steps_per_second=2)
        self.wait(2)
        b.go_to_pose(Stickman.REST)

        self.play(b.core.animate.move_to(7*LEFT))
        self.wait(1)

        b.walk(run_time=4)
        self.play(b.core.animate.move_to(7*RIGHT), run_time=4, rate_func=linear)

        b.go_to_pose(Stickman.REST)
        self.play(b.core.animate.move_to(7*LEFT))
        b.walk(run_time=3, rate_func=smooth)
        self.play(MoveRotateAligned(b.core, sin_wave, run_time=3, rate_func=smooth))
        
        b.go_to_pose(Stickman.REST, run_time=0.3)
        b.core.generate_target()
        b.core.target.rotate(PI/2 - b.angle)
        b.core.target.move_to(ORIGIN)
        self.play(MoveToTarget(b.core))

        self.wait(1)

        




        
        

        
        
