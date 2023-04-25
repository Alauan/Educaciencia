from manim import Animation, Mobject
from math import atan2, sin, cos
from typing import Callable, Sequence
from .Custom_mobjects import *
import numpy as np


def get_derivative_in_radians(function: Callable[[float], Sequence[float]], iterations = 120, **kwargs) -> Callable:
    """Retorna uma função que retorna o ângulo que a trajetória faz com a horizontal
    - Utilizado em funções que retornam a posição a partir de um alpha que vai de 0 a 1"""
    angles = []
    v1 = function(0)
    for alpha in [(1/iterations)*i for i in range(1, iterations+1)]:
        v2 = function(alpha, **kwargs)
        angles.append(atan2(v2[1]-v1[1], v2[0]-v1[0]))
        v1 = v2
    
    def saida(alpha):
        return angles[int(alpha*iterations)-1]
    
    return saida

class MoveRotate(Animation):
    """Esta classe move e rotaciona objetos ao mesmo tempo seguindo funções"""
    def __init__(self,
                 mobject: Mobject,
                 movement_function: Callable[[float], Sequence[float]], 
                 rotation_function: Callable[[float], float], 
                 **kwargs):
        self.movement_function = movement_function
        self.rotation_function = rotation_function
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)
        self.mobject.become(self.starting_mobject)
        self.mobject.move_to(self.mobject.get_center() + self.movement_function(alpha))
        self.mobject.rotate(self.rotation_function(alpha), about_point=self.mobject.get_center())


class MoveRotateAligned(MoveRotate):
    """Esta classe rotaciona objetos de acordo com a trajetória, como se fosse uma flecha"""
    def __init__(self, mobject: Mobject,
                 movement_function: Callable[[float], Sequence[float]], 
                 run_time=1, 
                 **kwargs):
        super().__init__(mobject, 
                         movement_function, 
                         get_derivative_in_radians(movement_function, iterations=run_time*120), 
                         run_time=run_time,
                         **kwargs)


class MoveRotateNumberLine(Animation):
    """Esta classe move e rotaciona NumberLine ao mesmo tempo seguindo funções"""
    def __init__(self,
                 mobject: NumberLine,
                 movement_function: Callable[[float], Sequence[float]], 
                 rotation_function: Callable[[float], float], 
                 about_number=0,
                 **kwargs):
        self.movement_function = movement_function
        self.rotation_function = rotation_function
        self.about_number=about_number
        self.d = mobject.get_center() - mobject.n2p(about_number) 
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate_about_number(self.about_number, self.rotation_function(alpha))
        R = self.mobject.get_angle()
        L = self.mobject.n2p(self.about_number) + self.movement_function(alpha)
        C = L + np.dot([[cos(R), -sin(R), 0], [sin(R), cos(R), 0], [0, 0, 1]], self.d.transpose())
        self.mobject.move_to(C)

