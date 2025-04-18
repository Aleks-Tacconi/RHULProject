import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from entities.abstract.physics_entity import PhysicsEntity
from utils import Vector

from .abstract import Enemy
from .attack import Attack
from .block import Block
from .utils import MultiAnimation, SpriteSheet, PlaySound
from .fire import Fire
import random

class DemonSlimeBoss(Enemy):
    def __init__(self, pos: Vector, level_id: str, start_direction = "LEFT") -> None:
        super().__init__(
            pos=pos,
            size=Vector(576, 320),
            hitbox=Vector(120, 200),
            vel=Vector(0, 0),
            hp=100000,
            level_id=level_id,
            hitbox_offset=Vector(0, 20),
            direction=start_direction,
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
        self.xp = 300
        self.direction = start_direction
        self.__current_animation = f"IDLE_{self.direction}"
        self.__animations.set_animation(self.__current_animation)
        self.__distance_x = 1000
        self.__distance_y = 0
        self.__detection_range_x = 500
        self.__detection_range_y = 500
        self.__attack_distance = 100
        self.__speed = 1
        self.__original_hp = self.hp
        self.__fires = []
        self.__dead = False
        self.boss = True
        self.__player = None
        self.__player_x = None
        self.seen_player = False
        self.knockback_chance = 0.01
        self.__sound = PlaySound()
        self.__sound.change_volume(0.3)
        self.__sounds = {"ATTACK1": "Sword Impact Hit 1.wav",
                         "ATTACK2": "Sword Impact Hit 2.wav",
                         "ATTACK3": "Sword Impact Hit 3.wav",
                         "ATTACK4": "Wave Attack 1.wav",
                         "ATTACK5": "Wave Attack 2.wav",
                         "FIRE1": "Fireball 1.wav",
                         "FIRE2": "Fireball 2.wav",
                         "FIRE3": "Fireball 3.wav",
                         }

    def __idle(self) -> None:
        if abs(self.__distance_x) > self.__detection_range_x:
            self.vel.x = 0
            self.__animations.set_animation(f"IDLE_{self.direction}")

    def update(self) -> None:
        self._get_direction()
        self._knockback(self.__player)
        self._gravity()
        self.__death()

        if self.__animations.done() and self.is_alive:
            self.__idle()
            self.__move()
            self.__attack()
            self.__fire()
            self.__take_damage()
        for fire in self.__fires:
            fire.interaction(self.__player)
            fire.update()
            if fire.remove():
                self.__fires.remove(fire)

        self.pos.x += self.vel.x
        Block.collisions_x(self, self._level_id)
        self.pos.y += self.vel.y
        Block.collisions_y(self, self._level_id)
        self.__animations.update()


    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y - 40))
        self.__animations.render(canvas, pos, self.size)
        if self.__fires:
            for fire in self.__fires:
                fire.render(canvas, offset_x, offset_y)
        self._render_hitbox(canvas, offset_x, offset_y)
        self.healthbar(canvas, offset_x, offset_y)

    def __fire(self) -> None:
        if abs(self.__distance_x) > self.__detection_range_x:
            return
        if random.randint(1,20) == 1:
            self.__fires.append(Fire(self.__player_x + random.randint(-20,20), level_id="LevelEditor"))
            self.__sound.play_sound(self.__sounds.get(f"FIRE{random.randint(1, 3)}"))



    def __attack(self) -> None:
        if (abs(self.__distance_x) > self.__attack_distance or
                self.__player is None or not self.seen_player):
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
            hitbox=Vector(69, 200),
            hitbox_offset=None,
            start_frame=7,
            end_frame=7,
            damage=1000,
            owner=self,
        )
        self.__sound.play_sound(self.__sounds.get(f"ATTACK{random.randint(1, 5)}"))

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
        if ((abs(self.__distance_x) > self.__detection_range_x or abs(self.__distance_y) > self.__detection_range_y) or
                self.__player is None):
            return

        if self.__player.crouched and not self.seen_player:
            if not (self.direction == "LEFT" and self.__distance_x > 0 or
                    self.direction == "RIGHT" and self.__distance_x < 0):
                return
        if self.__distance_x > 0:
            self.vel.x = -self.__speed
        else:
            self.vel.x = self.__speed
        self.seen_player = True
        self.__animations.set_animation(f"RUN_{self.direction}")

    def __take_damage(self):
        if self.__original_hp != self.hp:
            self.__original_hp = self.hp
            self.seen_player = True


    def interaction(self, entity: PhysicsEntity) -> None:
        self.__distance_x = self.pos.x - entity.pos.x
        self.__distance_y = self.pos.y - entity.pos.y
        self.__player_x = entity.pos.x
        self.__player = entity

    def __str__(self) -> str:
        return "DemonSlimeBoss"



