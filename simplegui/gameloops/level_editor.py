import os
from typing import Callable, Iterable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import SIZE, AbyssalRevenant, Block, Mage, DemonSlimeBoss, FlyingDemon, EvilKnight
from entities.abstract.entity import Entity
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

        self.__current = "grass.jpg"
        self.__type = "block"

        self.__labels = labels

        self.__toggle = True

        self._load_level(os.path.join("levels", LEVEL), "LevelEditor")

    def __set_text(self) -> None:
        self.__labels[0].set_text("Press q to return to main menu, do this before closing application to ensure the level saves!")
        self.__labels[7].set_text(f"current: {self.__current}")
        self.__labels[9].set_text("[1] grass block")
        self.__labels[10].set_text("[2] stone block")
        self.__labels[11].set_text("[3] abyssal revenant")
        self.__labels[12].set_text("[4] mage")
        self.__labels[13].set_text("[5] flying demon")
        self.__labels[14].set_text("[6] demon slime boss")
        self.__labels[15].set_text("[7] evil knight")
        self.__labels[16].set_text("[9] toggle lines")

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
                        self._enemies.append(AbyssalRevenant(pos=Vector(x, y), level_id="LevelEditor"))
                    if self.__current == "Mage":
                        self._enemies.append(Mage(pos=Vector(x, y), level_id="LevelEditor"))
                    if self.__current == "DEMON SLIME BOSS":
                        self._enemies.append(DemonSlimeBoss(pos=Vector(x, y), level_id="LevelEditor"))
                    if self.__current == "FLYING DEMON":
                        self._enemies.append(FlyingDemon(pos=Vector(x, y), level_id="LevelEditor"))
                    if self.__current == "EVIL KNIGHT":
                        self._enemies.append(EvilKnight(pos=Vector(x, y), level_id="LevelEditor"))

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
                f.write(f"{enemy_id},{enemy.pos.x},{enemy.pos.y}\n")


    def keyup_handler(self, key: int) -> None: ...

    def keydown_handler(self, key: int) -> None:
        if key == 87:
            self.__camera.y += 1
        if key == 83:
            self.__camera.y -= 1

        if key == 65:
            self.__camera.x += 1
        if key == 68:
            self.__camera.x -= 1
        if key == 49:
            self.__current = "grass.jpg"
            self.__type = "block"
        if key == 50:
            self.__current = "stone.png"
            self.__type = "block"
        if key == 51:
            self.__current = "AbyssalRevenant"
            self.__type = "enemy"
        if key == 52:
            self.__current = "Mage"
            self.__type = "enemy"
        if key == 53:
            self.__current = "FLYING DEMON"
            self.__type = "enemy"
        if key == 54:
            self.__current = "DEMON SLIME BOSS"
            self.__type = "enemy"
            if key == 55:
                self.__current = "EVIL KNIGHT"
                self.__type = "enemy"
        if key == 57:
            self.__toggle = not self.__toggle
        if key == 81:
            for label in self.__labels:
                label.set_text("")
            self.__reset()
