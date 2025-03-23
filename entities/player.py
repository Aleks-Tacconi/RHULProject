import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import PhysicsEntity
from .attack import Attack
from .block import Block
from .utils import Animation, SpriteSheet


class Player(PhysicsEntity):
    def __init__(self, pos: Vector) -> None:
        super().__init__(
            pos=pos,
            size=Vector(200, 200),
            vel=Vector(0, 0),
            hitbox=Vector(40, 80),
            hp=100,
            hitbox_offset=Vector(0, 30),
        )

        self.__animations = {
            "IDLE_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "IDLE.png"), rows=1, cols=5
                ),
                frames_per_sprite=15,
            ),
            "IDLE_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "IDLE.png"), rows=1, cols=5
                ).flip(),
                frames_per_sprite=15,
            ),
            "RUN_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "RUN.png"), rows=1, cols=8
                ),
                frames_per_sprite=15,
            ),
            "RUN_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "RUN.png"), rows=1, cols=8
                ).flip(),
                frames_per_sprite=15,
            ),
            "ATTACK_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "ATTACK_1.png"), rows=1, cols=5
                ),
                frames_per_sprite=5,
                one_iteration=True,
            ),
            "ATTACK_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "ATTACK_1.png"), rows=1, cols=5
                ).flip(),
                frames_per_sprite=5,
                one_iteration=True,
            ),
            "JUMP_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "ATTACK_1.png"), rows=1, cols=5
                ).flip(),
                frames_per_sprite=5,
                one_iteration=True,
            ),
            "JUMP_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "ATTACK_1.png"), rows=1, cols=5
                ).flip(),
                frames_per_sprite=5,
                one_iteration=True,
            ),
            "DEATH_RIGHT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "DEATH.png"), rows=1, cols=10
                ),
                frames_per_sprite=10,
                one_iteration=True,
            ),
            "DEATH_LEFT": Animation(
                spritesheet=SpriteSheet(
                    os.path.join("assets", "player", "DEATH.png"), rows=1, cols=10
                ).flip(),
                frames_per_sprite=10,
                one_iteration=True,
            )
        }

        self.current_animation = "IDLE"
        self.__direction = "RIGHT"
        self.jumps = 2

        self.__movement = []
        self.__speed = 3

    def remove(self) -> bool:
        animation = f"{self.current_animation}_{self.__direction}"
        if self.__animations[animation].done and not self.is_alive:
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

        animation = f"{self.current_animation}_{self.__direction}"
        self.__animations[animation].update()

        print(f"{self.hp=}")

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        animation = f"{self.current_animation}_{self.__direction}"
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations[animation].render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

    def set_idle(self) -> None:
        self.current_animation = "IDLE"
        self.__movement = []

    def __jump(self) -> None:
        if self.jumps > 0:
            self.vel.y = -12
            self.jumps -= 1

    def __allow_change_animation(self) -> bool:
        animation = f"{self.current_animation}_{self.__direction}"
        return self.__animations[animation].done

    def __horizontal_movement(self) -> None:
        if not self.__movement:
            self.vel.x = 0
            if self.__allow_change_animation():
                self.current_animation = "IDLE"
            return

        if self.__allow_change_animation():
            self.current_animation = "RUN"

        direction = self.__movement[-1]

        if direction == "A":
            self.vel.x = -self.__speed
            self.__direction = "LEFT"
        if direction == "D":
            self.vel.x = self.__speed
            self.__direction = "RIGHT"

    def __attack(self) -> None:
        offset = 50

        self.current_animation = "ATTACK"

        animation = f"{self.current_animation}_{self.__direction}"
        if self.__animations[animation].done:
            self.__animations[animation].set_one_iteration(True)

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
            self.current_animation = "DEATH"
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
