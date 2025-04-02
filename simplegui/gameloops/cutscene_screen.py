from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle
from .abstract import GameLoop
import os
from entities import Background
from utils import Vector

class CutSceneScreen(GameLoop):
    def __init__(self, next: Callable) -> None:
        super().__init__()

        self.__next = next

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        
        self.__next()
    
    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self._render_hitbox(canvas, offset_x, offset_y)