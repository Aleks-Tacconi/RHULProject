import os

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities.attack import Attack
from entities.block import Block
from entities.player import Player
from utils import Vector

from .abstract import Enemy, PhysicsEntity
from .utils import Animation, SpriteSheet


class LeftFireball(Enemy):
    def __init__(self, x: int, y: int, level_id: str) -> None:
        super().__init__(
            pos=Vector(x, y),
            size=Vector(50, 50),
            hitbox=Vector(0, 0),
            vel=Vector(-5, 0),
            hp=1,
            level_id=level_id,
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "fireball", "FIREBALL_FLIPPED.png"),
            rows=1,
            cols=5,
        )

        self.__detection_range_x = 30
        self.__detection_range_y = 4
        self.__hascollided = False

        self.__animations = Animation(spritesheet, 1)

    def update(self) -> None:
        self.pos += self.vel
        if not self.__hascollided:
            self.pos.y = self.pos.y
        self.__animations.update()
        self.remove()

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)
        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)

    def __idle(self) -> None:
        self.vel.x = 0

    def interaction(self, entity: Player) -> None:
        distance_x = self.pos.x - entity.pos.x
        distance_y = self.pos.y - entity.pos.y

        if abs(distance_x) < self.__detection_range_x and abs(distance_y) < self.__detection_range_y:
            Attack(
                pos=self.pos,
                hitbox=Vector(2, 2),
                hitbox_offset=None,
                damage=500,
                owner=self
            )

            self.__hascollided = True

    def remove(self) -> bool:
        # if self.__animation.done and not self.is_alive:
        #     return True
        # return False
        if self.pos.y > 800:
            return True

        return self.__hascollided
    
class RightFireball(Enemy):
    def __init__(self, x: int, y: int, level_id: str) -> None:
        super().__init__(
            pos=Vector(x, y),
            size=Vector(50, 50),
            hitbox=Vector(0, 0),
            vel=Vector(5, 0),
            hp=1,
            level_id=level_id,
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "fireball", "FIREBALL.png"),
            rows=1,
            cols=5,
        )

        self.__detection_range_x = 20
        self.__detection_range_y = 20
        self.__hascollided = False

        self.__animations = Animation(spritesheet, 1)

    def update(self) -> None:
        self.pos += self.vel
        if not self.__hascollided:
            self.pos.y = self.pos.y
        self.__animations.update()
        self.remove()

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)
        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)

    def __idle(self) -> None:
        self.vel.x = 0

    def interaction(self, entity: Player) -> None:
        distance_x = self.pos.x - entity.pos.x
        distance_y = self.pos.y - entity.pos.y

        if abs(distance_x) < self.__detection_range_x and abs(distance_y) < self.__detection_range_y:
            Attack(
                pos=self.pos,
                hitbox=Vector(2, 2),
                hitbox_offset=None,
                damage=1000,
                owner=self
            )

            self.__hascollided = True

    def remove(self) -> bool:
        if self.pos.y > 800:
            return True

        return self.__hascollided
    
