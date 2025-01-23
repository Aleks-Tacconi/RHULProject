try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import os

from dataclasses import dataclass
from dataclasses import field

from PIL import Image

def file():
    if os.name == "nt":
        return r"file:\\"

    return "file://"

@dataclass
class SpriteSheet():
    spritesheet: str = field()
    rows: int = field()
    columns: int = field()

    def __post_init__(self):
        self.spritesheet = os.path.join(os.getcwd(), self.spritesheet)

        print(self.spritesheet)
        image = Image.open(self.spritesheet)
        image_width, image_height = image.size

        self.frame_width = image_width / self.columns
        self.frame_height = image_height / self.rows

        self.frame_center_x = self.frame_width / 2
        self.frame_center_y = self.frame_height / 2

class Animation:
    def __init__(self, spritesheet, rows, columns, frames_per_sprite, flipped=False):
        self.frames_per_sprite = frames_per_sprite

        self.frame_index = [0, 0]
        self.counter = 0
        self.flipped = flipped

        path = os.path.join(os.getcwd(), spritesheet)

        if self.flipped:
            image = Image.open(path).transpose(Image.FLIP_LEFT_RIGHT)
            path = path.replace(".png", "_flipped.png")
            image.save(path)

        self.spritesheet = SpriteSheet(path, rows, columns)

    def update(self):
        self.counter += 1

        if self.counter == self.frames_per_sprite:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.spritesheet.rows

            if self.frame_index[1] == 0:
                self.frame_index[0] = (self.frame_index[0] + 1) % self.spritesheet.columns

            self.counter = 0

    def render(self, canvas, pos, size):
        source_center = [
            self.spritesheet.frame_width * self.frame_index[0] + self.spritesheet.frame_center_x,
            self.spritesheet.frame_height * self.frame_index[1] + self.spritesheet.frame_center_y,
        ]

        source_size = (self.spritesheet.frame_width, self.spritesheet.frame_height)
        img = simplegui.load_image(file() + self.spritesheet.spritesheet)

        canvas.draw_image(img, source_center, source_size, pos, size)
