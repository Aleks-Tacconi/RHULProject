import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet

class FlyingDemon(Enemy):
    def __init__(self, pos: Vector) -> None:
        super().__init__(
            pos=pos,
            size=Vector(158, 98),
            hitbox=Vector(100, 80),
            vel=Vector(0, 0),
            hp=300,
            hitbox_offset=Vector(0, 20),
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
        self.direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__detection_range = 200
        self.__attack_distance = 70
        self.__speed = 1
        self.__base_hp = self.hp
        self.__dead = False


    def __idle(self) -> None:
        if abs(self.__distance_x) > self.__detection_range:
            self.vel.x = 0
            self.__animations.set_animation(f"IDLE_{self.direction}")

    def update(self) -> None:
        self._get_direction()
        self._gravity()
        if self.__animations.done():
            self.__idle()
            self.__move()
            self.__attack()
            self.__death()

        self.pos.x += self.vel.x
        Block.collisions_x(self)
        self.pos.y += self.vel.y
        Block.collisions_y(self)
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)
        self.healthbar(canvas, offset_x, offset_y)


    def __attack(self) -> None:
        if abs(self.__distance_x) > self.__attack_distance:
            return

        self.vel.x = 0
        offset = 50

        if self.direction == "LEFT":
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 20)),
            hitbox=Vector(69, 70),
            hitbox_offset=None,
            damage=40,
            owner=self,
        )

        self.__animations.set_animation(f"ATTACK_{self.direction}")
        self.__animations.set_one_iteration(True)


    def remove(self) -> bool:
        if self.__animations.done() and self.__dead:
            return True
        return False


    def __death(self) -> None:
        if not self.is_alive:
            Attack(
                pos=Vector(int(self.pos.x), int(self.pos.y + 20)),
                hitbox=Vector(100, 100),
                hitbox_offset=None,
                damage=1000,
                owner=self,
            )

            self.vel.x = 0
            self.__animations.set_one_iteration(False)
            self.__animations.set_animation(f"DEATH_{self.direction}")
            self.__animations.set_one_iteration(True)
            self.__dead = True


    def __move(self) -> None:
        if abs(self.__distance_x) > self.__detection_range:
            return
        if self.__distance_x > 0:
            self.vel.x = -self.__speed
        else:
            self.vel.x = self.__speed
        self.__animations.set_animation(f"RUN_{self.direction}")


    def interaction(self, entity: PhysicsEntity) -> None:
        self.__distance_x = self.pos.x - entity.pos.x
        print("Health: ", self.hp)



