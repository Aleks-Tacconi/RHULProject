from entities import Trigger
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
from entities.utils import Animation, SpriteSheet

class Interactable:
    def __init__(self, function, img, rows, cols, frames, player, pos = Vector(0,0), size = Vector(256,256)):
        self.interactable = []
        self.__player = player
        self.__count = 0
        self.pos = pos
        self.size = size
        self.__img = img
        self.interactable.append((function, img, rows, cols, frames, Trigger(self.__player, pos, size)))
        self.__spritesheet = SpriteSheet(img, rows, cols)
        self.__animations = Animation(self.__spritesheet, frames)


    def new_interactable(self, function, img, rows, cols, frames, pos = Vector(0,0), size = Vector(256,256)):
        self.interactable.append((function, img, rows, cols, frames, Trigger(self.__player, pos, size)))

    def __is_interacting(self, function, interactable) -> None:
        if self.__player.interacting and self.__player.at_trigger(interactable):
            function()

    def update(self, interactable) -> None:
        self.__spritesheet = SpriteSheet(interactable[1], interactable[2], interactable[3])
        self.__animations = Animation(self.__spritesheet, interactable[4])
        self.__is_interacting(interactable[0], interactable[5])
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)



