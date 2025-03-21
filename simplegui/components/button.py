from dataclasses import dataclass, field
from typing import Callable, List

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector


@dataclass
class ButtonStyle:
    border_color: str = field()
    border_width: int = field()
    fill_color: str = field()
    font_size: int = field()
    font_color: str = field()
    text_offset_x: int = 0
    text_offset_y: int = 0


class Button:
    def __init__(self, pos: List[List[int]], text: str, style: ButtonStyle) -> None:
        self.__pos = pos
        self.__text = text
        self.__style = style

        self.__text_pos = [
            (pos[0][0] + pos[2][0]) // 2 + style.text_offset_x,
            (pos[0][1] + pos[2][1]) // 2 + style.text_offset_y,
        ]

    def render(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_polygon(
            self.__pos,
            self.__style.border_width,
            self.__style.border_color,
            self.__style.fill_color,
        )

        canvas.draw_text(
            self.__text,
            self.__text_pos,
            self.__style.font_size,
            self.__style.font_color,
        )

    def handle_click(self, pos: Vector, method: Callable) -> None:
        if self.__is_clicked(pos):
            method()

    def __is_clicked(self, pos: Vector) -> bool:
        return (
            (pos.x > self.__pos[0][0])
            and (pos.x < self.__pos[2][0])
            and (pos.y > self.__pos[0][1])
            and (pos.y < self.__pos[2][1])
        )
