from simplegui.components import Subtitles
from entities import Cinematic, Trigger
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector

class Cutscene:
    def __init__(self, player):
        self.cutscenes = []
        self.__player = player
        self.__count = 0
        self.__can_speak = True
        self.__cutscene_playing = False
        self.__subtitles = None
        self.__cinematic = Cinematic()
        self.__current_cutscene = None
        self.__end_cutscene = False

    def new_cutscene(self, pos = Vector(0,0), seconds=1, subtitles="", size = Vector(0,60),
                     subtitles_pos = Vector(260,360)) -> None:
        self.cutscenes.append((seconds, subtitles, subtitles_pos, Trigger(self.__player, pos, size)))

    def play_cutscene(self, cutscene: tuple) -> None:
        self.__current_cutscene = cutscene
        if self.__current_cutscene[3].at_trigger():
            self.__player.in_cutscene(True)
            self.__cutscene_playing = True
            if self.__can_speak:
                self.__end_cutscene = False
                self.__subtitles = Subtitles(self.__current_cutscene[1], self.__current_cutscene[2])
                self.__subtitles.start_subtitles()
                #if self.__subtitles != "":
                    # self.__ai.generate_response_voice(self.__subtitles)
                self.__can_speak = False
                self.__cinematic.cinematic_bars = True

            if self.__count // 60 == self.__current_cutscene[0]:
                self.__end_cutscene = True

            if not self.__subtitles.generate and self.__end_cutscene:
                self.__count = 0
                self.__can_speak = True
                self.__cinematic.cinematic_bars = False
                self.__cutscene_playing = False
                self.cutscenes.remove(self.__current_cutscene)
                self.__player.in_cutscene(False)

            if self.__cutscene_playing:
                self.__count += 1

    def render(self, canvas: simplegui.Canvas) -> None:
        if self.__cutscene_playing:
            self.__cinematic.render(canvas)
            self.__subtitles.render(canvas)


