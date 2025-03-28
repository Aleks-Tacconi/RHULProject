from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle, PlaySounds
from .abstract import GameLoop


class TitleScreen(GameLoop):
    def __init__(self, start_game: Callable, level_editor: Callable) -> None:
        super().__init__()

        sound_path = "TITLE_MUSIC.wav"
        self.__music = PlaySounds(sound_path)

        self.__start = Button(
            pos=[[300, 280], [500, 280], [500, 330], [300, 330]],
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

        self.__editor = Button(
            pos=[[300, 340], [500, 340], [500, 390], [300, 390]],
            text="Level Editor",
            style=ButtonStyle(
                border_color="Black",
                border_width=2,
                fill_color="White",
                font_size=20,
                font_color="Black",
                text_offset_x=-30,
                text_offset_y=6,
            ),
        )
        self.__start_game = start_game
        self.__level_editor = level_editor

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_text("Knightborne", (200, 200), 50, "White")
        self.__start.render(canvas)
        self.__editor.render(canvas)
        self.__music.play_sound()

        if self._mouse.clicked:
            self.__start.handle_click(self._mouse.last_click, self.__start_game)
            self.__editor.handle_click(self._mouse.last_click, self.__level_editor)

        self._mouse.update()

    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...
