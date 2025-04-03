import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity, PhysicsEntity
from .utils import Animation, SpriteSheet

SIZE = 32
SURROUNDINGS = [
    [2, 5],  [1, 5],  [0, 5],  [-1, 5],  [-2, 5],
    [2, 4],  [1, 4],  [0, 4],  [-1, 4],  [-2, 4],
    [2, 3],  [1, 3],  [0, 3],  [-1, 3],  [-2, 3],
    [2, 2],  [1, 2],  [0, 2],  [-1, 2],  [-2, 2],
    [2, 1],  [1, 1],  [0, 1],  [-1, 1],  [-2, 1],
    [2, 0],  [1, 0],  [0, 0],  [-1, 0],  [-2, 0],
    [2, -1], [1, -1], [0, -1], [-1, -1], [-2, -1],
    [2, -2], [1, -2], [0, -2], [-1, -2], [-2, -2],
    [2, -3], [1, -3], [0, -3], [-1, -3], [-2, -3],
    [2, -4], [1, -4], [0, -4], [-1, -4], [-2, -4],
    [2, -5], [1, -5], [0, -5], [-1, -5], [-2, -5],
]

SURROUNDINGS_CROUCHED = [[0, 3], [1, 3], [-1, 3], [0, 2], [1, 2], [-1, 2],[0, -1], [-1, -1], [1, -1]]





class Block(Entity):
    all = {}

    def __init__(self, pos: Vector, img: str, id: str) -> None:
        # id refers to the current level
        key = f"{id}|{pos.x}|{pos.y}"

        self.img = img

        super().__init__(
            pos=Vector(int(pos.x * SIZE), int(pos.y * SIZE)),
            size=Vector(SIZE, SIZE),
            hitbox=Vector(SIZE, SIZE),
        )

        self.__animation = Animation(
            spritesheet=SpriteSheet(img, rows=1, cols=1),
            frames_per_sprite=1,
        )

        Block.all[key] = self

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animation.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)

    def update(self) -> None: ...

    def handle_collision_x(self, entity: PhysicsEntity) -> None:
        if entity.collides_with(self):
            if entity.vel.x >= 0:
                entity.pos.x = (
                    self.pos.x - (self.hitbox.x // 2) - (entity.hitbox.x // 2)
                ) - entity.hitbox_offset.x
                entity.set_idle()
            if entity.vel.x < 0:
                entity.pos.x = (
                    self.pos.x + (self.hitbox.x // 2) + (entity.hitbox.x // 2)
                ) - entity.hitbox_offset.x
                entity.set_idle()

    def handle_collision_y(self, entity: PhysicsEntity) -> None:
        if entity.collides_with(self):
            if entity.vel.y >= 0:
                entity.pos.y = (
                    (self.pos.y - (self.hitbox.y // 2))
                    - (entity.hitbox.y // 2)
                    - entity.hitbox_offset.y
                )

                entity.vel.y = 0
                entity.jumps = 2

            if entity.vel.y < 0:
                entity.pos.y = (
                    (self.pos.y + (self.hitbox.y // 2))
                    + (entity.hitbox.y // 2)
                    - entity.hitbox_offset.y
                )

    @classmethod
    def __get_surroundings(cls, x: int, y: int, id: str) -> list:
        surroundings = []
        for sx, sy in SURROUNDINGS:
            key = f"{id}|{int(x + sx)}|{int(y + sy)}"
            if key in cls.all:
                surroundings.append(cls.all[key])

        return surroundings

    @classmethod
    def __get_surroundings_for_crouch(cls, x: int, y: int, id: str) -> list:
        surroundings = []
        for sx, sy in SURROUNDINGS_CROUCHED:
            key = f"{id}|{int(x + sx)}|{int(y + sy)}"
            if key in cls.all:
                surroundings.append(cls.all[key])

        return surroundings

    @classmethod
    def collisions_x(cls, entity: PhysicsEntity, id: str) -> None:
        x = int((entity.pos.x + entity.hitbox_offset.x) // SIZE)
        y = int((entity.pos.y + entity.hitbox_offset.y) // SIZE)

        for block in cls.__get_surroundings(x, y, id):
            block.handle_collision_x(entity)

    @classmethod
    def collisions_y(cls, entity: PhysicsEntity, id: str) -> None:
        x = int((entity.pos.x + entity.hitbox_offset.x) // SIZE)
        y = int((entity.pos.y + entity.hitbox_offset.y) // SIZE)

        for block in cls.__get_surroundings(x, y, id):
            block.handle_collision_y(entity)

    @classmethod
    def collisions_crouch_x(cls, entity: PhysicsEntity, id: str) -> bool:
        x = int((entity.pos.x + entity.hitbox_offset.x) // SIZE)
        y = int((entity.pos.y + entity.hitbox_offset.y) // SIZE)

        for block in cls.__get_surroundings(x, y, id):
            if block.handle_crouch_collision_y(entity):
                return True
        return False

    @classmethod
    def collisions_crouch_y(cls, entity: PhysicsEntity, id: str) -> bool:
        x = int((entity.pos.x + entity.hitbox_offset.x) // SIZE)
        y = int((entity.pos.y + entity.hitbox_offset.y) // SIZE)

        for block in cls.__get_surroundings_for_crouch(x, y, id):
           if block.handle_crouch_collision_y(entity):
               return True
        return False

    def handle_crouch_collision_x(self, entity: PhysicsEntity) -> bool:
        return entity.collides_with_crouch(self)


    def handle_crouch_collision_y(self, entity: PhysicsEntity) -> bool:
        return entity.collides_with_crouch(self)

