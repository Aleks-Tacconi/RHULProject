import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity

class Trigger(Entity):
    def __init__(self, pos: Vector, size = Vector(0,0)) -> None:

        super().__init__(
            pos=Vector(int(pos.x), int(pos.y)),
            size=Vector(0, 0),
            hitbox=Vector(size.x + 2, size.y + 2)
        )

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        self._render_hitbox(canvas, offset_x, offset_y)

    def update(self) -> None:
        ...