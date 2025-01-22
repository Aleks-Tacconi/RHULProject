try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import Player

class Game:
    def __init__(self):
        self.width = 800
        self.height = 800

        self.keys_pressed = set()
        self.player = Player(self)

        self.frame = simplegui.create_frame("Title", self.width, self.height)
        self.frame.set_draw_handler(self.mainloop)

        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_keyup_handler(self.keyup)

    def keydown(self, key):
        try:
            self.keys_pressed.add(chr(key))
        except ValueError:
            pass

    def keyup(self, key):
        try:
            self.keys_pressed.remove(chr(key))
        except ValueError:
            pass

    def start(self):
        self.frame.start()

    def mainloop(self, canvas):
        self.player.update()
        self.player.render(canvas)
