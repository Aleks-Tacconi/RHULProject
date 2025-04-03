from dataclasses import dataclass, field
from typing import Callable, List

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from utils import Vector

class Buff():
    def __init__(self,
                 url: str,
                 center_source: tuple | set,
                 dest_center: tuple | set,
                 dest_length: int,
                 buff_type: str):
        self.__image = simplegui._load_local_image(url)
        self.__dest_center = dest_center
        self.__center_source = center_source
        self.__dest_length = dest_length
        self.__buff_type = buff_type

        if self.__buff_type == "Health":
            self.__text = "Increase Health Points."
        if self.__buff_type == "Attack":
            self.__text = "Increase Attack Damage."
        if self.__buff_type == "Crit rate":
            self.__text = "Increase Critical DMG Rate."

        self.__pos = [
            [self.__dest_center[0] - dest_length/2, self.__dest_center[1] - dest_length/2],
            [self.__dest_center[0] - dest_length/2, self.__dest_center[1] + dest_length/2],
            [self.__dest_center[0] + dest_length/2, self.__dest_center[1] + dest_length/2],
            [self.__dest_center[0] + dest_length/2, self.__dest_center[1] - dest_length/2]
        ]
        self.__is_selected = False
    
    def is_clicked(self, pos: Vector) -> bool:
        return (
            (pos.x > self.__pos[0][0])
            and (pos.x < self.__pos[2][0])
            and (pos.y > self.__pos[0][1])
            and (pos.y < self.__pos[2][1])
        )

    def handle_click(self, pos: Vector) -> None:
        self.__is_selected = False
        if self.is_clicked(pos):
            self.__is_selected = True

    def get_is_selected(self):
        return self.__is_selected
    
    def force_select(self):
        self.__is_selected = True
    

    def mainloop(self, canvas: simplegui.Canvas) -> None:
        canvas.draw_image(image=self.__image,
                            center_source=self.__center_source,
                            width_height_source=(self.__image.get_width(), self.__image.get_height()),
                            center_dest=self.__dest_center, 
                            width_height_dest=(self.__dest_length, self.__dest_length))
        if self.__is_selected:
            canvas.draw_polygon(point_list=self.__pos,
                                line_width=3,
                                line_color="Red")
            canvas.draw_text(self.__text, (250, 270), 30, "White")
        