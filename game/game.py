try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


from .interaction import Interaction
from .title_screen import TitleScreen


class Game:
    def __init__(self):
        self.width = 800
        self.height = 800
        self.inter = Interaction()
        self.title_screen = TitleScreen()
        self.frame = simplegui.create_frame("Game", self.width, self.height)
        label = self.frame.add_label('My first label')
        label.set_text('New label')
        self.frame.set_canvas_background("#ADD8E6")
        self.frame.set_keydown_handler(self.inter.keyboard.keydown)
        self.frame.set_keyup_handler(self.inter.keyboard.keyup)
        self.frame.set_mouseclick_handler(self.inter.mouse.mouse_click)
        self.frame.set_draw_handler(self.title_screen_loop)

    def start(self):
        self.frame.start()


    def mainloop(self, canvas):
        self.inter.update()
        self.inter.player.update()
        self.inter.player.render(canvas)

    def title_screen_loop(self, canvas):
        self.title_screen.draw(canvas)
        self.title_screen.music.play()
        self.title_screen.music.set_volume(0.2)
        if 300 <= self.inter.mouse.mouse_position.x <= 500 and 700 <= self.inter.mouse.mouse_position.y <= 780:
            self.title_screen.music.pause()
            self.frame.set_draw_handler(self.mainloop)





