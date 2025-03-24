import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

from .abstract import Entity, PhysicsEntity


class Attack(Entity):
    all = []

    def __init__(
        self,
        pos: Vector,
        hitbox: Vector,
        damage: int,
        hitbox_offset: None,
        owner: Entity,
        frame_time: int=1,
    ) -> None:
        if hitbox_offset is None:
            hitbox_offset = Vector(0, 0)
        super().__init__(
            pos=pos, size=hitbox, hitbox=hitbox, hitbox_offset=hitbox_offset
        )
        self.__damage = damage
        self.__owner = owner
        self.__frame_time = frame_time
        self.__counter = 0

        Attack.all.append(self)

    def update(self) -> None:
        self.__counter += 1

        for entity in PhysicsEntity.all:
            if not entity.immune:
                if entity.id != self.__owner.id and entity.collides_with(self):
                    entity.hp -= self.__damage

        if self.__counter == self.__frame_time:
            Attack.remove_attack(self)

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        super()._render_hitbox(canvas, offset_x, offset_y)

    @classmethod
    def remove_attack(cls, attack: "Attack") -> None:
        cls.all.remove(attack)
