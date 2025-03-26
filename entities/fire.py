import os

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities.attack import Attack
from utils import Vector

from .abstract import Enemy, PhysicsEntity
from .utils import Animation, SpriteSheet


class Fire(Enemy):
    def __init__(self, x) -> None:
        super().__init__(
            pos=Vector(x, 0),
            size=Vector(50, 50),
            hitbox=Vector(0, 0),
            vel=Vector(0, 10),
            hp=1,
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "fire", "Fire1.png"),
            rows=1,
            cols=8,
        )
        self.__detection_range_x = 20
        self.__detection_range_y = 10
        self.__hascollided = False

        self.__animation = Animation(spritesheet, 8)

    def update(self) -> None:
        self.pos += self.vel
        if not self.__hascollided:
            self.pos.y = self.pos.y
        self.__animation.update()
        self.remove()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animation.render(canvas, pos, self.size)

    def __idle(self) -> None:
        self.vel.x = 0

    def interaction(self, entity: PhysicsEntity) -> None:
        distance_x = self.pos.x - entity.pos.x
        distance_y = self.pos.y - entity.pos.y

        if abs(distance_x) < self.__detection_range_x and abs(distance_y) < self.__detection_range_y:
            Attack(
                pos=self.pos,
                hitbox=Vector(50, 50),
                hitbox_offset=None,
                damage=1000,
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
    
    #TODO add a method that detects if the fire collides with the minecraft block. If it does, also remove the item from entity list.
