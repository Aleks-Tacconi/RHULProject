from entities.utils import SpriteSheet
from simplegui.components import Interactable


class Portal(Interactable):
    def __init__(self, spritesheet: SpriteSheet, animations: Animation):
        super().__init__(spritesheet, animations)