from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from .gameloops import MainLoop, TitleScreen
from .gameloops.abstract import GameLoop

class GUI:
    def __init__(self, title: str, width: int, height: int) -> None:
        self.__frame = simplegui.create_frame(title, width, height)
        self.__reset_game()

    def __set_draw_handler(self, gameloop: GameLoop) -> None:
        self.__frame.set_draw_handler(gameloop.mainloop)
        self.__frame.set_keyup_handler(gameloop.keyup_handler)
        self.__frame.set_keydown_handler(gameloop.keydown_handler)
        self.__frame.set_mouseclick_handler(gameloop.mouseclick_handler)

    def __reset_game(self) -> None:
        mainloop = MainLoop(self.__reset_game)
        title_screen = TitleScreen(lambda: self.__set_draw_handler(mainloop))
        self.__set_draw_handler(title_screen)

    def start(self) -> None:
        self.__frame.start()

    def stop(self) -> None:
        self.__frame.stop()
