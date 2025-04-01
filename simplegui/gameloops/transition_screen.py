from typing import Callable

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from simplegui.components import Button, ButtonStyle
from .abstract import GameLoop
import os
from entities import Background
from utils import Vector

class TransitionScreen(GameLoop):
    def __init__(self, prev_level: str, next_game: list, passed_level: bool, score: int) -> None:
        super().__init__()

        next_level = {
            "tutorial": "the Title Screen",
            "LevelOne": "Level Two",
            "LevelTwo": "Level Three",
            "LevelThree": "the Title Screen",
            "the Main Loop": "the Title Screen"
        }
        if passed_level:
            self.__start_game = next_game[1]
        else:            
            self.__start_game = next_game[0]
        self.__score = score

        if passed_level:
            self.__elements = [f"You passed {prev_level}.", f"Proceed to {next_level[prev_level]}"]
        else:
            self.__elements = [f"You died.", f"Retry {prev_level}."]
            if next_level[prev_level] == "the Title Screen":
                self.__elements[1] = "Return to the Title Screen."
                
        
        self.__start = Button(
            pos=[[290, 240], [510, 240], [510, 270], [290, 270]],
            text=self.__elements[1],
            style=ButtonStyle(
                border_color="Black",
                border_width=2,
                fill_color="White",
                font_size=20,
                font_color="Black",
                text_offset_x=-105,
                text_offset_y=6,
            )
        )

        self.__title_background = Background(
                pos=Vector(404, 200),
                img=os.path.join("assets", "black_background", "black-background.jpg"),
                size_x=1920,
                size_y=1080,
                scale_factor=1.5,
                frames=1,
                cols=1,
            )

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__title_background.render(canvas, 0, 0)
        self.__title_background.update()
        canvas.draw_text(self.__elements[0], (280, 50), 50, "White")
        canvas.draw_text(f"Score: {self.__score}", (280, 150), 50, "White")
        self.__start.render(canvas)

        if self._mouse.clicked:
            self.__start.handle_click(self._mouse.last_click, self.__start_game)
        
        self._mouse.update()
    
    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)