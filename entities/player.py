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
            "ATTACK_OVERHEAD_RIGHT": (0, 4, 4, False),
            "ATTACK_SLASH_RIGHT": (1, 6, 6, False),
            "ATTACK_SLASH_NO_MOVEMENT_RIGHT": (2, 6, 6, False),
            "ATTACK_COMBO_RIGHT": (3, 10, 10, False),
            "ATTACK_COMBO_NO_MOVEMENT_RIGHT": (4, 10, 10, False),
            "ATTACK_OVERHEAD_NO_MOVEMENT_RIGHT": (5, 4, 4, False),
            "CROUCH_RIGHT": (6, 1, 1, False),
            "CROUCH_ATTACK_RIGHT": (7, 4, 4, False),
            "CROUCH_FULL_RIGHT": (8, 3, 3, False),
            "CROUCH_TRANSITION_RIGHT": (9, 1, 1, False),
            "CROUCH_WALK_RIGHT": (10, 8, 8, False),
            "DASH_RIGHT": (11, 2, 2, False),
            "DEATH_RIGHT": (12, 10, 10, False),
            "DEATH_NO_MOVEMENT_RIGHT": (13, 10, 10, False),
            "FALL_RIGHT": (14, 3, 3, False),
            "HIT_RIGHT": (15, 1, 1, False),
            "IDLE_RIGHT": (16, 10, 10, False),
            "JUMP_RIGHT": (17, 3, 3, False),
            "JUMP_FALL_IN_BETWEEN_RIGHT": (18, 2, 2, False),
            "ROLL_RIGHT": (19, 12, 12, False),
            "RUN_RIGHT": (20, 10, 3, False),
            "SLIDE_RIGHT": (21, 2, 2, False),
            "SLIDE_FULL_RIGHT": (22, 4, 4, False),
            "SLIDE_TRANSITION_END_RIGHT": (23, 1, 1, False),
            "SLIDE_TRANSITION_START_RIGHT": (24, 1, 1, False),
            "TURN_AROUND_RIGHT": (25, 3, 3, False),
            "WALL_CLIMB_RIGHT": (26, 7, 7, False),
            "WALL_CLIMB_NO_MOVEMENT_RIGHT": (27, 7, 7, False),
            "WALL_HANG_RIGHT": (28, 1, 1, False),
            "WALL_SLIDE_RIGHT": (29, 3, 3, False),
            "ATTACK_OVERHEAD_LEFT": (0, 4, 4, True),
            "ATTACK_SLASH_LEFT": (1, 6, 6, True),
            "ATTACK_SLASH_NO_MOVEMENT_LEFT": (2, 6, 6, True),
            "ATTACK_COMBO_LEFT": (3, 10, 10, True),
            "ATTACK_COMBO_NO_MOVEMENT_LEFT": (4, 10, 10, True),
            "ATTACK_OVERHEAD_NO_MOVEMENT_LEFT": (5, 4, 4, True),
            "CROUCH_LEFT": (6, 1, 1, True),
            "CROUCH_ATTACK_LEFT": (7, 4, 4, True),
            "CROUCH_FULL_LEFT": (8, 3, 3, True),
            "CROUCH_TRANSITION_LEFT": (9, 1, 1, True),
            "CROUCH_WALK_LEFT": (10, 8, 8, True),
            "DASH_LEFT": (11, 2, 2, True),
            "DEATH_LEFT": (12, 10, 10, True),
            "DEATH_NO_MOVEMENT_LEFT": (13, 10, 10, True),
            "FALL_LEFT": (14, 3, 3, True),
            "HIT_LEFT": (15, 1, 1, True),
            "IDLE_LEFT": (16, 10, 10, True),
            "JUMP_LEFT": (17, 3, 3, True),
            "JUMP_FALL_IN_BETWEEN_LEFT": (18, 2, 2, True),
            "ROLL_LEFT": (19, 12, 12, True),
            "RUN_LEFT": (20, 10, 3, True),
            "SLIDE_LEFT": (21, 2, 2, True),
            "SLIDE_FULL_LEFT": (22, 4, 4, True),
            "SLIDE_TRANSITION_END_LEFT": (23, 1, 1, True),
            "SLIDE_TRANSITION_START_LEFT": (24, 1, 1, True),
            "TURN_AROUND_LEFT": (25, 3, 3, True),
            "WALL_CLIMB_LEFT": (26, 7, 7, True),
            "WALL_CLIMB_NO_MOVEMENT_LEFT": (27, 7, 7, True),
            "WALL_HANG_LEFT": (28, 1, 1, True),
            "WALL_SLIDE_LEFT": (29, 3, 3, True),
        }
                                           )

        self.__direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.__direction}"
        self.__animations.set_animation(self.__current_animation)
        self.jumps = 2
        self.__movement = []
        self.__speed = 5

    def remove(self) -> bool:
        if self.__animations.done() and not self.is_alive:
            return True
        return False

    def update(self) -> None:
        self.death()
        self.__horizontal_movement()
        self._gravity()

        self.pos.x += self.vel.x
        Block.collisions_x(self)

        self.pos.y += self.vel.y
        Block.collisions_y(self)

        self.__current_animation = f"{self.__current_animation}_{self.__direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__animations.update()

        print(f"{self.hp=}")

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        if self.__direction == "LEFT":
            pos = Vector(int(self.pos.x + offset_x - 10), int(self.pos.y + offset_y))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, offset_x, offset_y)
        else:
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
            if self.__animations.done():
                self.__current_animation = "IDLE"
            return

        if self.__animations.done():
            self.__current_animation = "RUN"

        direction = self.__movement[-1]

        if direction == "A":
            self.vel.x = -self.__speed
            self.__direction = "LEFT"
        if direction == "D":
            self.vel.x = self.__speed
            self.__direction = "RIGHT"

    def __attack(self) -> None:
        offset = 50
        self.__current_animation = f"ATTACK_SLASH_{self.__direction}"
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

    def __crouch_down(self) -> None:
        self.hitbox= Vector(40, 46)
        self.__current_animation = f"CROUCH_{self.__direction}"
        self.__animations.set_animation(self.__current_animation)

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
        if key == 83:  # S
            self.__crouch_down()
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
