"""Abyssal Revenant entity

This is a implementation of the abstract base class PhysicsEntity which represents
an enemy.

Attributes:
    current_animation: The current player animation.
    __animations (Dict[str, Animation]): A list of animations that can be rendered.

Methods:
    render(canvas: simplegui.Frame) -> None: Renders the player onto the canvas.
    update() -> None: Updates the state of the player.
"""

import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities import Player
from utils import Vector

from .abstract import PhysicsEntity
from .utils import SpriteSheet
from .block import Block
from .utils.animation import MultiAnimation


class AbyssalRevenant(PhysicsEntity):
    def __init__(self, pos: Vector) -> None:
        super().__init__(pos=pos, size=Vector(200, 200), vel=Vector(0, 0))

        spritesheet = SpriteSheet(
            os.path.join("assets", "abyssal_revenant", "ABYSSAL_REVENANT.png"),
            rows=5,
            cols=23,
        )

        self.__animations = MultiAnimation(
            spritesheet=spritesheet,
            animations={
                "IDLE_RIGHT": (0, 9, 9, False),
                "IDLE_LEFT": (0, 23, 9, True),
                "RUN_RIGHT": (1, 6, 6, False),
                "RUN_LEFT": (1, 23, 6, True),
            },
            current_anim="IDLE_LEFT",
        )

        self.current_animation = self.__animations.get_animation()

    def update(self) -> None:
        self.pos.x += self.vel.x
        Block.collisions_x(self, -80, -30)
        self.pos.y += self.vel.y
        Block.collisions_y(self, -80, -30)
        self.__animations.update()
        self._gravity()

    def render(self, canvas: simplegui.Canvas) -> None:
        self.__animations.render(canvas, self.pos, self.size)

    def interaction(self, player: Player):
        detection_range = 300
        speed = 3

        distance_x = self.pos.x - player.pos.x

        if distance_x < detection_range:
            if distance_x < 0:
                self.vel.x = speed
                self.__animations.set_animation("RUN_RIGHT")
            elif distance_x > 0:
                self.vel.x = -speed
                self.__animations.set_animation("RUN_LEFT")
        else:
            self.vel.x = 0
            if "LEFT" in self.current_animation:
                self.__animations.set_animation("IDLE_LEFT")
            else:
                self.__animations.set_animation("IDLE_RIGHT")
