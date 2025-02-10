from abc import abstractmethod
from abc import ABCMeta
from vector import Vector

class Entity(metaclass=ABCMeta):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

        self.vel = Vector(0, 0)
        self.vel_y_increment = 0.5
        self.max_vel_y = 20

    @abstractmethod
    def render(self, canvas): ...

    @abstractmethod
    def update(self): ...

    def gravity(self):
        self.vel.y = min(self.vel.y + self.vel_y_increment, self.max_vel_y)
        self.pos.y += self.vel.y

        # TODO: replace this with collision
        if self.pos.y > 600:
            self.vel.y = 0
            self.pos.y = 600

