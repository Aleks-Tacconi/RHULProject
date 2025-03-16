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
        super().__init__(pos=pos, size=Vector(200, 200), vel=Vector(0, 0), health=300)
        self.death_anim_length = 23 * 5

        spritesheet = SpriteSheet(
            os.path.join("assets", "abyssal_revenant", "ABYSSAL_REVENANT.png"),
            rows=5,
            cols=23,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "IDLE_RIGHT": (0, 9, 9, 9, False),
            "IDLE_LEFT": (0, 23, 9, 9, True),
            "RUN_RIGHT": (1, 6, 6, 6, False),
            "RUN_LEFT": (1, 23, 6, 6, True),
            "ATTACK_RIGHT": (2, 12, 12, 12, False),
            "ATTACK_LEFT": (2, 23, 12, 12, True),
            "Hurt_RIGHT": (3, 5, 5, 5, False),
            "Hurt_LEFT": (3, 23, 5, 5, True),
            "DEATH_RIGHT": (4, 23, 23, 9, False),
            "DEATH_LEFT": (4, 23, 23, 9, True),
        }, default="IDLE_LEFT"
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
        attack_distance = 100
        speed = 3

        distance_x = self.pos.x - player.pos.x
        self.take_damage(1)
        print(self.health)

        if self.alive:
            if distance_x < detection_range:
                if distance_x < attack_distance:
                    self.vel.x = 0
                    if distance_x > 0:
                        self.__animations.set_animation("ATTACK_LEFT")
                    else:
                        self.__animations.set_animation("ATTACK_RIGHT")
                else:
                    if  distance_x < 0:
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

        if self.death():
            self.vel.x = 0
            if "LEFT" in self.current_animation:
                self.__animations.set_animation("DEATH_LEFT")
            else:
                self.__animations.set_animation("DEATH_RIGHT")

