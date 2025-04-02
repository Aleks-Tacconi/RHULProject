import os
from abc import ABCMeta, abstractmethod
from typing import Tuple

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import AbyssalRevenant, Mage, EvilHand, EvilKnight, DemonSlimeBoss, FlyingDemon
from entities.abstract import Entity
from entities.block import Block
from utils import Mouse, Vector
from simplegui.components import Cutscene, Subtitles


def get_enemy(enemy: str, x: int, y: int, _id: str, direction: str) -> Entity | None:
    pos = Vector(x, y)

    match enemy:
        case "AbyssalRevenant":
            return AbyssalRevenant(pos, _id, start_direction=direction)
        case "Mage":
            return Mage(pos, _id, start_direction=direction)
        case "EvilHand":
            return EvilHand(pos, _id, start_direction=direction)
        case "EvilKnight":
            return EvilKnight(pos, _id, start_direction=direction)
        case "DemonSlimeBoss":
            return DemonSlimeBoss(pos, _id, start_direction=direction)
        case "FlyingDemon":
            return FlyingDemon(pos, _id, start_direction=direction)

class GameLoop(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._mouse = Mouse()
        self._environment = []
        self._enemies = []
        self.__cutscene = None
        self.__subtitles = None

    def _load_level(self, path: str, _id: str) -> None:
        file = os.path.join(path, "enemies.txt")
        with open(file=file, mode="r", encoding="utf-8") as f:
            enemies = [enemy.strip() for enemy in f.readlines()]

        file = os.path.join(path, "entities.txt")
        with open(file=file, mode="r", encoding="utf-8") as f:
            entities = [entity.strip() for entity in f.readlines()]

        for line in enemies:
            enemy, x, y, direction = line.split(",")
            enemy = get_enemy(enemy, int(x), int(y), _id, direction)
            self._enemies.append(enemy)

        for line in entities:
            entity, x, y = line.split(",")
            if "\\" in entity:
                entity = entity.split("\\")
                entity = os.path.join(*entity)
            elif "/" in entity:
                entity = entity.split("/")
                entity = os.path.join(*entity)
            Block(pos=Vector(int(x), int(y)), img=entity, id=_id)

    def mouseclick_handler(self, pos: Tuple[int, int]) -> None:
        self._mouse.click(*pos)

    @abstractmethod
    def mainloop(self, canvas: simplegui.Canvas) -> None: ...

    @abstractmethod
    def keydown_handler(self, key: int) -> None: ...

    @abstractmethod
    def keyup_handler(self, key: int) -> None: ...

    def is_entity_visible(self, player, entity) -> bool:
        hitbox = entity.hitbox_area
        player_x = player.pos.x
        player_y = player.pos.y
        direction = player.direction

        screen_right = player_x + 500
        screen_left = player_x - 500

        if (hitbox[0] < screen_right and hitbox[2] > screen_left):
            return True

        return False

    def cutscene(self, player: Entity) -> None:
        self.__cutscene = Cutscene(player)

    def subtitles(self, prompt: str) -> None:
        self.__subtitles = Subtitles(prompt)
