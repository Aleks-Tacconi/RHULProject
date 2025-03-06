"""PhysicsEntity module.

This module defines the PhysicsEntity class, which extends on the functionality
of the Entity class, providing a standardized way of creating entities which can
interact with other entities.

File:
    entities/abstract/physics_entity.py

Classes:
    Entity: representation of an physics entity in the game.
            Inherits from entity with additional methods / attrs to 
            deal with physics / interactions.
"""

from abc import ABCMeta

from utils import Vector

from .entity import Entity


class PhysicsEntity(Entity, metaclass=ABCMeta):
    """PhysicsEntity Object

    Attributes:
        _pos (Vector): The position of the entity.
        _size (Vector): The size of the entity.
        vel (Vector): The velocity of the entity.
        area (List[int | float]): The bounding box of the entity calculated
                                  from the entities position and size.

    Methods:
        collides_with(entity: Entity) -> bool: Checks if the entity collides with another entity.

    Abstract Methods:
        render(canvas: simplegui.Frame) -> None: Renders the entity onto the canvas.
        update() -> None: Updates the state of the Entity.
    """

    def __init__(self, pos: Vector, size: Vector, vel: Vector) -> None:
        super().__init__(pos, size)

        self.vel = vel

    def collides_with(self, entity: Entity) -> bool:
        """Checks if the entity collides with another entity.

        This method implements a simple collision detection using the PhysicsEntity's
        midpoint and checking weather its contained within the Entities bounding box

        Args:
            entity (Entity): The entity to check for collision with.

        Returns:
            bool: True if the entity collides with the other entity, False otherwise.
        """

        collision_x = [entity.area[0], entity.area[1]]
        collision_y = [entity.area[1], entity.area[2]]

        return (
            (self._pos.x > min(collision_x))
            and (self._pos.x < max(collision_x))
            and (self._pos.y > min(collision_y))
            and (self._pos.y < max(collision_y))
        )
