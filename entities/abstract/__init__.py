"""Package for abstract implementation of entities

This package defines base entity classes used for game objects, including 
both generic entities and physics-based entities with additional functionality.

Modules:
    physics_entity:
        Classes:
            Entity: representation of an physics entity in the game.
                    Inherits from entity with additional methods / attrs to
                    deal with physics / interactions. 
    entity:
        Classes:
            Entity: representation of an entity in the game.
"""

from .entity import Entity
from .physics_entity import PhysicsEntity

__all__ = ["Entity", "PhysicsEntity"]
