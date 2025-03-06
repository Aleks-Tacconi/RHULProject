"""Package containing custom SimpleGUICS2Pygame components

This package contains custom implementation of SimpleGUICS2Pygame components which
the package does not provide, for example buttons which can be rendered on a
SimpleGUICS2Pygame.simpleguics2pygame.Canvas

modules:
    button:
        classes:
            ButtonStyle: A class storing the style attributes of a button.
            Button: A custom implementation of a simplegui button with methods to render the
                    button and methods to check/handle button clicks.
"""
from .button import ButtonStyle, Button

__all__ = ["ButtonStyle", "Button"]
