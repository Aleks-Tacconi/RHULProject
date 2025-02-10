try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class TitleScreen:

    def draw(self, canvas):
        canvas.draw_text("Welcome to the Game", (250, 200), 48, "Black")
        canvas.draw_polygon([(300, 700), (500, 700), (500, 780), (300, 780)], 4, "Black", "White")
        canvas.draw_text("Start", (350, 750), 36, "Black")


