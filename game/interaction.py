from .mouse import Mouse

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from ai import AI
from .keyboard import Keyboard
from entities import Player
import threading

class Interaction:
    def __init__(self):
        self.player = Player(self)
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.single = True
        self.ai = AI()

    def update(self):
        self.player.speed = 5
        if self.keyboard.current_key == "":
            self.player.vel.x = 0
        if "D" in self.keyboard.keys_pressed:
            self.player.vel.x = 1 * self.player.speed
        if "A" in self.keyboard.keys_pressed:
            self.player.vel.x = -1 * self.player.speed
        if ("D" in self.keyboard.keys_pressed and self.keyboard.current_key == "D"
                and self.player.vel.x != 1 * self.player.speed):
            self.player.vel.x = 1 * self.player.speed
        if ("A" in self.keyboard.keys_pressed and self.keyboard.current_key == "A"
                and self.player.vel.x != -1 * self.player.speed):
            self.player.vel.x = -1 * self.player.speed
        if "W" in self.keyboard.keys_pressed and self.player.vel.y == 0 and self.player.pos.y == 600:
            self.player.vel.y = -10
        if "V" in self.keyboard.keys_pressed and self.single == True:
            self.single = False
            threading.Thread(target = self.voice_ai).start()


    def voice_ai(self):
        speech = self.ai.speak()
        response = self.ai.text_prompt("You are a game assistant meant to help the player. Responses must be a maximum of 50 words. Prompt: " + speech)
        self.ai.generate_response_voice_backup(response)
        self.single = True
