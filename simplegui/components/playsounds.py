import os
from just_playback import Playback

class PlaySound:
    def __init__(self, sound_name):
        self.__audio_file = os.path.join("assets", "sounds", sound_name)
        self.__audio = Playback()
        self.__audio.load_file(self.__audio_file)

    def play(self):
        self.__audio.play()

    def pause(self):
        self.__audio.pause()

    def resume(self):
        self.__audio.resume()

    def stop(self):
        self.__audio.stop()
