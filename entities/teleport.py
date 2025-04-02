from utils import Vector

class Teleport:
    def __init__(self, coordinate, player):
        self.__coordinate = coordinate
        self.__player = player

    def teleport(self):
        self.__player.pos = Vector(self.__coordinate.x, self.__coordinate.y)

