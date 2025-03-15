"""Player module.

This module defines the Player class, which is an implementation of the 
PhysicsEntity class and acts as the main player in the game. This class handles the
actions and rendering of the player.

File:
    entities/player.py

Classes:
    Player: Represents the player entity with animations and movement logic.
"""

import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import PhysicsEntity
from .utils import Animation, SpriteSheet

class Player(PhysicsEntity):
    """Player entity

    This is a implementation of the abstract base class PhysicsEntity which represents
    the playable character implementing actions such as rendering and handling the players
    movement.

    Attributes:
        current_animation: The current player animation.
        __animations (Dict[str, Animation]): A list of animations that can be rendered.

    Methods:
        render(canvas: simplegui.Frame) -> None: Renders the player onto the canvas.
        update() -> None: Updates the state of the player.
    """
    def __init__(self, pos: Vector) -> None:
        super().__init__(pos=pos, size=Vector(200, 200), vel=Vector(0, 0))

        self.__animations = {
            "IDLE_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "IDLE.png"), rows=1, cols=5
                ),
                frames_per_sprite=15,
            ),
            "IDLE_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "IDLE.png"), rows=1, cols=5
                ).flip(),
                frames_per_sprite=15,
            ),
            "RUN_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "RUN.png"), rows=1, cols=8
                ),
                frames_per_sprite=15,
            ),
            "RUN_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "RUN.png"), rows=1, cols=8
                ).flip(),
                frames_per_sprite=15,
            ),
        }

        self.current_animation = "IDLE_RIGHT"

    def update(self) -> None:
        self._pos += self.vel
        self.__animations[self.current_animation].update()

    def render(self, canvas: simplegui.Canvas) -> None:
        self.__animations[self.current_animation].render(canvas, self._pos, self._size)
