from abc import ABCMeta, abstractmethod

from utils import Vector

from .entity import Entity


class PhysicsEntity(Entity, metaclass=ABCMeta):
    all = []
    id = 0

    def __init__(
        self,
        pos: Vector,
        size: Vector,
        hitbox: Vector,
        vel: Vector,
        hp: int,
        hitbox_offset: Vector = Vector(0, 0),
    ) -> None:
        super().__init__(pos, size, hitbox, hitbox_offset)

        self.vel = vel
        self.hp = hp
        self.immune = False
        self.direction = None
        self.__max_gravity = 10
        self.__gravity_strength = 0.8

        self.id = PhysicsEntity.id
        PhysicsEntity.id += 1

        PhysicsEntity.all.append(self)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def _gravity(self) -> None:
        self.vel.y = min(self.__max_gravity, self.vel.y + self.__gravity_strength)

    def collides_with(self, entity: Entity) -> bool:
        x1, y1, x2, y2 = entity.hitbox_area
        a1, b1, a2, b2 = self.hitbox_area

        return x2 > a1 and x1 < a2 and y2 > b1 and y1 < b2

    def _get_direction(self) -> None:
        if self.vel.x > 0:
            self.direction = "RIGHT"
        elif self.vel.x < 0:
            self.direction = "LEFT"

    @abstractmethod
    def remove(self) -> bool: ...
