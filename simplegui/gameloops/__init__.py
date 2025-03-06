"""package providing implementations of game loops that can be ran through the GUI module.

This package contains the main game loops responsible for managing the game state and transitions
between different stages of the game.

Modules:
    titlescreen:
        Classes:
            TitleScreen: The title screen of the game.

    mainloop:
        Classes:
            MainLoop: The main loop of the game.
"""

from .mainloop import MainLoop
from .titlescreen import TitleScreen

__all__ = ["TitleScreen", "MainLoop"]
