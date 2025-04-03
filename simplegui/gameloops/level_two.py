import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (Block, Player, Attack, AbyssalRevenant, Fire, Background, DemonSlimeBoss, FlyingDemon, EvilHand,
                      Mage, EvilKnight, PlayerHealthBar, Cinematic)
from simplegui.components.xp import XP
from simplegui.gameloops.transition_screen import TransitionScreen
from utils import Vector

from .abstract import GameLoop
from simplegui.components import ScoreBoard, Cutscene, Interactable


ID = "LevelTwo"

class LevelTwo(GameLoop):
    def __init__(self, reset: Callable, failed: Callable, passed: Callable, scoreboard: ScoreBoard, xp: XP) -> None:
        super().__init__()

        self.__reset = reset
        self.__failed = failed
        self.__passed = passed

        self._load_level(os.path.join("levels", "level2"), ID)

        self.__scoreboard = scoreboard
        self.__xp = xp

        self.__environment = []

        for i in range(0, 10):
            self.__environment.append(
                Background(
                    pos=Vector(-420 + (1862 * i), 0),
                    img=os.path.join("assets", "background", "SURFACE_HELL_BACKGROUND.png"),
                    size_x=828,
                    size_y=358,
                    scale_factor=2.25,
                    frames=8,
                    cols=8,
                )
            )

        self.__player = Player(pos=Vector(-400, 80), level_id=ID)

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

        self.__interactions = Interactable(self.__next_scene, "Press F to go to the next level",
                                           os.path.join("assets", "portal", "red_portal.png"),
                                           1, 24, 4, self.__player, Vector(7980, 70),
                                           Vector(128, 128))


    def mainloop(self, canvas: simplegui.Canvas) -> None:

        self.__scoreboard.update()

        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 380 - self.__offset_x) // 10
        self.__offset_y += (self.__player.pos.y - 180 - self.__offset_y) // 10

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
                self.__xp.enemy_killed_xp(entity, ID)
            if entity.remove():
                self._enemies.remove(entity)

        if self.__player.remove():
            self.__scoreboard.calculate_score("LevelTwo")
            print("|||||||||||||||||||||||||||||||||")
            self.__scoreboard.print_score()
            self.__xp.print_xp()
            print("|||||||||||||||||||||||||||||||||")
            self.__reset(transition_screen=TransitionScreen(
                prev_level=ID,
                title=self.__reset,
                failed=self.__failed,
                passed=self.__passed,
                passed_level=self.__player.hp > 0,
                score=self.__scoreboard.return_score(ID),
                xp=self.__xp
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

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

        for interactable in self.__interactions.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                self.__interactions.update(interactable)
                self.__interactions.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)

    def __next_scene(self):
        self.__scoreboard.calculate_score(ID)
        print("|||||||||||||||||||||||||||||||||")
        self.__scoreboard.print_score()
        self.__xp.print_xp()
        print("|||||||||||||||||||||||||||||||||")
        self.__reset(transition_screen=TransitionScreen(
            prev_level=ID,
            title=self.__reset,
            failed=self.__failed,
            passed=self.__passed,
            passed_level=self.__player.hp > 0,
            score=self.__scoreboard.return_score(ID),
            xp=self.__xp
        ))