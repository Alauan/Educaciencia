from manim import Animation, Mobject
from math import atan2
from typing import Callable, Sequence
from .Custom_mobjects import *


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
        self.mobject.rotate(self.rotation_function(alpha), about_point=self.mobject.get_center())
        self.mobject.move_to(self.mobject.get_center() + self.movement_function(alpha))


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



