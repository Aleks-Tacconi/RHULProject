import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity
from .utils import Animation, SpriteSheet


class BackgroundOne(Entity):
    def __init__(self, pos: Vector, img: str) -> None:
        super().__init__(
            pos=Vector(int(pos.x * 400), int(pos.y * 400)),
            size=Vector(400, 400),
            hitbox=Vector(0, 0),
        )

        self.__animation = Animation(
            spritesheet=SpriteSheet(img, rows=1, cols=1),
            frames_per_sprite=1,
        )

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animation.render(canvas, pos, self.size)

    def update(self) -> None: ...





