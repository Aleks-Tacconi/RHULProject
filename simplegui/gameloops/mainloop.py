import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import Block, Player, Attack, AbyssalRevenant, Fire
from utils import Vector

from .abstract import GameLoop

ID = "MainLoop"

class MainLoop(GameLoop):
    def __init__(self, reset: Callable) -> None:
        super().__init__()

        self.__reset = reset

        self.__player = Player(pos=Vector(400, 200), level_id=ID)
        self._load_level(os.path.join("levels", "level1"), ID)

        self.__offset_x = 0
        self.__offset_y = 0

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 380 - self.__offset_x) // 30
        self.__offset_y += (self.__player.pos.y - 180 - self.__offset_y) // 30

        self.__player.update()
        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

        if self.__player.remove():
            self
            self.__reset()

        for k, entity in Block.all.items():
            if ID in k:
                entity.render(canvas, -self.__offset_x, -self.__offset_y)
                entity.update()

        for attack in Attack.all:
            attack.render(canvas, -self.__offset_x, -self.__offset_y)
            attack.update()

        for entity in self._enemies:
            entity.update()
            entity.interaction(self.__player)
            entity.render(canvas, -self.__offset_x, -self.__offset_y)



    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)
