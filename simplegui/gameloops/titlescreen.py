"""TitleScreen Module

This module defines the TitleScreen class which handles the rendering of
the title screen and handling io events of the buttons on the title screen

File:
    simplegui/gameloops/titlescreen.py

Classes:
    TitleScreen: The titles screen of the game.
"""

from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle, PlaySounds

from .abstract import GameLoop

class TitleScreen(GameLoop):
    """TitleScreen entity.

    Attributes:
        __music (simplegui.Sound): The music which will play in the background of the
                                   title screen

    Methods:
        mouseclick_handler(pos: Tuple[int, int]) -> None: Updates the mouse dataclass with
                                                                the most recent clicked position.
        mainloop(canvas: simplegui.Frame, *args) -> None: An implementation of a draw handler
        keyup_handler(key: int) -> None: Method to handle keyup events.
        keydown_handler(key: int) -> None: Method to handle keydown events.
        __render(canvas: simplegui.Canvas) -> None: Handles the drawing of the title screen
    """

    def __init__(self, start_game: Callable) -> None:
        super().__init__()


        self.sound_path = "TITLE_MUSIC.wav"
        self.music = PlaySounds(self.sound_path)


        button_style = ButtonStyle(
            border_color="Black",
            border_width=2,
            fill_color="White",
            font_size=40,
            font_color="Black",
            text_offset_x=-30,
            text_offset_y=6,
        )
        self.__start = Button(
            pos=[[300, 700], [500, 700], [500, 780], [300, 780]],
            text="start",
            style=button_style,
        )
        self.__start_game = start_game

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__render(canvas)
        self.music.play_sound()

        if self._mouse.clicked:
            #self.__start.handle_click(self._mouse.last_click, self.music.stop_sound)
            self.__start.handle_click(self._mouse.last_click, self.__start_game)

        self._mouse.update()

    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...

    def __render(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_text("Welcome to the Game", (250, 200), 100, "Black")
        self.__start.render(canvas)
