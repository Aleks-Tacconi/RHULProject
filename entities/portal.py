from entities import Background
from utils import Vector


class Portal(Background):
    def __init__(self, pos: Vector, img: str, size_x: int, size_y: int, scale_factor: int) -> None:
        super().__init__(pos=pos, img=img, size_x= size_x, size_y=size_y, scale_factor=scale_factor)