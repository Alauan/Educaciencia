from math import sin, cos
from manim import RIGHT, UP, LEFT, DOWN, PI
from typing import Sequence, Callable



def circular(alpha: float, radius=2) -> Sequence[float]:
    return radius*RIGHT*(-cos(2*PI*alpha)+1) + radius*UP*sin(2*PI*alpha)

def sin_wave(alpha: float, width=12, height=4, cicles=1) -> Sequence[float]:
    return RIGHT*alpha*width + UP*(height/2) * sin(cicles*2*PI*alpha)

def square(alpha: float, side=2) -> Sequence[float]:
    if alpha <= 0.25:
        return side * 4*alpha * RIGHT
    elif alpha <= 0.5:
        return side * (RIGHT + 4*(alpha-0.25) * UP)
    elif alpha <= 0.75:
        return side * (RIGHT + UP + 4*(alpha-0.5) * LEFT)
    else:
        return side * (UP + 4*(alpha-0.75) * DOWN)
    

class PositionFunc:
    def __init__(self, function, **kwargs):
        self.function = function
        self.kwargs = kwargs
    
    def __call__(self, alpha) -> Sequence[float]:
        return self.function(alpha, **self.kwargs)

    

