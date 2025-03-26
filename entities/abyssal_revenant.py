import os

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
            hp=3000,
            hitbox_offset=Vector(0, 20),
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "abyssal_revenant", "ABYSSAL_REVENANT.png"),
            rows=5,
            cols=23,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "IDLE_RIGHT": (0, 9, 3, False),
            "IDLE_LEFT": (0, 9, 3, True),
            "RUN_RIGHT": (1, 6, 3, False),
            "RUN_LEFT": (1, 6, 3, True),
            "ATTACK_RIGHT": (2, 12, 4, False),
            "ATTACK_LEFT": (2, 12, 4, True),
            "HURT_RIGHT": (3, 5, 5, False),
            "HURT_LEFT": (3, 5, 5, True),
            "DEATH_RIGHT": (4, 23, 3, False),
            "DEATH_LEFT": (4, 23, 3, True),
        }
                                           )

        self.points = 100
        self.direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__detection_range = 200
        self.__attack_distance = 70
        self.__speed = 3
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
            start_frame=5,
            end_frame=5,
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
                start_frame=5,
                end_frame=15,
                owner=self,
            )

            self.vel.x = 0
            self.vel.y = 12
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






