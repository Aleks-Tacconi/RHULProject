import json
import os
from typing import Callable
from entities.utils import PlaySound
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from entities import Background
from simplegui.components import Button, ButtonStyle
from simplegui.components.buffs import Buff
from simplegui.components.xp import XP
from utils import Vector
from utils.score import SCORE

from .abstract import GameLoop


class TransitionScreen(GameLoop):
    def __init__(
        self,
        prev_level: str,
        title: Callable,
        failed: Callable,
        passed: Callable,
        passed_level: bool,
        score: int,
        xp: XP,
    ) -> None:
        super().__init__()

        SCORE.add_score(score, passed_level)

        self.__title = title
        self.__passed_level = passed_level
        self.__xp = xp

        next_level = {
            "tutorial": "LevelOne",
            "LevelOne": "Level Two",
            "LevelTwo": "Level Three",
            "LevelThree": "the Title Screen",
        }
        this_level = {
            "tutorial": "the Tutorial",
            "LevelOne": "Level One",
            "LevelTwo": "Level Two",
            "LevelThree": "Level Three",
        }
        if self.__passed_level:
            self.__start_game = passed
        else:
            self.__start_game = failed

        self.__completed_game = False

        if self.__passed_level:
            self.__elements = [
                f"You passed {this_level[prev_level]}.",
                f"Proceed to {next_level[prev_level]}",
            ]

            if prev_level == "LevelThree":
                self.__completed_game = True
                self.__elements[0] = "You've completed the game!"

        else:
            self.__elements = [f"You died.", f"Retry {this_level[prev_level]}."]

        self.__selected = None
        self.__can_pick_buff = (passed_level and xp.return_xp(prev_level) >= 150) and \
        not self.__completed_game

        self.__xp.reset_xp(prev_level)
        self.__score = score
                
        if not self.__completed_game:
            self.__start = Button(
                pos=[[290, 280], [510, 280], [510, 310], [290, 310]],
                text=self.__elements[1],
                style=ButtonStyle(
                    border_color="Black",
                    border_width=2,
                    fill_color="White",
                    font_size=20,
                    font_color="Black",
                    text_offset_x=-105,
                    text_offset_y=6,
                ),
            )

        self.__title_screen = Button(
            pos=[[290, 320], [510, 320], [510, 350], [290, 350]],
            text="Return to the Title Screen.",
            style=ButtonStyle(
                border_color="Black",
                border_width=2,
                fill_color="White",
                font_size=20,
                font_color="Black",
                text_offset_x=-105,
                text_offset_y=6,
            ),
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
        if self.__can_pick_buff:
            health_buff_url = os.path.join("assets", "buffs", "Buff_Health.png")
            self.__health_buff_img = Buff(
                url=health_buff_url,
                center_source=(80, 80),
                dest_center=(310, 200),
                dest_length=40,
                buff_type="Health",
            )

            attack_buff_url = os.path.join("assets", "buffs", "Buff_Melee_Range.png")
            self.__attack_buff_img = Buff(
                url=attack_buff_url,
                center_source=(24, 24),
                dest_center=(390, 200),
                dest_length=40,
                buff_type="Attack",
            )

            crit_buff_url = os.path.join("assets", "buffs", "Buff_Accuracy.png")
            self.__crit_buff_img = Buff(
                url=crit_buff_url,
                center_source=(48, 48),
                dest_center=(470, 200),
                dest_length=40,
                buff_type="Crit rate",
            )

            self.__music = PlaySound()
            self.__music.loop(True)
            self.__music.change_volume(0.3)

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        self.__music.play_sound("ha-crunchy_1.wav")
        self.__title_background.render(canvas, 0, 0)
        self.__title_background.update()
        if self.__completed_game:
            canvas.draw_text(self.__elements[0], (160, 50), 50, "White")
        else:
            canvas.draw_text(self.__elements[0], (280, 50), 50, "White")
        canvas.draw_text(f"Score: {self.__score}", (280, 150), 50, "White")
        if not self.__completed_game:
            self.__start.render(canvas)
        self.__title_screen.render(canvas)

        if self.__can_pick_buff:
            self.__health_buff_img.mainloop(canvas)
            self.__attack_buff_img.mainloop(canvas)
            self.__crit_buff_img.mainloop(canvas)

        if self._mouse.clicked:
            if self.__can_pick_buff:
                self.__health_buff_img.handle_click(self._mouse.last_click)
                self.__attack_buff_img.handle_click(self._mouse.last_click)
                self.__crit_buff_img.handle_click(self._mouse.last_click)

                if (
                    self.__health_buff_img.get_is_selected() is False
                    and self.__attack_buff_img.get_is_selected() is False
                    and self.__crit_buff_img.get_is_selected() is False
                ):
                    if self.__selected == "Health":
                        self.__health_buff_img.force_select()
                    if self.__selected == "Attack":
                        self.__attack_buff_img.force_select()
                    if self.__selected == "Crit rate":
                        self.__crit_buff_img.force_select()
                else:
                    if self.__health_buff_img.get_is_selected():
                        self.__selected = "Health"
                    if self.__attack_buff_img.get_is_selected():
                        self.__selected = "Attack"
                    if self.__crit_buff_img.get_is_selected():
                        self.__selected = "Crit rate"

            if self.__can_pick_buff:
                
                if self.__selected is not None:
                    
                    with open("buffs.json") as f:
                        data = json.load(f)
                    for key, value in data.items():
                        data[key] = False
                    data[self.__selected] = True
                    with open("buffs.json", "w") as f:
                        json.dump(data, f)
            if not self.__completed_game:
                self.__start.handle_click(self._mouse.last_click, self.__start_game)
            self.__title_screen.handle_click(self._mouse.last_click, self.__title_screen_func)
            self._mouse.clicked = False

        self._mouse.update()

    def __title_screen_func(self) -> None:
        self.__title()
        SCORE.current_score = 0

    def keydown_handler(self, key: int) -> None: ...

    def keyup_handler(self, key: int) -> None: ...

    def render(self, canvas: simplegui.Canvas, offset_x: int, offset_y: int) -> None:
        pos = Vector(int(self.pos.x + offset_x), int(self.pos.y + offset_y))
        self.__animations.render(canvas, pos, self.size)
        self._render_hitbox(canvas, offset_x, offset_y)
