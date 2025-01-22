from abc import abstractmethod
from abc import ABCMeta

class Entity(metaclass=ABCMeta):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    @abstractmethod
    def render(self, canvas): ...

    @abstractmethod
    def update(self): ...
