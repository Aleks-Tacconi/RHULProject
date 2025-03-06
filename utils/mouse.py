"""Mouse Module.

This module provides a Mouse dataclass to track the last mouse click position.

Classes:
    Mouse: A dataclass that stores the last mouse click position and click state.
"""

from dataclasses import dataclass

from utils import Vector


@dataclass
class Mouse:
    """Dataclass storing the last mouse click.

    Attributes:
        x (int | None): The last clicked x coord. Defaults to None.
        y (int | None): The last clicked y coord. Defaults to None.
        clicked (bool): True if clicked during last frame else False.
        last_click (Vector): The last clicked coords as a Vector.

    Methods:
        click(x: int, y: int) -> None: Updates the last clicked position
        update() -> None: Updates the clicked boolean to show the last click is old.
    """

    x: int | None = None
    y: int | None = None
    clicked: bool = False

    @property
    def last_click(self) -> Vector:
        """The last clicked coordinates as a Vector.

        Returns:
            list: A list containing the x and y coordinates of the last click.

        Raises:
            ValueError: The mouse has not been clicked.
        """
        if self.x is None or self.y is None:
            raise ValueError("The mouse has not been clicked!")

        return Vector(self.x, self.y)

    def click(self, x: int, y: int) -> None:
        """Updates the last clicked position."""
        self.x = x
        self.y = y
        self.clicked = True

    def update(self) -> None:
        """Updates the clicked boolean to show the last click is old."""
        self.clicked = False
