from dataclasses import dataclass

from utils import Vector

@dataclass
class Mouse:
    x: int | None = None
    y: int | None = None
    clicked: bool = False

    @property
    def last_click(self) -> Vector:
        if self.x is None or self.y is None:
            raise ValueError("The mouse has not been clicked!")

        return Vector(self.x, self.y)

    def click(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.clicked = True

    def update(self) -> None:
        self.clicked = False
