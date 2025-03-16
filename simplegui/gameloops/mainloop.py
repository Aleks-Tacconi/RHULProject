"""MainLoop Module.

This module defines the MainLoop class which is the actual event loop.
This defines all the interactions between entities as well as rendering
the map and entities on the map themselves.

File:
    simplegui/gameloops/mainloop.py

Classes:
    MainLoop: The main loop of the game.
"""

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import Player, AbyssalRevenant
from utils import Vector
from ai import AI

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
        self.__player = Player(Vector(100, 400))
        self.__enemies = [AbyssalRevenant(Vector(700, 400))]
        self.__ai = AI()

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        for enemy in self.__enemies:
            enemy.render(canvas)
            enemy.update()
            enemy.interaction(self.__player)

        self.__player.render(canvas)
        self.__player.update()
        self.remove_dead()

    def keyup_handler(self, key: int) -> None:
        if key == 65: # A
            self.__player.vel = Vector(0, 0)
            self.__player.current_animation = "IDLE_LEFT"
        if key == 68: # D
            self.__player.vel = Vector(0, 0)
            self.__player.current_animation = "IDLE_RIGHT"

    def keydown_handler(self, key: int) -> None:
        if key == 65: # A
            self.__player.vel = Vector(-5, 0)
            self.__player.current_animation = "RUN_LEFT"
        if key == 68: # D
            self.__player.vel = Vector(5, 0)
            self.__player.current_animation = "RUN_RIGHT"

        if key == 86: # V
            self.__ai.listen_and_respond()

    def remove_dead(self):
        self.__enemies = [enemy for enemy in self.__enemies if not enemy.dead]

