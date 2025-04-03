from entities import Trigger
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
from entities.utils import Animation, SpriteSheet
from simplegui.components import Subtitles

class Interactable:
    def __init__(self, function, subtitles, img, rows, cols, frames, player, pos = Vector(0,0), size = Vector(256,256)):
        self.interactables = []
        self.__player = player
        self.__count = 0
        self.pos = pos
        self.size = size
        self.__img = img
        self.interactables.append((function, subtitles, img, rows, cols, frames, Trigger(self.__player, pos, size)))
        self.__spritesheet = SpriteSheet(img, rows, cols)
        self.__animations = Animation(self.__spritesheet, frames)
        self.__function = function
        self.__trigger = Trigger(self.__player, pos, size)
        self.__subtitles = Subtitles(subtitles, Vector(pos.x, pos.y + size.y / 4), 18)
        self.__subtitles_playing = False


    def new_interactable(self, function, subtitles, img, rows, cols, frames, pos = Vector(0,0), size = Vector(256,256)):
        self.interactables.append((function, subtitles, img, rows, cols, frames, Trigger(self.__player, pos, size)))

    def __is_interacting(self) -> None:
        if self.__player.interacting:
            self.__function()

    def update(self, interactable) -> None:
        if self.__spritesheet != SpriteSheet(interactable[2], interactable[3], interactable[4]):
            self.__spritesheet = SpriteSheet(interactable[2], interactable[3], interactable[4])
            self.__animations = Animation(self.__spritesheet, interactable[5])
            self.__subtitles = Subtitles(interactable[1], self.pos, 18)
            self.__function = interactable[0]
            self.__trigger = interactable[6]

        if self.__trigger.at_trigger():
            self.__is_interacting()
            self.__subtitles.generate = True
            if not self.__subtitles_playing:
                self.__subtitles_playing = True
                self.__subtitles.start_subtitles()
        else:
            self.__subtitles.generate = False
            if not self.__subtitles.generate:
                self.__subtitles_playing = False
                self.__subtitles.text = ""


        self.__animations.update()

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self.__trigger.render(canvas, offset_x, offset_y)
        self.__subtitles.render(canvas, offset_x, offset_y)



