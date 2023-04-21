from manim import *
from typing import Sequence, Union
from math import atan2, sin, cos

def get_positive_angle(angle):
    r = angle % (PI*2)
    if r < 0:
        r += PI*2
    return r

def get_smallest_distance_between_angles(starting_angle, final_angle):
    """This distance can be positive (if the starting angle needs to rotate counterclockwise)
      or negative (if it needs to rotate clockwise)"""
    starting_angle = get_positive_angle(starting_angle)
    final_angle = get_positive_angle(final_angle)
    CCW_distance = final_angle - starting_angle
    if -PI <= CCW_distance <= PI:
        return CCW_distance
    if CCW_distance < -PI:
        return CCW_distance + PI*2
    return CCW_distance - PI*2


class Member(VGroup):
    def __init__(self, angle1=0, angle2=0, length1=1, length2=1, self_update=True):
        self.linha1 = Line(ORIGIN, RIGHT*length1, stroke_width=8)
        self.linha2 = Line(ORIGIN, RIGHT*length2, stroke_width=8)
        self.linha2.add_updater(lambda m: m.shift(self.linha1.get_end() - self.linha2.get_start()))
        self.linha2.update()
        self.t = {}     #dicionário de temporizacão para updatefunctions
        super().__init__(self.linha1, self.linha2)

        self.angle1 = angle1
        self.angle2 = angle2

        if self_update:
            def angle_updater(m: Member):
                m.linha1.set_angle(m.angle1)
                m.linha2.set_angle(m.angle1 + m.angle2)

            self.add_updater(angle_updater)

        self.update()

    def wave(self, run_time=1):
        name = self.wave.__name__
        if name not in self.t:
            self.t[name] = 0

            def f(m: Member, dt):
                if m.t[name] >= run_time:
                    m.angle2 = sin(4*run_time)
                    m.remove_updater(f)
                    del m.t[name]
                else:
                    m.t[name] += dt
                    m.angle2 = sin(4*m.t[name])

            self.add_updater(f)

        else:
            raise Exception(f"{name} is already running!")

    def go_to_pose(self, angle1, angle2, run_time=1):
        """Goes gradually to defined state"""

        starting_angle1 = self.angle1
        starting_angle2 = self.angle2
        dif1 = get_smallest_distance_between_angles(self.angle1, angle1)
        dif2 = get_smallest_distance_between_angles(self.angle2, angle2)
        name = self.go_to_pose.__name__
        if name not in self.t:
            self.t[name] = 0

            def f(m: Member, dt):
                if m.t[name] >= run_time:
                    m.angle1 = angle1
                    m.angle2 = angle2
                    m.remove_updater(f)
                    del m.t[name]
                else:
                    m.t[name] += dt
                    m.angle1 = starting_angle1 + (dif1)*(m.t[name]/run_time)
                    m.angle2 = starting_angle2 + (dif2)*(m.t[name]/run_time)

            self.add_updater(f)

        else:
            raise Exception(f"{name} is already running!")

    def set_pose(self, angle1, angle2):
        self.angle1 = angle1
        self.angle2 = angle2

    def move_shoulder_to(self, position: Sequence[int]):
        self.linha1.shift(position - self.linha1.get_start())

    def rotate1(self, radians=PI):
        self.angle1 += radians

    def rotate2(self, radians=PI):
        self.angle2 += radians

    @property
    def main_mobject(self):
        """Object used to move the group"""
        return self.submobjects[0]


