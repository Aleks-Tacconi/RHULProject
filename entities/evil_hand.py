import os
import threading

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet



class EvilHand(Enemy):
    def __init__(self, pos: Vector, level_id: str, start_direction = "LEFT") -> None:
        super().__init__(
            pos=pos,
            size=Vector(186, 192),
            hitbox=Vector(150, 190),
            vel=Vector(0, 0),
            hp=3000,
            level_id=level_id,
            hitbox_offset=Vector(-10, 0),
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "evil_hand", "EVIL_HAND.png"),
            rows=1,
            cols=8,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "RUN_RIGHT": (0, 8, 3, False),
            "RUN_LEFT": (0, 8, 3, True),
        }
                                           )

        self.points = 100
        self.direction = start_direction
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__detection_range = 200
        self.__attack_distance = 10
        self.__speed = 3
        self.__base_hp = self.hp
        self.__dead = False
        self.__player = None
        self.__seen_player = False

    def __idle(self) -> None:
        if abs(self.__distance_x) > self.__detection_range:
            self.vel.x = 0
            self.__animations.set_animation(f"RUN_{self.direction}")

    def update(self) -> None:
        if self.hp != self.__base_hp:
            self.__seen_player = True
        self._get_direction()
        self._gravity()
        self.__death()

        if self.__animations.done():
            self.__idle()
            self.__move()
            self.__attack()

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)
        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)
        self.__animations.update()


    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)
        self.healthbar(canvas, offset_x, offset_y)

    def __attack(self) -> None:
        if abs(self.__distance_x) > self.__attack_distance or not self.__seen_player:
            return

        if self.__distance_x > 0:
            self.direction = "LEFT"
        else:
            self.direction = "RIGHT"

        self.vel.x = 0
        offset = 10

        if self.__distance_x > 0:
            self.direction = "LEFT"
            offset *= -1
        else:
            self.direction = "RIGHT"

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 20)),
            hitbox=Vector(69, 70),
            hitbox_offset=None,
            damage=40,
            start_frame=1,
            end_frame=1,
            owner=self,
        )

    def remove(self) -> bool:
        return self.__dead and self.__animations.done()

    def __death(self) -> None:
        if not self.is_alive:

            if not self.__dead:
                self.__animations.set_one_iteration(False)

            if self.__animations.done():
                self.vel.x = 0
                self.__dead = True

    def __move(self) -> None:
        if abs(self.__distance_x) > self.__detection_range or self.__player is None:
            return

        if self.__player.crouched and not self.__seen_player:
            if not (self.direction == "LEFT" and self.__distance_x > 0 or
                    self.direction == "RIGHT" and self.__distance_x < 0):
                return
        if self.__distance_x > 0:
            self.vel.x = -self.__speed
        else:
            self.vel.x = self.__speed
        self.__seen_player = True
        self.__animations.set_animation(f"RUN_{self.direction}")

    def interaction(self, entity: PhysicsEntity) -> None:
        self.__distance_x = self.pos.x - entity.pos.x
        self.__player = entity
        print("Health: ", self.hp)

    def __str__(self) -> str:
        return "EVIL HAND"