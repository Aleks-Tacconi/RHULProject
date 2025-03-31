import time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
import threading

class Subtitles:
    def __init__(self, text: str, pos: Vector = Vector(0, 0), size = 20, max_words=5) -> None:
        self.text = ""
        self.__size = size
        self.__max_words = max_words
        self.__colour = "White"
        self.__text_pos = (pos.x, pos.y)
        self.__count = 0
        self.__generate = True
        self.__words = []
        self.__subtitle = []
        self.__sentence = []
        self.__prompt = text.split(" ")



    def render(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_text(self.text, (270, 370), self.__size, "White")

    def start_subtitles(self) -> None:
        threading.Thread(target=self.generate_subtitles).start()

    def generate_subtitles(self) -> None:
        while self.__generate:
            for word in self.__prompt:
                self.__words.append(word)
                for letter in word:
                    self.text = self.text + "".join(letter)
                    time.sleep(0.05)
                self.text = self.text + " "
                if len(self.__words) >= self.__max_words:
                    time.sleep(0.25)
                    self.text = ""
                    self.__words.clear()


