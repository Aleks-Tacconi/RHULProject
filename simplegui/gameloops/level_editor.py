import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (
    SIZE,
    AbyssalRevenant,
    Block,
    DemonSlimeBoss,
    EvilHand,
    EvilKnight,
    FlyingDemon,
    Mage,
)

from entities.attack import Attack
from utils import Vector

from .abstract import GameLoop

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
LEVEL = "level1"


class LevelEditor(GameLoop):
    def __init__(self, reset: Callable, labels: list) -> None:
        super().__init__()

        self.__reset = reset
        self.__camera = Vector(0, 0)

        self.__current = "AbyssalRevenant"
        self.__type = "enemy"

        self.__labels = labels

        self.__toggle = True
        self.__direction = "LEFT"

        self._load_level(os.path.join("levels", LEVEL), "LevelEditor")

        self.__all_enemies = [
            "AbyssalRevenant",
            "Mage",
            "FlyingDemon",
            "DemonSlimeBoss",
            "EvilKnight",
            "EvilHand",
        ]
        self.__all_entities = os.listdir(os.path.join("assets", "blocks"))

    def __set_text(self) -> None:
        self.__labels[0].set_text(
            "Press q to return to main menu, do this before closing application to ensure the level saves!"
        )
        self.__labels[7].set_text(f"current: {self.__current}")
        self.__labels[10].set_text(f"type: {self.__type}")
        self.__labels[13].set_text(f"enemy direction: {self.__direction}")
        self.__labels[16].set_text("[1] enemies")
        self.__labels[17].set_text("[2] blocks")
        self.__labels[18].set_text("[3] toggle guidelines")
        self.__labels[19].set_text("[4] toggle enemy direction")

    def __change_selected(self, dir, lst) -> None:
        new_index = lst.index(self.__current) + dir

        if new_index < 0:
            new_index = len(lst) - 1

        self.__current = lst[new_index % len(lst)]

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__set_text()

        if self.__toggle:
            for i in range(SIZE // 2, CANVAS_WIDTH + 1, SIZE):
                canvas.draw_line((0, i), (CANVAS_HEIGHT, i), 2, "red")

            for i in range(SIZE // 2, CANVAS_HEIGHT + 1, SIZE):
                canvas.draw_line((i, 0), (i, CANVAS_WIDTH), 2, "red")

        if self._mouse.clicked:
            if self.__type == "block":
                x = (self._mouse.x + SIZE // 2) // SIZE - self.__camera.x
                y = (self._mouse.y + SIZE // 2) // SIZE - self.__camera.y
                key = f"LevelEditor|{x}|{y}"

                if key not in Block.all:
                    Block(
                        pos=Vector(x, y),
                        img=os.path.join("assets", "blocks", self.__current),
                        id="LevelEditor",
                    )
                else:
                    del Block.all[key]
            elif self.__type == "enemy":
                x = (self._mouse.x + SIZE // 2) - (self.__camera.x * SIZE)
                y = (self._mouse.y + SIZE // 2) - (self.__camera.y * SIZE)

                changes = False
                enemies = []
                for enemy in self._enemies:
                    if not enemy.collides_with(
                        Attack(Vector(x, y), Vector(5, 5), 0, Vector(0, 0), None)
                    ):
                        enemies.append(enemy)
                    else:
                        changes = True

                self._enemies = enemies

                if not changes:
                    if self.__current == "AbyssalRevenant":
                        self._enemies.append(
                            AbyssalRevenant(
                                pos=Vector(x, y),
                                level_id="LevelEditor",
                                start_direction=self.__direction,
                            )
                        )
                    if self.__current == "Mage":
                        self._enemies.append(
                            Mage(
                                pos=Vector(x, y),
                                level_id="LevelEditor",
                                start_direction=self.__direction,
                            )
                        )
                    if self.__current == "DemonSlimeBoss":
                        self._enemies.append(
                            DemonSlimeBoss(
                                pos=Vector(x, y),
                                level_id="LevelEditor",
                                start_direction=self.__direction,
                            )
                        )
                    if self.__current == "FlyingDemon":
                        self._enemies.append(
                            FlyingDemon(
                                pos=Vector(x, y),
                                level_id="LevelEditor",
                                start_direction=self.__direction,
                            )
                        )
                    if self.__current == "EvilKnight":
                        self._enemies.append(
                            EvilKnight(
                                pos=Vector(x, y),
                                level_id="LevelEditor",
                                start_direction=self.__direction,
                            )
                        )
                    if self.__current == "EvilHand":
                        self._enemies.append(
                            EvilHand(
                                pos=Vector(x, y),
                                level_id="LevelEditor",
                                start_direction=self.__direction,
                            )
                        )

            self._mouse.clicked = False

        self.__save()

        for k, block in Block.all.items():
            if "LevelEditor" in k:
                block.render(canvas, self.__camera.x * SIZE, self.__camera.y * SIZE)

        for enemy in self._enemies:
            enemy.render(canvas, self.__camera.x * SIZE, self.__camera.y * SIZE)

    def __save(self) -> None:
        path = os.path.join("levels", LEVEL)

        if not os.path.exists(path):
            os.mkdir(path)

        with open(
            file=os.path.join(path, "entities.txt"), mode="w+", encoding="utf-8"
        ) as f:
            for k, v in Block.all.items():
                if "LevelEditor" in k:
                    f.write(f"{v.img},{v.pos.x//SIZE},{v.pos.y//SIZE}\n")

        with open(
            file=os.path.join(path, "enemies.txt"), mode="w+", encoding="utf-8"
        ) as f:
            for enemy in self._enemies:
                enemy_id = str(enemy)
                f.write(f"{enemy_id},{enemy.pos.x},{enemy.pos.y},{enemy.direction}\n")

    def keyup_handler(self, key: int) -> None: ...

    def keydown_handler(self, key: int) -> None:
        print(key)

        if key == 49:
            self.__type = "enemy"
            self.__current = self.__all_enemies[0]
        if key == 50:
            self.__type = "block"
            self.__current = self.__all_entities[0]

        if key == 52:
            if self.__direction == "LEFT":
                self.__direction = "RIGHT"
            elif self.__direction == "RIGHT":
                self.__direction = "LEFT"

        if self.__type == "enemy":
            if key == 37:
                self.__change_selected(-1, self.__all_enemies)
            if key == 39:
                self.__change_selected(1, self.__all_enemies)
        elif self.__type == "block":
            if key == 37:
                self.__change_selected(-1, self.__all_entities)
            if key == 39:
                self.__change_selected(1, self.__all_entities)

        if key == 87:
            self.__camera.y += 1
        if key == 83:
            self.__camera.y -= 1

        if key == 65:
            self.__camera.x += 1
        if key == 68:
            self.__camera.x -= 1
        if key == 51:
            self.__toggle = not self.__toggle
        if key == 81:
            for label in self.__labels:
                label.set_text("")
            self.__reset()
