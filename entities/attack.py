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
        start_frame: int = 1,
        end_frame: int=1,
        frames_per_damage: int=1,
    ) -> None:
        if hitbox_offset is None:
            hitbox_offset = Vector(0, 0)
        super().__init__(
            pos=pos, size=hitbox, hitbox=hitbox, hitbox_offset=hitbox_offset
        )
        self.__damage = damage
        self.__owner = owner
        self.__start_frame = start_frame
        self.__end_frame = end_frame
        self.__frames_per_damage = frames_per_damage
        self.__counter = 0
        self.__still_attacking = True

        Attack.all.append(self)

    def update(self) -> None:
        self.__counter += 1

        if (self.__counter == self.__start_frame and self.__counter % self.__frames_per_damage == 0):
            if len(PhysicsEntity.all) == 0 or self.__owner is None:
                return
            for entity in PhysicsEntity.all:
                if not entity.seen_player:
                    critical_multiplier = 10
                else:
                    critical_multiplier = 1
                if not entity.immune and not self.__owner.friendly:
                    if entity.id != self.__owner.id and entity.collides_with(self):
                        entity.hp -= self.__damage * critical_multiplier
                elif not entity.immune and not entity.friendly:
                    if entity.id != self.__owner.id and entity.collides_with(self):
                        entity.hp -= self.__damage

        if self.__counter == self.__end_frame:
            Attack.remove_attack(self)

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        if self.__counter == self.__start_frame - 1:
            super()._render_hitbox(canvas, offset_x, offset_y)

    
    @classmethod
    def remove_attack(cls, attack: "Attack") -> None:
        cls.all.remove(attack)
