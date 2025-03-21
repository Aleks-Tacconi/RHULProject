from abc import ABCMeta, abstractmethod
from typing import Tuple

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Mouse


class GameLoop(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._mouse = Mouse()

    def mouseclick_handler(self, pos: Tuple[int, int]) -> None:
        self._mouse.click(*pos)

    @abstractmethod
    def mainloop(self, canvas: simplegui.Canvas) -> None: ...

    @abstractmethod
    def keydown_handler(self, key: int) -> None: ...

    @abstractmethod
    def keyup_handler(self, key: int) -> None: ...

