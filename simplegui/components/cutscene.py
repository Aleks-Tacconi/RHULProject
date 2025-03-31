from simplegui.components import Subtitles
from entities import Cinematic, Trigger
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from utils import Vector

class Cutscene:
    triggers = []

    def __init__(self, player):
        self.__cutscenes = []
        self.__player = player
        self.__index = 0
        self.__count = 0
        self.__can_speak = True
        self.__cutscene_playing = False
        self.__subtitles = None
        self.__cinematic = Cinematic()
        self.__trigger_original_size = 0

    def at_cutscene(self, trigger: Trigger) -> bool:
        hitbox = trigger
        return hitbox.collides_with(self.__player)

    def new_cutscene(self, pos = Vector(0,0), seconds=1, subtitles="", size = Vector(0,60),
                     subtitles_pos = Vector(260,360)) -> None:
        self.__cutscenes.append((seconds, subtitles, subtitles_pos))
        Cutscene.triggers.append((Trigger(pos, size), self.__index))
        self.__index += 1
        self.__trigger_original_size +=1

    def play_cutscene(self, trigger: tuple) -> None:
        index = trigger[1]
        if self.at_cutscene(trigger[0]):
            self.__player.in_cutscene(True)
            self.__cutscene_playing = True
            if self.__can_speak:
                self.__subtitles = Subtitles(self.__cutscenes[index][1],
                                             self.__cutscenes[index][2])
                self.__subtitles.start_subtitles()
                #if self.__subtitles != "":
                    # self.__ai.generate_response_voice(self.__subtitles)
                self.__can_speak = False
                self.__cinematic.cinematic_bars = True

            if self.__count // 60 == self.__cutscenes[index][0]:
                self.__count = 0
                self.__can_speak = True
                self.__cinematic.cinematic_bars = False
                self.__cutscene_playing = False
                Cutscene.triggers.remove(trigger)
                self.__player.in_cutscene(False)

        if self.__cutscene_playing:
            self.__count += 1

    def render(self, canvas: simplegui.Canvas) -> None:
        if self.__cutscene_playing:
            self.__cinematic.render(canvas)
            self.__subtitles.render(canvas)


