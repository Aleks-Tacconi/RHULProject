import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (Block, Player, Attack, AbyssalRevenant, Fire, Background, DemonSlimeBoss, FlyingDemon, EvilHand,
                      Mage, EvilKnight, PlayerHealthBar, Cinematic, Teleport)
from simplegui.components.xp import XP
from simplegui.gameloops.transition_screen import TransitionScreen
from utils import Vector

from .abstract import GameLoop
from simplegui.components import ScoreBoard, Cutscene, Interactable


ID = "tutorial"

class Tutorial(GameLoop):
    def __init__(self, reset: Callable, failed: Callable, passed: Callable, scoreboard: ScoreBoard, xp: XP) -> None:
        super().__init__()

        self.__reset = reset
        self.__failed = failed
        self.__passed = passed

        self._load_level(os.path.join("levels", "tutorial"), ID)

        self.__scoreboard = scoreboard
        self.__xp = xp

        self.__environment = []

        for i in range(0, 10):
            self.__environment.append(
                Background(
                    pos=Vector(0 + (1863 * i), 0),
                    img=os.path.join("assets", "background", "HELL_BACKGROUND.png"),
                    size_x=828,
                    size_y=358,
                    scale_factor=2.25,
                    frames=4,
                    cols=8,
                )
            )

        self.__player = Player(pos=Vector(100, 0), level_id=ID)

        self.__gui = []
        self.__player_healthbar = PlayerHealthBar(pos=Vector(130, 360), player=self.__player)
        self.__gui.append(self.__player_healthbar)

        self.__offset_x = 0
        self.__offset_y = 0
        #self.__offset_x_light = 0
        #self.__offset_y_light = 0
        self.__cutscenes = Cutscene(self.__player)
        self.__cutscenes.new_cutscene(Vector(-50, 0), 0, "Welcome to Knightborne."
                                             " The void stirs, whispering your name. Shadows coil,"
                                             " hungry for the weary and the weak."
                                             " Press A to drift left, D to wade right."
                                             " Keep moving… or be swallowed whole.", Vector(0,60))
        self.__cutscenes.new_cutscene(Vector(300, 0), 0, "Press W to jump the wall,"
                                               " your hands gripping the cold stone as the darkness presses"
                                               " close. Rise, or be trapped in the depths below.", Vector(0,60))
        self.__cutscenes.new_cutscene(Vector(850, 0),0, "Press E to attack. Press Space to roll"
                                                        " enemy attacks, whilst rolling you are immune to damage."
                                                        , Vector(0,300))
        self.__cutscenes.new_cutscene(Vector(2000, 0), 0, "Press S to crouch to sneak behind an"
                                                          " enemy undetected as long as they are not facing towards"
                                                          " you. Crouching can also help dodge projectile attacks. "
                                                          "Press E whilst sneaking to deal a sneak attack that"
                                                          " does critical-damage.", Vector(0, 300))
        self.__cutscenes.new_cutscene(Vector(3000, 0), 0, "This is a big gap."
                                                          " To cross you will need to run and jump"
                                                          " Press Shift to run.", Vector(0, 300))
        self.__cutscenes.new_cutscene(Vector(4000, 0), 0, "Press F to interact with objects"
                                                          " in the world. And with this, you have completed the basic"
                                                          " tutorial. Now you are ready, chosen one."
                                                          , Vector(0, 300))

        self.__interactions = Interactable(self.__next_scene, "Press F to end tutorial",
                                           os.path.join("assets", "portal", "red_portal.png"),
                                           1, 24, 4, self.__player, Vector(4700, 100),
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

        for cutscene in self.__cutscenes.cutscenes:
            if self.is_entity_visible(self.__player, cutscene[3]):
                self.__cutscenes.play_cutscene(cutscene)
                cutscene[3].render(canvas, -self.__offset_x, -self.__offset_y)
                self.__cutscenes.render(canvas)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)

    def __next_scene(self):
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
