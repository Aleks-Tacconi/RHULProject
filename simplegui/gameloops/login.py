from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle
from utils.score import SCORE

from .abstract import GameLoop


class Login(GameLoop):
    def __init__(self, back: Callable) -> None:
        super().__init__()
        self.__username = ""
        self.__password = ""
        self.__focus = "username"
        self.__back = back

        pos = [[300, 320], [500, 320], [500, 350], [300, 350]]
        self.__username_button = Button(
            pos=[[x, y - 160] for x, y in pos],
            text="",
            style=ButtonStyle(
                border_color="White",
                border_width=2,
                fill_color="Black",
                font_size=20,
                font_color="Black",
                text_offset_x=-30,
                text_offset_y=6,
            ),
        )

        self.__password_button = Button(
            pos=[[x, y - 120] for x, y in pos],
            text="",
            style=ButtonStyle(
                border_color="White",
                border_width=2,
                fill_color="Black",
                font_size=20,
                font_color="Black",
                text_offset_x=-30,
                text_offset_y=6,
            ),
        )

        self.__confirm = Button(
            pos=[[x, y - 80] for x, y in pos],
            text="Login",
            style=ButtonStyle(
                border_color="White",
                border_width=2,
                fill_color="White",
                font_size=20,
                font_color="Black",
                text_offset_x=-30,
                text_offset_y=6,
            ),
        )

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__confirm.render(canvas)
        self.__password_button.render(canvas)
        self.__username_button.render(canvas)

        canvas.draw_text(self.__username, [310, 180], 20, "White")
        canvas.draw_text(self.__password, [310, 220], 20, "White")

        if self._mouse.clicked:
            self.__password_button.handle_click(
                self._mouse.last_click, self.__focus_password
            )
            self.__username_button.handle_click(
                self._mouse.last_click, self.__focus_username
            )
            self.__confirm.handle_click(self._mouse.last_click, self.__login)
            self._mouse.clicked = False

    def __login(self) -> None:
        if SCORE.login(self.__username, self.__password):
            self.__back()

    def __focus_username(self) -> None:
        self.__focus = "username"

    def __focus_password(self) -> None:
        self.__focus = "password"

    def keydown_handler(self, key: int) -> None:
        # TODO:
        if key == 8:
            if self.__focus == "username":
                if self.__username:
                    self.__username = self.__username[: len(self.__username) - 2]
            if self.__focus == "password":
                if self.__password:
                    self.__password = self.__password[: len(self.__password) - 2]

            return

        try:
            key = chr(key).lower()
            print(key)
            if self.__focus == "username":
                self.__username += key
                self.__username = self.__username[:12]
            if self.__focus == "password":
                self.__password += key
                self.__password = self.__password[:12]
        except:
            pass

    def keyup_handler(self, key: int) -> None: ...
