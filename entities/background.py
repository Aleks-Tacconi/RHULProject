import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity

from .utils import Animation, SpriteSheet

class Background(Entity):
    def __init__(self, pos: Vector, img: str, size_x: int, size_y: int,
                 scale_factor: int, frames: int=1, cols: int=1, rows: int=1) -> None:

        original_size_x = size_x
        original_size_y = size_y
        scale_factor = scale_factor
        scaled_size_x = original_size_x * scale_factor
        scaled_size_y = original_size_y * scale_factor

        super().__init__(
            pos=Vector(int(pos.x), int(pos.y)),
            size=Vector(scaled_size_x, scaled_size_y),
            hitbox=Vector(scaled_size_x, scaled_size_y)
        )

        spritesheet = SpriteSheet(img, rows = rows, cols = cols)

        self.__animations = Animation(spritesheet, frames)

    def update(self) -> None:
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

