import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from SimpleGUICS2Pygame.simpleguics2pygame import canvas

from entities import (
    Attack,
    Background,
    Block,
    Player,
    PlayerHealthBar,
    Teleport,
)
from entities.utils import PlaySound
from simplegui.components import Cutscene, Interactable, ScoreBoard, Subtitles
from simplegui.components.xp import XP
from simplegui.gameloops.transition_screen import TransitionScreen
from utils import Vector
from ai import AI
import random
from .abstract import GameLoop

ID = "LevelOne"


class LevelOne(GameLoop):
    def __init__(
        self,
        reset: Callable,
        failed: Callable,
        passed: Callable,
        scoreboard: ScoreBoard,
        xp: XP,
    ) -> None:
        super().__init__()

        self.__reset = reset
        self.__failed = failed
        self.__passed = passed

        self._load_level(os.path.join("levels", "level1"), ID)

        self.__scoreboard = scoreboard
        self.__xp = xp

        self.__environment = []

        for i in range(0, 10):
            self.__environment.append(
                Background(
                    pos=Vector(-420 + (960 * i), 70),
                    img=os.path.join(
                        "assets", "background", "BATTLEFIELD_BACKGROUND.png"
                    ),
                    size_x=1280,
                    size_y=566,
                    scale_factor=0.75,
                    frames=4,
                    cols=17,
                )
            )
        self.__environment.append(
            Background(
                pos=Vector(-2000, 138),
                img=os.path.join("assets", "background", "lonely_knight.png"),
                size_x=776,
                size_y=410,
                scale_factor=0.5,
                frames=4,
                cols=27,
            )
        )

        self.__player = Player(pos=Vector(140, 170), level_id=ID)

        self.__gui = []
        self.__player_healthbar = PlayerHealthBar(
            pos=Vector(130, 360), player=self.__player
        )
        self.__gui.append(self.__player_healthbar)

        self.__offset_x = 0
        self.__offset_y = 0

        self.__teleport = Teleport(Vector(-1870, 80), self.__player)
        self.__teleport_back = Teleport(Vector(-480, 0), self.__player)
        self.__interactions = Interactable(
            self.__next_scene,
            "Press F to go to the next level",
            os.path.join("assets", "portal", "red_portal.png"),
            1,
            24,
            4,
            self.__player,
            Vector(4850, 195),
            Vector(128, 128),
        )
        self.__tower = Interactable(
            self.__teleport.teleport,
            "Press F to enter tower",
            os.path.join("assets", "background", "tower.png"),
            1,
            1,
            1,
            self.__player,
            Vector(-480, 50),
            Vector(512, 512),
        )

        self.__door = Interactable(
            self.__teleport_back.teleport,
            "Press F to exit tower",
            os.path.join("assets", "background", "door.png"),
            1,
            8,
            2,
            self.__player,
            Vector(-2130, 160),
            Vector(150, 150),
        )

        self.__npc = Interactable(
            self.__talk,
            "Press F to talk to mysterious knight",
            os.path.join("assets", "background", "transparent_square.png"),
            1,
            8,
            2,
            self.__player,
            Vector(-1970, 200),
            Vector(50, 100),
        )
        self.__npc_talk = Subtitles("", Vector(-2100, 169), 15)
        self.__npc_ai = AI()
        self.__music = PlaySound()
        self.__music.loop(True)
        self.__music.change_volume(0.3)

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__music.play_sound("ha-simplestring_1.wav")
        self.__scoreboard.update()

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

        for interactable in self.__interactions.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                self.__interactions.update(interactable)
                self.__interactions.render(canvas, -self.__offset_x, -self.__offset_y)

        for interactable in self.__tower.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                self.__tower.update(interactable)
                self.__tower.render(canvas, -self.__offset_x, -self.__offset_y)

        for interactable in self.__door.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                self.__door.update(interactable)
                self.__door.render(canvas, -self.__offset_x, -self.__offset_y)

        for interactable in self.__npc.interactables:
            if self.is_entity_visible(self.__player, interactable[6]):
                self.__npc.update(interactable)
                self.__npc.render(canvas, -self.__offset_x, -self.__offset_y)

        for entity in self.__gui:
            entity.update()
            entity.render(canvas, 0, 0)

        self.__player.render(canvas, -self.__offset_x, -self.__offset_y)
        self.__npc_talk.render(canvas, -self.__offset_x, -self.__offset_y)

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)

    def __next_scene(self):
        self.__scoreboard.calculate_score(ID)
        self.__music.stop()
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

    def __talk(self):
        response = self.__npc_ai.text_prompt("Act as a mysterious knight. Say one sentence about you grumbling about"
                                             " the war with the demons.")
        if response == "ERROR":
            responses = {"Talk": ["This war has gone for way too long, I wish it would just end!",
                                  "It never ends! How many have to die?",
                                  "Leave me alone stranger.",
                                  "The gods have forsaken us!",
                                  "God, please give me strength to live another day in this damned world!"]}
            response = random.choice(responses["Talk"])

        self.__npc_talk.new_subtitle(response)
        self.__npc_talk.start_subtitles()



