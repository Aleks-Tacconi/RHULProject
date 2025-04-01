from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from .gameloops import MainLoop, TitleScreen, LevelOne, Tutorial, Login
from .gameloops.abstract import GameLoop
from .gameloops.level_editor import LevelEditor

class GUI:
    def __init__(self, title: str, width: int, height: int) -> None:
        self.__frame = simplegui.create_frame(title, width, height)
        self.__labels = [self.__frame.add_label("") for _ in range(20)]

        self.__reset_game()

    def __set_draw_handler(self, gameloop: GameLoop) -> None:
        self.__frame.set_draw_handler(gameloop.mainloop)
        self.__frame.set_keyup_handler(gameloop.keyup_handler)
        self.__frame.set_keydown_handler(gameloop.keydown_handler)
        self.__frame.set_mouseclick_handler(gameloop.mouseclick_handler)

    def __reset_game(self, score=0, login_status=False) -> None:
        mainloop = MainLoop(self.__reset_game)
        level_one = LevelOne(self.__reset_game)
        tutorial = Tutorial(self.__reset_game)
        login = Login(lambda: self.__reset_game(login_status=True))

        level_editor = LevelEditor(self.__reset_game, self.__labels)
        title_screen = TitleScreen(lambda: self.__set_draw_handler(level_one),
                                   lambda: self.__set_draw_handler(tutorial),
                                   lambda: self.__set_draw_handler(level_editor),
                                   lambda: self.__set_draw_handler(login), login_status)
        self.__set_draw_handler(title_screen)

    def start(self) -> None:
        self.__frame.start()

    def stop(self) -> None:
        self.__frame.stop()
