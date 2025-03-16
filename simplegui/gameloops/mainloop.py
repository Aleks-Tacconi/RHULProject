"""MainLoop Module.

This module defines the MainLoop class which is the actual event loop.
This defines all the interactions between entities as well as rendering
the map and entities on the map themselves.

File:
    simplegui/gameloops/mainloop.py

Classes:
    MainLoop: The main loop of the game.
"""

import os

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from ai import AI
from entities import AbyssalRevenant, Block, Player
from utils import Vector

from .abstract import GameLoop


class MainLoop(GameLoop):
    """MainLoop entity.

    Attributes:
        __player (Player): An instance of the player class, the main character of the game.

    Methods:
        mainloop() -> None: The main loop of the game, this is the function that runs every frame.
        keyup_handler(key: int) -> None: The method that handles what happens when a key is pressed.
                                         The key is provided as the ordinal value of the character
        keydown_handler(key: int) -> None: The method that handles what happens when a key is
                                           released. The key is provided as the ordinal value of the
                                           character.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__player = Player(Vector(200, 400))
        self.__enemies = [AbyssalRevenant(Vector(700, 400))]
        self.__ai = AI()
        self.__left_right = []

        self.__blocks = {}

        for i in range(50):
            block = Block(
                Vector(-15 + i, 14),
                Vector(32, 32),
                os.path.join("assets", "blocks", "block.jpg"),
                rows=1,
                cols=1,
            )
            self.__blocks[block.key] = block

        block = Block(
            Vector(8, 13),
            Vector(32, 32),
            os.path.join("assets", "blocks", "block.jpg"),
            rows=1,
            cols=1,
        )
        self.__blocks[block.key] = block

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        for enemy in self.__enemies:
            enemy.render(canvas)
            enemy.update()
            enemy.interaction(self.__player)

        self.__player.render(canvas)
        self.__player.update()
        self.remove_dead()

        for block in self.__blocks.values():
            block.render(canvas)

    def keyup_handler(self, key: int) -> None:
        if key == 65:  # A
            self.__left_right.remove(65)
        if key == 68:  # D
            self.__left_right.remove(68)

        if not self.__left_right:
            if self.__player.vel.x < 0:
                self.__player.current_animation = "IDLE_LEFT"
            else:
                self.__player.current_animation = "IDLE_RIGHT"

            self.__player.vel = Vector(0, 0)
        else:
            self.__update_player_movement()

    def __update_player_movement(self) -> None:
        if self.__left_right:
            direction = self.__left_right[-1]
            if direction == 65:  # A
                self.__player.vel = Vector(-3, 0)
                self.__player.current_animation = "RUN_LEFT"
            if direction == 68:  # D
                self.__player.vel = Vector(3, 0)
                self.__player.current_animation = "RUN_RIGHT"

    def keydown_handler(self, key: int) -> None:
        if key in (65, 68):
            self.__left_right.append(key)
            self.__update_player_movement()

        if key == 86:  # V
            self.__ai.listen_and_respond()

        if key == 87:  # W
            self.__player.jump()


    def remove_dead(self):
        self.__enemies = [enemy for enemy in self.__enemies if not enemy.dead]
