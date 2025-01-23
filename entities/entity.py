from abc import abstractmethod
from abc import ABCMeta

class Entity(metaclass=ABCMeta):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

        self.vel_y = 0
        self.vel_y_increment = 0.4
        self.max_vel_y = 20

    @abstractmethod
    def render(self, canvas): ...

    @abstractmethod
    def update(self): ...

    def gravity(self):
        self.vel_y = min(self.vel_y + self.vel_y_increment, self.max_vel_y)
        self.pos[1] += self.vel_y

        # TODO: replace this with collision
        if self.pos[1] > 600:
            self.vel_y = 0
            self.pos[1] = 600

