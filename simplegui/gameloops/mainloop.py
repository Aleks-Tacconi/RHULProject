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
        self.__abyssal_revenant = AbyssalRevenant(Vector(700, 400))  # testing
        self.__ai = AI()

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

        self.__abyssal_revenant.render(canvas)
        self.__abyssal_revenant.update()
        self.__player.render(canvas)
        self.__player.update()
        self.__abyssal_revenant.interaction(self.__player)

        for block in self.__blocks.values():
            block.render(canvas)

    def keyup_handler(self, key: int) -> None:
        print(key)
        if key == 65:  # A
            self.__player.vel = Vector(0, 0)
            self.__player.current_animation = "IDLE_LEFT"
        if key == 68:  # D
            self.__player.vel = Vector(0, 0)
            self.__player.current_animation = "IDLE_RIGHT"
        if key == 87:  # W
            self.__player.jump()


    def keydown_handler(self, key: int) -> None:
        if key == 65:  # A
            self.__player.vel = Vector(-3, 0)
            self.__player.current_animation = "RUN_LEFT"
        if key == 68:  # D
            self.__player.vel = Vector(3, 0)
            self.__player.current_animation = "RUN_RIGHT"

        if key == 86:  # V
            self.__ai.listen_and_respond()
