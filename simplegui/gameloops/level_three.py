import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (Block, Player, Attack, AbyssalRevenant, Fire, Background, DemonSlimeBoss, FlyingDemon, EvilHand,
                      Mage, EvilKnight, PlayerHealthBar, Cinematic, Teleport)
from simplegui.components.xp import XP
from simplegui.gameloops.transition_screen import TransitionScreen
from utils import Vector
from entities.utils import PlaySound
from .abstract import GameLoop
from simplegui.components import ScoreBoard, Cutscene, Interactable


ID = "LevelThree"

class LevelThree(GameLoop):
    def __init__(self, reset: Callable, failed: Callable, passed: Callable, scoreboard: ScoreBoard, xp: XP) -> None:
        super().__init__()

        self.__reset = reset

        self.__reset = reset
        self.__failed = failed
        self.__passed = passed
        self._load_level(os.path.join("levels", "level3"), ID)

        self.__scoreboard = scoreboard
        self.__xp = xp

        self.__environment = []

        for i in range(0, 10):
            self.__environment.append(
                Background(
                    pos=Vector(-420 + (1863 * i), 0),
                    img=os.path.join("assets", "background", "HELL_BACKGROUND.png"),
                    size_x=828,
                    size_y=358,
                    scale_factor=2.25,
                    frames=4,
                    cols=8,
                )
            )

        self.__player = Player(pos=Vector(-150, 80), level_id=ID)


        self.__gui = []
        self.__player_healthbar = PlayerHealthBar(pos=Vector(130, 360), player=self.__player)
        self.__gui.append(self.__player_healthbar)

        self.__offset_x = 0
        self.__offset_y = 0


        self.__teleport = Teleport(Vector(7640, 80), self.__player)
        self.__interactions = Interactable(self.__teleport.teleport, "Press F to meet Demon King",
                                           os.path.join("assets", "portal", "red_portal.png"),
                                           1, 24, 4, self.__player, Vector(5950, 100),
                                           Vector(128, 128))
        self.__music = PlaySound()
        self.__music.loop(True)
        self.__music.change_volume(0.3)

        self.__interaction2 = Interactable(
            self.__next_scene,
            "Press F to complete the game",
            os.path.join("assets", "portal", "red_portal.png"),
            1,
            24,
            4,
            self.__player,
            Vector(9675, 83),
            Vector(128, 128)
        )
        self.__display_end_portal = False


    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__scoreboard.update()
        self.__music.play_sound("ha-pressure.wav")

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
                print(type(entity))
                print(type(entity) == DemonSlimeBoss)
                self._enemies.remove(entity)
                if type(entity) == DemonSlimeBoss:
                    self.__display_end_portal = True

        if self.__player.remove():
            self.__scoreboard.calculate_score(ID)
            self.__reset(transition_screen=TransitionScreen(
                prev_level=ID,
                title=self.__reset,
                failed=self.__failed,
                passed=self.__passed,
                passed_level=self.__player.hp > 0,
                score=self.__scoreboard.return_score(ID),
                xp=self.__xp
            ))

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        for interactable in self.__interactions.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                self.__interactions.update(interactable)
                self.__interactions.render(canvas, -self.__offset_x, -self.__offset_y)

        for interactable in self.__interaction2.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                if self.__display_end_portal:
                    self.__interaction2.update(interactable)
                    self.__interaction2.render(canvas, -self.__offset_x, -self.__offset_y)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)

    def __next_scene(self):
        self.__scoreboard.calculate_score(ID)
        self.__reset(
            transition_screen=TransitionScreen(
                prev_level=ID,
                title=self.__reset,
                failed=self.__failed,
                passed=self.__passed,
                passed_level=self.__player.hp > 0,
                score=self.__scoreboard.return_score(ID),
                xp=self.__xp,
            )
        )


