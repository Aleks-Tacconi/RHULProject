from SimpleGUICS2Pygame import simpleguics2pygame as simplegui

from simplegui.components.scoreboard import ScoreBoard
from simplegui.components.xp import XP
from simplegui.gameloops.cutscene_one import CutsceneOne
from simplegui.gameloops.cutscene_screen import CutSceneScreen

from .gameloops import LevelOne, LevelThree, LevelTwo, Login, TitleScreen, Tutorial, LeaderBoard
from .gameloops.abstract import GameLoop
from .gameloops.level_editor import LevelEditor


class GUI:
    def __init__(self, title: str, width: int, height: int) -> None:
        self.__frame = simplegui.create_frame(title, width, height)
        self.__labels = [self.__frame.add_label("") for _ in range(20)]

        self.__scoreboard = ScoreBoard()
        self.__xp = XP()

        with open("buffs.json", "w") as f:
            f.write('{"Health": false, "Attack": false, "Crit rate": false}')

        self.__reset_game()

    def __set_draw_handler(self, gameloop: GameLoop) -> None:
        self.__frame.set_draw_handler(gameloop.mainloop)
        self.__frame.set_keyup_handler(gameloop.keyup_handler)
        self.__frame.set_keydown_handler(gameloop.keydown_handler)
        self.__frame.set_mouseclick_handler(gameloop.mouseclick_handler)

    def __reset_game(
        self, login_status=False, transition_screen=None, cutscene=None
    ) -> None:
        tutorial = Tutorial(
            reset=self.__reset_game,
            failed=self.__reset_tutorial,
            passed=self.__reset_level_one,
            scoreboard=self.__scoreboard,
            xp=self.__xp,
        )
        login = Login(lambda: self.__reset_game(login_status=True))

        cutscene_1 = CutsceneOne(self.__reset_game, self.__reset_level_one)
        leaderboard = LeaderBoard(self.__reset_game)

        level_editor = LevelEditor(self.__reset_game, self.__labels)
        title_screen = TitleScreen(
            lambda: self.__set_draw_handler(cutscene_1),
            lambda: self.__set_draw_handler(tutorial),
            lambda: self.__set_draw_handler(level_editor),
            lambda: self.__set_draw_handler(login),
            login_status,
            lambda: self.__set_draw_handler(leaderboard),
        )
        if transition_screen is not None:
            self.__set_draw_handler(transition_screen)
        elif cutscene is not None:
            self.__set_draw_handler(cutscene)
        else:
            self.__set_draw_handler(title_screen)

    def __reset_tutorial(self):
        tutorial = Tutorial(
            self.__reset_game,
            failed=self.__reset_tutorial,
            passed=self.__reset_level_one,
            scoreboard=self.__scoreboard,
            xp=self.__xp,
        )
        self.__frame.set_canvas_background("Black")
        self.__set_draw_handler(tutorial)

    def __reset_level_one(self):
        level_one = LevelOne(
            reset=self.__reset_game,
            failed=self.__reset_level_one,
            passed=self.__reset_level_two,
            scoreboard=self.__scoreboard,
            xp=self.__xp,
        )
        self.__frame.set_canvas_background("Black")
        self.__set_draw_handler(level_one)

    def __reset_level_two(self):
        level_two = LevelTwo(
            self.__reset_game,
            failed=self.__reset_level_two,
            passed=self.__reset_level_three,
            scoreboard=self.__scoreboard,
            xp=self.__xp,
        )
        self.__frame.set_canvas_background("#8B8C8A")
        self.__set_draw_handler(level_two)

    def __reset_level_three(self):
        level_three = LevelThree(
            self.__reset_game,
            failed=self.__reset_level_three,
            passed=self.__reset_game,
            scoreboard=self.__scoreboard,
            xp=self.__xp,
        )
        self.__frame.set_canvas_background("Black")
        self.__set_draw_handler(level_three)

    def start(self) -> None:
        self.__frame.start()

    def stop(self) -> None:
        self.__frame.stop()
