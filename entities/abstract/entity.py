from abc import ABCMeta, abstractmethod
from typing import List

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector


class Entity(metaclass=ABCMeta):
    id = 0
    blocks = []

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
        self.points = 0
        self.give_points = True
        self.friendly = True
        self.seen_player = False
        self.id = Entity.id
        Entity.blocks.append(self)
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

    def collides_with(self, entity) -> bool:
        x1, y1, x2, y2 = entity.hitbox_area
        a1, b1, a2, b2 = self.hitbox_area

        return x2 > a1 and x1 < a2 and y2 > b1 and y1 < b2

    def collides_with_crouch(self, entity) -> bool:
        x1, y1, x2, y2 = entity.hitbox_area
        a1, b1, a2, b2 = self.hitbox_area

        return y1 < b2

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

    def healthbar(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int):
        hitbox = self.hitbox_area
        canvas.draw_polygon([[hitbox[0] + offset_x, hitbox[1] - 10 + offset_y],
                        [hitbox[2] + offset_x, hitbox[1] - 10 + offset_y],
                            [hitbox[2] + offset_x,hitbox[1 ] - 15 + offset_y],
                            [hitbox[0] + offset_x,hitbox[1 ] - 15 + offset_y]], 5, 'Red')
        canvas.draw_polygon([[hitbox[0] - 1 + offset_x, hitbox[1] - 9 + offset_y],
                        [hitbox[2] + 1 + offset_x, hitbox[1] - 9 + offset_y],
                            [hitbox[2] + 1 + offset_x,hitbox[1 ] - 16 + offset_y],
                            [hitbox[0] - 1 + offset_x,hitbox[1 ] - 16 + offset_y]], 3, 'White')

    @abstractmethod
    def render(
        self, canvas: simplegui.Canvas, offset_x: int, offset_y: int
    ) -> None: ...

    def set_idle(self) -> None:
        ...

    @abstractmethod
    def update(self) -> None: ...
