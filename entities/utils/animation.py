"""Animation module.

Module for handling sprite sheets and animations. This module provides a simple interface
for managing different animations which all have their own spritesheet.

File:
    entities/utils/animation.py

Functions:
    file: Returns the appropriate prefix for file paths depending on users OS.

Classes:
    SpriteSheet: Dataclass storing the attributes of a sprite sheet.
    Animation: An animation entity that updates and renders the sprite.
"""

import os
from copy import deepcopy
from dataclasses import dataclass, field

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from PIL import Image

from utils.vector import Vector


def file() -> str:
    """Prefix for rendering images from a file

    Returns:
        str: The prefix.
    """
    if os.name == "nt":
        return r"file:\\"

    return "file://"


@dataclass
class SpriteSheet:
    """Dataclass storing the attributes of a sprite sheet

    Attributes:
        path (str): The path to the sprite sheet.
        rows (int): The number of rows the sprite sheet contains.
        cols (int): The number of columns the sprite sheet contains.
        frame_width (int): The width of a single sprite sheet frame.
        frame_height (int): The height of a single sprite sheet frame.
        frame_center_x (int): The center of a single sprite sheet frame (relative to (0, 0))
        frame_center_y (int): The center of a single sprite sheet frame (relative to (0, 0))

    Methods:
        flip(self) -> SpriteSheet: Flips the sprite sheet.
    """

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

    def flip(self) -> "SpriteSheet":
        """Flips the sprite sheet.

        Returns:
            SpriteSheet: The flipped sprite sheet.
        """

        obj = deepcopy(self)

        image = Image.open(obj.path).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        obj.path = obj.path.replace(".png", "_FLIPPED.png")
        image.save(obj.path)

        return obj


class Animation:
    """Animation entity

    This class handles the logic for updating and rendering sprites from a sprite sheet.
    This class controls when the sprite frame should be updated and the rendering of the
    frame itself.

    Attributes:
        _spritesheet (SpriteSheet): dataclass instance which stores info about the spritesheet.
        _frames_per_sprite (int): The num of frames per sprite before moving on to the next frame.
        _frame_index (List[int]): A list containing the pos of the current frame.
        _counter (int): A counter to keep track of when to transition to the next frame.

    Methods:
        update() -> None: Moves on to the next frame accordingly.
        render(canvas: simplegui.Canvas, pos: Vector, size: Vector) -> None: Renders the current
                                                                             frame on the canvas
        __update_frame_index() -> None: Handles the logic of updating the __frame_index attribute
    """

    def __init__(self, spritesheet: SpriteSheet, frames_per_sprite: int) -> None:
        self._spritesheet = spritesheet
        self._flipped_spritesheet = spritesheet.flip()
        self._flipped = False
        self._frames_per_sprite = frames_per_sprite
        self._frame_index = [0, 0]
        self._counter = 0

    def update(self) -> None:
        """Moves on to the next frame accordingly.

        This function should be called every frame in the mainloop.
        """
        self._counter += 1

        if self._counter == self._frames_per_sprite:
            self.__update_frame_index()

    def render(self, canvas: simplegui.Canvas, pos: Vector, size: Vector) -> None:
        """Renders the current frame on the canvas

        Args:
            canvas (simplegui.Canvas): The canvas the frame will be rendered on.
            pos (Vector): Where the image will be rendered.
            size (Vector): The size of the image.
        """
        if self._flipped:
            source_center = [
                self._flipped_spritesheet.frame_width * self._frame_index[0]
                + self._flipped_spritesheet.frame_center_x,
                self._flipped_spritesheet.frame_height * self._frame_index[1]
                + self._flipped_spritesheet.frame_center_y,
            ]
            source_size = (self._flipped_spritesheet.frame_width, self._flipped_spritesheet.frame_height)
            img = simplegui.load_image(file() + self._flipped_spritesheet.path)

            canvas.draw_image(img, source_center, source_size, pos.get_p(), size.get_p())
        else:
            source_center = [
                self._spritesheet.frame_width * self._frame_index[0]
                + self._spritesheet.frame_center_x,
                self._spritesheet.frame_height * self._frame_index[1]
                + self._spritesheet.frame_center_y,
            ]

            source_size = (self._spritesheet.frame_width, self._spritesheet.frame_height)
            img = simplegui.load_image(file() + self._spritesheet.path)

            canvas.draw_image(img, source_center, source_size, pos.get_p(), size.get_p())

    def __update_frame_index(self) -> None:
        self._frame_index[0] = (self._frame_index[0] + 1) % self._spritesheet.cols

        if self._frame_index[0] == 0:
            self._frame_index[1] = (
                                           self._frame_index[1] + 1
            ) % self._spritesheet.rows

        self._counter = 0

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
class MultiAnimation(Animation):

    def __init__(self, spritesheet: SpriteSheet, animations: dict[str, tuple[int, int, int, int, bool]], default: str):
        self.__spriteshet = spritesheet
        super().__init__(spritesheet, animations[default][3])
        if animations[default][4]:
            self._flipped = True
        self.__animations = animations
        self.__current_animation = default
        self.__start_frame = animations[self.__current_animation][1] - animations[self.__current_animation][2]
        self.__end_frame = animations[self.__current_animation][1]
        self._frame_index = [self.__start_frame, animations[self.__current_animation][0]]

    def set_animation(self, animation_name: str):
        if animation_name in self.__animations and animation_name != self.__current_animation:
            if self.__animations[animation_name][4]:
                self._flipped = True
            else:
                self._flipped = False
            self.__current_animation = animation_name
            self.__start_frame = (self.__animations[self.__current_animation][1]
                                  - self.__animations[self.__current_animation][2])
            self.__end_frame = self.__animations[self.__current_animation][1]
            self._frame_index = [self.__start_frame, self.__animations[self.__current_animation][0]]
            self._frames_per_sprite = self.__animations[self.__current_animation][3]
            self._counter = 0

    def get_animation(self):
        return self.__current_animation

    def update(self) -> None:
        """Moves on to the next frame accordingly.

        This function should be called every frame in the mainloop.
        """
        self._counter += 1

        if self._counter == self._frames_per_sprite:
            self.__update_frame_index()

    def __update_frame_index(self) -> None:
        self._frame_index[0] = (self._frame_index[0] + 1) % self.__end_frame
        if self._frame_index[0] == 0:
            self._frame_index[0] = self.__start_frame
        self._counter = 0



