import os
from copy import deepcopy
from dataclasses import dataclass, field

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from PIL import Image

from utils import Vector


def file_prefix() -> str:
    if os.name == "nt":
        return r"file:\\"

    return "file://"


@dataclass
class SpriteSheet:
    path: str = field()
    rows: int = field()
    cols: int = field()

    def __post_init__(self) -> None:
        self.path = os.path.join(os.getcwd(), self.path)

        image = Image.open(self.path)

        self.frame_width = image.width / self.cols
        self.frame_height = image.height / self.rows

        self.frame_center_x = self.frame_width / 2
        self.frame_center_y = self.frame_height / 2
        self.flipped = False

    def flip(self) -> "SpriteSheet":
        obj = deepcopy(self)

        image = Image.open(obj.path).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        obj.path = obj.path.replace(".png", "_FLIPPED.png")
        image.save(obj.path)
        obj.flipped = True

        return obj


class Animation:
    def __init__(
        self,
        spritesheet: SpriteSheet,
        frames_per_sprite: int,
        one_iteration: bool = False,
    ) -> None:
        self.__spritesheet = spritesheet
        self.__flipped = spritesheet.flipped
        self.__frames_per_sprite = frames_per_sprite
        self.__frame_index = [0, 0]
        self.__counter = 0

        self.__one_iteration_counter = 0
        self.__one_iteration = one_iteration

    @property
    def done(self) -> bool:
        if not self.__one_iteration:
            # NOTE: This is so that loopable animations
            # can be overwritten at any time
            return True

        if (
            self.__one_iteration_counter
            == self.__spritesheet.rows * self.__spritesheet.cols
        ):
            self.__one_iteration_counter = 0
            return True

        return False

    def __update_frame_index(self) -> None:
        self.__frame_index[0] = (self.__frame_index[0] + 1) % self.__spritesheet.cols
        self.__one_iteration_counter += 1

        if self.__frame_index[0] == 0:
            self.__frame_index[1] = (
                self.__frame_index[1] + 1
            ) % self.__spritesheet.rows

        self.__counter = 0

    def update(self) -> None:
        if self.__one_iteration and self.done:
            return

        self.__counter += 1

        if self.__counter == self.__frames_per_sprite:
            self.__update_frame_index()

    def render(self, canvas: simplegui.Canvas, pos: Vector, size: Vector) -> None:
        if self.__flipped:
            source_center = [
                self.__spritesheet.frame_width
                * (self.__spritesheet.cols - self.__frame_index[0] - 1)
                + self.__spritesheet.frame_center_x,
                self.__spritesheet.frame_height
                * (self.__spritesheet.rows - self.__frame_index[1] - 1)
                + self.__spritesheet.frame_center_y,
            ]
        else:
            source_center = [
                self.__spritesheet.frame_width * self.__frame_index[0]
                + self.__spritesheet.frame_center_x,
                self.__spritesheet.frame_height * self.__frame_index[1]
                + self.__spritesheet.frame_center_y,
            ]

        source_size = (
            self.__spritesheet.frame_width,
            self.__spritesheet.frame_height,
        )
        img = simplegui.load_image(file_prefix() + self.__spritesheet.path)

        canvas.draw_image(img, source_center, source_size, pos.get_p(), size.get_p())
