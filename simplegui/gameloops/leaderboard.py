from typing import Callable
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils.score import SCORE
from simplegui.components import Button, ButtonStyle

from .abstract import GameLoop


class LeaderBoard(GameLoop):
    def __init__(self, back: Callable) -> None:
        super().__init__()
        self.__back = Button(
            pos=[[20, 350], [120, 350], [120, 380], [20, 380]],
            text="Back",
            style=ButtonStyle(
                border_color="Black",
                border_width=2,
                fill_color="White",
                font_size=20,
                font_color="Black",
                text_offset_x=-30,
                text_offset_y=6,
            ),
        )

        self.__back_func = back

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__back.render(canvas)
        scores = []

        for index, player in enumerate(SCORE.scores.keys()):
            scores.append([player, SCORE.scores[player]['score']])

        for index, item in enumerate(sorted(scores, key=lambda x: x[1], reverse=True)):
            player, score = item

            canvas.draw_text(
                text=player,
                point=[30, 30 + (30 * index)],
                font_color="White",
                font_size=30,
            )

            canvas.draw_text(
                text=f"|    {score}",
                point=[180, 30 + (30 * index)],
                font_color="White",
                font_size=30,
            )
        

        if self._mouse.clicked:
            self.__back.handle_click(self._mouse.last_click, self.__back_func)
            self._mouse.clicked = False

    def keydown_handler(self, key: int) -> None: ...
    def keyup_handler(self, key: int) -> None: ...
