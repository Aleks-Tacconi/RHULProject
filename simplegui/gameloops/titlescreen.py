import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import Background
from simplegui.components import Button, ButtonStyle
from utils import Vector

from .abstract import GameLoop


class TitleScreen(GameLoop):
    def __init__(
        self,
        start_game: Callable,
        tutorial: Callable,
        level_editor: Callable,
        login_func: Callable,
        login: bool,
    ) -> None:
        super().__init__()

        sound_path = "TITLE_MUSIC.wav"
        self.__start = Button(
            pos=[[300, 240], [500, 240], [500, 270], [300, 270]],
            text="Start",
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

        self.__settings = Button(
            pos=[[300, 280], [500, 280], [500, 310], [300, 310]],
            text="Settings",
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

        self.__tutorials = Button(
            pos=[[300, 320], [500, 320], [500, 350], [300, 350]],
            text="Tutorial",
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

        self.__editor = Button(
            pos=[[300, 360], [500, 360], [500, 390], [300, 390]],
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

        self.__login = Button(
            pos=[[595, 5], [795, 5], [795, 35], [595, 35]],
            text="login",
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
        self.__tutorial = tutorial
        self.__level_editor = level_editor
        self.__login_func = login_func
        self.__music_is_playing = False

        self.__title_background = Background(
            pos=Vector(404, 200),
            img=os.path.join("assets", "background", "titlescreen.png"),
            size_x=540,
            size_y=304,
            scale_factor=1.5,
            frames=3,
            cols=9,
        )
        self.__login_status = login

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__title_background.render(canvas, 0, 0)
        self.__title_background.update()
        canvas.draw_text("Knightborne", (280, 50), 50, "White")
        self.__start.render(canvas)
        self.__settings.render(canvas)
        self.__tutorials.render(canvas)
        self.__editor.render(canvas)
        self.__login.render(canvas)

        if self.__login_status:
            canvas.draw_text("login successfull!", [600, 60], 20, "White")

        if not self.__music_is_playing:
            self.__music_is_playing = True

        if self._mouse.clicked:
            self.__start.handle_click(self._mouse.last_click, self.__start_game)
            self.__tutorials.handle_click(self._mouse.last_click, self.__tutorial)
            self.__editor.handle_click(self._mouse.last_click, self.__level_editor)
            self.__login.handle_click(self._mouse.last_click, self.__login_func)

        self._mouse.update()

    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...
