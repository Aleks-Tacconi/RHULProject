import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from simplegui.components import ScoreBoard
from entities import Block, Player, Attack, AbyssalRevenant, Fire, PlayerHealthBar, Background
from utils import Vector

from .abstract import GameLoop


class LevelOne(GameLoop):
    def __init__(self, reset: Callable) -> None:
        super().__init__()

        self.__reset = reset

        self.__scoreboard = ScoreBoard()

        self.__environment = []

        self.__environment.append(Background(pos=Vector(400, 500),
                                             img=os.path.join("assets", "background", "01 background.png")))
        self.__environment.append(Background(pos=Vector(400, 500),
                                             img=os.path.join("assets", "background", "02 background.png")))
        self.__environment.append(Background(pos=Vector(400, 400),
                                             img=os.path.join("assets", "background", "03 background A.png")))
        self.__environment.append(Background(pos=Vector(400, 300),
                                             img=os.path.join("assets", "background", "04 background.png")))
        self.__environment.append(Background(pos=Vector(400, 200),
                                             img=os.path.join("assets", "background", "05 background.png")))



        self.__player = Player(pos=Vector(400, 400))

        self.__enemies = []
        self.__enemies.append(AbyssalRevenant(pos=Vector(90, 200)))
        self.__enemies.append(AbyssalRevenant(pos=Vector(600, 200)))

        self.__gui = []
        self.__player_healthbar = PlayerHealthBar(pos=Vector(130, 760), player=self.__player)
        self.__gui.append(self.__player_healthbar)

        self.__entities = []


        block_path = os.path.join("assets", "blocks", "block.jpg")
        for i in range(0, 80):
            self.__entities.append(Block(Vector(i, 15), block_path))

        self.__entities.append(Block(Vector(14, 14), block_path))

        self.__offset_x = 0
        self.__offset_y = 0

    def mainloop(self, canvas: simplegui.Canvas) -> None:

        self.__scoreboard.update()

        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 400 - self.__offset_x) // 30
        self.__offset_y += (self.__player.pos.y - 400 - self.__offset_y) // 30

        self.__player.update()

        for entity in self.__environment:
            entity.render(canvas, -self.__offset_x, -self.__offset_y)
            #entity.render(canvas, -self.__offset_x + 1704, -self.__offset_y)

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        for entity in self.__entities:
            entity.render(canvas, -self.__offset_x, -self.__offset_y)
            entity.update()

        for attack in Attack.all:
            attack.render(canvas, -self.__offset_x, -self.__offset_y)
            attack.update()

        for entity in self.__enemies:
            entity.update()
            entity.interaction(self.__player)
            entity.render(canvas, -self.__offset_x, -self.__offset_y)
            if not entity.is_alive:
                self.__scoreboard.enemy_killed_score(entity)
            if entity.remove():
                self.__enemies.remove(entity)

        if self.__player.remove():
            self.__scoreboard.calculate_score("LEVEL ONE")
            print("|||||||||||||||||||||||||||||||||")
            self.__scoreboard.print_score()
            print("|||||||||||||||||||||||||||||||||")
            self.__reset()

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)
