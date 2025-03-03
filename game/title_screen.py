try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class TitleScreen:
    def __init__(self):
        self.music = simplegui.load_sound('https://archive.org/details/title-music_202502.mp3')
        #https://archive.org/details/title-music_202502.mp3

    def draw(self, canvas):
        canvas.draw_text("Welcome to the Game", (250, 200), 48, "Black")
        canvas.draw_polygon([(300, 700), (500, 700), (500, 780), (300, 780)], 4, "Black", "White")
        canvas.draw_text("Start", (350, 750), 36, "Black")



