import os

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Enemy, PhysicsEntity
from .utils import Animation, SpriteSheet


class Fire(Enemy):
    def __init__(self, x) -> None:
        super().__init__(
            pos=Vector(x, 0),
            size=Vector(50, 50),
            hitbox=Vector(50, 50),
            vel=Vector(0, 3),
            hp=1,
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "fire", "Fire1.png"),
            rows=1,
            cols=8,
        )

        self.__animation = Animation(spritesheet, 8)

    def update(self) -> None:
        self.pos += self.vel
        self.pos.y = self.pos.y % 800
        self.__animation.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animation.render(canvas, pos, self.size)

    def set_idle(self) -> None:
        self.vel.x = 0

    def interaction(self, entity: PhysicsEntity) -> None: ...

    def remove(self) -> bool:
        if self.__animation.done and not self.is_alive:
            return True
        return False
