"""Package with implementation of entities which can be used in a platformer game.

This package provides classes that represent various entities in a platformer game.
The entities provided by this package can be used to create and manage different characters
or objects in the game.

Modules:
    player:
        Classes:
            Player: Represents the player entity with animations and movement logic.
"""

from .player import Player

__all__ = ["Player"]
