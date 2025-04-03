import os
from just_playback import Playback

class PlaySound:
    def __init__(self) -> None:
        self.__audio_file = None
        self.__audio_file_2 = None
        self.__audio = Playback()
        self.__audio_2 = Playback()


    def play(self) -> None:
        self.__audio.play()

    def pause(self) -> None:
        self.__audio.pause()

    def resume(self) -> None:
        self.__audio.resume()

    def stop(self) -> None:
        self.__audio.stop()

    def change_volume(self, volume: float) -> None:
        self.__audio.set_volume(volume)

    def play_sound(self, audio_file, audio_file_2 = None) -> None:
        if self.__audio_file != audio_file:
            self.__audio_file = audio_file
            self.__audio.load_file(os.path.join("assets", "sounds", self.__audio_file))
            self.__audio.play()
        if self.__audio_file_2 != audio_file_2 and audio_file_2 is not None:
            self.__audio_file_2 = audio_file_2
            self.__audio_2.load_file(os.path.join("assets", "sounds", self.__audio_file_2))
            self.__audio_2.play()



