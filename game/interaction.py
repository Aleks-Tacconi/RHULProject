from .mouse import Mouse

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from ai import AI
from .keyboard import Keyboard
from entities import Player

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
            #Make it only call once + Threading (Will be done soon)
            self.single = False
            speech = self.ai.speak()
            print(speech)
            response = self.ai.text_prompt(speech + "\n\n" + "Act like a game tutorial assistant and address the player as the chosen one.")
            self.ai.generate_response_voice_backup(response)
            self.single = True
        print(self.single)

