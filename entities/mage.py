import os
import threading

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet



class Mage(Enemy):
    def __init__(self, pos: Vector, level_id: str) -> None:
        super().__init__(
            pos=pos,
            size=Vector(256, 256),
            hitbox=Vector(40, 120),
            vel=Vector(0, 0),
            hp=2000,
            level_id=level_id,
            hitbox_offset=Vector(0, 60),
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "mage", "MAGE.png"),
            rows=7,
            cols=17,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "IDLE_RIGHT": (0, 8, 8, False),
            "IDLE_LEFT": (0, 8, 8, True),
            "RUN_RIGHT": (1, 8, 8, False),
            "RUN_LEFT": (1, 8, 8, True),
            "ATTACK_RIGHT": (4, 17, 8, False),
            "ATTACK_LEFT": (4, 17, 8, True),
            "HURT_RIGHT": (5, 5, 5, False),
            "HURT_LEFT": (5, 5, 5, True),
            "DEATH_RIGHT": (6, 9, 8, False),
            "DEATH_LEFT": (6, 9, 8, True),
        }
                                           )

        self.points = 100
        self.__direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.__direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__detection_range = 650
        self.__stopdetection_range = 350
        self.__attack_distance = 70
        self.__speed = 1.5

    def __idle(self) -> None:
        ...
        #self.__current_animation = "IDLE_LEFT"
        #self.vel.x = 0

    def update(self) -> None:
        self._gravity()

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
        offset = 50

        if "LEFT" in self.__current_animation:
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 20)),
            hitbox=Vector(69, 70),
            hitbox_offset=None,
            damage=40,
            owner=self,
        )

    def __death_attack(self) -> None:
        Attack(
            pos=Vector(int(self.pos.x), int(self.pos.y + 20)),
            hitbox=Vector(100, 100),
            hitbox_offset=None,
            damage=1000,
            owner=self,
        )

    def remove(self) -> bool:
        if self.__animations.done() and not self.is_alive:
            return True
        return False

    def interaction(self, entity: PhysicsEntity) -> None:
        distance_x = self.pos.x - entity.pos.x 
        print(distance_x)
        print("Health: ", self.hp)

        self.__animations.set_animation(self.__current_animation)
        self.__animations.update()

        if not self.is_alive:
            self.vel.x = 0
            self.__animations.set_one_iteration(False)
            self.__death_attack()
            if distance_x > 0:
                self.__current_animation = "DEATH_LEFT"
                self.__animations.set_animation(self.__current_animation)
                self.__animations.set_one_iteration(True)
            else:
                self.__current_animation = "DEATH_RIGHT"
                self.__animations.set_animation(self.__current_animation)
                self.__animations.set_one_iteration(True)

        if self.__animations.done():
            if abs(distance_x) < self.__attack_distance:
                if self.__animations.done:
                    self.__attack()
                    if distance_x > 0:
                        self.__current_animation = "ATTACK_LEFT"
                        self.__animations.set_animation(self.__current_animation)
                        self.__animations.set_one_iteration(True)
                    else:
                        self.__current_animation = "ATTACK_RIGHT"
                        self.__animations.set_animation(self.__current_animation)
                        self.__animations.set_one_iteration(True)
                self.vel.x = 0

                return

            if abs(distance_x) < self.__detection_range:
                if self.__animations.done:
                    if distance_x > 0:
                        self.__current_animation = "RUN_LEFT"
                        self.vel.x = -self.__speed
                    else:
                        self.__current_animation = "RUN_RIGHT"
                        self.vel.x = self.__speed
                return

            if self.__animations.done:
                self.vel.x = 0
                if distance_x > 0:
                    self.__current_animation = "IDLE_LEFT"
                else:
                    self.__current_animation = "IDLE_RIGHT"

                return

    def __str__(self) -> str:
        return "Mage"


