from entities import Trigger
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
from entities.utils import Animation, SpriteSheet

class Interactable:
    def __init__(self, function, img, rows, cols, frames, player, pos = Vector(0,0), size = Vector(256,256)):
        self.interactables = []
        self.__player = player
        self.__count = 0
        self.pos = pos
        self.size = size
        self.__img = img
        self.interactables.append((function, img, rows, cols, frames, Trigger(self.__player, pos, size)))
        self.__spritesheet = SpriteSheet(img, rows, cols)
        self.__animations = Animation(self.__spritesheet, frames)
        self.__function = function
        self.__trigger = Trigger(self.__player, pos, size)


    def new_interactable(self, function, img, rows, cols, frames, pos = Vector(0,0), size = Vector(256,256)):
        self.interactables.append((function, img, rows, cols, frames, Trigger(self.__player, pos, size)))

    def __is_interacting(self) -> None:
        if self.__player.interacting and self.__trigger.at_trigger():
            self.__function()

    def update(self, interactable) -> None:
        if self.__spritesheet != SpriteSheet(interactable[1], interactable[2], interactable[3]):
            self.__spritesheet = SpriteSheet(interactable[1], interactable[2], interactable[3])
            self.__animations = Animation(self.__spritesheet, interactable[4])
            self.__function = interactable[0]
            self.__trigger = interactable[5]
        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self.__trigger.render(canvas, offset_x, offset_y)



