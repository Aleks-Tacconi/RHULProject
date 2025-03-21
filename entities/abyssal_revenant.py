import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities import abyssal_revenant
from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .player import Player
from .utils import Animation, SpriteSheet


class AbyssalRevenant(Enemy):
    def __init__(self, pos: Vector) -> None:
        super().__init__(
            pos=pos,
            size=Vector(200, 200),
            hitbox=Vector(50, 80),
            vel=Vector(0, 0),
            hp=300,
            hitbox_offset=Vector(0, 20),
        )

        self.__animations = {
            "IDLE_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "abyssal_revenant", "IDLE.png"),
                    rows=1,
                    cols=9,
                ),
                frames_per_sprite=8,
            ),
            "IDLE_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "abyssal_revenant", "IDLE.png"),
                    rows=1,
                    cols=9,
                ).flip(),
                frames_per_sprite=8,
            ),
            "RUN_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "abyssal_revenant", "RUN.png"),
                    rows=1,
                    cols=6,
                ),
                frames_per_sprite=15,
            ),
            "RUN_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "abyssal_revenant", "RUN.png"),
                    rows=1,
                    cols=6,
                ).flip(),
                frames_per_sprite=15,
            ),
            "ATTACK_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "abyssal_revenant", "ATTACK.png"),
                    rows=1,
                    cols=12,
                ),
                frames_per_sprite=5,
                one_iteration=True,
            ),
            "ATTACK_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "abyssal_revenant", "ATTACK.png"),
                    rows=1,
                    cols=12,
                ).flip(),
                frames_per_sprite=5,
                one_iteration=True,
            ),
        }
        self.current_animation = "IDLE"
        self.__direction = "LEFT"
        self.__detection_range = 300
        self.__attack_distance = 100
        self.__speed = 1.5

    def set_idle(self) -> None:
        self.current_animation = "IDLE"
        self.vel.x = 0

    def update(self) -> None:
        self._gravity()

        self.pos.x += self.vel.x
        Block.collisions_x(self)
        self.pos.y += self.vel.y
        Block.collisions_y(self)

        animation = f"{self.current_animation}_{self.__direction}"
        self.__animations[animation].update()

    def __allow_change_animation(self) -> bool:
        animation = f"{self.current_animation}_{self.__direction}"
        return self.__animations[animation].done

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        animation = f"{self.current_animation}_{self.__direction}"
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations[animation].render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

    def __attack(self) -> None:
        self.current_animation = "ATTACK"
        offset = 50

        if self.__direction == "LEFT":
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 20)),
            hitbox=Vector(90, 50),
            damage=40,
            owner=self,
        )

    def interaction(self, entity: PhysicsEntity) -> None:
        distance_x = self.pos.x - entity.pos.x

        if abs(distance_x) < self.__attack_distance:
            if self.__allow_change_animation():
                self.__attack()
                self.current_animation = "ATTACK"

            self.vel.x = 0

            if distance_x > 0:
                self.__direction = "LEFT"
            else:
                self.__direction = "RIGHT"

            return

        if abs(distance_x) < self.__detection_range:
            if self.__allow_change_animation():
                self.current_animation = "RUN"
            if distance_x > 0:
                self.__direction = "LEFT"
                self.vel.x = -self.__speed
            else:
                self.__direction = "RIGHT"
                self.vel.x = self.__speed

            return

        if self.__allow_change_animation():
            self.current_animation = "IDLE"
