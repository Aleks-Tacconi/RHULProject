import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import PhysicsEntity
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet


class Player(PhysicsEntity):
    def __init__(self, pos: Vector) -> None:
        super().__init__(
            pos=pos,
            size=Vector(200, 200),
            vel=Vector(0, 0),
            hitbox=Vector(40, 92),
            hp=100,
            hitbox_offset=Vector(-5, 55),
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "player", "KNIGHT.png"),
            rows=30,
            cols=12,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "ATTACK_OVERHEAD": (0, 4, 4),
            "ATTACK_SLASH": (1, 6, 6),
            "ATTACK_SLASH_NO_MOVEMENT": (2, 6, 6),
            "ATTACK_COMBO": (3, 10, 10),
            "ATTACK_COMBO_NO_MOVEMENT": (4, 10, 10),
            "ATTACK_OVERHEAD_NO_MOVEMENT": (5, 4, 4),
            "CROUCH": (6, 1, 1),
            "CROUCH_ATTACK": (7, 4, 4),
            "CROUCH_FULL": (8, 3, 3),
            "CROUCH_TRANSITION": (9, 1, 1),
            "CROUCH_WALK": (10, 8, 8),
            "DASH": (11, 2, 2),
            "DEATH": (12, 10, 10),
            "DEATH_NO_MOVEMENT": (13, 10, 10),
            "FALL": (14, 3, 3),
            "HIT": (15, 1, 1),
            "IDLE": (16, 10, 10),
            "JUMP": (17, 3, 3),
            "JUMP_FALL_IN_BETWEEN": (18, 2, 2),
            "ROLL": (19, 12, 12),
            "RUN": (20, 10, 3),
            "RUN2": (20, 10, 10),
            "SLIDE": (21, 2, 2),
            "SLIDE_FULL": (22, 4, 4),
            "SLIDE_TRANSITION_END": (23, 1, 1),
            "SLIDE_TRANSITION_START": (24, 1, 1),
            "TURN_AROUND": (25, 3, 3),
            "WALL_CLIMB": (26, 7, 7),
            "WALL_CLIMB_NO_MOVEMENT": (27, 7, 7),
            "WALL_HANG": (28, 1, 1),
            "WALL_SLIDE": (29, 3, 3),
        }
                                           )

        self.__current_animation = "IDLE"
        self.__animations.set_animation(self.__current_animation)
        self.__direction = "RIGHT"
        self.__animation = f"{self.__current_animation}_{self.__direction}"
        self.jumps = 2

        self.__movement = []
        self.__speed = 5

    def remove(self) -> bool:
        if self.__animations.done() and not self.is_alive:
            return True
        return False

    def __get_direction(self):
        if self.vel.x > 0:
            self.__direction = "RIGHT"
        elif self.vel.x < 0:
            self.__direction = "LEFT"

    def update(self) -> None:
        print("Start Frame", self.__animations.get_start_frame())
        print("End Frame", self.__animations.get_end_frame())
        print(self.vel.x)
        self.death()
        self.__horizontal_movement()
        self._gravity()
        self.__get_direction()
        if self.__direction == "LEFT":
            self.__animations.set_flip(True)
            self.hitbox_offset = Vector(5, 55)
        if self.__direction == "RIGHT":
            self.__animations.set_flip(False)
            self.hitbox_offset = Vector(-5, 55)

        self.pos.x += self.vel.x
        Block.collisions_x(self)

        self.pos.y += self.vel.y
        Block.collisions_y(self)

        self.__animations.set_animation(self.__current_animation)
        self.__animations.update()

        print(f"{self.hp=}")

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

    def set_idle(self) -> None:
        self.__current_animation = "IDLE"
        self.__movement = []

    def __jump(self) -> None:
        if self.jumps > 0:
            self.vel.y = -12
            self.jumps -= 1

    def __horizontal_movement(self) -> None:
        if not self.__movement:
            self.vel.x = 0

            self.set_idle()
            return


        self.__current_animation = "RUN"



        direction = self.__movement[-1]

        if direction == "A":
            self.vel.x = -self.__speed
        if direction == "D":
            self.vel.x = self.__speed

    def __attack(self) -> None:
        offset = 50
        self.__current_animation = "ATTACK_SLASH"
        self.__animations.set_animation(self.__current_animation)
        self.__animations.set_one_iteration(True)

        if self.__direction == "LEFT":
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 30)),
            hitbox=Vector(100, 50),
            damage=100,
            owner=self,
        )

    def death(self) -> None:
        if not self.is_alive:
            self.vel.x = 0
            self.vel.y = 1
            self.__current_animation = "DEATH"
            self.__movement = []

    def keydown_handler(self, key: int) -> None:
        if key == 65:  # A
            self.__movement.append("A")
        if key == 68:  # D
            self.__movement.append("D")
        if key == 87:  # W
            self.__jump()
        if key == 69:  # E
            self.__attack()

    def keyup_handler(self, key: int) -> None:
        if key == 65:  # A
            if "A" in self.__movement:
                self.__movement.remove("A")
        if key == 68:  # D
            if "D" in self.__movement:
                self.__movement.remove("D")
