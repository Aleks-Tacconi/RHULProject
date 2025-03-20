import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities import Player
from utils import Vector

from .abstract import PhysicsEntity
from .utils import SpriteSheet
from .utils.animation import Animation

class Fire(PhysicsEntity):
    def __init__(self, x) -> None:
        super().__init__(pos=Vector(x, 0), size=Vector(50, 50), vel=Vector(0, 3), health=1)

        spritesheet = SpriteSheet(
            os.path.join("assets", "fire", "Fire1.png"),
            rows=1,
            cols=8,
        )

        self.animation = Animation(spritesheet, 8)

    def update(self) -> None:
        self.pos.add(self.vel)
        self.pos.y = self.pos.y % 800
        self.animation.update()

    def render(self, canvas):
        self.animation.render(canvas, self.pos, self.size)
