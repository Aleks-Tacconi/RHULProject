import os
from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import (Block, Player, Attack, AbyssalRevenant, Fire, Background, DemonSlimeBoss, FlyingDemon, EvilHand,
                      Mage, EvilKnight, PlayerHealthBar, Cinematic)
from simplegui.gameloops.cutscene_screen import CutSceneScreen

from entities.utils import PlaySound
from utils import Vector

from .abstract import GameLoop
from simplegui.components import ScoreBoard, Cutscene


ID = "CutsceneOne"

class CutsceneOne(GameLoop):
    def __init__(self, reset: Callable, passed: Callable) -> None:
        super().__init__()
        self.__reset = reset
        self.__passed = passed
        self.__environment = []


        self.__environment.append(
            Background(
                pos=Vector(400, 200),
                img=os.path.join("assets", "background", "king_background.png"),
                size_x=1720,
                size_y=840,
                scale_factor=0.5,
                frames=4,
                cols=10,
            )
        )
        self.__player = Player(pos=Vector(400, 190), level_id=ID)


        self.__offset_x = 0
        self.__offset_y = 0

        self.__cutscenes = Cutscene(self.__player)
        self.__cutscenes.new_cutscene(Vector(400, 190), 0, "You have come, my most loyal warrior. The"
                                                         " world beyond these walls is drowning in darkness, and the"
                                                         " air is thick with the stench of decay. The kingdom stands on"
                                                         " the edge of oblivion, its people lost, its banners torn. But"
                                                         " you remain. My son… my heir… is gone. Taken by the unholy"
                                                         " blight that seeks to devour all that is good. I am the last"
                                                         " of my line, but a broken man cannot lead an unbroken war. My"
                                                         " flesh is weak, bound to this throne, but you… have walked"
                                                         " through ruin before. And you endured. The Demon Lord sits"
                                                         " upon his black throne, wreathed in the ruin of our world,"
                                                         " convinced that no soul remains to stand against him. He is"
                                                         " wrong! You will ride into the storm, cast down his wretched"
                                                         " spawn, and carve a path through the abyss itself! The"
                                                         " shadows may close in, the air may choke with death, but you"
                                                         " will not falter! You will descend into hell, where the"
                                                         " wicked reign and the sky weeps ash—and there, upon his"
                                                         " cursed throne, you will strike him down! Let them whisper of"
                                                         " the knight who did not break. Let them tremble at the name"
                                                         " of the one who would not yield. I have seen warriors fall,"
                                                         " seen their spirits shattered—but you… you are different. I"
                                                         " have known men who fell into the abyss and never returned."
                                                         " But I have also known those whose fire burned too bright to"
                                                         " be extinguished. You, my knight, will not falter. You"
                                                         " survived because the fire inside you burned brighter than"
                                                         " the hellfire around you. Now, let that fire set the world"
                                                         " ablaze. Go now. Ride forth, and do not return until the"
                                                         " Demon Lord is nothing but dust and the last echo of his"
                                                         " shadow has faded from this world.", Vector(1000, 1000),
                                                         Vector(250,390), Vector(830, 700))

        self.__speech = PlaySound()
        self.__sound_playing = False



    def mainloop(self, canvas: simplegui.Canvas) -> None:
        if not self.__sound_playing:
            self.__speech.play_sound("king_speech.wav")
            self.__sound_playing = True
        # TODO: 400 is half the screen width - not good magic number
        self.__offset_x += (self.__player.pos.x - 380 - self.__offset_x) // 10
        self.__offset_y += (self.__player.pos.y - 180 - self.__offset_y) // 10


        for entity in self.__environment:
            if self.is_entity_visible(self.__player, entity):
                entity.update()
                entity.render(canvas, -self.__offset_x, -self.__offset_y)

        for cutscene in self.__cutscenes.cutscenes:
            if self.is_entity_visible(self.__player, cutscene[3]):
                self.__cutscenes.play_cutscene(cutscene)
                cutscene[3].render(canvas, -self.__offset_x, -self.__offset_y)
                self.__cutscenes.render(canvas)

        if self.__cutscenes.next_scene:
            self.__reset(cutscene=CutSceneScreen(
                next=self.__passed
            ))

    def keyup_handler(self, key: int) -> None:
        self.__player.keyup_handler(key)

    def keydown_handler(self, key: int) -> None:
        self.__player.keydown_handler(key)
