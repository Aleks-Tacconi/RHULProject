import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import PhysicsEntity
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, Animation, SpriteSheet


class Player(PhysicsEntity):
    def __init__(self, pos: Vector, level_id: str) -> None:
        super().__init__(
            pos=pos,
            size=Vector(200, 200),
            vel=Vector(0, 0),
            hitbox=Vector(40, 92),
            hp=10000,
            level_id=level_id,
            hitbox_offset=Vector(-5, 55),
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "player", "PLAYER.png"),
            rows=30,
            cols=12,
        )

        self.__animations = MultiAnimation(spritesheet=spritesheet, animations={
            "ATTACK_OVERHEAD_RIGHT": (0, 4, 4, False),
            "ATTACK_SLASH_RIGHT": (1, 6, 6, False),
            "ATTACK_SLASH_NO_MOVEMENT_RIGHT": (2, 6, 6, False),
            "ATTACK_COMBO_RIGHT": (3, 10, 2, False),
            "ATTACK_COMBO_NO_MOVEMENT_RIGHT": (4, 10, 10, False),
            "ATTACK_OVERHEAD_NO_MOVEMENT_RIGHT": (5, 4, 4, False),
            "CROUCH_RIGHT": (6, 1, 1, False),
            "CROUCH_FULL_RIGHT": (7, 3, 1, False),
            "CROUCH_ATTACK_RIGHT": (8, 4, 2, False),
            "CROUCH_TRANSITION_RIGHT": (9, 1, 1, False),
            "CROUCH_WALK_RIGHT": (10, 8, 2, False),
            "DASH_RIGHT": (11, 2, 2, False),
            "DEATH_RIGHT": (12, 10, 10, False),
            "DEATH_NO_MOVEMENT_RIGHT": (13, 10, 10, False),
            "FALL_RIGHT": (14, 3, 3, False),
            "HIT_RIGHT": (15, 1, 1, False),
            "IDLE_RIGHT": (16, 10, 10, False),
            "JUMP_RIGHT": (17, 3, 3, False),
            "JUMP_FALL_IN_BETWEEN_RIGHT": (18, 2, 2, False),
            "ROLL_RIGHT": (19, 12, 1, False),
            "RUN_RIGHT": (20, 10, 3, False),
            "SLIDE_RIGHT": (21, 2, 2, False),
            "SLIDE_FULL_RIGHT": (22, 4, 4, False),
            "SLIDE_TRANSITION_END_RIGHT": (23, 1, 1, False),
            "SLIDE_TRANSITION_START_RIGHT": (24, 1, 1, False),
            "TURN_AROUND_RIGHT": (25, 1, 1, False),
            "WALL_CLIMB_RIGHT": (26, 7, 7, False),
            "WALL_CLIMB_NO_MOVEMENT_RIGHT": (27, 7, 7, False),
            "WALL_HANG_RIGHT": (28, 1, 1, False),
            "WALL_SLIDE_RIGHT": (29, 3, 3, False),
            "ATTACK_OVERHEAD_LEFT": (0, 4, 4, True),
            "ATTACK_SLASH_LEFT": (1, 6, 6, True),
            "ATTACK_SLASH_NO_MOVEMENT_LEFT": (2, 6, 6, True),
            "ATTACK_COMBO_LEFT": (3, 10, 2, True),
            "ATTACK_COMBO_NO_MOVEMENT_LEFT": (4, 10, 10, True),
            "ATTACK_OVERHEAD_NO_MOVEMENT_LEFT": (5, 4, 4, True),
            "CROUCH_LEFT": (6, 1, 1, True),
            "CROUCH_FULL_LEFT": (7, 3, 1, True),
            "CROUCH_ATTACK_LEFT": (8, 4, 2, True),
            "CROUCH_TRANSITION_LEFT": (9, 1, 1, True),
            "CROUCH_WALK_LEFT": (10, 8, 2, True),
            "DASH_LEFT": (11, 2, 2, True),
            "DEATH_LEFT": (12, 10, 10, True),
            "DEATH_NO_MOVEMENT_LEFT": (13, 10, 10, True),
            "FALL_LEFT": (14, 3, 3, True),
            "HIT_LEFT": (15, 1, 1, True),
            "IDLE_LEFT": (16, 10, 10, True),
            "JUMP_LEFT": (17, 3, 3, True),
            "JUMP_FALL_IN_BETWEEN_LEFT": (18, 2, 2, True),
            "ROLL_LEFT": (19, 12, 1, True),
            "RUN_LEFT": (20, 10, 3, True),
            "SLIDE_LEFT": (21, 2, 2, True),
            "SLIDE_FULL_LEFT": (22, 4, 4, True),
            "SLIDE_TRANSITION_END_LEFT": (23, 1, 1, True),
            "SLIDE_TRANSITION_START_LEFT": (24, 1, 1, True),
            "TURN_AROUND_LEFT": (25, 1, 1, True),
            "WALL_CLIMB_LEFT": (26, 7, 7, True),
            "WALL_CLIMB_NO_MOVEMENT_LEFT": (27, 7, 7, True),
            "WALL_HANG_LEFT": (28, 1, 1, True),
            "WALL_SLIDE_LEFT": (29, 3, 3, True),
        }
                                           )

        self.direction = "RIGHT"
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__jumps = 1
        self.__movement_x = []
        self.__movement_y = []
        self.__speed = 1
        self.crouched = False
        self.__rolling = False
        self.__dead = False
        self.immune = True
        self.__movement_x_locked = False
        self.__movement_y_locked = False
        self.friendly = False
        self.is_attacking = False
        self.__running = False
        self.__jumping = False


    def remove(self) -> bool:
        if self.__animations.done() and self.__dead:
            return True
        return False

    def update(self) -> None:
        self._get_direction()
        if self.__animations.done():
            self.is_attacking = False
            self.immune = False
            self.__movement_x_locked = False
            self.__movement_y_locked = False
        self.__death()
        if self.is_alive:
            self.__idle()
            self.__vertical_movement()
            self.__horizontal_movement()
        self._gravity()

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)

        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)



        self.__current_animation = f"{self.__current_animation}_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__animations.update()

        print(f"{self.hp=}")

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        if self.direction == "LEFT":
            pos = Vector(int(self.pos.x + offset_x - 10), int(self.pos.y + offset_y))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, offset_x, offset_y)
        else:
            pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, offset_x, offset_y)

    def __idle(self) -> None:
        if (not self.__movement_x and not self.__movement_y and not self.__jumping and self.vel.x == 0 and
                self.vel.y == 0 and not self.__movement_x_locked and not self.__movement_y_locked):
            self.hitbox = Vector(40, 92)
            self.hitbox_offset = Vector(-5, 55)
            self.vel.x = 0
            self.__current_animation = "IDLE"

    def __jump(self) -> None:
        if self.__jumps > 0:
            self.vel.y = -12.91
            self.__jumps -= 1


    def __horizontal_movement(self) -> None:
        if not self.__movement_x:
            if self.direction == "LEFT":
                self.vel.x = min(self.vel.x + self.__speed * 0.25, 0)
            else:
                self.vel.x = max(self.vel.x - self.__speed * 0.25, 0)
            return

        if self.__rolling:
            self.__roll()
            return

        if self.__animations.done() and not self.crouched:
            self.__current_animation = "RUN"
        else:
            self.__current_animation = "CROUCH_WALK"

        direction_x = self.__movement_x[-1]
        multiplier = 1.1

        if self.__running:
            multiplier = 1.2

        if not self.__movement_x_locked:
            if self.crouched:
                if direction_x == "A":
                    self.vel.x = max(self.vel.x - self.__speed * multiplier, -5)
                if direction_x == "D":
                    self.vel.x = min(self.vel.x + self.__speed * multiplier, 5)
                return
            if self.__running and not self.crouched:
                if direction_x == "A":
                    self.vel.x = max(self.vel.x - self.__speed * multiplier, -15)
                    if self.direction == "RIGHT":
                        self.__current_animation = "TURN_AROUND"
                if direction_x == "D":
                    self.vel.x = min(self.vel.x + self.__speed * multiplier, 15)
                    if self.direction == "LEFT":
                        self.__current_animation = "TURN_AROUND"
            else:
                if direction_x == "A":
                    self.vel.x = max(self.vel.x - self.__speed * multiplier, -10)
                    if self.direction == "RIGHT":
                        self.__current_animation = "TURN_AROUND"
                if direction_x == "D":
                    self.vel.x = min(self.vel.x + self.__speed * multiplier, 10)
                    if self.direction == "LEFT":
                        self.__current_animation = "TURN_AROUND"



    def __vertical_movement(self) -> None:
        if self.__jumping:
            if self.vel.y == 0:
                self.__current_animation = "FALL"
                self.__jumping = False


        if not self.__movement_y:
            return

        direction_y = self.__movement_y[-1]

        if not self.__movement_y_locked:
            if direction_y == "W" and not self.__jumping:
                self.__jump()
                self.__current_animation = "JUMP"
                self.__jumping = True

            if direction_y == "S":
                self.__crouch()
            if self.vel.y == 0 and self.__animations.done():
                self.__jumps = 1


    def __attack(self) -> None:
        offset = 50
        self.is_attacking = True
        if self.direction == "LEFT":
            offset *= -1

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 30)),
            hitbox=Vector(100, 100),
            hitbox_offset=Vector(0, 30),
            start_frame= 10,
            end_frame=10,
            damage=100,
            owner=self,
        )

        if self.crouched:
            self.__animations.set_animation(f"CROUCH_ATTACK_{self.direction}")
            self.__animations.set_one_iteration(True)
            return


        self.__animations.set_animation(f"ATTACK_COMBO_{self.direction}")
        self.__animations.set_one_iteration(True)

    def __crouch(self) -> None:
        self.vel.y = 12
        self.crouched = True
        self.hitbox = Vector(40, 66)
        self.hitbox_offset = Vector(-5, 68)
        if self.vel.x == 0:
            self.__current_animation = "CROUCH"
        else:
            self.__current_animation = "CROUCH_WALK"

    def __roll(self):
        if self.vel.x == 0:
            if self.direction == "RIGHT":
                self.vel.x += self.__speed
            else:
                self.vel.x -= self.__speed
        self.__current_animation = f"ROLL_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.immune = True
        self.__movement_x_locked = True
        self.__movement_y_locked = True
        self.__animations.set_one_iteration(True)

    def __death(self) -> None:
        if not self.is_alive:
            self.vel.x = 0
            self.vel.y = 12

            if not self.__dead:
                self.__animations.set_one_iteration(False)

            if self.__animations.done():
                self.__current_animation = f"DEATH_{self.direction}"
                self.__animations.set_animation(self.__current_animation)
                self.__animations.set_one_iteration(True)
                self.__movement_x = []
                self.__dead = True

    def block_animation_change(self, boolean: bool) -> None:
        self.__animations.set_one_iteration(boolean)

    def keydown_handler(self, key: int) -> None:
        if key == 17: #SHIFT
            self.__running = True
        if key == 32: # SPACE
            self.__movement_x.append("SPACE")
            self.__rolling = True
        if key == 65:  # A
            self.__movement_x.append("A")
        if key == 68:  # D
            self.__movement_x.append("D")
        if key == 83:  # S
            self.__movement_y.append("S")
            self.crouched = True
        if key == 87:  # W
            self.__movement_y.append("W")
        if key == 69:  # E
            self.__attack()


    def keyup_handler(self, key: int) -> None:
        if key == 17: #SHIFT
            self.__running = False
        if key == 32: # SPACE
            self.__movement_x.remove("SPACE")
            self.__rolling = False
        if key == 65:  # A
            if "A" in self.__movement_x:
                self.__movement_x.remove("A")
        if key == 68:  # D
            if "D" in self.__movement_x:
                self.__movement_x.remove("D")
        if key == 83:  # S
            if "S" in self.__movement_y:
                self.__movement_y.remove("S")
                self.crouched = False
        if key == 87:  # W
            if "W" in self.__movement_y:
                self.__movement_y.remove("W")
