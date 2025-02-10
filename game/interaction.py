from .mouse import Mouse

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from .keyboard import Keyboard
from entities import Player

class Interaction:
    def __init__(self):
        self.player = Player(self)
        self.keyboard = Keyboard()
        self.mouse = Mouse()

    def update(self):
        speed = 5
        if self.keyboard.current_key == "":
            self.player.vel.x = 0
        if "D" in self.keyboard.keys_pressed:
            self.player.vel.x = 1 * speed
        if "A" in self.keyboard.keys_pressed:
            self.player.vel.x = -1 * speed
        if "D" in self.keyboard.keys_pressed and self.keyboard.current_key == "D" and self.player.vel.x != 1 * speed:
            self.player.vel.x = 1 * speed
        if "A" in self.keyboard.keys_pressed and self.keyboard.current_key == "A" and self.player.vel.x != -1 * speed:
            self.player.vel.x = -1 * speed
        if "W" in self.keyboard.keys_pressed and self.player.vel.y == 0 and self.player.pos.y == 600:
            self.player.vel.y = -10
