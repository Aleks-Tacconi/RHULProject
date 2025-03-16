"""Entity module.

This module defines the Entity class, which serves as the base class for
all entities in the game. This class provides a standardized way of creating
entities and adding them to the game.

File:
    entities/abstract/entity.py

Classes:
    Entity: representation of an entity in the game.
"""

from abc import ABCMeta, abstractmethod
from typing import List

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector


class Entity(metaclass=ABCMeta):
    """Entity Object.

    Attributes:
        _size (Vector): The size of the entity.
        pos (Vector): The position of the entity.
        area (List[int | float]): The bounding box of the entity calculated
                                  from the entities position and size.

    Abstract Methods:
        render(canvas: simplegui.Frame) -> None: Renders the entity onto the canvas.
        update() -> None: Updates the state of the Entity.
    """

    def __init__(self, pos: Vector, size: Vector) -> None:
        self.pos = pos
        self.size = size

    @abstractmethod
    def render(self, canvas: simplegui.Canvas) -> None:
        """Renders the entity onto the canvas.

        This is an abstract method which must be implemented by all
        subclasses of the Entity abstract base class.

        Args:
            canvas (simplegui.Frame): The canvas on which to render.
        """

    @abstractmethod
    def update(self) -> None:
        """Updates the state of the Entity.

        This is an abstract method which must be implemented by all
        subclasses of the Entity abstract base class.

        This method should update the state of the entity accordingly to
        its role in the game. This method will be called every iteration
        of the games mainloop.
        """

    @property
    def area(self) -> List[int | float]:
        """The bounding box of the entity calculated from the entities position and size.

        This property calculates the coordinates of the bounding box based
        on its self._pos and self._size. 

        Returns:
            List[int | float]: A list representing the bounding box of the entity 
                                in the format [x1, y1, x2, y2].
        """
        half_width = self.size.x // 2
        half_height = self.size.x // 2

        x1 = self.pos.x - half_width
        x2 = x1 + half_width

        y1 = self.pos.y - half_height
        y2 = y1 + half_height

        return [x1, y1, x2, y2]
