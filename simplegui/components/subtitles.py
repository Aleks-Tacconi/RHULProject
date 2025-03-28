import time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector

class Subtitles:
    def __init__(self, text: str, pos: Vector = Vector(0, 0), size = 20, max_words=10) -> None:
        self.text = text
        self.size = size
        self.__max_words = max_words
        self.colour = "White"
        self.__text_pos = (pos.x, pos.y)
        self.__count = 0
        self.__sentence = ""
        self.__words = self.text.split()


    def render(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_text(self.text, (270, 370), self.size, "White")

