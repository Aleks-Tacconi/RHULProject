import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity, PhysicsEntity
from .utils import Animation, SpriteSheet


class Block(Entity):
    all = []

    def __init__(
        self, pos: Vector, size: Vector, img: str, rows: int, cols: int
    ) -> None:
        # NOTE: the pos for the block works in grid coords contrary to the pos for other entities
        self.key = f"{pos.x}|{pos.y}"
        pos = Vector(int(pos.x * size.x), int(pos.y * size.y))

        super().__init__(pos, size)

        self.__animation = Animation(
            spritesheet=SpriteSheet(img, rows=rows, cols=cols),
            frames_per_sprite=1,
        )

        Block.all.append(self)

    def render(self, canvas: simplegui.Canvas) -> None:
        self.__animation.render(canvas, self.pos, self.size)

    def update(self) -> None: ...

    def handle_collision_y(self, entity: PhysicsEntity, off_x: int, off_y: int) -> None:
        # TODO: use maths to speed up collisions
        if entity.collides_with(self, off_x, off_y):
            if entity.vel.y > 0:
                while entity.collides_with(self, off_x, off_y):
                    entity.pos.y -= 1
                entity.vel.y = 0
                entity.jumps = 2

    def handle_collision_x(self, entity: PhysicsEntity, off_x: int, off_y: int) -> None:
        # TODO: use maths to speed up collisions
        if entity.collides_with(self, off_x, off_y):
            if entity.vel.x > 0:
                while entity.collides_with(self, off_x, off_y):
                    entity.pos.x -= 1
                entity.vel.x = 0
                entity.current_animation = "IDLE_RIGHT"
            if entity.vel.x < 0:
                while entity.collides_with(self, off_x, off_y):
                    entity.pos.x += 1
                entity.vel.x = 0
                entity.current_animation = "IDLE_LEFT"

    @classmethod
    def collisions_x(cls, entity: PhysicsEntity, off_x: int, off_y: int) -> None:
        for block in cls.all:
            block.handle_collision_x(entity, off_x, off_y)

    @classmethod
    def collisions_y(cls, entity: PhysicsEntity, off_x: int, off_y: int) -> None:
        for block in cls.all:
            block.handle_collision_y(entity, off_x, off_y)
