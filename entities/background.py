import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity

from .utils import Animation, SpriteSheet

class Background(Entity):
    def __init__(self, pos: Vector, img: str, size_x: int, size_y: int, scale_factor: int) -> None:

        original_size_x = size_x
        original_size_y = size_y
        scale_factor = scale_factor
        scaled_size_x = original_size_x * scale_factor
        scaled_size_y = original_size_y * scale_factor

        super().__init__(
            pos=Vector(int(pos.x), int(pos.y)),
            size=Vector(scaled_size_x, scaled_size_y),
            hitbox=Vector(0,0)
        )

        spritesheet = SpriteSheet(img, rows = 1, cols = 1)

        self.__animation = Animation(spritesheet, 1)

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animation.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

    def update(self) -> None:
        ...
