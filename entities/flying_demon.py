import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet

class FlyingDemon(Enemy):
    def __init__(self, pos: Vector, level_id: str, start_direction = "LEFT") -> None:
        super().__init__(
            pos=pos,
            size=Vector(158, 98),
            hitbox=Vector(100, 80),
            vel=Vector(0, 0),
            hp=500,
            level_id=level_id,
            hitbox_offset=Vector(0, 20),
            direction=start_direction,
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "flying_demon", "FLYING_DEMON.png"),
            rows=5,
            cols=8,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "ATTACK_LEFT": (0, 8, 8, False),
            "DEATH_LEFT": (1, 6, 6, False),
            "RUN_LEFT": (2, 4, 4, False),
            "HURT_LEFT": (3, 4, 4, False),
            "IDLE_LEFT": (4, 4, 4, False),
            "ATTACK_RIGHT": (0, 8, 8, True),
            "DEATH_RIGHT": (1, 6, 6, True),
            "RUN_RIGHT": (2, 4, 4, True),
            "HURT_RIGHT": (3, 4, 4, True),
            "IDLE_RIGHT": (4, 4, 4, True),
        }
                                           )

        self.points = 100
        self.direction = start_direction
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__distance_y = 0
        self.__detection_range_x = 200
        self.__detection_range_y = 10
        self.__attack_distance = 70
        self.__speed = 1
        self.xp = 200
        self.__base_hp = self.hp
        self.__dead = False
        self.__player = None
        self.__seen_player = False

    def __idle(self) -> None:
        if abs(self.__distance_x) > self.__detection_range_x:
            self.vel.x = 0
            self.__animations.set_animation(f"IDLE_{self.direction}")

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
        offset = 50

        if self.direction == "LEFT":
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 20)),
            hitbox=Vector(69, 70),
            hitbox_offset=None,
            damage=200,
            owner=self,
        )

        self.__animations.set_animation(f"ATTACK_{self.direction}")
        self.__animations.set_one_iteration(True)


    def remove(self) -> bool:
        return self.__dead and self.__animations.done()


    def __death(self) -> None:
        if not self.is_alive:
            Attack(
                pos=Vector(int(self.pos.x), int(self.pos.y + 20)),
                hitbox=Vector(100, 100),
                hitbox_offset=None,
                damage=1000,
                owner=self,
            )

            if not self.__dead:
                self.__animations.set_one_iteration(False)

            if self.__animations.done():
                self.vel.x = 0
                self.__animations.set_animation(f"DEATH_{self.direction}")
                self.__animations.set_one_iteration(True)
                self.__dead = True

    def __move(self) -> None:
        if ((abs(self.__distance_x) > self.__detection_range_x and abs(self.__distance_y) > self.__detection_range_y) or
                self.__player is None):
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
        self.__distance_y = self.pos.y - entity.pos.y
        self.__player = entity

    def __str__(self) -> str:
        return "FlyingDemon"



