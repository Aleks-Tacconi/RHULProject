import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (Block, Player, Attack, AbyssalRevenant, Fire, Background, DemonSlimeBoss, FlyingDemon, EvilHand,
                      Mage, EvilKnight, PlayerHealthBar, Cinematic, Teleport)
from simplegui.gameloops.transition_screen import TransitionScreen
from utils import Vector

from .abstract import GameLoop
from simplegui.components import ScoreBoard, Cutscene, Interactable


ID = "LevelOne"

class LevelOne(GameLoop):
    def __init__(self, reset: Callable, failed: Callable, passed: Callable) -> None:
        super().__init__()

        self.__reset = reset
        self.__failed = failed
        self.__passed = passed

        self._load_level(os.path.join("levels", "level1"), ID)

        self.__scoreboard = ScoreBoard()

        self.__environment = []

        for i in range(0, 10):
            self.__environment.append(
                Background(
                    pos=Vector(-420 + (960 * i), 70),
                    img=os.path.join("assets", "background", "BATTLEFIELD_BACKGROUND.png"),
                    size_x=1280,
                    size_y=566,
                    scale_factor=0.75,
                    frames=4,
                    cols=17,
                )
            )

        self.__player = Player(pos=Vector(100, 0), level_id=ID)

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
        self.__teleport = Teleport(Vector(0, -500), self.__player)
        self.__interactions = Interactable(self.__teleport.teleport,
                                           os.path.join("assets", "portal", "red_portal.png"),
                                           1, 24, 4, self.__player, Vector(300, 100),
                                           Vector(128, 128))


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
            self.__reset(transition_screen=TransitionScreen(
                    prev_level=ID,
                    title=self.__reset,
                    failed=self.__failed,
                    passed=self.__passed,
                    passed_level=self.__player.hp > 0,
                    score=self.__scoreboard.return_score(ID)
                ))

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

        for interactable in self.__interactions.interactables:
            self.__interactions.update(interactable)
            self.__interactions.render(canvas, -self.__offset_x, -self.__offset_y)

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)
