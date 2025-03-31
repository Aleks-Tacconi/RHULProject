import time
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector
import threading

class Subtitles:
    def __init__(self, text: str, pos: Vector = Vector(0, 0), size = 20, max_words=12, max_characters=20) -> None:
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
        self.__end_of_sentence = False
        self.__max_characters = max_characters

    def render(self, canvas: simplegui.Canvas) -> None:
        if self.__generate:
            canvas.draw_text(self.text, (self.__text_pos[0], self.__text_pos[1]),
                             self.__size, "White")

    def start_subtitles(self) -> None:
        threading.Thread(target=self.generate_subtitles).start()

    def generate_subtitles(self) -> None:
        while self.__generate:
            for word in self.__prompt:
                self.__words.append(word)
                for letter in word:
                    self.text = self.text + "".join(letter)
                    time.sleep(0.05)
                    if letter == ".":
                        self.__end_of_sentence = True
                self.text = self.text + " "
                if (len(self.__words) >= self.__max_words or len(self.__words) >= self.__max_characters or
                        self.__end_of_sentence):
                    self.__end_of_sentence = False
                    time.sleep(0.5)
                    self.text = ""
                    self.__words.clear()
                if word == self.__prompt[len(self.__prompt) - 1]:
                    self.__generate = False


