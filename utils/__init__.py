"""Package providing utilities to be used throughout the game.

Modules:
    vector:
        Classes:
            Vector: A class for dealing with 2D Vector coordinates.
    
    mouse:
        Classes:
            Mouse: A dataclass that stores the last mouse click position and click state.
"""

from .vector import Vector
from .mouse import Mouse

__all__ = ["Vector", "Mouse"]
