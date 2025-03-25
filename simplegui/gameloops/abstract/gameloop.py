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

    def is_entity_visible(self, player, entity) -> bool:
        hitbox = entity.hitbox_area
        player_x = player.pos.x
        player_y = player.pos.y
        direction = player.direction

        screen_right = player_x + 250
        screen_left = player_x - 250

        if (hitbox[0] < screen_right and hitbox[2] > screen_left):
            if direction == "RIGHT":
                if hitbox[2] > player.pos.x - 100:
                    return True
            else:
                if hitbox[0] < player.pos.x + 100:
                    return True

        return False

