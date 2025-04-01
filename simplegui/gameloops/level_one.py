import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (Block, Player, Attack, AbyssalRevenant, Fire, Background, DemonSlimeBoss, FlyingDemon, EvilHand,
                      Mage, EvilKnight, PlayerHealthBar, Cinematic)
from utils import Vector

from .abstract import GameLoop
from simplegui.components import ScoreBoard, Cutscene


ID = "LevelOne"

class LevelOne(GameLoop):
    def __init__(self, reset: Callable) -> None:
        super().__init__()

        self.__reset = reset

        self._load_level(os.path.join("levels", "level1"), ID)

        self.__scoreboard = ScoreBoard()

        self.__environment = []

        for i in range(0, 10):
            self.__environment.append(
                Background(
                    pos=Vector(-420 + (1863 * i), 0),
                    img=os.path.join("assets", "background", "CASTLE_BACKGROUND.png"),
                    size_x=828,
                    size_y=358,
                    scale_factor=2.25,
                    frames=4,
                    cols=6,
                )
            )

        self.__player = Player(pos=Vector(100, -100), level_id=ID)

        """"
        self.__player_light = Background(
            pos=Vector(0, 0),
            img=os.path.join("assets", "player", "FRAME_HARD.png"),
            size_x=1200,
            size_y=1200,
            scale_factor=1,
        )
        self.__player_light_flip = Background(
            pos=Vector(0, 0),
            img=os.path.join("assets", "player", "FRAME_HARD_FLIPPED.png"),
            size_x=1200,
            size_y=1200,
            scale_factor=1,
        )
        """

        self.__gui = []
        self.__player_healthbar = PlayerHealthBar(pos=Vector(130, 360), player=self.__player)
        self.__gui.append(self.__player_healthbar)

        self.__offset_x = 0
        self.__offset_y = 0
        #self.__offset_x_light = 0
        #self.__offset_y_light = 0


    def mainloop(self, canvas: simplegui.Canvas) -> None:

        self.__scoreboard.update()

        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 380 - self.__offset_x) // 10
        self.__offset_y += (self.__player.pos.y - 180 - self.__offset_y) // 10

        #self.__offset_x_light += (self.__player_light.pos.x - 400 - self.__offset_x) // 30
        #self.__offset_y_light += (self.__player_light.pos.y - 400 - self.__offset_y) // 30

        self.__player.update()

        for entity in self.__environment:
            if self.is_entity_visible(self.__player, entity):
                entity.update()
                entity.render(canvas, -self.__offset_x, -self.__offset_y)

        for k, entity in Block.all.items():
            if ID not in k:
                continue

            if self.is_entity_visible(self.__player, entity):
                entity.render(canvas, -self.__offset_x, -self.__offset_y)
                entity.update()

        for attack in Attack.all:
            attack.render(canvas, -self.__offset_x, -self.__offset_y)
            attack.update()

        for entity in self._enemies:
            entity.update()
            self.__player._knockback(entity)
            if self.is_entity_visible(self.__player, entity):
                entity.interaction(self.__player)
                entity.render(canvas, -self.__offset_x, -self.__offset_y)

            if not entity.is_alive:
                self.__scoreboard.enemy_killed_score(entity)
            if entity.remove():
                self._enemies.remove(entity)

        if self.__player.remove():
            self.__scoreboard.calculate_score("LevelOne")
            print("|||||||||||||||||||||||||||||||||")
            self.__scoreboard.print_score()
            print("|||||||||||||||||||||||||||||||||")
            self.__reset(self.__scoreboard.return_score("LevelOne"))
            canvas.draw_text(f"Score: {self.__scoreboard.return_score("LevelOne")}", (400, 50), 30, "White")

        """
        if self.__player.direction == "LEFT":
            self.__player_light.render(
                canvas,
                self.__player.pos.x - self.__offset_x,
                self.__player.pos.y - self.__offset_y,
            )
        else:
            self.__player_light_flip.render(
                canvas,
                self.__player.pos.x - self.__offset_x,
                self.__player.pos.y - self.__offset_y,
            )
        """

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)
