
import threading
import os

from pydub import AudioSegment
from pydub.playback import play

class PlaySounds:
    def __init__(self, file_path, volume = -20):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.current_dir, '..', '..', 'sounds', file_path)
        self.file_path_absolute = os.path.abspath(self.file_path)
        self.sound = AudioSegment.from_file(self.file_path_absolute)
        self.volume = volume
        self.event = threading.Event()
        self.thread = None

    def play_sound_thread(self):
        play(self.sound + self.volume)

    def play_sound(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.play_sound_thread)
            self.thread.start()

    def stop_sound(self):
        self.event.set()
        self.thread.join()
        self.thread = None

