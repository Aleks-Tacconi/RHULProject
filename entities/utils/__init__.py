"""Package with utilities for entities

This package includes utilities applicable to any subclass of the Entity class,

Modules:
    animation:
        Functions:
            file: Returns the appropriate prefix for file paths depending on users OS.

        Classes:
            SpriteSheet: Dataclass storing the attributes of a sprite sheet.
            Animation: An animation entity that updates and renders the sprite.
"""

from .animation import Animation, SpriteSheet, file

__all__ = ["Animation", "SpriteSheet", "file"]
