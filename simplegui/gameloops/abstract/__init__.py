"""Package for GameLoop-related functionality.

This package contains the abstract base class GameLoop, which defines the structure 
and methods for implementing a game loop. Its intended to be used as a template to 
create a standardized format of implementing game loops.

Modules:
    gameloop:
        Classes:
            GameLoop: An abstract base class for implementing game loops.
"""

from .gameloop import GameLoop

__all__ = ["GameLoop"]
