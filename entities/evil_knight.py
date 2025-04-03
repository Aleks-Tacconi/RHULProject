import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import PhysicsEntity
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet, PlaySound
import random


class EvilKnight(PhysicsEntity):
    def __init__(self, pos: Vector, level_id: str, start_direction = "LEFT") -> None:
        super().__init__(
            pos=pos,
            size=Vector(200, 200),
            vel=Vector(0, 0),
            hitbox=Vector(40, 92),
            hp=5000,
            level_id=level_id,
            hitbox_offset=Vector(-5, 55),
            direction=start_direction,
        )

        spritesheet = SpriteSheet(
            os.path.join("assets", "evil_knight", "KNIGHT.png"),
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
            "CROUCH_ATTACK_RIGHT": (7, 4, 2, False),
            "CROUCH_FULL_RIGHT": (8, 3, 1, False),
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
            "ROLL_RIGHT": (19, 12, 1, False),
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
            "ATTACK_COMBO_LEFT": (3, 10, 2, True),
            "ATTACK_COMBO_NO_MOVEMENT_LEFT": (4, 10, 10, True),
            "ATTACK_OVERHEAD_NO_MOVEMENT_LEFT": (5, 4, 4, True),
            "CROUCH_LEFT": (6, 1, 1, True),
            "CROUCH_ATTACK_LEFT": (7, 4, 2, True),
            "CROUCH_FULL_LEFT": (8, 3, 1, True),
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
            "ROLL_LEFT": (19, 12, 1, True),
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

        self.__sound = PlaySound()
        self.__sound.change_volume(0.3)
        self.__sounds = {"DEATH": "death_2_ian.wav",
                         "DAMAGE1": "damage_1_ian.wav",
                         "DAMAGE2": "damage_2_ian.wav",
                         "DAMAGE3": "damage_3_ian.wav",
                         "DAMAGE4": "damage_4_ian.wav",
                         "DAMAGE5": "damage_5_ian.wav",
                         "DAMAGE6": "damage_6_ian.wav",
                         "DAMAGE7": "damage_7_ian.wav",
                         "DAMAGE8": "damage_8_ian.wav",
                         "DAMAGE9": "damage_9_ian.wav",
                         "DAMAGE10": "damage_10_ian.wav",
                         "ATTACK1": "07_human_atk_sword_1.wav",
                         "ATTACK2": "07_human_atk_sword_2.wav",
                         "ATTACK3": "07_human_atk_sword_3.wav",
                         "GRUNT1": "grunting_1_ian.wav",
                         "GRUNT2": "grunting_2_ian.wav",
                         "GRUNT3": "grunting_3_ian.wav",
                         "GRUNT4": "grunting_4_ian.wav",
                         "GRUNT5": "grunting_5_ian.wav",
                         "GRUNT6": "grunting_6_ian.wav",
                         "GRUNT7": "grunting_7_ian.wav",
                         "GRUNT8": "grunting_8_ian.wav",
                         "GRUNT9": "grunting_9_ian.wav",
                         "GRUNT10": "grunting_10_ian.wav",
                         }

        self.points = 100
        self.xp = 50
        self.direction = start_direction
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__jumps = 1
        self.__movement_x = []
        self.__movement_y = []
        self.__speed = 5
        self.__crouched = False
        self.__rolling = False
        self.__dead = False
        self.immune = True
        self.__distance_x = 1000
        self.__distance_y = 0
        self.__detection_range_x = 300
        self.__detection_range_y = 100
        self.__attack_distance = 70
        self.__base_hp = self.hp
        self.__player = None
        self.__seen_player = False


    def remove(self) -> bool:
        if self.__animations.done() and self.__dead:
            return True
        return False

    def update(self) -> None:
        if self.hp != self.__base_hp:
            self.__seen_player = True
        self._get_direction()
        self._knockback(self.__player)
        self._gravity()
        self.__death()

        self.__roll()
        if self.__animations.done():
            self.__rolling = False
            self.immune = False
            self.__idle()
            self.__move()
            self.__attack()

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)
        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        if self.direction == "LEFT":
            pos = Vector(int(self.pos.x + offset_x - 10), int(self.pos.y + offset_y))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, offset_x, offset_y)
        else:
            pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
            self.__animations.render(canvas, pos, self.size)
            self._render_hitbox(canvas, offset_x, offset_y)
        self.healthbar(canvas, offset_x, offset_y)

    def __idle(self) -> None:
        if abs(self.__distance_x) > self.__detection_range_x:
            self.vel.x = 0
            self.__animations.set_animation(f"IDLE_{self.direction}")

    def __jump(self) -> None:
        if self.__jumps > 0:
            self.vel.y = -12
            self.__jumps -= 1

    def __move(self) -> None:
        if ((abs(self.__distance_x) > self.__detection_range_x or abs(self.__distance_y) > self.__detection_range_y) or
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

    def __attack(self) -> None:
        if abs(self.__distance_x) > self.__attack_distance or not self.__seen_player:
            return

        self.vel.x = 0
        offset = 50

        if self.__distance_x > 0:
            self.direction = "LEFT"
            offset *= -1
        else:
            self.direction = "RIGHT"

        Attack(
            pos=Vector(int(self.pos.x + offset), int(self.pos.y + 30)),
            hitbox=Vector(100, 100),
            hitbox_offset=Vector(0, 30),
            start_frame= 10,
            end_frame=10,
            damage=500,
            owner=self,
        )
        self.__sound.play_sound(self.__sounds.get(f"GRUNT{random.randint(1, 10)}"),
                                self.__sounds.get(f"ATTACK{random.randint(1, 3)}"))

        if self.__crouched:
            self.__animations.set_animation(f"CROUCH_ATTACK_{self.direction}")
            self.__animations.set_one_iteration(True)
            return


        self.__animations.set_animation(f"ATTACK_COMBO_{self.direction}")
        self.__animations.set_one_iteration(True)

    def __crouch(self) -> None:
        self.vel.y = 12
        self.__crouched = True
        self.hitbox = Vector(40, 66)
        self.hitbox_offset = Vector(-5, 68)
        self.__current_animation = "CROUCH"

    def __roll(self):
        if (random.randint(1,10) == 1 and abs(self.__distance_x) <= self.__attack_distance and
                self.__player.is_attacking and self.vel.x == 0):
            if self.direction == "RIGHT":
                self.vel.x += self.__speed
            else:
                self.vel.x -= self.__speed

            if not self.__rolling:
                self.__animations.set_one_iteration(False)
            self.__current_animation = f"ROLL_{self.direction}"
            self.__animations.set_animation(self.__current_animation)
            self.immune = True
            self.__rolling = True
            self.__animations.set_one_iteration(True)

    def __take_damage(self):
        if self.__original_hp != self.hp:
            self.__original_hp = self.hp
            self.__sound.play_sound(self.__sounds.get(f"DAMAGE{random.randint(1, 10)}"))

    def __death(self) -> None:
        if not self.is_alive:
            self.__sound.play_sound(self.__sounds.get("DEATH"))
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

    def interaction(self, entity: PhysicsEntity) -> None:
        self.__distance_x = self.pos.x - entity.pos.x
        self.__distance_y = self.pos.y - entity.pos.y
        self.__player = entity

    def __str__(self) -> str:
        return "EvilKnight"

