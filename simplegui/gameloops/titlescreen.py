from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle

from .abstract import GameLoop


class TitleScreen(GameLoop):
    def __init__(self, start_game: Callable) -> None:
        super().__init__()

        self.__start = Button(
            pos=[[300, 700], [500, 700], [500, 780], [300, 780]],
            text="start",
            style=ButtonStyle(
                border_color="Black",
                border_width=2,
                fill_color="White",
                font_size=40,
                font_color="Black",
                text_offset_x=-30,
                text_offset_y=6,
            ),
        )
        self.__start_game = start_game

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_text("Welcome to the Game", (200, 300), 50, "White")
        self.__start.render(canvas)

        if self._mouse.clicked:
            self.__start.handle_click(self._mouse.last_click, self.__start_game)

        self._mouse.update()

    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...
