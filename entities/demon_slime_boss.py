import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet
from .fire import Fire
import random

class DemonSlimeBoss(Enemy):
    def __init__(self, pos: Vector) -> None:
        super().__init__(
            pos=pos,
            size=Vector(576, 320),
            hitbox=Vector(120, 200),
            vel=Vector(0, 0),
            hp=300,
            hitbox_offset=Vector(0, 20),
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "demon_slime_boss", "DEMON_SLIME_BOSS.png"),
            rows=5,
            cols=22,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "IDLE_LEFT": (0, 6, 6, False),
            "RUN_LEFT": (1, 12, 12, False),
            "ATTACK_LEFT": (2, 15, 5, False),
            "HURT_LEFT": (3, 5, 5, False),
            "DEATH_LEFT": (4, 22, 4, False),
            "RUN_RIGHT": (0, 6, 6, True),
            "WALK_RIGHT": (1, 12, 12, True),
            "ATTACK_RIGHT": (2, 15, 5, True),
            "HURT_RIGHT": (3, 5, 5, True),
            "DEATH_RIGHT": (4, 22, 4, True),
        }
                                           )

        self.points = 1000
        self.direction = "LEFT"
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__detection_range = 500
        self.__attack_distance = 100
        self.__speed = 1
        self.__base_hp = self.hp
        self.__dead = False
        self.__fires = []

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
            self.__fire()
            self.__death()
        for fire in self.__fires:
            fire.interaction(self.__player)
            fire.update()
            if fire.remove():
                self.__fires.remove(fire)

        self.pos.x += self.vel.x
        Block.collisions_x(self)
        self.pos.y += self.vel.y
        Block.collisions_y(self)
        self.__animations.update()


    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y - 40))
        self.__animations.render(canvas, pos, self.size)
        if self.__fires:
            for fire in self.__fires:
                fire.render(canvas, offset_x, offset_y)
        self._render_hitbox(canvas, offset_x, offset_y)

    def __fire(self) -> None:
        if abs(self.__distance_x) > self.__detection_range:
            return
        if random.randint(1,20) == 1:
            self.__fires.append(Fire(self.__player_x + random.randint(-20,20)))



    def __attack(self) -> None:
        if abs(self.__distance_x) > self.__attack_distance:
            return

        self.vel.x = 0
        offset = 50

        if self.direction == "LEFT":
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 20)),
            hitbox=Vector(69, 200),
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
                hitbox=Vector(120, 200),
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
        self.__player_x = entity.pos.x
        self.__player = entity
        print("Health: ", self.hp)



