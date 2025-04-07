import os
import threading

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from entities.fireball import LeftFireball, RightFireball
from utils import Vector
import random
from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet, PlaySound



class Mage(Enemy):
    def __init__(self, pos: Vector, level_id: str, start_direction = "LEFT") -> None:
        super().__init__(
            pos=pos,
            size=Vector(256, 256),
            hitbox=Vector(40, 120),
            vel=Vector(0, 0),
            hp=2000,
            level_id=level_id,
            hitbox_offset=Vector(0, 60),
            direction=start_direction
        )
        self.__left_fireball = None
        self.__right_fireball = None

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
            "ATTACK_RIGHT": (4, 17, 2, False),
            "ATTACK_LEFT": (4, 17, 2, True),
            "HURT_RIGHT": (5, 5, 5, False),
            "HURT_LEFT": (5, 5, 5, True),
            "DEATH_RIGHT": (6, 9, 8, False),
            "DEATH_LEFT": (6, 9, 8, True),
        }
                                           )

        self.points = 100
        self.xp = 100
        self.direction = start_direction
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__distance_y = 0
        self.__detection_range_x = 500
        self.__detection_range_y = 100
        self.__attack_distance = 400
        self.__speed = 3
        self.__original_hp = self.hp
        self.__dead = False
        self.__player = None
        self.seen_player = False

        self.__sound = PlaySound()
        self.__sound.change_volume(0.3)
        self.__sounds = {"FIRE1": "Fireball 1.wav",
                         "FIRE2": "Fireball 2.wav",
                         "FIRE3": "Fireball 3.wav",
                         }

    def __idle(self) -> None:
        if abs(self.__distance_x) > self.__detection_range_x:
            self.vel.x = 0
            self.__animations.set_animation(f"IDLE_{self.direction}")

    def update(self) -> None:
        self._get_direction()
        self._knockback(self.__player)
        self._gravity()
        self.__death()

        if self.__animations.done() and self.is_alive:
            self.__idle()
            self.__move()
            self.__attack()
            self.__take_damage()

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)
        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)
        self.__animations.update()

        if self.__animations.get_animation() == "ATTACK_LEFT" and self.__animations.get_frame() == [6, 4]:
            self.__left_fireball = LeftFireball(self.pos.x, self.pos.y+35, "LevelThree")

        if self.__animations.get_animation() == "ATTACK_RIGHT" and self.__animations.get_frame() == [11, 4]:
            self.__right_fireball = RightFireball(self.pos.x, self.pos.y+35, "LevelThree")

        if self.__left_fireball is not None:
            self.__left_fireball.update()
            

        if self.__right_fireball is not None:
            self.__right_fireball.update()
            


    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)
        self.healthbar(canvas, offset_x, offset_y)

        if self.__left_fireball is not None:
            self.__left_fireball.render(canvas, offset_x, offset_y)

        if self.__right_fireball is not None:
            self.__right_fireball.render(canvas, offset_x, offset_y)

    def __attack(self) -> None:
        if ((abs(self.__distance_x) > self.__attack_distance or abs(self.__distance_y) > self.__detection_range_y) or
                self.__player is None or not self.seen_player):
            return
        if self.__distance_x > 0:
            self.direction = "LEFT"
        else:
            self.direction = "RIGHT"

        self.vel.x = 0
        offset = 50

        if self.direction == "LEFT":
            offset *= -1

        self.__sound.play_sound(self.__sounds.get(f"FIRE{random.randint(1, 3)}"))
        self.__animations.set_animation(f"ATTACK_{self.direction}")
        self.__animations.set_one_iteration(True)

    def remove(self) -> bool:
        return self.__dead and self.__animations.done()

    def __death(self) -> None:
        if not self.is_alive:

            if not self.__dead:
                self.__animations.set_one_iteration(False)

            if self.__animations.done():
                self.vel.x = 0
                self.__animations.set_animation(f"DEATH_{self.direction}")
                self.__animations.set_one_iteration(True)
                self.__dead = True

    def __move(self) -> None:
        if ((abs(self.__distance_x) > self.__detection_range_x or abs(self.__distance_y) > self.__detection_range_y) or
                self.__player is None):
            return

        if self.__player.crouched and not self.seen_player:
            if not (self.direction == "LEFT" and self.__distance_x > 0 or
                    self.direction == "RIGHT" and self.__distance_x < 0):
                return
        if self.__distance_x > 0:
            self.vel.x = -self.__speed
        else:
            self.vel.x = self.__speed
        self.seen_player = True
        self.__animations.set_animation(f"RUN_{self.direction}")

    def __take_damage(self):
        if self.__original_hp != self.hp:
            self.__original_hp = self.hp
            self.seen_player = True

    def interaction(self, entity: PhysicsEntity) -> None:
        self.__distance_x = self.pos.x - entity.pos.x
        self.__distance_y = self.pos.y - entity.pos.y
        self.__player = entity

        if self.__left_fireball is not None:
            self.__left_fireball.interaction(entity)

        if self.__right_fireball is not None:
            self.__right_fireball.interaction(entity)


    def __str__(self) -> str:
        return "Mage"


