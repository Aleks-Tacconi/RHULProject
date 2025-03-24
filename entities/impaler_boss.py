import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet



class ImpalerBoss(Enemy):
    def __init__(self, pos: Vector) -> None:
        super().__init__(
            pos=pos,
            size=Vector(256, 106),
            hitbox=Vector(50, 80),
            vel=Vector(0, 0),
            hp=300,
            hitbox_offset=Vector(0, 20),
        )

        #TODO Update the spritesheet with higher resolution version for better quality

        spritesheet = SpriteSheet(
            os.path.join("assets", "impaler_boss", "sprite_sheet (13).png"),
            rows=1,
            cols=25,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "WALK_RIGHT": (1, 6, 6, False),
            "SPEAR_STRIKE_RIGHT": (0, 25, 10, False),
            "SPEAR_SPIN_RIGHT": (2, 8, 8, False),
            "SPEAR_SPIN_COMBO_RIGHT": (3, 21, 21, False),
            "SPEAR_THRUST_RIGHT": (4, 26, 4, False),
            "DUPLICATE_ATTACK_RIGHT": (5, 29, 29, False),
            "SPEAR_THURST_RIGHT": (6, 20, 20, False),
            "DEATH_RIGHT": (7, 25, 25, False),
            "IDLE_RIGHT": (8, 4, 4, False),
            "WALK_LEFT": (1, 6, 6, True),
            "SPEAR_STRIKE_LEFT": (0, 25, 10, True),
            "SPEAR_SPIN_LEFT": (2, 8, 8, True),
            "SPEAR_SPIN_COMBO_LEFT": (3, 21, 21, True),
            "SPEAR_THRUST_LEFT": (4, 26, 4, True),
            "DUPLICATE_ATTACK_LEFT": (5, 29, 29, True),
            "SPEAR_THURST_LEFT": (6, 20, 20, True),
            "DEATH_LEFT": (7, 25, 25, True),
            "IDLE_LEFT": (8, 4, 4, True),


        }
                                           )

        self.points = 100
        self.__direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.__direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__detection_range = 100
        self.__attack_distance = 70
        self.__speed = 1.5

    def __idle(self) -> None:
        ...
        # self.__current_animation = "IDLE_LEFT"
        # self.vel.x = 0

    def update(self) -> None:
        if self.vel.x > 0:
            self.__direction = "RIGHT"
        else:
            self.__direction = "LEFT"
        self._gravity()

        self.pos.x += self.vel.x
        Block.collisions_x(self)
        self.pos.y += self.vel.y
        Block.collisions_y(self)

        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        if self.__direction == "LEFT":
            pos = Vector(int(self.pos.x + offset_x - 50), int(self.pos.y + offset_y - 35))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, offset_x, offset_y)
        else:
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
                        self.__current_animation = "SPEAR_STRIKE_LEFT"
                        self.__animations.set_animation(self.__current_animation)
                        self.__animations.set_one_iteration(True)
                    else:
                        self.__current_animation = "SPEAR_STRIKE_RIGHT"
                        self.__animations.set_animation(self.__current_animation)
                        self.__animations.set_one_iteration(True)
                self.vel.x = 0

                return

            if abs(distance_x) < self.__detection_range:
                if self.__animations.done:
                    if distance_x > 0:
                        self.__current_animation = "WALK_LEFT"
                        self.vel.x = -self.__speed
                    else:
                        self.__current_animation = "WALK_RIGHT"
                        self.vel.x = self.__speed
                return

            if self.__animations.done:
                self.vel.x = 0
                if distance_x > 0:
                    self.__current_animation = "IDLE_LEFT"
                else:
                    self.__current_animation = "IDLE_RIGHT"

                return