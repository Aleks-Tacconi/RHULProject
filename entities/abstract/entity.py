from abc import ABCMeta, abstractmethod
from typing import List

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector


class Entity(metaclass=ABCMeta):
    id = 0

    def __init__(
        self,
        pos: Vector,
        size: Vector,
        hitbox: Vector,
        hitbox_offset: Vector = Vector(0, 0),
    ) -> None:
        self.pos = pos
        self.size = size
        self.hitbox = hitbox
        self.hitbox_offset = hitbox_offset

        self.id = Entity.id
        Entity.id += 1

    @property
    def hitbox_area(self) -> List[int | float]:
        half_width = self.hitbox.x // 2
        half_height = self.hitbox.y // 2

        x1 = self.pos.x - half_width + self.hitbox_offset.x
        x2 = self.pos.x + half_width + self.hitbox_offset.x

        y1 = self.pos.y - half_height + self.hitbox_offset.y
        y2 = self.pos.y + half_height + self.hitbox_offset.y

        return [x1, y1, x2, y2]

    def _render_hitbox(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        canvas.draw_polygon(
            [
                [self.hitbox_area[0] + offset_x, self.hitbox_area[1] + offset_y],
                [self.hitbox_area[2] + offset_x, self.hitbox_area[1] + offset_y],
                [self.hitbox_area[2] + offset_x, self.hitbox_area[3] + offset_y],
                [self.hitbox_area[0] + offset_x, self.hitbox_area[3] + offset_y],
            ],
            3,
            "red",
        )

    @abstractmethod
    def render(
        self, canvas: simplegui.Canvas, offset_x: int, offset_y: int
    ) -> None: ...

    def set_idle(self) -> None:
        ...

    @abstractmethod
    def update(self) -> None: ...
