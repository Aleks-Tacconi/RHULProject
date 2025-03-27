from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle

from .abstract import GameLoop


class TitleScreen(GameLoop):
    def __init__(self, start_game: Callable) -> None:
        super().__init__()

        sound_path = "TITLE_MUSIC.wav"
        # self.__music = PlaySounds(sound_path)

        self.__start = Button(
            pos=[[300, 300], [500, 300], [500, 380], [300, 380]],
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
        canvas.draw_text("Welcome to the Game", (200, 200), 50, "White")
        self.__start.render(canvas)
        # self.__music.play_sound()

        if self._mouse.clicked:
            self.__start.handle_click(self._mouse.last_click, self.__start_game)

        self._mouse.update()

    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...
