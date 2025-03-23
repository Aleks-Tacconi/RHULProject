import os
import threading

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet



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

        spritesheet = SpriteSheet(
            os.path.join("assets", "abyssal_revenant", "ABYSSAL_REVENANT.png"),
            rows=5,
            cols=23,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "IDLE_RIGHT": (0, 9, 9, False),
            "IDLE_LEFT": (0, 9, 9, True),
            "RUN_RIGHT": (1, 6, 6, False),
            "RUN_LEFT": (1, 6, 6, True),
            "ATTACK_RIGHT": (2, 12, 12, False),
            "ATTACK_LEFT": (2, 12, 12, True),
            "HURT_RIGHT": (3, 5, 5, False),
            "HURT_LEFT": (3, 5, 5, True),
            "DEATH_RIGHT": (4, 23, 9, False),
            "DEATH_LEFT": (4, 23, 9, True),
        }
                                           )

        self.points = 100
        self.__direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.__direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__detection_range = 300
        self.__attack_distance = 70
        self.__speed = 1.5

    def __idle(self) -> None:
        ...
        #self.__current_animation = "IDLE_LEFT"
        #self.vel.x = 0

    def update(self) -> None:
        self._gravity()

        self.pos.x += self.vel.x
        Block.collisions_x(self)
        self.pos.y += self.vel.y
        Block.collisions_y(self)

        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

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



