import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import Block, Player, Attack, AbyssalRevenant, Fire
from utils import Vector

from .abstract import GameLoop


class MainLoop(GameLoop):
    def __init__(self, reset: Callable) -> None:
        super().__init__()

        self.__reset = reset

        self.__player = Player(pos=Vector(400, 400))

        self.__enemies = []
        self.__enemies.append(AbyssalRevenant(pos=Vector(300, 200)))
        self.__enemies.append(Fire(400))

        self.__entities = []

        block_path = os.path.join("assets", "blocks", "block.jpg")
        for i in range(0, 80):
            self.__entities.append(Block(Vector(i, 15), block_path))

        self.__entities.append(Block(Vector(14, 14), block_path))

        self.__offset_x = 0
        self.__offset_y = 0

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 400 - self.__offset_x) // 30
        self.__offset_y += (self.__player.pos.y - 400 - self.__offset_y) // 30

        self.__player.update()
        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

        if not self.__player.is_alive:
            self.__reset()

        for entity in self.__entities:
            entity.render(canvas, -self.__offset_x, -self.__offset_y)
            entity.update()

        for attack in Attack.all:
            attack.render(canvas, -self.__offset_x, -self.__offset_y)
            attack.update()

        for entity in self.__enemies:
            entity.render(canvas, -self.__offset_x, -self.__offset_y)
            entity.update()
            entity.interaction(self.__player)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)
