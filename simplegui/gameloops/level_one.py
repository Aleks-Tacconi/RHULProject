import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from simplegui.components import ScoreBoard
from entities import Block, Player, Attack, AbyssalRevenant, Fire, PlayerHealthBar, Background, ImpalerBoss, FlyingDemon, DemonSlimeBoss
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

        for i in range(0, 8):
            self.__environment.append(Background(pos=Vector(0 + (700 * i), 240),
                                                 img=os.path.join("assets", "background",
                                                                  f"Purple_Nebula_0{i + 1}-1024x1024.png"),
                                                 size_x=1000, size_y=1000, scale_factor=0.7))
            self.__environment.append(Background(pos=Vector(0 - (700 * i), 240),
                                                 img=os.path.join("assets", "background",
                                                                  f"Purple_Nebula_0{i + 1}-1024x1024.png"),
                                                 size_x=1000, size_y=1000, scale_factor=0.7))



        self.__player = Player(pos=Vector(400, 400))
        self.__player_light = Background(pos=Vector(0, 0),
                                             img=os.path.join("assets", "player", "FRAME_HARD.png"),
                                             size_x=1200, size_y=1200, scale_factor=1)
        self.__player_light_flip = Background(pos=Vector(0, 0),
                                             img=os.path.join("assets", "player", "FRAME_HARD_FLIPPED.png"),
                                             size_x=1200, size_y=1200, scale_factor=1)

        self.__enemies = []
        self.__enemies.append(AbyssalRevenant(pos=Vector(90, 200)))
        self.__enemies.append(FlyingDemon(pos=Vector(700, 200)))
        self.__enemies.append(DemonSlimeBoss(pos=Vector(1000, 300)))
        self.__enemies.append(Fire(400))

        self.__gui = []
        self.__player_frame = Background(pos=Vector(400, 400),
                                             img=os.path.join("assets", "player", "FANTASY_FRAME.png"),
                                             size_x=1024, size_y=1024, scale_factor=1)
        self.__player_healthbar = PlayerHealthBar(pos=Vector(130, 760), player=self.__player)
        self.__gui.append(self.__player_healthbar)

        self.__entities = []


        block_path = os.path.join("assets", "blocks", "BLOCK1.png")
        for i in range(0, 80):
            self.__entities.append(Block(Vector(i - 20, 15), block_path))

        self.__entities.append(Block(Vector(14, 14), block_path))
        self.__entities.append(Block(Vector(14, 24), block_path))

        self.__offset_x = 0
        self.__offset_y = 0

    def mainloop(self, canvas: simplegui.Canvas) -> None:

        self.__scoreboard.update()

        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 380 - self.__offset_x) // 30
        self.__offset_y += (self.__player.pos.y - 480 - self.__offset_y)

        self.__player.update()

        for entity in self.__environment:
            if self.is_entity_visible(self.__player, entity):
                entity.render(canvas, -self.__offset_x, -self.__offset_y)

        for entity in self.__entities:
            if self.is_entity_visible(self.__player, entity):
                entity.render(canvas, -self.__offset_x, -self.__offset_y)
                entity.update()

        for attack in Attack.all:
            attack.render(canvas, -self.__offset_x, -self.__offset_y)
            attack.update()

        for entity in self.__enemies:
            if self.is_entity_visible(self.__player, entity):
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

        if self.__player.direction == "LEFT":
            self.__player_light.render(canvas, self.__player.pos.x - self.__offset_x,
                                       self.__player.pos.y - self.__offset_y)
        else:
            self.__player_light_flip.render(canvas, self.__player.pos.x - self.__offset_x,
                                       self.__player.pos.y - self.__offset_y)

        self.__player_frame.render(canvas, 0, 0)

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)


