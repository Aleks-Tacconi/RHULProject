import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity

class Trigger(Entity):
    def __init__(self, entity,  pos: Vector, size = Vector(0,0)) -> None:

        super().__init__(
            pos=Vector(int(pos.x), int(pos.y)),
            size=Vector(0, 0),
            hitbox=Vector(size.x + 2, size.y + 2)
        )
        self.__entity = entity

    def at_trigger(self) -> bool:
        return self.collides_with(self.__entity)

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        self._render_hitbox(canvas, offset_x, offset_y)

    def interact(self, function):
        if self.at_trigger() and self.__entity.interacting:
            function()

    def update(self) -> None:
        ...