import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity

from .utils import Animation, SpriteSheet

class Cinematic(Entity):
    def __init__(self) -> None:

        super().__init__(
            pos=Vector(int(405), int(205)),
            size=Vector(810, 410),
            hitbox=Vector(0, 0)
        )

        spritesheet = SpriteSheet(os.path.join("assets", "player_gui", "CINEMATIC_BARS.png"), rows = 1, cols = 1)

        self.__animations = Animation(spritesheet, 1)

        self.cinematic_bars = False

    def update(self) -> None:
        ...

    def render(self, canvas: simplegui.Canvas) -> None:
        if self.cinematic_bars:
            pos = Vector(int(self.pos.x), int(self.pos.y))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, 0, 0)