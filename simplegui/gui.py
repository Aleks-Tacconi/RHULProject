# -*- coding: utf-8 -*-
"""GUI module.

This module defines the GUI class, which is responsible for creating and managing
the graphical user interface (GUI) and controlling the execution of the mainloop.

File:
    simplegui/gui.py

Classes:
    GUI: A class responsible for creating and managing the GUI of the game.
"""

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities import Player
from utils.vector import Vector

from .gameloops import MainLoop, TitleScreen
from .gameloops.abstract import GameLoop


class GUI:
    """A class responsible for creating and managing the GUI of the game.

    Attributes:
        __frame (simplegui.Frame): The frame object used for rendering and input handling.

    Methods:
        __set_draw_handler(gameloop: GameLoop, *args) -> None: Sets up the drawing and input
                                                               handlers for the given game loop.
        start() -> None: Entry point for the game.
        stop() -> None: Ends the game.
    """

    def __init__(self, title: str, width: int, height: int) -> None:
        self.__frame = simplegui.create_frame(title, width, height)

        player = Player(Vector(400, 400))
        mainloop = MainLoop(player)

        title_screen = TitleScreen(lambda: self.__set_draw_handler(mainloop))
        self.__set_draw_handler(title_screen)

    def __set_draw_handler(self, gameloop: GameLoop) -> None:
        self.__frame.set_draw_handler(gameloop.mainloop)
        self.__frame.set_keyup_handler(gameloop.keyup_handler)
        self.__frame.set_keydown_handler(gameloop.keydown_handler)
        self.__frame.set_mouseclick_handler(gameloop.mouseclick_handler)

    def start(self) -> None:
        """Entry point for the game."""
        self.__frame.start()

    def stop(self) -> None:
        """Ends the game."""
        self.__frame.stop()
