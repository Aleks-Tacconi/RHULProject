"""GameLoop Module

This module defines the abstract base class which acts as a template for creating game loops
It provides methods for handling user input, mouse events, and the main game loop
rendering and updating entities.

File:
    simplegui/gameloops/abstract/gameloop.py

Classes:
    GameLoop: An abstract base class creating a standardized way to create gameloops
              which can handle keyboard and mouse input events.
"""
from abc import ABCMeta, abstractmethod
from typing import Tuple

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Mouse


class GameLoop(metaclass=ABCMeta):
    """Abstract base class for handling the games mainloop.

    Attributes:
        _mouse (Mouse): A dataclass storing the position of the last click.

    Methods:
        mouseclick_handler(pos: Tuple[int, int]) -> None: Updates the mouse dataclass with
                                                          the most recent clicked position.

    Abstract Methods:
        mainloop(canvas: simplegui.Frame, *args) -> None: An implementation of a draw handler
        keyup_handler(key: int) -> None: Abstract method to handle keyup events.
        keydown_handler(key: int) -> None: Abstract method to handle keydown events.
    """

    def __init__(self) -> None:
        self._mouse = Mouse()

    def mouseclick_handler(self, pos: Tuple[int, int]) -> None:
        """Updates the mouse dataclass with the most recent clicked position.

        Args:
            pos (List[int]): The coords of the last click.
        """
        self._mouse.click(*pos)

    @abstractmethod
    def mainloop(self, canvas: simplegui.Canvas) -> None:
        """An implementation of a draw handler and mainloop for the game.

        Args:
            canvas (simplegui.Frame): The SimpleGUICS2Pygame Frame object
                                       that will be used for rendering the game.
        """

    @abstractmethod
    def keydown_handler(self, key: int) -> None:
        """Abstract method to handle keydown events.

        Args:
            key (int): The ordinal value of the key pressed.
        """

    @abstractmethod
    def keyup_handler(self, key: int) -> None:
        """Abstract method to handle keyup events.

        Args:
            key (int): The ordinal value of the key released.
        """
