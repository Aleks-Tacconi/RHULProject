import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from simplegui.components import ScoreBoard
from entities import Block, Player, Attack, AbyssalRevenant, Fire, PlayerHealthBar, Background
from utils import Vector
#from OpenGL.GL import *
#OpenGL.GLUT import *
#from OpenGL.GLU import *
from .abstract import GameLoop


class LevelOne(GameLoop):
    def __init__(self, reset: Callable) -> None:
        super().__init__()

        self.__reset = reset

        self.__scoreboard = ScoreBoard()

        self.__environment = []

        self.__environment.append(Background(pos=Vector(-26, 310),
                                             img=os.path.join("assets", "background", "03 background B_FLIPPED.png"),
                                             size_x=426, size_y=468, scale_factor=1))
        self.__environment.append(Background(pos=Vector(400, 310),
                                             img=os.path.join("assets", "background", "03 background B.png"),
                                             size_x=426, size_y=468, scale_factor=1))
        self.__environment.append(Background(pos=Vector(826, 310),
                                             img=os.path.join("assets", "background", "03 background B_FLIPPED.png"),
                                             size_x=426, size_y=468, scale_factor=1))

        #TODO: I will optimise this and only render background when in its in view
        #for i in range(1, 5):
            #self.__environment.append(Background(pos=Vector(-26 - (426 * i), 310),
             #                                    img=os.path.join("assets", "background",
             #                                                     "03 background B_FLIPPED.png"),
             #                                    size_x=426, size_y=468, scale_factor=1))

        #for i in range(0, 5):
            #self.__environment.append(Background(pos=Vector(-826 + (426 * i), 310),
                                                 #img=os.path.join("assets", "background",
                                                 #                 "03 background B_FLIPPED.png"),
                                                 #size_x=426, size_y=468, scale_factor=1))

        self.__player = Player(pos=Vector(400, 400))
        self.__player_light = Background(pos=Vector(0, 0),
                                             img=os.path.join("assets", "player", "PLAYER_LIGHT.png"),
                                             size_x=1200, size_y=1200, scale_factor=3/4)

        self.__enemies = []
        self.__enemies.append(AbyssalRevenant(pos=Vector(90, 200)))
        self.__enemies.append(AbyssalRevenant(pos=Vector(600, 200)))
        self.__enemies.append(Fire(400))

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
        self.__offset_x_light = 0
        self.__offset_y_light = 0

    def mainloop(self, canvas: simplegui.Canvas) -> None:

        self.__scoreboard.update()

        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 400 - self.__offset_x) // 30
        self.__offset_y += (self.__player.pos.y - 400 - self.__offset_y) // 30

        self.__offset_x_light += (self.__player_light.pos.x - 400 - self.__offset_x) // 30
        self.__offset_y_light += (self.__player_light.pos.y - 400 - self.__offset_y) // 30

        self.__player.update()

        for entity in self.__environment:
            entity.render(canvas, -self.__offset_x, -self.__offset_y)

        for entity in self.__entities:
            if self.is_entity_visible(self.__player, entity):
                entity.render(canvas, -self.__offset_x, -self.__offset_y)
                entity.update()

        for attack in Attack.all:
            attack.render(canvas, -self.__offset_x, -self.__offset_y)
            attack.update()

        for entity in self.__enemies:
            entity.update()
            entity.interaction(self.__player)
            if self.is_entity_visible(self.__player, entity):
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

        self.__player_light.render(canvas, self.__player.pos.x - self.__offset_x, self.__player.pos.y - self.__offset_y)

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)


