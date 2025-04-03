from abc import ABCMeta, abstractmethod

from utils import Vector
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from .entity import Entity
import random

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
        level_id: str,
        hitbox_offset: Vector = Vector(0, 0),
        direction="LEFT",
    ) -> None:
        super().__init__(pos, size, hitbox, hitbox_offset)

        self.vel = vel
        self._level_id = level_id
        self.hp = hp
        self.xp = 50
        self.immune = False
        self.__max_gravity = 10
        self.__gravity_strength = 0.8
        self.__original_hp = self.hp
        self.__new_hp = self.hp
        self.boss = False
        self.id = PhysicsEntity.id
        self.knockback_received_multiplier_x = 10
        self.knockback_received_multiplier_y = 10
        self.knockback_given_multiplier_x = 2
        self.knockback_given_multiplier_y = 2
        self.knockback_chance = 0.3
        self.knockback_chance_multiplier = 1
        self.direction = direction
        PhysicsEntity.id += 1

        PhysicsEntity.all.append(self)

    def healthbar(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int):
        hitbox = self.hitbox_area
        health_percentage = (self.hp / self.__original_hp)
        hitbox_difference = hitbox[2] - hitbox[0]

        if self.hp > 0:
            canvas.draw_polygon([[hitbox[0] + offset_x,
                                  hitbox[1] - 10 + offset_y],
                            [min(hitbox[2] + offset_x, hitbox[0] + offset_x + hitbox_difference * health_percentage),
                             hitbox[1] - 10 + offset_y],
                                [min(hitbox[2] + offset_x, hitbox[0] + offset_x + hitbox_difference * health_percentage),
                                 hitbox[1 ] - 15 + offset_y],
                                [hitbox[0] + offset_x,hitbox[1 ] - 15 + offset_y]], 5, 'Red')
        if not self.boss:
            canvas.draw_polygon([[hitbox[0] - 1 + offset_x, hitbox[1] - 9 + offset_y],
                            [hitbox[2] + 1 + offset_x, hitbox[1] - 9 + offset_y],
                                [hitbox[2] + 1 + offset_x,hitbox[1 ] - 16 + offset_y],
                                [hitbox[0] - 1 + offset_x,hitbox[1 ] - 16 + offset_y]], 3, 'White')

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

    def _knockback(self, entity) -> None:
        if self.__new_hp != self.hp:
            self.__new_hp = self.hp
            if random.random() < self.knockback_chance * self.knockback_chance_multiplier:
                if entity.direction == "RIGHT":
                    self.vel.x += 1 * (self.knockback_received_multiplier_x + entity.knockback_given_multiplier_x)
                    self.vel.y -= 1 * (self.knockback_received_multiplier_y + entity.knockback_given_multiplier_y)
                else:
                    self.vel.x -= 1 * (self.knockback_received_multiplier_x + entity.knockback_given_multiplier_x)
                    self.vel.y -= 1 * (self.knockback_received_multiplier_y + entity.knockback_given_multiplier_y)

    @abstractmethod
    def remove(self) -> bool: ...
