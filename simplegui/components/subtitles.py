import time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
import threading

class Subtitles:
    def __init__(self, text: str, pos: Vector = Vector(0, 0), size = 20, max_words=12, max_characters=36) -> None:
        self.text = ""
        self.__size = size
        self.__max_words = max_words
        self.__colour = "White"
        self.__text_pos = (pos.x, pos.y)
        self.__count = 0
        self.generate = True
        self.__words = []
        self.__subtitle = []
        self.__sentence = []
        self.__letters = []
        self.__prompt = text.split(" ")
        self.__end_of_sentence = False
        self.__max_characters = max_characters

    def render(self, canvas: simplegui.Canvas, offset_x = 0, offset_y = 0) -> None:
        if self.generate:
            canvas.draw_text(self.text, (self.__text_pos[0] + offset_x, self.__text_pos[1] + offset_y),
                             self.__size, "White")

    def start_subtitles(self) -> None:
        threading.Thread(target=self.generate_subtitles).start()

    def generate_subtitles(self) -> None:
        while self.generate:
            for word in self.__prompt:
                self.__words.append(word)
                for letter in word:
                    self.text = self.text + "".join(letter)
                    self.__letters.append(letter)
                    time.sleep(0.05)
                    if letter == ".":
                        self.__end_of_sentence = True
                self.text = self.text + " "
                if (len(self.__words) >= self.__max_words or len(self.__letters) >= self.__max_characters or
                        self.__end_of_sentence):
                    self.__end_of_sentence = False
                    time.sleep(0.7)
                    self.text = ""
                    self.__words.clear()
                    self.__letters.clear()
                if word == self.__prompt[len(self.__prompt) - 1]:
                    time.sleep(1)
                    self.text=""
                    self.generate = False