class Stickman(VGroup):
    # Poses for the stickman
    REST = [[a := PI + 0.3, b := -0.3], [a - 0.6, -b], [a, b], [a - 0.6, -b]]

    def __init__(self, size=1):
        self.body = Line(ORIGIN, size*1.6*UP, stroke_width=8)

        leg_kwargs = {"length1": size, "length2": size , "self_update":False}
        self.leg1 = Member(**leg_kwargs)
        self.leg2 = Member(**leg_kwargs)

        arm_kwargs = {"length1": size*0.8, "length2": size*0.8 , "self_update":False}
        self.arm1 = Member(**arm_kwargs)
        self.arm2 = Member(**arm_kwargs)

        self.head = Circle(head_radius := size*0.3, color=WHITE, stroke_width=8)

        members = [self.arm1, self.arm2, self.leg1, self.leg2]
        super().__init__(*members, self.head, self.body)

        self.t = {}     #dicionário de temporização para updatefunctions
        self.facing_right = True    #para onde o boneco está apontado

        # ____________________ MEMBER UPDATERS _____________________________
        def rotation_member_updater(m: Stickman):
            for submobject in members:
                submobject.linha1.set_angle(submobject.angle1 + m.angle)
                submobject.linha2.set_angle(submobject.angle2 + submobject.angle1 + m.angle)
        
        self.add_updater(rotation_member_updater)

        self.add_updater(lambda m: m.leg1.move_shoulder_to(m.hip))
        self.add_updater(lambda m: m.leg2.move_shoulder_to(m.hip))
        self.add_updater(lambda m: m.arm1.move_shoulder_to(m.neck))
        self.add_updater(lambda m: m.arm2.move_shoulder_to(m.neck))

        # ____________________ HEAD UPDATER _________________________________
        def head_updater(m: Stickman):
            pos = m.neck + [head_radius*cos(m.angle), head_radius*sin(m.angle), 0]
            m.head.move_to(pos)
        self.add_updater(head_updater)
        
        self.update()

        self.set_pose(Stickman.REST)

    def walk(self, run_time=1, rate_func=linear, steps_per_second=1): 
        name = self.walk.__name__
        if name not in self.t:
            self.t[name] = 0

            dir = 1 if self.facing_right else -1

            # Declaração de funções que vão ser usadas no movimento dos membros. Ciclo: de 0 a 1

            def leg_angle1_func(x:float):
                x *= 2*PI
                return dir*(-PI/2 + (-1.5*sin(x) + 0.3*sin(2*x))*0.35 - 1.4)
            
            def leg_angle2_func(x:float):
                return dir*(-0.5 + 0.207*x + -0.101*x**2 + 0.0218*x**3 + -2.02e-03*x**4 + 7.99e-05*x**5 + -1.12e-06*x**6)
            
            def arm_angle1_func(x:float):
                x *= 2*PI
                return dir*(-PI/2 + (-1.6*sin(x) + 0.2*sin(3*x))*0.25 - 1.8)
            
            def arm_angle2_func(x:float):
                x *= 2*PI
                return dir*(sin(x)/3 + 0.3)
            

            def f(m: Stickman, dt):
                if m.t[name] >= run_time:
                    m.remove_updater(f)
                    del m.t[name]
                else:
                    x = rate_func(m.t[name]/run_time)*run_time*steps_per_second

                    m.leg1.angle1 = leg_angle1_func(x - 1/6)
                    m.leg1.angle2 = leg_angle2_func(24*(x%1))

                    m.leg2.angle1 = leg_angle1_func(x - 1/6 - 1/2)
                    m.leg2.angle2 = leg_angle2_func(24*((x+0.5)%1))

                    m.arm1.angle1 = arm_angle1_func(x - 1/8)
                    m.arm1.angle2 = arm_angle2_func(x + 1/8)

                    m.arm2.angle1 = arm_angle1_func(x - 1/8 + 1/2)
                    m.arm2.angle2 = arm_angle2_func(x + 1/8 + 1/2)

                    m.t[name] += dt

            self.add_updater(f)

        else:
            raise Exception(f"{name} is already running!")

    def go_to_pose(self, state:Sequence[Sequence], run_time=1):
        leg1, leg2, arm1, arm2 = state
        self.leg1.go_to_pose(*leg1, run_time)
        self.leg2.go_to_pose(*leg2, run_time)
        self.arm1.go_to_pose(*arm1, run_time)
        self.arm2.go_to_pose(*arm2, run_time)

    def set_pose(self, state:Sequence[Sequence]):
        leg1, leg2, arm1, arm2 = state
        self.leg1.set_pose(*leg1)
        self.leg2.set_pose(*leg2)
        self.arm1.set_pose(*arm1)
        self.arm2.set_pose(*arm2)

    def turn(self):
        self.facing_right = not self.facing_right

    @property
    def angle(self):
        return self.body.get_angle()

    @property
    def neck(self):
        return self.body.get_end()

    @property
    def hip(self):
        return self.body.get_start()

    @property
    def core(self):
        """Objeto para usar quando for mover o grupo, """
        return self.body


class ArrowSquare(VGroup):
    """Simple test object"""
    def __init__(self, **kwargs):
        self.arrow = Arrow()
        self.square = Square(0.7)
        self.square.add_updater(lambda m: m.next_to(self.arrow, UP))
        self.square.add_updater(lambda m, dt: m.rotate(PI*dt))
        super().__init__(self.arrow, self.square, **kwargs)

    def rotate_clockwise(self):
        self.square.updaters[1] = lambda m, dt: m.rotate(-PI*dt)
        
    def rotate_counterclockwise(self):
        self.square.updaters[1] = lambda m, dt: m.rotate(PI*dt)


    @property
    def main_mobject(self):
        """Objeto para usar quando for mover o grupo, """
        return self.submobjects[0]
