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
            == (self.__spritesheet.rows * self.__spritesheet.cols) - 1
        ):
            self.__one_iteration_counter = 0
            self.__one_iteration = False
            return True

        return False

    def set_one_iteration(self, boolean: bool):
        self.__one_iteration = boolean

    def __update_frame_index(self) -> None:
        self.__frame_index[0] = (self.__frame_index[0] + 1) % self.__spritesheet.cols

        if self.__frame_index[0] == 0:
            self.__frame_index[1] = (
                self.__frame_index[1] + 1
            ) % self.__spritesheet.rows

        self.__counter = 0
        if self.__one_iteration:
            self.__one_iteration_counter += 1

    def update(self) -> None:


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

    """MultiAnimation entity

    This class handles the logic for updating and rendering sprites from a sprite sheet with multiple animations.
    This class controls when the sprite frame should be updated and the rendering of the
    frame itself. Uses the Animation class as its basis.

    Attributes:
        _spritesheet (SpriteSheet): dataclass instance which stores info about the spritesheet.
        animations (dict [str, tuple[int, int, int, int, bool]]): Dictionary of each animation and its starting row,
        start column, ending column, number of frames, and a boolean for if the spritesheet needs to be flipped.
        current_anim (str): Name of animation

    Methods:
        update() -> None: Moves on to the next frame accordingly.
        __update_frame_index() -> None: Handles the logic of updating the __frame_index attribute
        set_animation -> To change the animation
        get_animation -> To get the current animation
    """
class MultiAnimation:

    def __init__(self, spritesheet: SpriteSheet, animations: dict[str, tuple[int, int, int, bool]]):
        self.__spritesheet = spritesheet
        self.__flipped_spritesheet = spritesheet.flip()
        self.__animations = animations
        self.__current_animation = None
        self.__flip = False
        self.__one_iteration_counter = 0
        self.__one_iteration = False
        self.__frames_per_animation = 0
        self.__counter = 0
        self.__start_frame = 0
        self.__end_frame = 0
        self.__frame_index = [0,0]

    def done(self) -> bool:
        if not self.__one_iteration:
            # NOTE: This is so that loopable animations
            # can be overwritten at any time
            return True

        if (
            self.__one_iteration_counter
            == (self.__animations[self.__current_animation][1]) - 1
        ):
            self.__one_iteration_counter = 0
            self.__one_iteration = False
            return True

        return False

    def set_animation(self, animation_name: str):
        if not self.__one_iteration:
            if animation_name in self.__animations and animation_name != self.__current_animation:
                self.__current_animation = animation_name
                if self.__animations[animation_name][3]:
                    self.__flip = True
                    self.__start_frame = self.__spritesheet.cols - 1
                    self.__end_frame = self.__start_frame - self.__animations[self.__current_animation][1]
                else:
                    self.__flip = False
                    self.__end_frame = self.__animations[self.__current_animation][1]
                    self.__start_frame = 0
                self.__frame_index = [self.__start_frame, self.__animations[self.__current_animation][0]]
                self.__frames_per_animation = self.__animations[self.__current_animation][2]
                self.__counter = 0

    def get_animation(self):
        return self.__current_animation

    def set_one_iteration(self, boolean: bool):
        self.__one_iteration = boolean

    def update(self) -> None:


        self.__counter += 1


        if self.__counter == self.__frames_per_animation:
            self.__update_frame_index()

    def __update_frame_index(self) -> None:

        if not self.__flip:
            self.__frame_index[0] = (self.__frame_index[0] + 1) % self.__end_frame
            if self.__frame_index[0] == 0:
                self.__frame_index[0] = self.__start_frame
        else:
            self.__frame_index[0] = (self.__frame_index[0] - 1)
            if self.__frame_index[0] <= self.__end_frame:
                self.__frame_index[0] = self.__start_frame
        self.__counter = 0

        if self.__one_iteration:
            self.__one_iteration_counter += 1


    def render(self, canvas: simplegui.Canvas, pos: Vector, size: Vector) -> None:
        if self.__flip:
            source_center = [
                self.__flipped_spritesheet.frame_width * self.__frame_index[0]
                + self.__flipped_spritesheet.frame_center_x,
                self.__flipped_spritesheet.frame_height * self.__frame_index[1]
                + self.__flipped_spritesheet.frame_center_y,
            ]
            img = simplegui.load_image(file_prefix() + self.__flipped_spritesheet.path)
        else:
            source_center = [
                self.__spritesheet.frame_width * self.__frame_index[0]
                + self.__spritesheet.frame_center_x,
                self.__spritesheet.frame_height * self.__frame_index[1]
                + self.__spritesheet.frame_center_y,
            ]
            img = simplegui.load_image(file_prefix() + self.__spritesheet.path)

        source_size = (
            self.__spritesheet.frame_width,
            self.__spritesheet.frame_height,
        )

        canvas.draw_image(img, source_center, source_size, pos.get_p(), size.get_p())
