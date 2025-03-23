import os

from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity, PhysicsEntity

from .utils import Animation, SpriteSheet

class PlayerHealthBar(Entity):
    def __init__(self, pos: Vector, player: PhysicsEntity) -> None:

        original_size_x = 64
        original_size_y = 16
        scale_factor = 4
        scaled_size_x = original_size_x * scale_factor
        scaled_size_y = original_size_y * scale_factor

        super().__init__(
            pos=Vector(int(pos.x), int(pos.y)),
            size=Vector(scaled_size_x, scaled_size_y),
            hitbox=Vector(0,0)
        )

        spritesheet = SpriteSheet(os.path.join("assets", "player_gui", "HEALTHBAR.png"), rows = 41, cols = 1)

        self.__animation = Animation(spritesheet, 1)
        self.__player = player
        self.__max_hp = self.__player.hp
        self.__hp_per_frame = self.__player.hp / (spritesheet.rows - 1)
        self.__frame = 0

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animation.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

    def __threshold_hp_change(self):
        while self.__frame < 40 and self.__player.hp < self.__max_hp - (self.__frame + 1) * self.__hp_per_frame:
            self.__frame += 1
            return True

    def update(self) -> None:
        if self.__threshold_hp_change():
            self.__animation.update()
