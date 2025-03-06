"""Button Module.

This module provides a custom implementation of a button using SimpleGUICS2Pygame.
It includes a Button class with style attributes and methods to handle rendering
and click events, as well as a ButtonStyle dataclass simplifying the customization of the button.

File:
    simplegui/components/button.py

Classes:
    ButtonStyle: A class storing the style attributes of a button.
    Button: A custom implementation of a simplegui button with methods to render the
            button and methods to check/handle button clicks.
"""
from dataclasses import dataclass, field
from typing import Callable, List

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector


@dataclass
class ButtonStyle:
    """A class storing the style properties of a button.

    Attributes:
        border_color (str): The color of the button border.
        border_width (int): The width of the button border.
        fill_color (str): The buttons background color.
        font_size (int): The size of the button text.
        font_color (str): The color of the button text.
        text_offset_x: The offset of the text - used to align text with button.
        text_offset_y: The offset of the text - used to align text with button.
    """

    border_color: str = field()
    border_width: int = field()
    fill_color: str = field()
    font_size: int = field()
    font_color: str = field()
    text_offset_x: int = 0
    text_offset_y: int = 0


class Button:
    """Custom implementation of a simplegui Button.

    Attributes:
        __pos (List[List[int]]): The position of the button.
        __text (str): The text which will be displayed on the button.
        __style (ButtonStyle): The style which will be applied to the button
        __text_pos (List[int]): The position of the text.

    Methods:
        render(canvas: simplegui.Canvas) -> None: Renders the button on the given canvas.
        handle_click(pos: Vector, method: Callable) -> None: Handles the click event.
        __is_clicked(pos: Vector) -> bool: Checks if the button has been clicked.
    """

    def __init__(self, pos: List[List[int]], text: str, style: ButtonStyle) -> None:
        self.__pos = pos
        self.__text = text
        self.__style = style

        self.__text_pos = [
            (pos[0][0] + pos[2][0]) // 2 + style.text_offset_x,
            (pos[0][1] + pos[2][1]) // 2 + style.text_offset_y,
        ]

    def render(self, canvas: simplegui.Canvas) -> None:
        """Renders the button on the given canvas.

        Args:
            canvas (simplegui.Canvas): the canvas the button should be rendered on
        """
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
        """Handles the click event.

        Args:
            pos (Vector): The position of the mouse click.
            method (Callable): The method to be executed if the button
                               is clicked.
        """
        if self.__is_clicked(pos):
            method()

    def __is_clicked(self, pos: Vector) -> bool:
        return (
            (pos.x > self.__pos[0][0])
            and (pos.x < self.__pos[2][0])
            and (pos.y > self.__pos[0][1])
            and (pos.y < self.__pos[2][1])
        )
